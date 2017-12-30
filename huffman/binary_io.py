"""
Module to handle writing/reading binary to/from a binary file (python, why do this to me?)
"""


class BinaryWriter:
    """
    Class to handle writing binary
    """
    def __init__(self, f):
        """
        :param f: binary output file
        :param buf_size: size of the buffer in bits (make it a multiple of 8)
        """
        self.output_file = f
        self.buf_size = 8
        self.bit_count = 0
        self.bin_buf = 0
        self.bytearray = bytearray()

    def append(self, bit):
        """
        append data to the buffer and write if the data reached
        buffer size
        :return:
        """
        if bit:
            bit = 1
        else:
            bit = 0
        self.bin_buf <<= 1
        self.bin_buf |= bit
        self.bit_count += 1
        if self.bit_count == self.buf_size:
            self.bytearray.append(self.bin_buf)
            self.bit_count = 0
            self.bin_buf = 0



    def write(self):
        """
        Dumps the stored byte array.
        If there is anything left (in buffer) that wasn't added to the byte array
        It will be left shifted with the amount of bits left to finish a byte.
        Extra zeros in the end won't matter in decompressing
        :return: The number of left shifted bits in the last byte
        """
        if self.bit_count  > 0:
            self.bin_buf = self.bin_buf << (8 - self.bit_count)
            self.bytearray.append(self.bin_buf)
        self.output_file.write(self.bytearray)
        returnValue = 8 - self.bit_count
        self.bit_count = 0
        self.bin_buf = 0
        return returnValue

    def close(self):
        self.output_file.close()
