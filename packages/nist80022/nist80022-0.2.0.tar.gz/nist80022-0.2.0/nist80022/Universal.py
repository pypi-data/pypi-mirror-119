import math
from typing import List, Tuple

import numpy as np

from scipy.special import erfc


class Universal:

    @staticmethod
    def statistical_test(binary_data:str, verbose=False) -> List[Tuple[str, float, bool]]:
        """
        Note that this description is taken from the NIST documentation [1]
        [1] http://csrc.nist.gov/publications/nistpubs/800-22-rev1a/SP800-22rev1a.pdf
        The focus of this test is the number of bits between matching patterns (a measure that is related to the
        length of a compressed sequence). The purpose of the test is to detect whether or not the sequence can be
        significantly compressed without loss of information. A significantly compressible sequence is considered
        to be non-random. **This test is always skipped because the requirements on the lengths of the binary
        strings are too high i.e. there have not been enough trading days to meet the requirements.

        :param      binary_data:    a binary string
        :param      verbose             True to display the debug messgae, False to turn off debug message
        :return:    [(test_name, p_value, bool)] A tuple containing the test_name, p_value and
            pass/fail result of the test.
        """
        length_of_binary_data = len(binary_data)
        pattern_size = 5
        if length_of_binary_data >= 387840:
            pattern_size = 6
        elif length_of_binary_data >= 904960:
            pattern_size = 7
        elif length_of_binary_data >= 2068480:
            pattern_size = 8
        elif length_of_binary_data >= 4654080:
            pattern_size = 9
        elif length_of_binary_data >= 10342400:
            pattern_size = 10
        elif length_of_binary_data >= 22753280:
            pattern_size = 11
        elif length_of_binary_data >= 49643520:
            pattern_size = 12
        elif length_of_binary_data >= 107560960:
            pattern_size = 13
        elif length_of_binary_data >= 231669760:
            pattern_size = 14
        elif length_of_binary_data >= 496435200:
            pattern_size = 15
        elif length_of_binary_data >= 1059061760:
            pattern_size = 16

        if 5 < pattern_size < 16:
            # Create the biggest binary string of length pattern_size
            ones = ""
            for i in range(pattern_size):
                ones += "1"

            # How long the state list should be
            num_ints = int(ones, 2)
            vobs = np.zeros(num_ints + 1)

            # Keeps track of the blocks, and whether were are initializing or summing
            num_blocks = math.floor(length_of_binary_data / pattern_size)
            # Q = 10 * pow(2, pattern_size)
            init_bits = 10 * pow(2, pattern_size)

            test_bits = num_blocks - init_bits

            # These are the expected values assuming randomness (uniform)
            c = 0.7 - 0.8 / pattern_size + (4 + 32 / pattern_size) * pow(test_bits, -3 / pattern_size) / 15
            variance = [0, 0, 0, 0, 0, 0, 2.954, 3.125, 3.238, 3.311, 3.356, 3.384, 3.401, 3.410, 3.416, 3.419, 3.421]
            expected = [0, 0, 0, 0, 0, 0, 5.2177052, 6.1962507, 7.1836656, 8.1764248, 9.1723243,
                        10.170032, 11.168765, 12.168070, 13.167693, 14.167488, 15.167379]
            sigma = c * math.sqrt(variance[pattern_size] / test_bits)

            cumsum = 0.0
            # Examine each of the K blocks in the test segment and determine the number of blocks since the
            # last occurrence of the same L-bit block (i.e., i – Tj). Replace the value in the table with the
            # location of the current block (i.e., Tj= i). Add the calculated distance between re-occurrences of
            # the same L-bit block to an accumulating log2 sum of all the differences detected in the K blocks
            for i in range(num_blocks):
                block_start = i * pattern_size
                block_end = block_start + pattern_size
                block_data = binary_data[block_start: block_end]
                # Work out what state we are in
                int_rep = int(block_data, 2)

                # Initialize the state list
                if i < init_bits:
                    vobs[int_rep] = i + 1
                else:
                    initial = vobs[int_rep]
                    vobs[int_rep] = i + 1
                    cumsum += math.log(i - initial + 1, 2)

            # Compute the statistic
            phi = float(cumsum / test_bits)
            stat = abs(phi - expected[pattern_size]) / (float(math.sqrt(2)) * sigma)

            # Compute for P-Value
            p_value = erfc(stat)

            if verbose:
                print("Maurer\'s Universal Statistical Test:")
                print("  {:<40}{:>20}".format("Length of input:", length_of_binary_data))
                print("  {:<40}{:>20}".format("Length of each block:", pattern_size))
                print("  {:<40}{:>20}".format("Number of Blocks:", init_bits))
                print("  {:<40}{:>20}".format("Value of phi:", phi))
                print("  {:<40}{:>20}".format("P-Value:", p_value))

            return [("universal_statistic", p_value, (p_value>=0.01))]
        else:
            return [("universal_statistic", -1.0, False)]
