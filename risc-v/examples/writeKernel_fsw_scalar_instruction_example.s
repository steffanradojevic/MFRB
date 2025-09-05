// example of the writeKernel for the scalar store fsw instruction
// 13 stride unrolls, 5 portion unrolls

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

# loop bound=7773696
	lui x1, 1898
	addi x1, x1, -512

# stride 1 | bytes offset: 0 
	lui x4, 0
	addi x4, x4, 0
	add x4, x4, a0

# stride 2 | bytes offset: 155473920 
	lui x5, 37958
	addi x5, x5, -2048
	add x5, x5, x4

# stride 3 | bytes offset: 310947840 
	lui x6, 75915
	addi x6, x6, 0
	add x6, x6, x4

# stride 4 | bytes offset: 466421760 
	lui x7, 113873
	addi x7, x7, -2048
	add x7, x7, x4

# stride 5 | bytes offset: 621895680 
	lui x8, 151830
	addi x8, x8, 0
	add x8, x8, x4

# stride 6 | bytes offset: 777369600 
	lui x9, 189788
	addi x9, x9, -2048
	add x9, x9, x4

# stride 7 | bytes offset: 932843520 
	lui x10, 227745
	addi x10, x10, 0
	add x10, x10, x4

# stride 8 | bytes offset: 1088317440 
	lui x11, 265703
	addi x11, x11, -2048
	add x11, x11, x4

# stride 9 | bytes offset: 1243791360 
	lui x12, 303660
	addi x12, x12, 0
	add x12, x12, x4

# stride 10 | bytes offset: 1399265280 
	lui x13, 341618
	addi x13, x13, -2048
	add x13, x13, x4

# stride 11 | bytes offset: 1554739200 
	lui x14, 379575
	addi x14, x14, 0
	add x14, x14, x4

# stride 12 | bytes offset: 1710213120 
	lui x15, 417533
	addi x15, x15, -2048
	add x15, x15, x4

# stride 13 | bytes offset: 1865687040 
	lui x16, 455490
	addi x16, x16, 0
	add x16, x16, x4

.Loop:
	fcvt.s.w f0, x3 

	# stride 1
	fsw f0, 0(x4) #array id: 0 bytes=0
	fsw f0, 4(x4) #array id: 1 bytes=4
	fsw f0, 8(x4) #array id: 2 bytes=8
	fsw f0, 12(x4) #array id: 3 bytes=12
	fsw f0, 16(x4) #array id: 4 bytes=16

	# stride 2
	fsw f0, 0(x5) #array id: 38868480 bytes=155473920
	fsw f0, 4(x5) #array id: 38868481 bytes=155473924
	fsw f0, 8(x5) #array id: 38868482 bytes=155473928
	fsw f0, 12(x5) #array id: 38868483 bytes=155473932
	fsw f0, 16(x5) #array id: 38868484 bytes=155473936

	# stride 3
	fsw f0, 0(x6) #array id: 77736960 bytes=310947840
	fsw f0, 4(x6) #array id: 77736961 bytes=310947844
	fsw f0, 8(x6) #array id: 77736962 bytes=310947848
	fsw f0, 12(x6) #array id: 77736963 bytes=310947852
	fsw f0, 16(x6) #array id: 77736964 bytes=310947856

	# stride 4
	fsw f0, 0(x7) #array id: 116605440 bytes=466421760
	fsw f0, 4(x7) #array id: 116605441 bytes=466421764
	fsw f0, 8(x7) #array id: 116605442 bytes=466421768
	fsw f0, 12(x7) #array id: 116605443 bytes=466421772
	fsw f0, 16(x7) #array id: 116605444 bytes=466421776

	# stride 5
	fsw f0, 0(x8) #array id: 155473920 bytes=621895680
	fsw f0, 4(x8) #array id: 155473921 bytes=621895684
	fsw f0, 8(x8) #array id: 155473922 bytes=621895688
	fsw f0, 12(x8) #array id: 155473923 bytes=621895692
	fsw f0, 16(x8) #array id: 155473924 bytes=621895696

	# stride 6
	fsw f0, 0(x9) #array id: 194342400 bytes=777369600
	fsw f0, 4(x9) #array id: 194342401 bytes=777369604
	fsw f0, 8(x9) #array id: 194342402 bytes=777369608
	fsw f0, 12(x9) #array id: 194342403 bytes=777369612
	fsw f0, 16(x9) #array id: 194342404 bytes=777369616

	# stride 7
	fsw f0, 0(x10) #array id: 233210880 bytes=932843520
	fsw f0, 4(x10) #array id: 233210881 bytes=932843524
	fsw f0, 8(x10) #array id: 233210882 bytes=932843528
	fsw f0, 12(x10) #array id: 233210883 bytes=932843532
	fsw f0, 16(x10) #array id: 233210884 bytes=932843536

	# stride 8
	fsw f0, 0(x11) #array id: 272079360 bytes=1088317440
	fsw f0, 4(x11) #array id: 272079361 bytes=1088317444
	fsw f0, 8(x11) #array id: 272079362 bytes=1088317448
	fsw f0, 12(x11) #array id: 272079363 bytes=1088317452
	fsw f0, 16(x11) #array id: 272079364 bytes=1088317456

	# stride 9
	fsw f0, 0(x12) #array id: 310947840 bytes=1243791360
	fsw f0, 4(x12) #array id: 310947841 bytes=1243791364
	fsw f0, 8(x12) #array id: 310947842 bytes=1243791368
	fsw f0, 12(x12) #array id: 310947843 bytes=1243791372
	fsw f0, 16(x12) #array id: 310947844 bytes=1243791376

	# stride 10
	fsw f0, 0(x13) #array id: 349816320 bytes=1399265280
	fsw f0, 4(x13) #array id: 349816321 bytes=1399265284
	fsw f0, 8(x13) #array id: 349816322 bytes=1399265288
	fsw f0, 12(x13) #array id: 349816323 bytes=1399265292
	fsw f0, 16(x13) #array id: 349816324 bytes=1399265296

	# stride 11
	fsw f0, 0(x14) #array id: 388684800 bytes=1554739200
	fsw f0, 4(x14) #array id: 388684801 bytes=1554739204
	fsw f0, 8(x14) #array id: 388684802 bytes=1554739208
	fsw f0, 12(x14) #array id: 388684803 bytes=1554739212
	fsw f0, 16(x14) #array id: 388684804 bytes=1554739216

	# stride 12
	fsw f0, 0(x15) #array id: 427553280 bytes=1710213120
	fsw f0, 4(x15) #array id: 427553281 bytes=1710213124
	fsw f0, 8(x15) #array id: 427553282 bytes=1710213128
	fsw f0, 12(x15) #array id: 427553283 bytes=1710213132
	fsw f0, 16(x15) #array id: 427553284 bytes=1710213136

	# stride 13
	fsw f0, 0(x16) #array id: 466421760 bytes=1865687040
	fsw f0, 4(x16) #array id: 466421761 bytes=1865687044
	fsw f0, 8(x16) #array id: 466421762 bytes=1865687048
	fsw f0, 12(x16) #array id: 466421763 bytes=1865687052
	fsw f0, 16(x16) #array id: 466421764 bytes=1865687056

# update stride address registers
	addi x4, x4, 20
	addi x5, x5, 20
	addi x6, x6, 20
	addi x7, x7, 20
	addi x8, x8, 20
	addi x9, x9, 20
	addi x10, x10, 20
	addi x11, x11, 20
	addi x12, x12, 20
	addi x13, x13, 20
	addi x14, x14, 20
	addi x15, x15, 20
	addi x16, x16, 20

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

