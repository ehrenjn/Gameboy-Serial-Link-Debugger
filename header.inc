section "header", ROM0[$100] ;the name of this section doesn't matter, what's important is that it's 256 bytes into rom0
;ROM0 tells the assembler to put the following code in the ROM0 section of the cart. ROM0 is the non-banked rom of the cart.

entry_point: ;first 4 bytes of header are code. that's enough space to execute 2 instructions. BUT BE CAREFUL BECAUSE SOME INSTRUCTIONS ARE LONGER THAN 2 BYTES
    nop ;we've got nothing else to do so lets nop
    jp main

;now we have the actual header. we can just fill it with 0's because rgbfix.exe will fix it all for us
db 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0