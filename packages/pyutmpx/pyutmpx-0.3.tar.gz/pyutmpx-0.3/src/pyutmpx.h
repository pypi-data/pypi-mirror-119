/* ****************************************************************************
 * pyutmpx.h -- pyutmpx module header.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */
#ifndef  PYUTMPX_H
# define PYUTMPX_H 2018020602
# define PY_SSIZE_T_CLEAN 1
# include <Python.h>
# include <pyerrors.h>
# include <structmember.h>

/* Common utilities defined in utils.c. */

extern PyObject *pyutmpx_get_datetime(struct timeval const *tv);
extern void pyutmpx_put_str(char **ps, size_t *pn, char const *s);
extern void pyutmpx_put_repr(char **ps, size_t *pn, PyObject *o);
extern Py_ssize_t pyutmpx_get_len(char const *s, Py_ssize_t n);

/* Common API defined in utmp_entry.c:
 * Define a utmp entry (for utmp and wtmp files). */

# define PYUTMPX_BOOT_TIME      1
# define PYUTMPX_OLD_TIME       2
# define PYUTMPX_NEW_TIME       3
# define PYUTMPX_USER_PROCESS   4
# define PYUTMPX_INIT_PROCESS   5
# define PYUTMPX_LOGIN_PROCESS  6
# define PYUTMPX_DEAD_PROCESS   7

extern PyTypeObject pyutmpx_utmp_entry_type;
extern PyTypeObject pyutmpx_lastlog_entry_type;

/* Setup functions for all modules. */

extern int pyutmpx_init_utils(PyObject *module);
extern int pyutmpx_init_utmp_entry(PyObject *module);
extern int pyutmpx_init_utmp(PyObject *module);
extern int pyutmpx_init_lastlog_entry(PyObject *module);
extern int pyutmpx_init_lastlog(PyObject *module);

extern void pyutmpx_exit_lastlog(void);
extern void pyutmpx_exit_lastlog_entry(void);
extern void pyutmpx_exit_utmp(void);
extern void pyutmpx_exit_utmp_entry(void);
extern void pyutmpx_exit_utils(void);

#endif /* PYUTMPX_H */
