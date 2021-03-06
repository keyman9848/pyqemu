#!/usr/bin/env python

# This file defines Events that will be instantiated by
# ev_* in PyQemu.py
#
# Event classes are used to handle them correctly in
# VirtualMachine/OS/Heuristic ...
#

class QemuEvent:
	def __init__(self, event_type, *args):
		self.event_type = event_type
		self.args = args
	
class QemuFunctionEntropyEvent(QemuEvent):
	def getStart(self):
		return self.args[0]
	def getEntropyChange(self):
		return self.args[1]
	start = property(getStart)
	entropychange = property(getEntropyChange)

class QemuFunctionTaintEvent(QemuEvent):
	def getStart(self):
		return self.args[0]
	def getQuotient(self):
		return self.args[1]
	start = property(getStart)
	quotient = property(getQuotient)


class QemuConstSearchEvent(QemuEvent):
	def getEIP(self):
		return self.args[1]
	def getPattern(self):
		return self.args[0]
	eip = property(getEIP)
	pattern = property(getPattern)

class QemuCodeSearchEvent(QemuEvent):
	def getEIP(self):
		return self.args[1]
	def getPattern(self):
		return self.args[0]
	eip = property(getEIP)
	pattern = property(getPattern)

class QemuFunctiontraceEvent(QemuEvent):
	def getEIP(self):
		return self.args[0]
	def getType(self):
		return self.args[1]

	def isCall(self):
		return self.args[1] == 0
	def isRet(self):
		return self.args[1] == 1
	def isLateRet(self):
		return self.args[1] == 2
	eip = property(getEIP)
	type = property(getType)

class QemuArithwindowEvent(QemuEvent):
	def getEIP(self):
		return self.args[0]
	eip = property(getEIP)

class QemuCaballeroEvent(QemuEvent):
	def getEIP(self):
		return self.args[0]
	def getICount(self):
		return self.args[1]
	def getArithCount(self):
		return self.args[2]
	eip    = property(getEIP)
	icount = property(getICount)
	arith  = property(getArithCount)

class QemuBranchEvent(QemuEvent):
	def getFrom(self):
		return self.args[0]
	def getTo(self):
		return self.args[1]
	fromaddr = property(getFrom)
	toaddr   = property(getTo)

class QemuCallEvent(QemuBranchEvent):
	def getNext(self):
		return self.args[2]
	def getESP(self):
		return self.args[3]
	nextaddr = property(getNext)
	esp      = property(getESP)

class QemuJmpEvent(QemuBranchEvent):
	pass

class QemuSyscallEvent(QemuEvent):
	def getNumber(self):
		return self.args[0]
	number = property(getNumber)

class QemuRetEvent(QemuBranchEvent):
	pass
	
class QemuBreakpointEvent(QemuEvent):
	def getAddr(self):
		return self.args[0]
	addr = property(getAddr)

class QemuMemtraceEvent(QemuEvent):
	def getAddr(self):
		return self.args[0]
	def getValue(self):
		return self.args[1]
	def getSize(self):
		return self.args[2]
	def isWrite(self):
		return self.args[3]==1

	addr    = property(getAddr)
	value   = property(getValue)
	size    = property(getSize)
	writes  = property(isWrite)

class QemuBBLEvent(QemuEvent):
	def getEIP(self):
		return self.args[0]
	def getESP(self):
		return self.args[1]
	eip = property(getEIP)
	esp = property(getESP)

class QemuScheduleEvent(QemuEvent):
	def getPrevious(self):
		return self.args[0]
	def getCurrent(self):
		return self.args[1]
	prev = property(getPrevious)
	cur  = property(getCurrent)

QemuEventTypes = {
	"call":QemuCallEvent,
	"jmp":QemuJmpEvent,
	"ret":QemuRetEvent,
	"syscall":QemuSyscallEvent,
	"breakpoint":QemuBreakpointEvent,
	"memtrace":QemuMemtraceEvent,
	"schedule":QemuScheduleEvent,
	"bbl":QemuBBLEvent,
	"caballero":QemuCaballeroEvent,
	"arithwindow":QemuArithwindowEvent,
	"functiontrace":QemuFunctiontraceEvent,
	"functionentropy":QemuFunctionEntropyEvent,
	"functiontaint":QemuFunctionTaintEvent,
	"constsearch":QemuConstSearchEvent,
	"codesearch":QemuCodeSearchEvent,
}



def createEventObject(ev, *args):
	try:
		return QemuEventTypes[ev](ev, *args)
	except KeyError:
		raise Exception("Unknown event type: %s"%ev)
