from glob import glob

files = glob("C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\Jomesa Data\\ZF Inner\\*.txt")
file = open("C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\Jomesa Data\\ZF Inner\\MASTER.txt",'w')

for f in files:

    x = open(f, 'r')
    try:
        data = x.read().splitlines()[0]
    except IndexError:
        pass
    x.close()

    try:
        file.write(data+"\n")
    except NameError:
        file.write("\n")

file.close()
