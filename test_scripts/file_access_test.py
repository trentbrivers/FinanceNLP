fileref = open("my_file.txt", "r")
## other code here that refers to variable fileref
test = fileref.readlines()
for line in test:
	print(line)
fileref.close()