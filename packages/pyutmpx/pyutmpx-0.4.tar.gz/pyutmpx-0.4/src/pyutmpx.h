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

/* Platform specific functions for gathering entries. */

struct utmp_exit_status {
	int *termination_code;
	int *status_code;
};

struct utmp_node {
	struct utmp_node *next;

	struct timeval *time;
	struct utmp_exit_status *exit;

	int *type;

	char *id;
	char *user;
	char *host;
	char *line;
	char *addr;

	unsigned long *pid;
	unsigned long *sid;

	Py_ssize_t id_size;
	Py_ssize_t user_size;
	Py_ssize_t host_size;
	Py_ssize_t line_size;
	Py_ssize_t addr_size;

	unsigned long data[]; /* For alignment purposes. */
};

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

extern int pyutmpx_get_utmp_nodes(struct utmp_node **nodep);
extern int pyutmpx_get_wtmp_nodes(struct utmp_node **nodep);
extern int pyutmpx_get_btmp_nodes(struct utmp_node **nodep);
extern int pyutmpx_get_lastlog_nodes(struct lastlog_node **nodep);

extern char const *pyutmpx_get_utmp_path(void);
extern char const *pyutmpx_get_wtmp_path(void);
extern char const *pyutmpx_get_btmp_path(void);
extern char const *pyutmpx_get_lastlog_path(void);

/* Common utilities defined in utils.c. */

extern void pyutmpx_put_str(char **ps, size_t *pn, char const *s);
extern void pyutmpx_put_repr(char **ps, size_t *pn, PyObject *o);

extern Py_ssize_t pyutmpx_get_len(char const *s, Py_ssize_t n);

extern PyObject *pyutmpx_build_datetime(struct timeval const *tv);
extern PyObject *pyutmpx_build_utmp_entry(struct utmp_node const *node);
extern PyObject *pyutmpx_build_lastlog_entry(struct lastlog_node const *node);

/* Common API defined in utmp_entry.c:
 * Define a utmp entry (for utmp and wtmp files). */

# define PYUTMPX_BOOT_TIME      1
# define PYUTMPX_OLD_TIME       2
# define PYUTMPX_NEW_TIME       3
# define PYUTMPX_USER_PROCESS   4
# define PYUTMPX_INIT_PROCESS   5
# define PYUTMPX_LOGIN_PROCESS  6
# define PYUTMPX_DEAD_PROCESS   7

extern PyTypeObject pyutmpx_exit_status_type;
extern PyTypeObject pyutmpx_utmp_entry_type;
extern PyTypeObject pyutmpx_lastlog_entry_type;

/* Setup functions for all modules. */

extern int pyutmpx_init_utils(PyObject *module);
extern int pyutmpx_init_exit_status_type(PyObject *module);
extern int pyutmpx_init_utmp_entry_type(PyObject *module);
extern int pyutmpx_init_utmp_type(PyObject *module);
extern int pyutmpx_init_wtmp_type(PyObject *module);
extern int pyutmpx_init_btmp_type(PyObject *module);
extern int pyutmpx_init_lastlog_entry_type(PyObject *module);
extern int pyutmpx_init_lastlog_type(PyObject *module);

extern void pyutmpx_exit_lastlog_type(void);
extern void pyutmpx_exit_lastlog_entry_type(void);
extern void pyutmpx_exit_btmp_type(void);
extern void pyutmpx_exit_wtmp_type(void);
extern void pyutmpx_exit_utmp_type(void);
extern void pyutmpx_exit_utmp_entry_type(void);
extern void pyutmpx_exit_exit_status_type(void);
extern void pyutmpx_exit_utils(void);

#endif /* PYUTMPX_H */
