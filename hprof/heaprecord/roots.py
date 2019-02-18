#!/usr/bin/env python3
#coding=utf8

from .heaprecord import HeapRecord

from ..offset import offset, AutoOffsets, idoffset
from ..errors import RefError

class GcRoot(HeapRecord):
	__slots__ = ()

	@property
	def objid(self):
		return self._read_id(self.offsets.ID)

	def __len__(self):
		return self.offsets.END.flatten(self.hf.idsize)

	def _info(self):
		return 'objid=0x%x' % self.objid

	def __str__(self):
		return '%s(%s)' % (type(self).__name__, self._info())

class UnknownRoot(GcRoot):
	__slots__ = ()
	TAG = 0xff
	offsets = AutoOffsets(1, 'ID', idoffset(1), 'END')

class GlobalJniRoot(GcRoot):
	__slots__ = ()
	TAG = 0x01
	offsets = AutoOffsets(1,
			'ID',     idoffset(1),
			'REFID',  idoffset(1),
			'END')

	@property
	def grefid(self):
		return self._read_id(self.offsets.REFID)

	def _info(self):
		return super()._info() + ', grefid=0x%x' % self.grefid

class LocalJniRoot(GcRoot):
	__slots__ = ()
	TAG = 0x02
	offsets = AutoOffsets(1,
			'ID',     idoffset(1),
			'STRACE', 4,
			'FRAME',  4,
			'END')

	def _info(self):
		return super()._info() + ' in <func>' # TODO: actually show the function here.

class JavaStackRoot(GcRoot):
	__slots__ = ()
	TAG = 0x03
	offsets = AutoOffsets(1,
			'ID',     idoffset(1),
			'THREAD', 4,
			'FRAME',  4,
			'END')

	def _info(self):
		return super()._info() + ' in <func>' # TODO: not <func>

class NativeStackRoot(GcRoot):
	__slots__ = ()
	TAG = 0x04
	offsets = AutoOffsets(1,
			'ID',     idoffset(1),
			'THREAD', 4,
			'END')

	def _info(self):
		return super()._info() + ' from thread ???' # TODO: not "???"

class StickyClassRoot(GcRoot):
	__slots__ = ()
	TAG = 0x05
	offsets = AutoOffsets(1, 'ID', idoffset(1), 'END')

class ThreadRoot(GcRoot):
	__slots__ = ()
	TAG = 0x08
	offsets = AutoOffsets(1,
			'ID',     idoffset(1),
			'THREAD', 4,
			'STRACE', 4,
			'END')

	def _info(self):
		return super()._info() + ' from thread ???' # TODO: actually show the thread here.

class InternedStringRoot(GcRoot):
	__slots__ = ()
	TAG = 0x89
	offsets = AutoOffsets(1, 'ID', idoffset(1), 'END')

class VmInternalRoot(GcRoot):
	__slots__ = ()
	TAG = 0x8d
	offsets = AutoOffsets(1,
			'ID',    idoffset(1),
			'END')
