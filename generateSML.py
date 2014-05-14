import sys
from subprocess import call
from measure import measure
from file_util import deleteFile, writeToFile

def x(i):
    return "x" + str(i)

# haha this code is kind of terrible
def buildPathological(depth):
    ret = """structure P = struct
fun main _ = 0
val wat = fn _ =>
   let val x0 = (fn y => fn z => z y y) in
"""

    # print the top part of the nesting 
    d1 = 1
    d0 = d1 - 1
    while (d1 <= depth):
        ret = ret + ('   ' * (d1 + 1))
        ret = ret + 'let val ' + x(d1) + ' = (fn y => ' + x(d0) + '(' + x(d0) + '(' + x(d0) + '(y)))) in\n'
        d1 = d1 + 1
        d0 = d1 - 1

    # print the inner let's body
    ret = ret + ('   ' * (depth + 2)) + x(depth) + '\n'

    # print the bottom part of the nesting
    d = depth
    while (d > 0):
        ret = ret + ('   ' * (d + 1))
        ret = ret + 'end\n'
        d = d - 1

    ret = ret + """   end
end"""

    return ret

def main():
    filename="pathological.sml"
    depth=int(sys.argv[1])

    deleteFile("microbench.smlnj")

    d=1
    while (d <= depth):
        # clean up after previous loop iteration
        deleteFile(filename)
        deleteFile("pathological.x86-linux")

        # build up pathological case
        src = buildPathological(d)
        print(src)
        writeToFile(filename, src)

        # time compilation of 'pathological.cm' via SML/NJ
        # write output of time to file with depth
        measure(str(depth), "microbench.smlnj",
                ["ml-build", "pathological.cm", "P.main"])

        d = d + 1

if __name__ == "__main__":
    main()
