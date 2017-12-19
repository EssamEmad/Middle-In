"""
Module to handle writing/reading binary to/from a binary file (python, why do this to me?)
"""


class BinaryWriter:
    """
    Class to handle writing binary
    """
    def __init__(self, f, buf_size):
        """
        :param f: binary output file
        :param buf_size: size of the buffer in bits (make it a multiple of 8)
        """
        self.output_file = f
        self.buf_size = buf_size
        self.bit_count = 0
        self.bin_buf = 0

    def write(self, bit):
        """
        append data to the buffer and write if the data reached
        buffer size
        :return:
        """
        self.bin_buf <<= 1
        self.bin_buf |= bit
        self.bit_count += 1
        if self.bit_count is self.buf_size:
            self._write()

    def _write(self):
        self.output_file.write(bytes([self.bin_buf]))
        self.bit_count, self.bin_buf = 0, 0

    def close(self):
        if self.bit_count is not 0:
            while self.bit_count % 8 != 0:
                # TODO: this is terrible for performance but the deadline is come
                self.bin_buf += '0'
            self._write()
        self.output_file.close()
