# Generate files with random data of different sizes
# Usage: python generator.py <size> <file_name>
# Example: python generator.py 1000 test.txt

import sys
import random
import string

def generate_file(size, file_name):
    with open(file_name, 'w') as f:
        for i in range(size):
            f.write(random.choice(string.ascii_letters))
        f.close()

if __name__ == '__main__':
    size = int(sys.argv[1]) * 1000000
    file_name = sys.argv[2]
    generate_file(size, file_name)