/* ****************************************************************************
 * utmp_entry.c -- utmp and wtmp entry definition and utilities.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <string.h>
#include <limits.h>

/* Constants representing entry types. */

static PyObject *boot_time;
static PyObject *old_time;
static PyObject *new_time;
static PyObject *user_process;
static PyObject *init_process;
static PyObject *login_process;
static PyObject *dead_process;

/* ---
 * Entry object definition.
 * --- */

/* ``entry_type``: the type of the entry. */

struct entry_type {
	PyObject_HEAD

	PyObject *id;
	PyObject *type;
	PyObject *user;
	PyObject *host;
	PyObject *line;
	PyObject *time;
	PyObject *pid;
};

/* `new_entry()`: create the Python object. */

static PyObject *new_entry(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	struct entry_type *self;

	self = (struct entry_type *)type->tp_alloc(type, 0);

	if (self) {
		self->id = NULL;
		self->type = NULL;
		self->user = NULL;
		self->host = NULL;
		self->line = NULL;
		self->time = NULL;
		self->pid = NULL;
	}

	return ((PyObject *)self);
}

/* `init_entry()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int init_entry(struct entry_type *self,
	PyObject *args, PyObject *kw)
{
	char *keywords[] = {"id", "type", "user", "host", "line", "time",
		"pid", NULL};

	/* Main parsing and default arguments. */

	if (!PyArg_ParseTupleAndKeywords(args, kw, "|$OOOOOOO", keywords,
		&self->id, &self->type, &self->user, &self->host, &self->line,
		&self->time, &self->pid))
		return (-1);

	/* Check the arguments.
	 * TODO: check their types too! (here?) */

	if (!self->id)
		self->id = Py_None;
	if (!self->type)
		self->type = Py_None;
	if (!self->user)
		self->user = Py_None;
	if (!self->host)
		self->host = Py_None;
	if (!self->line)
		self->line = Py_None;
	if (!self->time)
		self->time = Py_None;
	if (!self->pid)
		self->pid = Py_None;

	Py_INCREF(self->id);
	Py_INCREF(self->type);
	Py_INCREF(self->user);
	Py_INCREF(self->host);
	Py_INCREF(self->line);
	Py_INCREF(self->time);
	Py_INCREF(self->pid);

	return 0;
}

/* `del_entry()`: destroy the Python object.
 * Deinitializes everything it can. */

static void del_entry(struct entry_type *self)
{
	if (!self)
		return;

	Py_XDECREF(self->id);
	Py_XDECREF(self->type);
	Py_XDECREF(self->user);
	Py_XDECREF(self->host);
	Py_XDECREF(self->line);
	Py_XDECREF(self->time);
	Py_XDECREF(self->pid);

	Py_TYPE(self)->tp_free((PyObject*)self);
}

/* ``repr_entry()``: actual C implementation of the ``__repr__`` function
 * for the utmp entry. */

static PyObject *repr_entry(struct entry_type *self)
{
	char buf[1024], *s = buf, *type_name;
	size_t len = 1024;
	int type, haslast = 0;

#define prop(PROP, NAME) \
	if (PyObject_IsTrue(NAME)) { \
		if (haslast) \
			pyutmpx_put_str(&s, &len, ", "); \
		pyutmpx_put_str(&s, &len, PROP " = "); \
		pyutmpx_put_repr(&s, &len, NAME); \
		haslast = 1; \
	}

	pyutmpx_put_str(&s, &len, "pyutmpx.utmp_entry(");

	if (PyObject_IsTrue(self->type)) {
		if (PyArg_Parse(self->type, "i", &type) < 0)
			type = 0;

		switch (type) {
		case PYUTMPX_BOOT_TIME:
			type_name = "pyutmpx.BOOT_TIME";
			break;
		case PYUTMPX_OLD_TIME:
			type_name = "pyutmpx.OLD_TIME";
			break;
		case PYUTMPX_NEW_TIME:
			type_name = "pyutmpx.NEW_TIME";
			break;
		case PYUTMPX_USER_PROCESS:
			type_name = "pyutmpx.USER_PROCESS";
			break;
		case PYUTMPX_INIT_PROCESS:
			type_name = "pyutmpx.INIT_PROCESS";
			break;
		case PYUTMPX_LOGIN_PROCESS:
			type_name = "pyutmpx.LOGIN_PROCESS";
			break;
		case PYUTMPX_DEAD_PROCESS:
			type_name = "pyutmpx.DEAD_PROCESS";
			break;
		default:
			type_name = "(unknown)";
		}

		pyutmpx_put_str(&s, &len, "type = ");
		pyutmpx_put_str(&s, &len, type_name);
		haslast = 1;
	}

	prop("time", self->time)
	prop("user", self->user)
	prop("host", self->host)
	prop("line", self->line)
	prop("pid",  self->pid)

	pyutmpx_put_str(&s, &len, ")");

	return (Py_BuildValue("s", buf));
}

/* Entry object definition. */

static PyMethodDef entry_methods[] = {
	{NULL, NULL, 0, NULL}
};

static PyMemberDef entry_members[] = {
	{"id", T_OBJECT, offsetof(struct entry_type, id),
		READONLY, "Unspecified initialization process identifier."},
	{"type", T_OBJECT, offsetof(struct entry_type, type),
		READONLY, "Type of entry."},
	{"user", T_OBJECT, offsetof(struct entry_type, user),
		READONLY, "User login name."},
	{"line", T_OBJECT, offsetof(struct entry_type, line),
		READONLY, "Device name."},
	{"time", T_OBJECT, offsetof(struct entry_type, time),
		READONLY, "Time entry was made."},
	{"pid", T_OBJECT, offsetof(struct entry_type, pid),
		READONLY, "Process ID."},

	{NULL}
};

PyTypeObject pyutmpx_utmp_entry_type = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp_entry",
	.tp_doc = "utmp entry",
	.tp_basicsize = sizeof(struct entry_type),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = new_entry,
	.tp_init = (initproc)init_entry,
	.tp_dealloc = (destructor)del_entry,
	.tp_repr = (reprfunc)repr_entry,

	/* Members. */

	.tp_methods = entry_methods,
	.tp_members = entry_members
};

/* ---
 * Module setup.
 * --- */

/* `pyutmpx_setup_utmp_entry()`: setup utmp entries and utilities at
 * module-level for further usage. */

#define SETUP_CONST(STATIC_NAME, VALUE, IN_MODULE_NAME) \
	{ \
		if (!(STATIC_NAME = Py_BuildValue("i", VALUE))) \
			return -1; \
		if (PyModule_AddObject(m, IN_MODULE_NAME, STATIC_NAME) < 0) { \
			Py_XDECREF(STATIC_NAME); \
			return -1; \
		} \
	}

int pyutmpx_init_utmp_entry(PyObject *m)
{
	/* Create the utmp constants. */

	SETUP_CONST(boot_time,     PYUTMPX_BOOT_TIME,     "BOOT_TIME")
	SETUP_CONST(old_time,      PYUTMPX_OLD_TIME,      "OLD_TIME")
	SETUP_CONST(new_time,      PYUTMPX_NEW_TIME,      "NEW_TIME")
	SETUP_CONST(user_process,  PYUTMPX_USER_PROCESS,  "USER_PROCESS")
	SETUP_CONST(init_process,  PYUTMPX_INIT_PROCESS,  "INIT_PROCESS")
	SETUP_CONST(login_process, PYUTMPX_LOGIN_PROCESS, "LOGIN_PROCESS")
	SETUP_CONST(dead_process,  PYUTMPX_DEAD_PROCESS,  "DEAD_PROCESS")

	/* Create the utmp entry type to the module. */

	if (PyType_Ready(&pyutmpx_utmp_entry_type) < 0)
		return -1;

	Py_INCREF((PyObject *)&pyutmpx_utmp_entry_type);
	if (PyModule_AddObject(m, "utmp_entry",
		(PyObject *)&pyutmpx_utmp_entry_type) < 0) {
		Py_DECREF(&pyutmpx_utmp_entry_type);
		return -1;
	}

	/* Prepare types. */

	return 0;
}

void pyutmpx_exit_utmp_entry(void)
{
	/* Nothing to do here. */
}
