// example of the writeKernel for the vector store ST1 instruction
// 3 stride unrolls, 11 portion unrolls

	.text 
	.global microKernel // ARM 

microKernel:  // arr_length=23529396 | in bytes=94117584

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

// loop bound=178253
	movz x2, #47181
	movk x2, #2, LSL #16
	movk x2, #0, LSL #32
	movk x2, #0, LSL #48

// stride 1 | array_id: 0 | bytes offset: 0 
	movz x3, #0
	movk x3, #0, LSL #16
	movk x3, #0, LSL #32
	movk x3, #0, LSL #48
	add x3, x3, x0

// stride 2 | array_id: 7843132 | bytes offset: 31372528 
	movz x4, #46320
	movk x4, #478, LSL #16
	movk x4, #0, LSL #32
	movk x4, #0, LSL #48
	add x4, x4, x0

// stride 3 | array_id: 15686264 | bytes offset: 62745056 
	movz x5, #27104
	movk x5, #957, LSL #16
	movk x5, #0, LSL #32
	movk x5, #0, LSL #48
	add x5, x5, x0

.Loop:
	scvtf s0, x1
	fmov w30, s0
	dup v0.4s, w30 // v0.4s (st1) == q0 (str)

	// stride 1
	st1 { v0.4S }, [x3], #16 //array id: 0 bytes=0
	st1 { v0.4S }, [x3], #16 //array id: 4 bytes=16
	st1 { v0.4S }, [x3], #16 //array id: 8 bytes=32
	st1 { v0.4S }, [x3], #16 //array id: 12 bytes=48
	st1 { v0.4S }, [x3], #16 //array id: 16 bytes=64
	st1 { v0.4S }, [x3], #16 //array id: 20 bytes=80
	st1 { v0.4S }, [x3], #16 //array id: 24 bytes=96
	st1 { v0.4S }, [x3], #16 //array id: 28 bytes=112
	st1 { v0.4S }, [x3], #16 //array id: 32 bytes=128
	st1 { v0.4S }, [x3], #16 //array id: 36 bytes=144
	st1 { v0.4S }, [x3], #16 //array id: 40 bytes=160

	// stride 2
	st1 { v0.4S }, [x4], #16 //array id: 7843132 bytes=31372528
	st1 { v0.4S }, [x4], #16 //array id: 7843136 bytes=31372544
	st1 { v0.4S }, [x4], #16 //array id: 7843140 bytes=31372560
	st1 { v0.4S }, [x4], #16 //array id: 7843144 bytes=31372576
	st1 { v0.4S }, [x4], #16 //array id: 7843148 bytes=31372592
	st1 { v0.4S }, [x4], #16 //array id: 7843152 bytes=31372608
	st1 { v0.4S }, [x4], #16 //array id: 7843156 bytes=31372624
	st1 { v0.4S }, [x4], #16 //array id: 7843160 bytes=31372640
	st1 { v0.4S }, [x4], #16 //array id: 7843164 bytes=31372656
	st1 { v0.4S }, [x4], #16 //array id: 7843168 bytes=31372672
	st1 { v0.4S }, [x4], #16 //array id: 7843172 bytes=31372688

	// stride 3
	st1 { v0.4S }, [x5], #16 //array id: 15686264 bytes=62745056
	st1 { v0.4S }, [x5], #16 //array id: 15686268 bytes=62745072
	st1 { v0.4S }, [x5], #16 //array id: 15686272 bytes=62745088
	st1 { v0.4S }, [x5], #16 //array id: 15686276 bytes=62745104
	st1 { v0.4S }, [x5], #16 //array id: 15686280 bytes=62745120
	st1 { v0.4S }, [x5], #16 //array id: 15686284 bytes=62745136
	st1 { v0.4S }, [x5], #16 //array id: 15686288 bytes=62745152
	st1 { v0.4S }, [x5], #16 //array id: 15686292 bytes=62745168
	st1 { v0.4S }, [x5], #16 //array id: 15686296 bytes=62745184
	st1 { v0.4S }, [x5], #16 //array id: 15686300 bytes=62745200
	st1 { v0.4S }, [x5], #16 //array id: 15686304 bytes=62745216

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
