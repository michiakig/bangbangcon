from file_util import deleteFile, writeToFile
from measure import measure

def microbench(srcFile, benchFile, depth, cleanupFn, pathoFn, buildCmd):
    deleteFile(benchFile)

    d = 1
    while (d <= depth):
        # clean up after previous loop iteration
        cleanupFn()

        # build up pathological case
        src = pathoFn(d)
        print(src)
        writeToFile(srcFile, src)

        # time compilation
        measure(str(d), benchFile, buildCmd)

        d = d + 1
