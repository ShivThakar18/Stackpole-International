from glob import glob

files = glob("C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\Jomesa Data\\10R140 Slide\\*.txt")
file = open("C:\\Users\\vrerecich\\Desktop\\Jomesa 5.0\\Jomesa Data\\10R140 Slide\\MASTER.txt",'w')

for f in files:

    x = open(f, 'r')
    data = x.read().splitlines()[0]
    x.close()

    file.write(data+"\n")

file.close()
