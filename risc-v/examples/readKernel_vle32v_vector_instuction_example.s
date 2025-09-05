// example of the readKernel for the vector load vle32.v instruction
// 3 stride unrolls, 1 portion unrolls

	.text 
	.global microKernel # Vector

microKernel:  # arr_length=505290240 | in bytes=2021160960

# put registers on stack 
	addi sp, sp, -128
	sd x1, 0(sp)
	sd x3, 8(sp)
	sd x4, 16(sp)
	sd x8, 24(sp)
	sd x9, 32(sp)
	sd x10, 40(sp)
	sd x18, 48(sp)
	sd x19, 56(sp)
	sd x20, 64(sp)
	sd x21, 72(sp)
	sd x22, 80(sp)
	sd x23, 88(sp)
	sd x24, 96(sp)
	sd x25, 104(sp)
	sd x26, 112(sp)
	sd x27, 120(sp)

# loop counter and loop bound  
	addi x3, x0, 0

# loop bound=21053760
	lui x1, 5140
	addi x1, x1, 320

# stride 1 | bytes offset: 0 
	lui x4, 0
	addi x4, x4, 0
	add x4, x4, a0

# stride 2 | bytes offset: 673720320 
	lui x5, 164483
	addi x5, x5, -2048
	add x5, x5, x4

# stride 3 | bytes offset: 1347440640 
	lui x6, 328965
	addi x6, x6, 0
	add x6, x6, x4

	vsetivli x0, 8, e32, m1

.Loop:

	# stride 1
	vle32.v v0, (x4)  #array id: 0 bytes=0
	addi x4, x4, 32

	# stride 2
	vle32.v v1, (x5)  #array id: 0 bytes=0
	addi x5, x5, 32

	# stride 3
	vle32.v v2, (x6)  #array id: 0 bytes=0
	addi x6, x6, 32

# loop control
	addi x3, x3, 1
	bne x3, x1, .Loop


# put registers on stack 
.Epilogue:
	ld x1, 0(sp)
	ld x3, 8(sp)
	ld x4, 16(sp)
	ld x8, 24(sp)
	ld x9, 32(sp)
	ld x10, 40(sp)
	ld x18, 48(sp)
	ld x19, 56(sp)
	ld x20, 64(sp)
	ld x21, 72(sp)
	ld x22, 80(sp)
	ld x23, 88(sp)
	ld x24, 96(sp)
	ld x25, 104(sp)
	ld x26, 112(sp)
	ld x27, 120(sp)
	addi sp, sp, 128
	ret

