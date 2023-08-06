/* ****************************************************************************
 * sys.c -- system-specific implementation.
 * Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <utmp.h>

#ifndef  _PATH_BTMP
# define _PATH_BTMP "/var/log/btmp"
#endif

/* ---
 * utmp entries gathering.
 * --- */

/* ``get_utmp_node()``: get a utmp node for GNU/Linux. */

struct utmp_node_data {
	int type;
	int exit_termination_code;
	int exit_status_code;

	unsigned long pid;
	unsigned long sid;

	struct timeval time;
	struct utmp_exit_status exit;

	char data[];
};

static struct utmp_node *get_utmp_node(struct utmp const *ent)
{
	int type;
	char formatted_addr[100];
	char const *addr;
	Py_ssize_t id_len, user_len, host_len, line_len, addr_len;
	struct utmp_node *node;
	size_t node_size;

	/* Get the entry type. */

	switch (ent->ut_type) {
#ifdef BOOT_TIME
	case BOOT_TIME:
		type = PYUTMPX_BOOT_TIME;
		break;
#endif
#ifdef OLD_TIME
	case OLD_TIME:
		type = PYUTMPX_OLD_TIME;
		break;
#endif
#ifdef NEW_TIME
	case NEW_TIME:
		type = PYUTMPX_NEW_TIME;
		break;
#endif
#ifdef USER_PROCESS
	case USER_PROCESS:
		type = PYUTMPX_USER_PROCESS;
		break;
#endif
#ifdef INIT_PROCESS
	case INIT_PROCESS:
		type = PYUTMPX_INIT_PROCESS;
		break;
#endif
#ifdef LOGIN_PROCESS
	case LOGIN_PROCESS:
		type = PYUTMPX_LOGIN_PROCESS;
		break;
#endif
#ifdef DEAD_PROCESS
	case DEAD_PROCESS:
		type = PYUTMPX_DEAD_PROCESS;
		break;
#endif
	default:
		return NULL;
	}

	/* Prepare the address. */

	addr = NULL;
	if (ent->ut_addr_v6[1] || ent->ut_addr_v6[2] || ent->ut_addr_v6[3])
		addr = inet_ntop(AF_INET6, &ent->ut_addr_v6,
			formatted_addr, sizeof formatted_addr);
	else if (ent->ut_addr_v6[0])
		addr = inet_ntop(AF_INET, &ent->ut_addr_v6,
			formatted_addr, sizeof formatted_addr);

	if (!addr)
		addr = "";

	/* Get the lengths. */

	id_len = pyutmpx_get_len(ent->ut_id, 4);
	user_len = pyutmpx_get_len(ent->ut_user, sizeof ent->ut_user);
	host_len = pyutmpx_get_len(ent->ut_host, sizeof ent->ut_host);
	line_len = pyutmpx_get_len(ent->ut_line, sizeof ent->ut_line);
	addr_len = strlen(addr);

	/* Allocate the node. */

	node_size = sizeof(struct utmp_node)
		+ sizeof(struct utmp_node_data)
		+ id_len + user_len + host_len + line_len + addr_len;
	node = malloc(node_size);
	if (!node)
		return 0; /* We quit cowardly, pretenting nothing follows. */

	memset(node, 0, node_size);

	node->next = NULL;

	{
		struct utmp_node_data *data = (struct utmp_node_data *)&node->data;

		node->type = &data->type;
		data->type = type;

		if (type == PYUTMPX_DEAD_PROCESS) {
			node->exit = &data->exit;
			node->exit->termination_code = &data->exit_termination_code;
			node->exit->status_code = &data->exit_status_code;

			data->exit_termination_code = ent->ut_exit.e_termination;
			data->exit_status_code = ent->ut_exit.e_exit;
		}

		node->pid = &data->pid;
		node->sid = &data->sid;
		node->time = &data->time;

		data->pid = ent->ut_pid;
		data->sid = ent->ut_session;
		data->time.tv_sec = ent->ut_tv.tv_sec;
		data->time.tv_usec = ent->ut_tv.tv_usec;

		node->id = data->data;
		node->user = node->id + id_len;
		node->host = node->user + user_len;
		node->line = node->host + host_len;
		node->addr = node->line + line_len;

		node->id_size = id_len;
		node->user_size = user_len;
		node->host_size = host_len;
		node->line_size = line_len;
		node->addr_size = addr_len;

		if (id_len)
			memcpy(node->id, ent->ut_id, id_len);
		if (user_len)
			memcpy(node->user, ent->ut_user, user_len);
		if (host_len)
			memcpy(node->host, ent->ut_host, host_len);
		if (line_len)
			memcpy(node->line, ent->ut_line, line_len);
		if (addr_len)
			memcpy(node->addr, addr, addr_len);
	}

	return (node);
}

/* ``pyutmpx_get_utmp_nodes()``: gathers the utmp entries as nodes. */

int pyutmpx_get_utmp_nodes(struct utmp_node **nodep)
{
	int fd;

	*nodep = NULL;

	fd = open(_PATH_UTMP, O_RDONLY, 0);
	if (fd < 0)
		return 0; /* Escape cowardly. */

	while (1) {
		struct utmp arr[100];
		size_t arr_size;
		ssize_t read_size;

		read_size = read(fd, &arr, sizeof (arr));
		if (read_size <= 0)
			break; /* Escape cowardly. */

		arr_size = read_size / sizeof (arr[0]);
		for (size_t i = 0; i < arr_size; i++) {
			struct utmp_node *node;

			node = get_utmp_node(&arr[i]);
			if (node) {
				*nodep = node;
				nodep = &node->next;
			}
		}
	}

	close(fd);
	return 0;
}

/* ``pyutmpx_get_wtmp_nodes()``: gather the wtmp entries as nodes. */

int pyutmpx_get_wtmp_nodes(struct utmp_node **nodep)
{
	struct utmp_node *node;
	int fd;

	*nodep = NULL;

	fd = open(_PATH_WTMP, O_RDONLY, 0);
	if (fd < 0)
		return 0; /* Escape cowardly. */

	while (1) {
		struct utmp arr[100];
		size_t arr_size;
		ssize_t read_size;

		read_size = read(fd, &arr, sizeof (arr));
		if (read_size <= 0)
			break; /* Escape cowardly. */

		arr_size = read_size / sizeof (arr[0]);
		for (size_t i = 0; i < arr_size; i++) {
			node = get_utmp_node(&arr[i]);
			if (node) {
				*nodep = node;
				nodep = &node->next;
			}
		}
	}

	close(fd);
	return 0;
}

/* ``pyutmpx_get_btmp_nodes()``: gather the wtmp entries as nodes. */

int pyutmpx_get_btmp_nodes(struct utmp_node **nodep)
{
	struct utmp_node *node;
	int fd;

	*nodep = NULL;

	fd = open(_PATH_BTMP, O_RDONLY, 0);
	if (fd < 0)
		return 0; /* Escape cowardly. */

	while (1) {
		struct utmp arr[100];
		size_t arr_size;
		ssize_t read_size;

		read_size = read(fd, &arr, sizeof (arr));
		if (read_size <= 0)
			break; /* Escape cowardly. */

		arr_size = read_size / sizeof (arr[0]);
		for (size_t i = 0; i < arr_size; i++) {
			node = get_utmp_node(&arr[i]);
			if (node) {
				*nodep = node;
				nodep = &node->next;
			}
		}
	}

	close(fd);
	return 0;
}

/* ---
 * lastlog entries gathering.
 * --- */

/* `pyutmpx_get_lastlog_nodes()`: gather last nodes. */

int pyutmpx_get_lastlog_nodes(struct lastlog_node **nodep)
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
			break; /* Escape cowardly. */
		if (!result)
			break; /* End of file! */

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
 * Get paths.
 * --- */

/* ``pyutmpx_get_utmp_path()``: get the path for the utmp file. */

char const *pyutmpx_get_utmp_path(void)
{
	return _PATH_UTMP;
}

/* ``pyutmpx_get_wtmp_path()``: get the path for the wtmp file. */

char const *pyutmpx_get_wtmp_path(void)
{
	return _PATH_WTMP;
}

/* ``pyutmpx_get_btmp_path()``: get the path for the btmp file. */

char const *pyutmpx_get_btmp_path(void)
{
	return _PATH_BTMP;
}

/* ``pyutmpx_get_lastlog_path()``: getthe path for the lastlog file. */

char const *pyutmpx_get_lastlog_path(void)
{
	return _PATH_LASTLOG;
}
