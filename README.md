# gdb-m33
This repository groups a set of gdb script for m33

## sau_mpu_dump
It's a python module for gdb. This adds some gdb commands to:
- dump sau
- dump mpu secure or non secure

### Dependencies
- [gdb](https://www.gnu.org/software/gdb/)

### How to use
These commands support tab completion to complete parameters
- Source the sau_mpu_dump module in gdb interface:
```
(gdb) source ../gdb-m33/sau_mpu_dump.py
```

#### sau_dump
- Help:
```
(gdb) help sau_dump
Perform a sau dump on ARM Cortex M device
```

- Dump
```
(gdb) sau_dump
show 8 sau region(s)
sau0 addr: base:0x80100000 limit:0x808fffff enabled
sau1 addr: base:0x80a00000 limit:0x811fffff enabled
sau2 addr: base:0x800ffd00 limit:0x800ffd5f enabled  Region is Non-secure callable
sau3 addr: base:0x40000000 limit:0x4fffffff enabled
sau4 addr: base:0x81200000 limit:0x812fffff enabled
sau5 addr: base:0x00000000 limit:0x0000001f disabled
sau6 addr: base:0x00000000 limit:0x0000001f disabled
sau7 addr: base:0x00000000 limit:0x0000001f disabled
```

#### mpu_dump
- Help:
```
(gdb) help mpu_dump
Perform a Mpu dump on ARM Cortex M device.

       mpu_dump [secure|non-secure]
```

- Dump
```
(gdb) mpu_dump secure
mpu: secure
mpu ctrl: 0x00000007: enabled

16 mpu region(s)
----------------
mpu0 	addr: base:0x800ffd00 limit:0x800ffd3f enabled
		-Non-shareable
		-Read-only by any privilege level
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 1
mpu1 	addr: base:0x800158c0 limit:0x800333bf enabled
		-Non-shareable
		-Read-only by any privilege level
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 1
mpu2 	addr: base:0x80008ce0 limit:0x8000a71f enabled
		-Non-shareable
		-Read-only by any privilege level
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 1
mpu3 	addr: base:0x80901000 limit:0x80902a7f enabled
		-Non-shareable
		-Read/write by any privilege level
		-Execution not permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 2
mpu4 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu5 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu6 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu7 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu8 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu9 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu10 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu11 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu12 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu13 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu14 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0
mpu15 	addr: base:0x00000000 limit:0x0000001f disabled
		-Non-shareable
		-Read/write by privileged code only
		-Execution only permitted if read permitted
		-Execution only permitted if read permitted
		-Attribute index associates to MPU_MAIR0|1: 0

memory attributes
-----------------
	index0 attributes:0x04
		-Device-nGnRE
	index1 attributes:0xaa
		-Normal memory, Outer write-through non-transient read
		-Normal memory, Inner write-through non-transient read
	index2 attributes:0xff
		-Normal memory, Outer write-back non-transient read write
		-Normal memory, Inner write-back non-transient read write
	index3 attributes:0x00
		-Device-nGnRnE
	index4 attributes:0x00
		-Device-nGnRnE
	index5 attributes:0x00
		-Device-nGnRnE
	index6 attributes:0x00
		-Device-nGnRnE
	index7 attributes:0x00
		-Device-nGnRnE
```
## Authors
Ludovic Barre 1udovic.6arre@gmail.com

## License
This project is licensed under the GPL V2 License - see the [LICENSE.md](LICENSE.md) file for details
