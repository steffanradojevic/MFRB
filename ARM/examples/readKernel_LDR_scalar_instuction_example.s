// example of the readKernel for the scalar load LDR instruction
// 2 stride unrolls, 5 portion unrolls

	.text 
	.global microKernel // ARM 

microKernel:  // arr_length=23529410 | in bytes=94117640

// put registers on stack 
	sub sp, sp, #128 
	stp x19, x20, [sp, #16]  
	stp x21, x22, [sp, #32]  
	stp x23, x24, [sp, #48]  
	stp x25, x26, [sp, #64]  
	stp x27, x28, [sp, #80]  
	stp x29, x30, [sp, #96]  

// loop counter and loop bound  
	movz x1, #0

// loop bound=2352941
	movz x2, #59181
	movk x2, #35, LSL #16
	movk x2, #0, LSL #32
	movk x2, #0, LSL #48

// stride 1 | array_id: 0 | bytes offset: 0 
	movz x3, #0
	movk x3, #0, LSL #16
	movk x3, #0, LSL #32
	movk x3, #0, LSL #48
	add x3, x3, x0

// stride 2 | array_id: 11764705 | bytes offset: 47058820 
	movz x4, #3972
	movk x4, #718, LSL #16
	movk x4, #0, LSL #32
	movk x4, #0, LSL #48
	add x4, x4, x0

.Loop:

	// stride 1
	ldr s0,[x3], #4 //array id: 0 bytes=0
	ldr s1,[x3], #4 //array id: 1 bytes=4
	ldr s2,[x3], #4 //array id: 2 bytes=8
	ldr s3,[x3], #4 //array id: 3 bytes=12
	ldr s4,[x3], #4 //array id: 4 bytes=16

	// stride 2
	ldr s5,[x4], #4 //array id: 11764705 bytes=47058820
	ldr s6,[x4], #4 //array id: 11764706 bytes=47058824
	ldr s7,[x4], #4 //array id: 11764707 bytes=47058828
	ldr s8,[x4], #4 //array id: 11764708 bytes=47058832
	ldr s9,[x4], #4 //array id: 11764709 bytes=47058836

// loop condition
	add x1, x1, #1
	cmp x1, x2
	BNE .Loop

.Eind:

// put registers on stack 
	ldp x19, x20, [sp, #16]  
	ldp x21, x22, [sp, #32]  
	ldp x23, x24, [sp, #48]  
	ldp x25, x26, [sp, #64]  
	ldp x27, x28, [sp, #80]  
	ldp x29, x30, [sp, #96]  
	add sp, sp, #128
	ret
