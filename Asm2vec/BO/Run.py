from os import system

epochs = 50

pathToBench = "./BOC/"
toDo = [("O0","O1"),("O0","O2"),("O0","O3"),("O1","O2"),("O1","O3"),("O2","O3")]

command = ""
for O0, O1 in toDo:
    nameE = "B" + O0 + O1
    command += "java -Xmx7g -jar asm2veckC.jar "+nameE+" 0 "+pathToBench+" "+str(epochs)+" "+O0+" "+O1+" & "

command += "wait"
system(command)
