# Gameboy-Serial-Link-Debugger
A Game Boy ROM to help debug link cable connections in which the Game Boy is the slave device


When the ROM boots up the initial screen will look something like this:

![](https://i.imgur.com/YSRo812.jpg)

There are 0's everywhere because the initial state of the Game Boy's VRAM is filled with null bytes. 
It's normal to have a few random bytes in the middle (like the ones seen in the image).

When a byte is recieved it will be printed, starting in the top left corner of the screen.
When the byte printout reaches the bottom right of the screen it will wrap back up to the top left.

visable ASCII bytes (or more specifically, ASCII chars 32 - 126 inclusive) are displayed as ASCII characters,
whereas bytes that are blank (or outside of ASCII range) are displayed as 2 digit hexidecimal numbers.
A line is also included under each hex number to increase readability.

Note that a space is the only character that appears completely blank. 

Below is an image of characters that can be printed (in order from 0x00 to 0xFF) look like:

![](https://i.imgur.com/8YLUTUj.jpg)

What they all look like printed on an actual Game Boy:

![](https://i.imgur.com/Qi00Nm5.jpg)
