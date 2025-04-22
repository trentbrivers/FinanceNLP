with open("my_file.txt", "w") as file:
    file.write("1"*1000)
    file.write("This is a new line.\n")
    file.write("*"*500)
    file.write("another line\n")
    file.write("happy"*200)
    file.write("another new line\n")