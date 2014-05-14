import sys
from file_util import deleteFile
from microbench import microbench

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

if __name__ == "__main__":
    filename = "pathological.sml"
    depth = int(sys.argv[1])

    def cleanup():
        deleteFile(filename)
        deleteFile("pathological.x86-linux")

    microbench("pathological.sml",
               "microbench.smlnj",
               depth,
               cleanup,
               buildPathological,
               ["ml-build", "pathological.cm", "P.main"])
