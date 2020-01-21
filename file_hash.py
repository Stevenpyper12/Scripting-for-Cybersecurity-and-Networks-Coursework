#Script: file_hash.py
#Desc:   Generate file hash signature - start code
#Author Steven Pyper(40319882)
#Modified: 28/11/18
#
import sys
import os
import hashlib

def get_hash(filename):
    """returns a hex hash signature of the file passed in as arg"""
    try:
        with open(filename,'rb') as f:
            file_content = f.read()
            #take the content from the file and turn it into a md5 hash (with hexdigest)
            file_hashsig = hashlib.md5(file_content).hexdigest()
        return file_hashsig
    except Exception as err:
        print(f'[-] {err}')
        sys.exit()

def main():
    # Test case
    sys.argv.append(r'c:\temp\a_file.txt')
    # Check args
    if len(sys.argv) != 2:
        print('[-] usage: file_hash filename')
        sys.exit(1)

    filename = sys.argv[1]
    print(get_hash(filename))


if __name__ == '__main__':
    main()
