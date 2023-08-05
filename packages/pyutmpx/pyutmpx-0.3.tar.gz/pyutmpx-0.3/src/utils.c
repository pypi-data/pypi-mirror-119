/* ****************************************************************************
 * utils.c -- general utilities.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <datetime.h>

/* ---
 * Global utilities.
 * --- */

/* `pyutmpx_get_datetime()`: utility to get a datetime from a timeval. */

PyObject *pyutmpx_get_datetime(struct timeval const *tv)
{
	PyObject *result = NULL;
	PyObject *epoch = NULL, *date_delta = NULL;

	epoch = PyDateTime_FromDateAndTime(1970, 1, 1, 0, 0, 0, 0);
	date_delta = PyDelta_FromDSU(0, tv->tv_sec, tv->tv_usec);
	if (!epoch || !date_delta)
		goto fail;

	result = PyNumber_Add(epoch, date_delta);

fail:
	Py_XDECREF(epoch);
	Py_XDECREF(date_delta);

	return (result);
}

/* ``pyutmpx_put_str()``: at the end of ``*ps`` of size ``*pn``, copies the
 * ``s`` string up to ``*pn`` bytes at a maximum, then updates ``*ps`` to the
 * end of the copy and ``*pn`` to the number of left bytes after copy. */

void pyutmpx_put_str(char **ps, size_t *pn, char const *s)
{
	size_t len;

	strncpy(*ps, s, *pn);
	len = strlen(*ps);
	*ps += len;
	*pn -= len;
}

/* ``pyutmpx_put_repr()``: at the end of ``*ps`` of size ``*pn``, copies the
 * string representation of the object ``o`` to ``*pn`` bytes at a maximum,
 * then updates ``*ps`` to the end of the copy and ``*pn`` to the number of
 * left bytes after copy. */

void pyutmpx_put_repr(char **ps, size_t *pn, PyObject *o)
{
	PyObject *repr, *repr_utf8;
	char const *r;
	int has_failed = 1;

	/* Get the representation. */

	repr = PyObject_Repr(o);
	if (!repr)
		goto fail;

	/* Encode the representation as UTF-8 */

	repr_utf8 = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
	Py_DECREF(repr);
	if (!repr_utf8)
		goto fail;

	/* Get a C string from the Python encoded string. */

	r = PyBytes_AS_STRING(repr_utf8);
	Py_DECREF(repr_utf8);

	/* Get a default string if has failed. */

	has_failed = 0;
fail:
	if (has_failed)
		r = "(unknown)";

	/* Copy into the final buffer. */

	pyutmpx_put_str(ps, pn, r);
}

/* `pyutmpx_get_len()`: get the length of the ``s`` string, up to ``n``
 * bytes at a maximum. */

Py_ssize_t pyutmpx_get_len(char const *s, Py_ssize_t n)
{
	Py_ssize_t len;

	if (!s)
		len = 0;
	else if (n <= 0) {
		size_t slen = strlen(s);

		if (slen > INT_MAX)
			len = INT_MAX;
		else
			len = (Py_ssize_t)slen;
	} else {
		char const *ptr = memchr(s, '\0', (size_t)n);

		if (!ptr)
			len = n;
		else
			len = (Py_ssize_t)(ptr - s);
	}

	return (len);
}

/* ---
 * Setup.
 * --- */

int pyutmpx_init_utils(PyObject *module)
{
	/* Import the datetime module. */

	PyDateTime_IMPORT;

	return 0;
}

void pyutmpx_exit_utils(void)
{
	/* Nothing to do here. */
}
