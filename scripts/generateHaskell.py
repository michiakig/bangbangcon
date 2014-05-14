import sys
from file_util import deleteFile
from microbench import microbench

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

if __name__ == "__main__":
    filename = "pathological.hs"
    depth = int(sys.argv[1])

    def cleanup():
        deleteFile(filename)
        deleteFile("pathological.hi")
        deleteFile("pathological.o")
        deleteFile("pathological")

    microbench("pathological.hs",
               "microbench.ghc",
               depth,
               cleanup,
               buildPathological,
               ["ghc", "pathological.hs"])
