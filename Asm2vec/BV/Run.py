from os import system

epochs = 50

pathToBench = "../BigVG5000/"
toDo = [("V0","V1"),("V0","V2"),("V0","V3"),("V1","V2"),("V1","V3"),("V2","V3")]

command = ""
for V0, V1 in toDo:
    nameE = "B" + V0 + V1
    command += "java -Xmx7g -jar asm2veck.jar "+nameE+" 0 "+pathToBench+" "+str(epochs)+" "+V0+" "+V1+" & "

command += "wait"
system(command)
