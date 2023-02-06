from os import system

epochs = 50
pathToBench = "../CoreutilsVG5000/"
toDo = [("5.","6."),("5.","7."),("5.","8."),("6.","7."),("6.","8."),("7.","8.")]

command = ""

for V0, V1 in toDo:
    nameE = "C" + V0 + V1
    command += "java -Xmx7g -jar asm2veck.jar "+nameE+" 0 "+pathToBench+" "+str(epochs)+" "+V0+" "+V1+" & "

command += "wait"
system(command)
