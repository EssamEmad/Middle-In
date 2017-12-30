import argparse
from binary_io import BinaryWriter


class Decompress:
    @staticmethod
    def decompress(codes, input):
        output = ""
        currentCharIndex = 0
        for i in range(len(input)):
            if input[currentCharIndex : i] in codes:
                output += codes[input[currentCharIndex: i]]
                currentCharIndex = i
        return output

    @staticmethod
    def print_decompressed_binary(file, data):
        bw = BinaryWriter(file)
        for digit in data:
            bw.append(digit != '0')
        bw.write()
        bw.close()


if __name__ == '__main__':

    # Program Arguments setup
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="File Name to be compressed", required=True)
    parser.add_argument('-o', '--output', help="Compressed Filename (Default: same as the file name)")
    parser.add_argument('-b', '--binary', action="store_true", help="Is Binary File?")

    args = parser.parse_args()

    file_name = args.file
    output_file_name = args.output if args.output else file_name[:-3]
    is_binary = args.binary

    mode = "wb" if is_binary else "w"
    with open(file_name ,"rb") as f, open(output_file_name, mode) as output_file:
        compressed = f.read()
        header_length_bits = 12 # 12 bits for the number of entries in the header
        codes_bits_length = 4 # 4 bits for the length of the huffman code in each entry
        character_bits = 8 # 8 bits for the ascii representation of the character
        with open("test", "wb") as out:
            out.write(compressed)
        codes = {}
        binary = ""
        for i in range(len(compressed)):
            binary += "{0:08b}".format(compressed[i])
        headerLength = int(binary[0:header_length_bits],2)
        startIndex = header_length_bits
        for i in range(headerLength):
            numberbits = int(binary[startIndex: startIndex + codes_bits_length],2)
            charStart = startIndex + codes_bits_length
            if is_binary:
                char = binary[charStart: charStart + character_bits]
            else:
                char = chr(int(binary[charStart: charStart + character_bits],2))
            codes[binary[charStart + character_bits : charStart + character_bits + numberbits]] = char
            startIndex = startIndex + codes_bits_length+ character_bits +numberbits
        if is_binary:
            Decompress.print_decompressed_binary(output_file,
                                                 Decompress.decompress(codes, binary[startIndex:]))
        else:
            output_file.write(Decompress.decompress(codes, binary[startIndex:]))
