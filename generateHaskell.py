import os.path
import sys
from subprocess import call

def x(i):
    return "x" + str(i)

def buildPathological(depth):
    ret = """module Wat (wat) where
main = undefined
wat  = \\_ -> let x0 = (\\x -> \\y -> \\z -> z x y)
"""

    d1 = 1
    d0 = d1 - 1
    while (d1 <= depth):
        ret = ret + "                 " + x(d1) + " = (\y -> " + x(d0) + "(" + x(d0) + "(" + x(d0) + "(y))))\n"
        d1 = d1 + 1
        d0 = d1 - 1

    ret = ret + "             in " + x(depth)

    return ret

# delete a file if it exists
def deleteFile(filename):
    if os.path.isfile(filename):
        call(["rm", filename])

def writeToFile(filename, s):
    with open(filename, 'a') as f:
        f.write(s)
        f.write('\n')

# time compilation of 'pathological.hs' via GHC
def timeGhc():
    call(["/usr/bin/time", "-f", "%e %U %S", "ghc", "pathological.hs"])

def main():
    filename="pathological.hs"
    depth=int(sys.argv[1])

    d=1
    while (d <= depth):
        deleteFile(filename)
        src = buildPathological(d)
        print(src)
        d = d + 1
        writeToFile(filename, src)
        timeGhc()

if __name__ == "__main__":
    main()
