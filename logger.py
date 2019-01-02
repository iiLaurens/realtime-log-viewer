from time import sleep

with open("file.log", "w+", buffering=1) as myfile:
    i = 0
    while True:
        myfile.write(f"{i}\n")
        i = i + 1
        sleep(2)