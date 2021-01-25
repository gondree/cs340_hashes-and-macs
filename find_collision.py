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
    # initialize
    count = 0
    fd = open("/dev/urandom", 'rb',  buffering=0)
    hashtable = {}
    
    done = False
    while not done:
        msg = fd.read(4)
    
        digest = hashlib.sha256(msg).hexdigest()
        digest = digest[62:]
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
