#!/usr/bin/env python
#
# Copyright 2022 Ludovic Barre <1udovic.6arre@gmail.com>
#
# sau_mpu_dump is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# sau_mpu_dump is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with sau_mpu_dump.  If not, see <https://www.gnu.org/licenses/>.
"""
ARM Cortex-M toolbox:
    - SAU dump
    - MPU dump

Load script into GDB via:
(gdb) source sau_mpu_dump.py

(gdb) sau_dump
(gdb) mpu_dump

"""

import gdb

long_int = gdb.lookup_type('unsigned long')

def to_hex(v: gdb.Value) -> str:
    """Returns v in hex padded with leading zeros"""
    return f"{int(v):#0{8}x}"

def get_register(reg_addr):
    value = int(gdb.parse_and_eval("*(uint32_t *){:#x}".format(reg_addr)).cast(long_int))
    return value

def set_register(addr, value):
    gdb.execute("set *{:#x}={}".format(addr, value))

class SauDump(gdb.Command):
    """Perform a sau dump on ARM Cortex M device."""

    def __init__(self):
        super(SauDump, self).__init__("sau_dump", gdb.COMMAND_USER)
        self.sau_registers = {'SAU_CTRL':0xe000edd0,
                              'SAU_TYPE':0xe000edd4,
                              'SAU_RNR':0xe000edd8,
                              'SAU_RBAR':0xe000eddc,
                              'SAU_RLAR':0xe000ede0,
                              'SFSR':0xe000ede4,
                              'SFAR':0xe000ede8}

    def en_description(self, reg_rlar):
        en_desc = {0: "disabled",
                   1: "enabled"}

        en = (reg_rlar & 0x1)
        return en_desc.get(en)

    def nsc_description(self, reg_rlar):
        nsc_desc = {0: "",
                    1: "Region is Non-secure callable"}

        nsc = (reg_rlar & 0x2) >> 1
        return nsc_desc.get(nsc)

    def get_sau_region(self, indice):
        """Get sau region X"""
        sau_region = []

        set_register(self.sau_registers['SAU_RNR'], indice)

        rbar = get_register(self.sau_registers['SAU_RBAR'])
        rlar = get_register(self.sau_registers['SAU_RLAR'])

        sau_region += [{"indice": indice,
                        "rbar": rbar,
                        "rlar": rlar}]

        return sau_region

    def show_sau_region(self, regions):
        """Show sau region X"""
        gdb.write("show {} sau region(s)\n".format(len(regions)))

        for reg in regions:
            gdb.write("sau{} addr: base:{:#010x} limit:{:#010x} {:8} {}\n".format(
                reg['indice'],
                reg['rbar'] & 0xFFFFFFE0,
                reg['rlar'] | 0x1F,
                self.en_description(reg['rlar']),
                self.nsc_description(reg['rlar'])))

    def invoke(self, arg, from_tty):
        regions = []

        nb_region = get_register(self.sau_registers['SAU_TYPE'])

        for i in range(nb_region):
            regions += self.get_sau_region(i)

        self.show_sau_region(regions)

class MpuDump(gdb.Command):
    """Perform a Mpu dump on ARM Cortex M device.

       mpu_dump [secure|non-secure]
    """

    def __init__(self):
        super(MpuDump, self).__init__("mpu_dump", gdb.COMMAND_USER)
        self.mpu_reg = self.mpu_s_reg = {'MPU_TYPE':0xe000ed90,
                                         'MPU_CTRL':0xe000ed94,
                                         'MPU_RNR':0xe000ed98,
                                         'MPU_RBAR':0xe000ed9c,
                                         'MPU_RLAR':0xe000eda0,
                                         'MPU_MAIR0':0xe000edc0,
                                         'MPU_MAIR1':0xe000edc4}

        self.mpu_ns_reg = {'MPU_TYPE':0xe002ed90,
                           'MPU_CTRL':0xe002ed94,
                           'MPU_RNR':0xe002ed98,
                           'MPU_RBAR':0xe002ed9c,
                           'MPU_RLAR':0xe002eda0,
                           'MPU_MAIR0':0xe002edc0,
                           'MPU_MAIR1':0xe002edc4}

        self.parameters = {'secure': self.mpu_s_reg ,
                           'non-secure': self.mpu_ns_reg}

    def complete(self, text, word):
        args = str(text).split(" ")
        if len(args) > 1:
            return gdb.COMPLETE_NONE

        filt = filter(lambda x: x.startswith(args[0]), self.parameters)

        return filt

    def get_mpu_region(self, indice):
        """Get mpu region X"""
        mpu_region = []

        set_register(self.mpu_reg['MPU_RNR'], indice)

        rbar = get_register(self.mpu_reg['MPU_RBAR'])
        rlar = get_register(self.mpu_reg['MPU_RLAR'])

        mpu_region += [{"indice": indice,
                        "rbar": rbar,
                        "rlar": rlar}]

        return mpu_region

    def sh_description(self, reg_rbar):
        sh_desc = {0: "Non-shareable",
                   1: "reserved",
                   2: "Outer Shareable",
                   3: "Inner Shareable"}

        sh = (reg_rbar & 0x18) >> 3
        return sh_desc.get(sh)

    def ap_description(self, reg_rbar):
        ap_desc = {0: "Read/write by privileged code only",
                   1: "Read/write by any privilege level",
                   2: "Read-only by privileged code only",
                   3: "Read-only by any privilege level"}

        ap = (reg_rbar & 0x6) >> 1
        return ap_desc.get(ap)

    def xn_description(self, reg_rbar):
        xn_desc = {0: "Execution only permitted if read permitted",
                   1: "Execution not permitted"}

        xn = (reg_rbar & 0x1)
        return xn_desc.get(xn)

    def pxn_description(self, reg_rlar):
        pxn_desc = {0: "Execution only permitted if read permitted",
                    1: "Execution from a privileged mode is not permitted"}

        pxn = (reg_rlar & 0x10) >> 4
        return pxn_desc.get(pxn)

    def attr_dev_description(self, attr):
        dev_desc = {0: "Device-nGnRnE",
                    1: "Device-nGnRE",
                    2: "Device-nGRE",
                    3: "Device-GRE"}

        device = (attr & 0xC) >> 2
        return dev_desc.get(device)

    def attr_description(self, attr):
        pol_desc = {0: "write-through transient",
                    1: "write-back transient",
                    2: "write-through non-transient",
                    3: "write-back non-transient"}

        policy = (attr & 0xC) >> 2
        rw = (attr & 0x3)

        if policy == 0x1 and rw == 0x0:
            return "non-cacheable"

        desc = pol_desc.get(policy)

        if rw & 0x2:
            desc += " read"

        if rw & 0x1:
            desc += " write"

        return desc

    def attr_idx(self, reg_rlar):
        idx = (reg_rlar & 0xE) >> 1
        return idx

    def attr_device(self, attr):
        if attr & 0xF0:
            return False
        return True

    def en_description(self, reg_rlar):
        en_desc = {0: "disabled",
                   1: "enabled"}

        en = (reg_rlar & 0x1)
        return en_desc.get(en)

    def show_mpu_region(self, regions):
        """Show mpu region X"""

        for reg in regions:
            gdb.write("mpu{} \taddr: base:{:#010x} limit:{:#010x} {}\n".format(
                reg['indice'],
                reg['rbar'] & 0xFFFFFFE0,
                reg['rlar'] | 0x1F,
                self.en_description(reg['rlar'])))

            gdb.write("\t\t-{}\n".format(self.sh_description(reg['rbar'])))
            gdb.write("\t\t-{}\n".format(self.ap_description(reg['rbar'])))
            gdb.write("\t\t-{}\n".format(self.xn_description(reg['rbar'])))
            gdb.write("\t\t-{}\n".format(self.pxn_description(reg['rlar'])))
            gdb.write("\t\t-Attribute index associates to MPU_MAIR0|1: {}\n".format(
                self.attr_idx(reg['rlar'])))

    def invoke(self, arg, from_tty):
        args = str(arg).split(" ")
        regions = []

        filt = filter(lambda x: x == args[0], self.parameters)

        if len(args) > 1 or not list(filt):
            gdb.write("Invalide parameter\n")
            gdb.execute("help mpu_dump")
            return

        gdb.write("mpu: {}\n".format(args[0]))
        self.mpu_reg = self.parameters[args[0]]

        mpu_ctrl = get_register(self.mpu_reg['MPU_CTRL'])
        gdb.write("mpu ctrl: {:#010x}: {}\n\n".format(mpu_ctrl, self.en_description(mpu_ctrl)))

        mpu_type = get_register(self.mpu_reg['MPU_TYPE'])
        nb_region = (mpu_type & 0xFF00) >> 8

        for i in range(nb_region):
            regions += self.get_mpu_region(i)

        gdb.write("{} mpu region(s)\n".format(len(regions)))
        gdb.write("----------------\n")
        self.show_mpu_region(regions)

        gdb.write("\nmemory attributes\n")
        gdb.write("-----------------\n")

        mair0 = get_register(self.mpu_reg['MPU_MAIR0'])
        mair1 = get_register(self.mpu_reg['MPU_MAIR1'])
        mair = (mair1 << 32) | mair0

        for j in range(8):
            attr = (mair >> (8*j)) & 0xFF
            inner = attr & 0xF
            outer = (attr & 0xF0) >> 4
            gdb.write("\tindex{} attributes:{:#04x}\n".format(j, attr))

            if self.attr_device(attr):
                gdb.write("\t\t-{}\n".format(self.attr_dev_description(attr)))
            else:
                gdb.write("\t\t-Normal memory, Outer {}\n".format(self.attr_description(outer)))
                gdb.write("\t\t-Normal memory, Inner {}\n".format(self.attr_description(inner)))

MpuDump()
SauDump()
