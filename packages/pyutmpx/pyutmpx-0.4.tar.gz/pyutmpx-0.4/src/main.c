/* ****************************************************************************
 * main.c -- pyutmpx module definition.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"

/* ---
 * Module definition.
 * --- */

/* Module deinitialization.
 * We ought to deinitialize objects that the user can't see. */

static void del_module(void *module)
{
	pyutmpx_exit_lastlog_type();
	pyutmpx_exit_lastlog_entry_type();
	pyutmpx_exit_btmp_type();
	pyutmpx_exit_wtmp_type();
	pyutmpx_exit_utmp_type();
	pyutmpx_exit_utmp_entry_type();
	pyutmpx_exit_exit_status_type();
	pyutmpx_exit_utils();
}

/* Module methods. */

static PyMethodDef module_methods[] = {
	{NULL, NULL, 0, NULL}
};

/* Module definition. */

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,

	/* .m_name = */ "pyutmpx",
	/* .m_doc = */ "This module provides a utmp reader.",
	/* .m_size = */ -1,
	/* .m_methods = */ module_methods,
	/* .m_slots = */ NULL,
	/* .m_traverse = */ NULL,
	/* .m_clear = */ NULL,
	/* .m_free = */ &del_module
};

/* ---
 * Module initialization.
 * --- */

PyMODINIT_FUNC PyInit_pyutmpx(void)
{
	PyObject *m;

	/* Initialize the module. */

	m = PyModule_Create(&module);
	if (!m)
		goto fail;

	/* Version. */

	if (PyModule_AddStringConstant(m, "version", PYUTMPX_VERSION) < 0)
		goto fail;

	/* Setup the various modules. */

	if (pyutmpx_init_utils(m))
		goto fail;
	if (pyutmpx_init_exit_status_type(m))
		goto fail;
	if (pyutmpx_init_utmp_entry_type(m))
		goto fail;
	if (pyutmpx_init_utmp_type(m))
		goto fail;
	if (pyutmpx_init_wtmp_type(m))
		goto fail;
	if (pyutmpx_init_btmp_type(m))
		goto fail;
	if (pyutmpx_init_lastlog_entry_type(m))
		goto fail;
	if (pyutmpx_init_lastlog_type(m))
		goto fail;

	/* Everything went well in the end :) */

	return (m);
fail:
	Py_XDECREF(m);
	return (NULL);
}
