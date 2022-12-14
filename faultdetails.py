#!/usr/bin/env python
"""
ARM Cortex-M stack frame rollback and fault details renderer for GDB. Call this
from inside the fault handler to help determine the cause and soruce of the
fault.

Load script into GDB via:
(gdb) source faultdetails.py

Then in your fault handler/BP:
(gdb) faultdetails()
Fault Status Registers:
  SHCSR: 0x00070008
  CFSR:  0x00020001
  HFSR:  0x40000000
  UsageFault exception active!
  UFSR: 0x0002

Previous Stack Frame: msp
  R0:   0x08007BCC
  R1:   0x00000000
  R2:   0x0000100A
  R3:   0x20010CE0
  R12:  0x00000000
  LR:   0xFFFFFFFD // (EXC_RETURN)
  PC:   0x602B3200
  xPSR: 0x20000006
"""

import gdb


class FaultDetails (gdb.Command):
    """Perform a stack rollback on an ARM Cortex M device, and shows the
    main fault status registers."""

    def __init__(self):
        super(FaultDetails, self).__init__("faultdetails", gdb.COMMAND_USER)

    def dumpfaultregs(self):
        """Dump useful fault status registers"""

        print("Fault Status Registers:")
        # System Handler Control & State Register
        shcsr = int(gdb.parse_and_eval("*(uint32_t *)0xE000ED24"))
        print("  SHCSR: 0x%08X" % shcsr)

        # Configurable Fault Status Register
        cfsr = int(gdb.parse_and_eval("*(uint32_t *)0xE000ED28"))
        print("  CFSR:  0x%08X" % cfsr)

        # Hard Fault Status Register
        hfsr = int(gdb.parse_and_eval("*(uint32_t *)0xE000ED2C"))
        print("  HFSR:  0x%08X" % hfsr)

        # Show fault reason depending on family
        if shcsr & (1 << 0):
            print("  MemManage exception active!")
            print("  MMFSR: 0x%02X\n" % cfsr)
        if shcsr & (1 << 1):
            print("  BusFault exception active!")
            print("  BFSR: 0x%02X\n" % (cfsr >> 8))
        if shcsr & (1 << 3):
            print("  UsageFault exception active!")
            print("  UFSR: 0x%04X\n" % (cfsr >> 16))

    def dumpframe(self, addr):
        """Dump the previous stack frame"""
        # Dumps a stack frame at the specific address
        # gdb.execute("p/a *(uint32_t[8]*)0x%x" % addr)
        r0 = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr)))
        r1 = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+4)))
        r2 = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+8)))
        r3 = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+12)))
        r12 = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+16)))
        lr = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+20)))
        pc = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+24)))
        xpsr = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+28)))
        print("  R0:   0x%08X" % r0)
        print("  R1:   0x%08X" % r1)
        print("  R2:   0x%08X" % r2)
        print("  R3:   0x%08X" % r3)
        print("  R12:  0x%08X" % r12)
        print("  LR:   0x%08X // (EXC_RETURN)" % lr)
        print("  PC:   0x%08X" % pc)
        print("  xPSR: 0x%08X" % xpsr)

    def dumpfunc(self, addr):
        """List the source code from the previous stack frame"""
        pc = int(gdb.parse_and_eval("*(uint32_t *)0x%08X" % (addr+24)))
        print("\nPrevious Function:")
        gdb.execute("list *0x%08X" % pc)

    def invoke(self, arg, from_tty):
        # Dump useful debug registers
        self.dumpfaultregs()

        # Check bit 2 of EXC_RETURN ($lr) for stack pointer and dump stack
        exc_return = gdb.parse_and_eval("$lr")
        sp = None
        if (exc_return & (1 << 2)):
            print("Previous Stack Frame: psp")
            sp = gdb.parse_and_eval("$psp")
        else:
            print("Previous Stack Frame: msp")
            sp = gdb.parse_and_eval("$msp")

        # Dump the previous stack frame's contents
        self.dumpframe(sp)

        # Display the calling function
        self.dumpfunc(sp)


FaultDetails()
