'''
This script takes as input a file name and a number. The script calculates 
a hash for the input file. It then tries to find a new file, such that when 
the new data is hashed, the last input number of hex digits match the 
last digits of the original match. The larger the input number, the longer 
it will take. When (and if) it finds a match, it will display the number 
of tries it took as well as the data that matches.
'''
import os, sys
import hashlib


def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


if __name__ == '__main__':
    if len(sys.argv) != 3 :
        print("Usage:", sys.argv[0], "filename numbytes",
          "\nWhere 'numbytes' is a number from 1-to-64 (inclusive)",
          "representing whether the hash needs",
          "to match on one hex digit or 64 digits (256-bits).")
        exit(1)

    file, bytes = sys.argv[1], int(sys.argv[2])

    if not os.access(file, os.R_OK):
        print("Error: '" + file + "' either does not exist or is not readable.")
        exit(1)

    if not (1 <= bytes <= 64):
        print("Error: '" + bytes + "' should be between 1 and 64.")
        exit(1)

    digest = sha256sum(file)
    print(digest, "\t", file)
    tdigest = digest[-bytes:]
    digest = None
    
    count = 0
    fd = open("/dev/urandom", 'rb', buffering=0)
    while digest != tdigest:
        msg = fd.read(256)
        digest = hashlib.sha256(msg).hexdigest()[-bytes:]
        count += 1
        if bytes < 3:
            print(digest)
    fd.close()

    if count > 1:
        print(count, "hashes were performed before a match was found.")
    else:
        print(count, "hash was performed and we immediately found a match.")

