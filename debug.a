;MIGHT WANT TO FIX THAT BUG THAT HAPPENS WHEN YOU SPAM A HUGE AMOUNT OF DATA

include "hardware.inc"
include "Gameboy Serial Link Debugger/header.inc"


section "queue variables", WRAM0
QUEUE: ds 255 ;the largest queue I can handle with one byte
rHEAD: ds 1
rTAIL: ds 1
rSIZE: ds 1 ;amount of data in the queue (the head will keep filling up the queue even if it's full so I need to keep track of the size)

section "screen variables", WRAM0 
rSCREEN_X: ds 1
rCURRENT_LINE_ADDR: ds 2 ;needs to be 2 bytes because I'm gonna store an address

TILEMAP_START equ $9800 ;start address of the tilemap
TILEMAP_END_HIGH equ $9A ;high byte of the address of the end of the visable (unscrolled) tilemap
TILEMAP_END_LOW equ $3F

section "serial interrupt", ROM0[$0058]
    jp serial_interrupt

section "vblank interrupt", ROM0[$0040]
    jp vblank_interrupt


section "main", ROM0[$0150] ;NEED TO PUT THIS IN THE RIGHT SPOT (after header) otherwise it'll try to put it between the interrupts and the header

main:

    di
    call init_display
    call init_serial
    ld a, 0
    ld [rIF], a ;CLEAR INTERRUPT FLAGS!!
    ei
.loop
    halt ;everything's going to happen in vblank and serial interrupts
jr .loop


init_serial:
 
    push af
    push hl
 
    ld a, %10000000 ;external serial clock, normal speed, SET THE BEGIN TRANSFER BIT SO I CAN RECIEVE DATA (begin transfer bit really just means "when the serial clock ticks, latch/send data")
    ld [rSC], a

    ld a, 0
    ld [rHEAD], a
    ld [rTAIL], a
    ld [rSIZE], a ;clear head, tail, and size
 
    ld hl, rIE
    set 3, [hl] ;enable serial interrupt
 
    pop hl
    pop af
ret


init_display: ;many parts of this procedure were copied/pasted/modified from https://eldred.fr/gb-asm-tutorial/hello-world.html

    push af
    push hl
    push bc
    push de

.wait_v_blank 
    ld a, [rLY]
    cp 144 ; Check if the LCD is past VBlank
    jr c, .wait_v_blank

    ld a, 0
    ld [rLCDC], a ;turn lcd off once we hit vblank (don't do this to your hardware too much! but it's fine for now just to load in the huge amount of character data)

    ld hl, $8000 ;load font data into vram
    ld de, FONT_START ;start of font data
    ld bc, FONT_END - FONT_START ;amount of font data (could have gone without this but then it would be a little more annoying to tell when count was 0)
.copy_font
    ld a, [de] ; nab a byte of the font
    ld [hli], a ; put it in vram, incrementing hl
    inc de ; Move to next byte
    dec bc ; Decrement remaining byte count
    ld a, b ; Check if count is 0
    or c
    jr nz, .copy_font

;init other lcd registers and turn lcd back on
    ld a, %11100100
    ld [rBGP], a ;set pallette 

    ld a, 0
    ld [rSCY], a
    ld [rSCX], a ;scroll window x and y to 0

    ld hl, rIE
    set 0, [hl] ;enable vblank interrupt

    ld a, %10010001
    ld [rLCDC], a ;turn lcd back on, put it in the proper mode

;init SCREEN_X and CURRENT_LINE_ADDR
    ld a, 0
    ld [rSCREEN_X], a ;init SCREEN_X as 0
    ld hl, rCURRENT_LINE_ADDR
    ld [hl], (TILEMAP_START >> 8) ;init first byte of CURRENT_LINE_ADDR (can't do hli with a const :( )
    inc hl
    ld [hl], (TILEMAP_START & $00FF) ;init 2nd byte of CURRENT_LINE_ADDR

    pop de
    pop bc
    pop hl
    pop af
ret


serial_interrupt:

    push af
    push bc
    push de
    push hl
 
    ld a, [rSB] ;get the recieved serial data
    ld d, a ;save data for later
    ld a, [rHEAD]
    ld c, a ;save head for later
    ld hl, QUEUE
    ld b, 0 ;so I can add bc to hl and get the address to put the data into
    add hl, bc ;set hl to QUEUE[HEAD] (the location we want to put the data)
    ld [hl], d ;load data into the queue

    inc a ;increment the head
    cp 255 ;check if head is at the end of the queue
    jr nz, .load_head 
    ld a, 0 ;if head is at the end of the queue, reset it to 0
.load_head
    ld [rHEAD], a ;save the head

    ld hl, rSIZE
    ld a, [hl] ;I could just do ld a [rSIZE] but I want to use hl agian later so
    ld b, 255
    cp b
    jr z, .return
    inc [hl] ;increment the size of the queue if it's not 255

.return
    ld hl, rSC
    set 7, [hl] ;BEGIN SERIAL TRANSFER AGIAN so that when the external clock ticks I recieve more data

    pop hl
    pop de
    pop bc
    pop af
reti


;@return CURRENT_LINE_ADDR in hl
get_current_line_addr:

    push af

    ld hl, rCURRENT_LINE_ADDR
    ld a, [hl]
    inc hl ;go to 2nd byte of rCURRENT_LINE_ADDRESS
    ld l, [hl] ;set low byte of line address
    ld h, a ;set high byte of line address

    pop af
ret


vblank_interrupt:
 
    ei ;SO THAT YOU CAN GET SERIALS IN THE MIDDLE OF THIS
    push af
    push bc
    push de
    push hl

    ld a, [rSCREEN_X] ;get screen_x for later use
    ld c, a ;store in C so I can later set B to 0 and add hl, bc

.draw_loop
    ld a, [rSIZE] ;check how much data is in the queue
    cp 0
    jr z, .return ;stop looping if there's no data left to draw

;get the current byte of data from the queue
    ld hl, QUEUE ;start getting the tail address
    ld a, [rTAIL]
    ld d, 0 ;set d to 0 so I can add hl, e
    ld e, a
    add hl, de ;hl = QUEUE[rTAIL] (theres no add de, hl opcode sadly)
    ld d, [hl] ;get current byte of data

;get the current line address
    call get_current_line_addr ;hl = CURRENT_LINE_ADDRESS

;put the current byte of data in the tilemap
    ld b, 0 
    add hl, bc ;hl = TILEMAP[CURRENT_LINE_ADDRESS + SCREEN_X]
    ld [hl], d ;finally, load the current data byte into the tilemap

;make sure we're still in vblank
    ld a, [rSTAT]
    ld b, %00000011 ;bit mask to get bottom 2 bits out of a
    and a, b
    cp 1 ;check if bottom 2 bits of lcdc STAT register are 1
    jr nz, .return ;if it's not currently vblank then don't update anything (since this means previous instructions may have been done outside of vblank)

;update queue size
    ld hl, rSIZE ;decrease queue size
    dec [hl] ;I DONT THINK THIS IS UNSAFE BUT YOU MIGHT WANNA MAKE SURE (can an interrupt occur in the middle of a multi cycle instruction?), ALSO KEEP IN MIND THAT THIS IS THE ONLY FUNC THAT DECREASES IT SO IT CAN'T GO BELOW 0 BY ACCIDENT

;update the tail
    ld a, [rTAIL] ;a = TAIL
    inc a
    cp 255 ;check if tail has reached end of queue
    jr nz, .save_tail
    ld a, 0 ;set tail to beginning of the queue if it's past the end
.save_tail
    ld [rTAIL], a

;start update of SCREEN_X  
    inc c ;increase SCREEN_X 
    ld a, c
    cp 20 ;check if SCREEN_X is larger than 20
    jr c, .save_screen_x ;if SCREEN_X - 20 < 0 we don't need to update the line address. otherwise, we do

    ;if SCREEN_X is off the screen
    ld c, 0 ;set SCREEN_X to 0 since we're going to the beginning of the next line on the screen
    call get_current_line_addr ;hl = CURRENT_LINE_ADDR
    ld de, 32 
    add hl, de ;CURRENT_LINE_ADDR += 32 (go to the next line on the screen)

;check if the current_line_addr needs to be reset    
    ld a, h
    cp TILEMAP_END_HIGH ;check if high byte of next line address is outside of the tilemap
    jr c, .save_screen_pos ;if we're still in the tilemap then we can save the screen position
    jr nz, .reset_current_line_addr ;if we're past the end of the tilemap, we need to reset the line address back to the start of the tilemap
    
    ;then check high byte of current_line_addr   
    ld a, l ;in the case that high byte of CURRENT_LINE_ADDRESS equals TILEMAP_END_HIGH
    cp TILEMAP_END_LOW ;we must compare the low byte of CURRENT_LINE_ADDRESS to TILEMAP_END_LOW
    jr c, .save_screen_pos ;the current CURRENT_LINE_ADDR is fine if it's still less than the TILEMAP_END

.reset_current_line_addr
    ld hl, TILEMAP_START ;prepare to do CURRENT_LINE_ADDR = TILEMAP_START

.save_screen_pos ;saves HL as CURRENT_LINE_ADDR and then saves C as SCREEN_X
    ld de, rCURRENT_LINE_ADDR
    ld a, h ;prepare to update high byte
    ld [de], a ;update high byte of CURRENT_LINE_ADDR to high byte of TILEMAP_START, increment hl to get to low byte
    inc de ;move to the low byte of rCURRENT_LINE_ADDR
    ld a, l ;prepare to update low byte
    ld [de], a ;update low byte of CURRENT_LINE_ADDR to low byte of TILEMAP_START

.save_screen_x
    ld hl, rSCREEN_X
    ld [hl], c ;save the current screen x position
    jr .draw_loop ;finally, restart the draw loop

.return
    pop af
    pop bc
    pop de
    pop hl
ret ;NO RETI BECAUSE NESTED INTERRUPTS


FONT_START
    incbin "Gameboy Serial Link Debugger/font.chr"
FONT_END