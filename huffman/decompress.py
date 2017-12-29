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
                # printf("output: {}".format(output))

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
        # str = "{0:0" + "{}".format(len(compressed) * 8) + "b}"
        codes = {}
        binary = ""
        for i in range(len(compressed)):
            binary += "{0:08b}".format(compressed[i])
        # print("BINARRYYYYY: {}".format(binary))
        headerLength = int(binary[0:12],2)
        # print("Header length: {}".format(headerLength))
        startIndex = 12
        for i in range(headerLength):
            numberbits = int(binary[startIndex: startIndex + 4],2)
            charStart = startIndex + 4
            if is_binary:
                char = binary[charStart: charStart + 8]
            else:
                char = chr(int(binary[charStart: charStart + 8],2))
            codes[binary[charStart + 8 : charStart + 8 + numberbits]] = char
            startIndex = startIndex + 4+8+numberbits
        print("Codes: {}".format(codes))
        # print("output:{}".format(Decompress.decompress(codes, binary[startIndex:])))
        if is_binary:
            Decompress.print_decompressed_binary(output_file,
                                                 Decompress.decompress(codes, binary[startIndex:]))
        else:
            output_file.write(Decompress.decompress(codes, binary[startIndex:]))