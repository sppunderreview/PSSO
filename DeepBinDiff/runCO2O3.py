# python src/deepbindiff.py --input1 experiment_data/coreutils/binaries/coreutils-5.93-O0/chroot --input2 experiment_data/coreutils/binaries/coreutils-5.93-O1/chroot --outputDir output/ > outtest.txt

from os import system
from random import shuffle

path1 = "coreutils-5.93-O2"
path2 = "coreutils-5.93-O3"
files = ["unlink","basename","printenv","hostname","mkfifo","tee","sync","echo","chroot","whoami","cp","logname","tty","false","yes","hostid","link","uname","rmdir"]

files1 = ["experiment_data/coreutils/binaries/"+path1+"/"+f for f in files]
files2 = ["experiment_data/coreutils/binaries/"+path2+"/"+f for f in files]

shuffle(files1)
shuffle(files2)

for a in files1:
	for b in files2:
		print(a)
		print(b)
		command = "python src/deepbindiff.py --input1 "+a+" --input2 "+a+" --outputDir output/"
		system(command)
