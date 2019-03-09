# Gameboy-Serial-Link-Debugger
A Game Boy ROM to help debug link cable connections in which the Game Boy is the slave device


When the ROM boots up the initial screen will look something like this:

![](http://puu.sh/CXeZy/86d12b8a44.png)

There are 0's everywhere because the initial state of the Game Boy's VRAM is filled with 0's. 
It's normal to have a few random bytes in the middle (like the ones seen in the image)

non-blank ASCII bytes (or more specifically, ASCIIs 33 - 126) are displayed as ASCII characters 
whereas bytes that are blank (or outside of ASCII range) are displayed as 2 digit hexidecimal numbers.
A line is also included under each hex number to increase readability.
