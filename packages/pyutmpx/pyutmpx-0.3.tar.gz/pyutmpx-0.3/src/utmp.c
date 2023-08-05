/* ****************************************************************************
 * utmp.c -- utmpx file iterator definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <errno.h>
#include <utmpx.h>

/* Here, we want to decide which interface we want to use.
 * There are several we can use with various degrees of confidence:
 *
 * - the <utmpx.h> interface standardized in POSIX.1, which only allows us
 *   to interact with the utmp file and not the wtmp and btmp ones.
 * - the GNU <utmp.h> interface, which allows us to interact with wtmp
 *   and btmp as well, but with a global cursor.
 * - opening the files and interacting with them directly. This requires us
 *   to know exactly where the files are and what the structures are, plus
 *   some systems maintain a modern file set named after the standard and
 *   an older one for compatibility with older software.
 * - the utmpd interface, which is very similar to the standard.
 *
 * Here, for now, we only interact with the utmpx files using the standard
 * interface. */

#include <utmpx.h>

/* The affected functions are `pyutmpx_reset_utmp()` and `pyutmpx_next_utmp()`,
 * although the `HAS_WTMP` and `HAS_BTMP` are used in the
 * `pyutmpx_prepare_iterators()` to know if the `wtmp` and `btmp` objects
 * shall be opened. */

/* ---
 * utmpx entries storage.
 * --- */

/* In this section, we define the main function ``get_utmp_entries()``
 * that gathers all of the entries at iterator creation. This guarantees
 * that two iterators used separately simultaneously don't use the
 * same global state defined by the standard. */

struct utmp_node {
	int type;
	struct utmp_node *next;

	char *id;
	char *user;
	char *host;
	char *line;

	Py_ssize_t id_size;
	Py_ssize_t user_size;
	Py_ssize_t host_size;
	Py_ssize_t line_size;

	unsigned long pid;
	struct timeval date;

	char data[];
};

/* `get_pyutmpx_utmp_entry_type()`: get the type. */

static int get_pyutmpx_utmp_entry_type(short type)
{
	switch (type) {
	case BOOT_TIME:
		return (PYUTMPX_BOOT_TIME);
	case OLD_TIME:
		return (PYUTMPX_OLD_TIME);
	case NEW_TIME:
		return (PYUTMPX_NEW_TIME);
	case USER_PROCESS:
		return (PYUTMPX_USER_PROCESS);
	case INIT_PROCESS:
		return (PYUTMPX_INIT_PROCESS);
	case LOGIN_PROCESS:
		return (PYUTMPX_LOGIN_PROCESS);
	case DEAD_PROCESS:
		return (PYUTMPX_DEAD_PROCESS);
	}

	return (0);
}

/* ``get_utmp_entries()``: gathers the utmp entries as nodes. */

int get_utmp_entries(struct utmp_node **nodep)
{
	struct utmp_node *node;
	struct utmpx *ent;
	int type, id_len, user_len, host_len, line_len;

	*nodep = NULL;

	setutxent();
	while (1) {
		ent = getutxent();
		if (!ent)
			break;
		if (!(type = get_pyutmpx_utmp_entry_type(ent->ut_type)))
			continue;

		id_len = pyutmpx_get_len(ent->ut_id, 0);
		user_len = pyutmpx_get_len(ent->ut_user, 0);
		host_len = pyutmpx_get_len(ent->ut_host, 0);
		line_len = pyutmpx_get_len(ent->ut_line, 0);

		node = malloc(sizeof(struct utmp_node)
			+ id_len + user_len + host_len + line_len);
		if (!node)
			return 0; /* We quit cowardly, pretenting nothing follows. */

		node->type = type;
		node->next = NULL;
		node->pid = ent->ut_pid;
		node->date.tv_sec = ent->ut_tv.tv_sec;
		node->date.tv_usec = ent->ut_tv.tv_usec;

		node->id = node->data;
		node->user = node->id + id_len;
		node->host = node->user + user_len;
		node->line = node->host + host_len;

		node->id_size = id_len;
		node->user_size = user_len;
		node->host_size = host_len;
		node->line_size = line_len;

		memcpy(node->id, ent->ut_id, id_len);
		memcpy(node->user, ent->ut_user, user_len);
		memcpy(node->host, ent->ut_host, host_len);
		memcpy(node->line, ent->ut_line, line_len);

		*nodep = node;
		nodep = &node->next;
	}

	return 0;
}

/* ---
 * utmp_iter object definition.
 * --- */

/* ``utmp_iter_type``: the main iterator type. */

struct utmp_iter_type {
	PyObject_HEAD

	struct utmp_node *nodes;
};

/* `new_utmp_iter()`: initialize a utmp iterator. */

static PyObject *new_utmp_iter(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct utmp_iter_type *self;

	self = (struct utmp_iter_type *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `init_utmp_iter()`: initialize the Python object. */

static int init_utmp_iter(struct utmp_iter_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Load all entries now to avoid having problems with multiple
	 * iterators. */

	get_utmp_entries(&self->nodes);

	/* Reset the thing and return. */

	return (0);
}

/* `del_utmp_iter()`: destroy the Python object. */

static void del_utmp_iter(struct utmp_iter_type *self)
{
	if (!self)
		return ;

	while (self->nodes) {
		struct utmp_node *node = self->nodes;

		self->nodes = self->nodes->next;
		free(node);
	}

	Py_TYPE(self)->tp_free((PyObject *)self);
}

/* `repr_utmp_iter()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_utmp_iter(struct utmp_iter_type *Py_UNUSED(self))
{
	return (Py_BuildValue("s", "pyutmpx.utmp_iter_type()"));
}

/* `next_utmp_iter()`: return next element in self. */

static PyObject *next_utmp_iter(struct utmp_iter_type *self)
{
	struct utmp_node *node;
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

		kwargs = Py_BuildValue("{s:s#,s:i,s:s#,s:s#,s:s#,s:O,s:k}",
			"id", node->id, node->id_size,
			"type", node->type,
			"user", node->user, node->user_size,
			"host", node->host, node->host_size,
			"line", node->line, node->line_size,
			"time", date_object,
			"pid", node->pid);
		if (!kwargs) {
			Py_XDECREF(date_object);
			Py_XDECREF(args);
			return (NULL);
		}

		entry = PyObject_Call((PyObject *)&pyutmpx_utmp_entry_type,
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

static PyMethodDef utmp_iter_methods[] = {
	{NULL, NULL, 0, NULL}
};

PyTypeObject utmp_iter_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_iter_type",
	.tp_doc = "utmp entries iterator",
	.tp_basicsize = sizeof(struct utmp_iter_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_utmp_iter,
	.tp_init = (initproc)init_utmp_iter,
	.tp_dealloc = (destructor)del_utmp_iter,
	.tp_iternext = (iternextfunc)next_utmp_iter,
	.tp_repr = (reprfunc)repr_utmp_iter,

	/* Members. */

	.tp_methods = utmp_iter_methods
};

/* ---
 * utmp object definition.
 * --- */

/* ``utmp_type``: the main utmp structure.
 * Doesn't define much.
 *
 * TODO: store the path in there? */

struct utmp_type {
	PyObject_HEAD
};

/* ``utmp_instance``: the single instance of this type.
 *
 * Only one utmp_type instance subsists, and it is the one instanciated
 * by default. ``type(pyutmpx.utmp)()`` will return ``pyutmpx.utmp``,
 * much like ``None``. */

static struct utmp_type *utmp_instance = NULL;

/* `new_utmp()`: create an instance of utmp_type.
 * Actually, returns the single instance if already exists. */

static PyObject *new_utmp(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct utmp_type *self;

	if (utmp_instance) {
		Py_XINCREF(utmp_instance);
		return ((PyObject *)utmp_instance);
	}

	self = (struct utmp_type *)type->tp_alloc(type, 0);
	utmp_instance = self;
	return ((PyObject *)self);
}

/* `init_utmp()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_utmp(struct utmp_type *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	return (0);
}

/* `del_utmp()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_utmp(struct utmp_type *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;

	Py_TYPE(self)->tp_free((PyObject *)self);
	utmp_instance = NULL;
}

/* `repr_utmp()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *repr_utmp(struct utmp_type *self)
{
	return (Py_BuildValue("s", "pyutmpx.utmp"));
}

/* `iter_utmp()`: return self because we are iterable. */

static PyObject *iter_utmp(struct utmp_type *self)
{
	return (PyObject_CallObject((PyObject *)&utmp_iter_type, NULL));
}

/* `get_utmp_path()`: getter to the `path` property. */

PyObject *get_utmp_path(PyObject *self, void *cookie)
{
	(void)cookie;

	PyErr_SetString(PyExc_NotImplementedError, "");
	return (NULL);
}

/* Entry object definition. */

static PyMethodDef utmp_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef utmp_getset[] = {
	{"path", (getter)&get_utmp_path, NULL,
		"Path to the raw file, if present.", NULL},
	{NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject utmp_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_type",
	.tp_doc = "utmp entries iterator",
	.tp_basicsize = sizeof(struct utmp_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_utmp,
	.tp_init = (initproc)init_utmp,
	.tp_dealloc = (destructor)del_utmp,
	.tp_iter = (getiterfunc)iter_utmp,
	.tp_repr = (reprfunc)repr_utmp,

	/* Members. */

	.tp_methods = utmp_methods,
	.tp_getset = utmp_getset
};

/* ---
 * Module setup.
 * --- */

int pyutmpx_init_utmp(PyObject *m)
{
	PyObject *utmp;

	/* Create the utmp iterator type. */

	if (PyType_Ready(&utmp_type) < 0
	 || PyType_Ready(&utmp_iter_type) < 0)
		goto fail;

	Py_INCREF(&utmp_type);
	Py_INCREF(&utmp_iter_type);

	/* Create an instance of the utmp type and add it
	 * to the module. */

	utmp = PyObject_CallObject((PyObject *)&utmp_type, NULL);
	if (!utmp || PyModule_AddObject(m, "utmp", utmp) < 0)
		goto fail;

	return (0);
fail:
	return (-1);
}

void pyutmpx_exit_utmp(void)
{
	Py_XDECREF(&utmp_type);
	Py_XDECREF(&utmp_iter_type);
}
