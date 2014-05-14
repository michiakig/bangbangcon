import os.path
from subprocess import call

# delete a file if it exists
def deleteFile(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def writeToFile(filename, s):
    with open(filename, 'a') as f:
        f.write(s)
        f.write('\n')
