class Decompress:
    def decompress(codes,input):
        output = ""
        currentCharIndex = 0
        for i in range(len(input)):
            if input[currentCharIndex : i] in codes:
                output += codes[input[currentCharIndex: i]]
                currentCharIndex = i
                # printf("output: {}".format(output))

        return output

if __name__ == '__main__':

    file_name = 'sample.em'
    with open(file_name ,"rb") as f:
        compressed = f.read()
        # str = "{0:0" + "{}".format(len(compressed) * 8) + "b}"
        codes = {}
        binary = ""
        for i in range(len(compressed)):
            binary += "{0:08b}".format(compressed[i])
        print("BINARRYYYYY: {}".format(binary))
        headerLength = int(binary[0:12],2)
        print("Header length: {}".format(headerLength))
        startIndex = 12
        for i in range(headerLength):
            numberbits = int(binary[startIndex: startIndex + 4],2)
            charStart = startIndex + 4
            char = chr(int(binary[charStart: charStart + 8],2))
            codes[binary[charStart + 8 : charStart + 8 + numberbits]] = char
            startIndex = startIndex + 4+8+numberbits
        print("Codes: {}".format(codes))
        print("output:{}".format(Decompress.decompress(codes, binary[startIndex:])))
