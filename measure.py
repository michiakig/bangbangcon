from subprocess import call

# run command under time, printing label before time output
def measure(label, filename, command):
    with open(filename, 'a') as f:
        f.write(label + ' ')

    command = [
        "/usr/bin/time",
        "-o", filename, "-a",
        "-f", "%e %U %S"
    ] + command

    call(command)
