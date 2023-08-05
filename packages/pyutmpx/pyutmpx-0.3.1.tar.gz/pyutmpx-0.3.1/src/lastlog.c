/* ****************************************************************************
 * lastlog.c -- lastlog file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <utmp.h>

/* ---
 * lastlog entries storage.
 * --- */

/* In this section, we define the main function ``get_entries()``
 * that gathers all of the entries at iterator creation. This guarantees
 * that two iterators used separately simultaneously don't use the
 * same global state defined by the standard. */

struct lastlog_node {
	struct lastlog_node *next;

	char *host;
	char *line;

	Py_ssize_t host_size;
	Py_ssize_t line_size;

	unsigned long uid;
	struct timeval date;

	char data[];
};

/* ``get_nodes()``: gathers the lastlog entries as nodes. */

int get_nodes(struct lastlog_node **nodep)
{
	struct lastlog_node *node;
	int fd;

	*nodep = NULL;

	fd = open(_PATH_LASTLOG, O_RDONLY, 0);
	if (fd < 0)
		return 0; /* Escape cowardly. */

	for (unsigned long uid_start = 0;;) {
		struct lastlog lla[100];
		ssize_t result;
		unsigned long count;

		result = read(fd, &lla, sizeof (lla));
		if (result < 0)
			return 0; /* Escape cowardly. */

		if (!result)
			return 0; /* End of file! */

		count = (size_t)result / sizeof (struct lastlog);

		for (unsigned long uid_off = 0; uid_off < count; uid_off++) {
			unsigned long uid = uid_start + uid_off;
			struct lastlog *ll = &lla[uid_off];
			Py_ssize_t host_len, line_len;

			if (!ll->ll_time)
				continue;

			/* This entry exists! Let's create our node. */

			host_len = pyutmpx_get_len(ll->ll_host, UT_HOSTSIZE);
			line_len = pyutmpx_get_len(ll->ll_line, UT_LINESIZE);

			node = malloc(sizeof(struct lastlog_node)
				+ host_len + line_len);
			if (!node)
				return 0; /* Escape cowardly. */

			node->uid = uid;
			node->date.tv_sec = ll->ll_time;
			node->next = NULL;

			node->host = node->data;
			node->line = node->host + host_len;

			node->host_size = host_len;
			node->line_size = line_len;

			memcpy(node->host, ll->ll_host, host_len);
			memcpy(node->line, ll->ll_line, line_len);

			*nodep = node;
			nodep = &node->next;
		}

		uid_start += count;
	}

	close(fd);

	return 0;
}

/* ---
 * lastlog_iter object definition.
 * --- */

/* ``lastlog_iter_type``: the main iterator type. */

struct lastlog_iter_type {
	PyObject_HEAD

	struct lastlog_node *nodes;
};

/* `new_lastlog_iter()`: initialize a lastlog iterator. */

static PyObject *new_lastlog_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct lastlog_iter_type *self;

	self = (struct lastlog_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_lastlog_iter()`: initialize the Python object. */

static int init_lastlog_iter(struct lastlog_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	get_nodes(&self->nodes);

	/* Reset the thing and return. */

	return (0);
}

/* `del_lastlog_iter()`: destroy the Python object. */

static void del_lastlog_iter(struct lastlog_iter_type *self)
{
	if (!self)
		return ;

	while (self->nodes) {
		struct lastlog_node *node = self->nodes;

		self->nodes = self->nodes->next;
		free(node);
	}

	Py_TYPE(self)->tp_free((PyObject *)self);
}

/* `repr_lastlog_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_lastlog_iter(struct lastlog_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.lastlog_iter_type()"));
}

/* `next_lastlog_iter()`: return next element in self. */

static PyObject *next_lastlog_iter(struct lastlog_iter_type *self)
{
	struct lastlog_node *node;
	PyObject *entry = NULL;

	if (!self->nodes) {
		PyErr_SetNone(PyExc_StopIteration);
		return (NULL);
	}

	/* Consume the node! */

	node = self->nodes;

	{
		PyObject *date_object = NULL;
		PyObject *args = NULL, *kwargs = NULL;

		if (!(date_object = pyutmpx_get_datetime(&node->date)))
			return (NULL);

		args = Py_BuildValue("()");
		if (!args) {
			Py_XDECREF(date_object);
			return (NULL);
		}

		kwargs = Py_BuildValue("{s:k,s:s#,s:s#,s:O}",
			"uid", node->uid,
			"host", node->host, node->host_size,
			"line", node->line, node->line_size,
			"time", date_object);
		if (!kwargs) {
			Py_XDECREF(date_object);
			Py_XDECREF(args);
			return (NULL);
		}

		entry = PyObject_Call((PyObject *)&pyutmpx_lastlog_entry_type,
			args, kwargs);
		Py_XDECREF(date_object);
		Py_XDECREF(args);
		Py_XDECREF(kwargs);

		if (!entry)
			return (NULL);

		Py_INCREF(entry);
	}

	self->nodes = node->next;
	free(node);

	return (entry);
}

/* Entry object definition. */

static PyMethodDef lastlog_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

PyTypeObject lastlog_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.lastlog_iter_type",
	.tp_doc = "lastlog entries iterator",
	.tp_basicsize = sizeof(struct lastlog_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_lastlog_iter,
	.tp_init = (initproc)init_lastlog_iter,
	.tp_dealloc = (destructor)del_lastlog_iter,
	.tp_iternext = (iternextfunc)next_lastlog_iter,
	.tp_repr = (reprfunc)repr_lastlog_iter,

	/* Members. */

	.tp_methods = lastlog_iter_methods
};

/* ---
 * lastlog object definition.
 * --- */

/* ``lastlog_type``: the main lastlog structure.
 * Doesn't define much.
 *
 * TODO: store the path in there? */

struct lastlog_type {
	PyObject_HEAD
};

/* ``lastlog_instance``: the single instance of this type.
 *
 * Only one lastlog_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.lastlog)()`` will return ``pyutmpx.lastlog``,
 * much like ``None``. */

static struct lastlog_type *lastlog_instance = NULL;

/* `new_lastlog()`: create an instance of lastlog_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_lastlog(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct lastlog_type *self;

	if (lastlog_instance) {
		Py_XINCREF(lastlog_instance);
		return ((PyObject *)lastlog_instance);
	}

	self = (struct lastlog_type *)type->tp_alloc(type, 0);
	lastlog_instance = self;
	return ((PyObject *)self);
}

/* `init_lastlog()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_lastlog(struct lastlog_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_lastlog()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_lastlog(struct lastlog_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	lastlog_instance = NULL;
}

/* `repr_lastlog()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_lastlog(struct lastlog_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.lastlog"));
}

/* `iter_lastlog()`: return self because we are iterable. */

static PyObject *iter_lastlog(struct lastlog_type *self)
{
	return (PyObject_CallObject((PyObject *)&lastlog_iter_type, NULL));
}

/* `get_lastlog_path()`: getter to the `path` property. */

PyObject *get_lastlog_path(PyObject *self, void *cookie)
{
	(void)cookie;

	PyErr_SetString(PyExc_NotImplementedError, "");
	return (NULL);
}

/* Entry object definition. */

static PyMethodDef lastlog_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef lastlog_getset[] = {
	{"path", (getter)&get_lastlog_path, NULL,
		"Path to the raw file, if present.", NULL},
	{NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject lastlog_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.lastlog_type",
	.tp_doc = "lastlog entries iterator",
	.tp_basicsize = sizeof(struct lastlog_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_lastlog,
	.tp_init = (initproc)init_lastlog,
	.tp_dealloc = (destructor)del_lastlog,
	.tp_iter = (getiterfunc)iter_lastlog,
	.tp_repr = (reprfunc)repr_lastlog,

	/* Members. */

	.tp_methods = lastlog_methods,
	.tp_getset = lastlog_getset
};

/* ---
 * Module setup.
 * --- */

int pyutmpx_init_lastlog(PyObject *m)
{
	PyObject *lastlog;

	/* Create the lastlog iterator type. */

	if (PyType_Ready(&lastlog_type) < 0
	 || PyType_Ready(&lastlog_iter_type) < 0)
		goto fail;

	Py_INCREF(&lastlog_type);
	Py_INCREF(&lastlog_iter_type);

	/* Create an instance of the lastlog type and add it
	 * to the module. */

	lastlog = PyObject_CallObject((PyObject *)&lastlog_type, NULL);
	if (!lastlog || PyModule_AddObject(m, "lastlog", lastlog) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

void pyutmpx_exit_lastlog(void)
{
	Py_XDECREF(&lastlog_type);
	Py_XDECREF(&lastlog_iter_type);
}
