// example of the readKernel for the scalar load flw instruction
// 2 stride unrolls, 2 portion unrolls

	.text 
	.global microKernel # Scalar

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

# loop bound=126322560
	lui x1, 30840
	addi x1, x1, 1920

# stride 1 | bytes offset: 0 
	lui x4, 0
	addi x4, x4, 0
	add x4, x4, a0

# stride 2 | bytes offset: 1010580480 
	lui x5, 246724
	addi x5, x5, -1024
	add x5, x5, x4

.Loop:

	# stride 1
	flw f0, 0(x4) #array id: 0 bytes=0
	flw f1, 4(x4) #array id: 1 bytes=4

	# stride 2
	flw f2, 0(x5) #array id: 252645120 bytes=1010580480
	flw f3, 4(x5) #array id: 252645121 bytes=1010580484

# update stride address registers
	addi x4, x4, 8
	addi x5, x5, 8

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

