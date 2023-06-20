from glob import glob

files = glob("C:\\Users\\vrerecich\\Desktop\\Jomesa 4 Testing\\Jomesa Data\\ZF\\*.txt")
file = open("C:\\Users\\vrerecich\\Desktop\\Jomesa 4 Testing\\MASTER_ZF.txt",'w')

for f in files:

    x = open(f, 'r')
    data = x.read().splitlines()[0]
    x.close()

    file.write(data+"\n")

file.close()
