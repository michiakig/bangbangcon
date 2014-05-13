import os.path
import sys
from subprocess import call

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
        ret = ret + 'let val x' + str(d1) + ' = (fn y => x' + str(d0) + '(x' + str(d0) + '(y))) in\n'
        d1 = d1 + 1
        d0 = d1 - 1

    # print the inner let's body
    ret = ret + ('   ' * (depth + 2)) + 'x' + str(depth) + '\n'

    # print the bottom part of the nesting
    d = depth
    while (d > 0):
        ret = ret + ('   ' * (d + 1))
        ret = ret + 'end\n'
        d = d - 1

    ret = ret + """   end
end"""

    return ret

# delete a file if it exists
def deleteFile(filename):
    if os.path.isfile(filename):
        call(["rm", filename])

def writeToFile(filename, s):
    with open(filename, 'a') as f:
        f.write(s)
        f.write('\n')

# time compilation of 'pathological.cm' via SML/NJ
# write output of time to file with depth
def timeSmlNj(depth):
    filename = 'microbenchmarks.smlnj'
    with open(filename, 'a') as f:
        f.write('(' + str(depth) + ') ')
    call(["/usr/bin/time", "-o", filename, "-a", "-f", "%e %U %S", "ml-build", "pathological.cm", "P.main"])

def main():
    filename="pathological.sml"
    depth=int(sys.argv[1])

    d=1
    while (d <= depth):
        deleteFile(filename)
        writeToFile(filename, buildPathological(d))
        timeSmlNj(d)
        d = d + 1

if __name__ == "__main__":
    main()
