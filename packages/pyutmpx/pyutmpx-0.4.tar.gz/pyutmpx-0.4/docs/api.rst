API Reference
=============

.. py:module:: pyutmpx

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

utmp entry types
----------------

.. py:data:: BOOT_TIME: int = 1

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a host boot event.

.. py:data:: OLD_TIME: int = 2

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a time yield event before system time change.

.. py:data:: NEW_TIME: int = 3

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a time yield event after system time change.

.. py:data:: USER_PROCESS: int = 4

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a user process.

.. py:data:: INIT_PROCESS: int = 5

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a process spawned by the init process.

.. py:data:: LOGIN_PROCESS: int = 6

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a process which is the session leader of a user.

.. py:data:: DEAD_PROCESS: int = 7

	When :py:attr:`utmp_entry.type` is set to this value, the event is
	a session leader who has exited.

Entry formats
-------------

.. py:class:: utmp_entry

	Representation of a utmp entry as found in the utmp and wtmp files.

	.. py:attribute:: id: str

		The unspecified initialization process identifier of the event.

		Equivalent of ``utx->ut_id``

	.. py:attribute:: type: int

		The event type, amongst the values described previously.

		Equivalent of ``utx->ut_type``.

	.. py:attribute:: user: str

		The login of the user involved in the event.

		Equivalent of ``utx->ut_user``.

	.. py:attribute:: host: str

		The host from which the event has occurred.

		Equivalent of ``utx->ut_host``.

	.. py:attribute:: line: str

		The line on which the event has occurred.

		Equivalent of ``utx->ut_line``.

	.. py:attribute:: time: datetime.datetime

		The local time at which the event has occurred.

		Equivalent of ``utx->ut_tv``.

	.. py:attribute:: pid: int

		The identifier of the process that acts as session leader for
		the given user (for most events).

		Equivalent of ``utx->ut_pid``.

.. py:class:: lastlog_entry

	Representation of a lastlog entry as found in the lastlog file.

	.. py:attribute:: uid: int

		The user identifier, to be matched with entries in ``/etc/passwd``.

		Determined from the offset of the entry within the file, as a
		factor of ``sizeof(struct lastlog)``.

	.. py:attribute:: host: str

		The host from which last login has occurred.

		Equivalent of ``ll->ll_host``.

	.. py:attribute:: line: str

		The line on which last login has occurred.

		Equivalent of ``ll->ll_line``.

	.. py:attribute:: time: datetime.datetime

		The local time of last login.

		Equivalent of ``ll->ll_time``.

Classes abstracting the databases
---------------------------------

.. py:class:: utmp

	An iterable read-only view of the utmp database, yielding
	:py:class:`utmp_entry` instances.

.. py:class:: lastlog

	An iterable read-only view of the lastlog database, yielding
	:py:class:`lastlog_entry` instances.
