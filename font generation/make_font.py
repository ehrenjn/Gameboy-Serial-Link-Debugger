def read_char_txt():
        with open("3x5_chars.txt") as char_file:
                chars = char_file.read().split('\n\n')
                chars = [c.split('\n') for c in chars]
        return chars

def chars_to_bin(chars):
	bin_chars = []		
	for char in chars:
		bin_lines = []
		for line in char:
			bin_lines.append(int(line, 2))
		bin_chars.append(bin_lines)
	return bin_chars

def bin_chars_to_byte_str(bin_chars):
        bin_str = bytes()
        for i in range(0x100):
                hi_char = bin_chars[i >> 4]
                lo_char = bin_chars[i % 0x10]
                combined = []
                for b1, b2 in zip(hi_char, lo_char):
                        bin_line = (b1 << 5) + (b2 << 1)
                        bin_str += bytes([bin_line, bin_line]) #double up binline because of 2 bit color depth
                extra_line = 0b01111100 #extra line below each char to more easily tell each nybble pair apart
                end_lines = [0, 0, extra_line, extra_line, 0, 0] #so we have a total of 16 lines for the char
                bin_str += bytes(end_lines)
        return bin_str

def add_in_ascii(bin_char_str):
        with open('ascii_font.chr', 'rb') as ascii_font:
                ascii_bin_char = ascii_font.read()
        good_ascii_start = 32 * 16 #chars between char 32 (space) and 127 (DEL) are visible in ascii
        good_ascii_end = 127 * 16 #*16 since each char is represented by 16 bytes
        good_ascii_chars = ascii_bin_char[good_ascii_start: good_ascii_end]
        return bin_char_str[:good_ascii_start] + good_ascii_chars + bin_char_str[good_ascii_end:]
        


chars = read_char_txt()
bin_chars = chars_to_bin(chars)
bin_char_str = bin_chars_to_byte_str(bin_chars)
bin_char_str = add_in_ascii(bin_char_str)

print(len(bin_char_str))

with open("debug_font.chr", "wb") as font_file:
	font_file.write(bin_char_str)
