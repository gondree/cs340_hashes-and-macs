"""
This Python script generates random messages, hashes them with SHA256 and 
then truncates the hash to the last byte. These hashes are then saved. 
With each truncated hash it looks to see if it has been seen before. 
When it finds a match it stops and displays how many tries it took to find 
a match.
"""
import sys
import hashlib

if __name__ == '__main__':
    if len(sys.argv) != 2 :
        print("Usage:", sys.argv[0], "numbytes",
          "\nWhere 'numbytes' is a number from 1-to-64 (inclusive)",
          "representing whether the hash needs",
          "to match on one hex digit or 64 digits (256-bits).")
        exit(1)

    bytes = int(sys.argv[1])
    assert(1<= bytes <= 64)

    # initialize
    count = 0
    fd = open("/dev/urandom", 'rb',  buffering=0)
    hashtable = {}
    
    done = False
    while not done:
        msg = fd.read(4)
    
        digest = hashlib.sha256(msg).hexdigest()
        digest = digest[-bytes:]
        print("message", count, "hashes to", digest)
    
        if digest in hashtable:
            print("found after", count, "tries:")
            output = " ".join(hex(n) for n in msg) + " = " 
            output = output + " ".join(hex(n) for n in hashtable[digest]) 
            print(output)     
            done = True
        else:
            hashtable[digest] = msg
            count += 1
    fd.close()
