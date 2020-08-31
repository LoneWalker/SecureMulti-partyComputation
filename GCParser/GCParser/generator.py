import math

file = open("input.txt", 'r')
circuit = open("multiplication.cir", 'w')

lineNumber = 1;
varNumber = 1;
alice = list([])
bob = list([])
server = "serverXinput"  #Bob
client = "clientXinput" #Alice
for line in file:
	splitted = line.split()
	if (lineNumber == 1):
		vectorSize = int(splitted[0])
		lineNumber += 1
	elif (lineNumber == 2):
		domainSize = int(splitted[0])
		lineNumber += 1
	elif (lineNumber == 3):
		threshold = int(splitted[0])
		lineNumber += 1
	elif (lineNumber == 4):
		for i in splitted:
			alice.append(int(i))
		lineNumber += 1
	elif (lineNumber == 5):
		for i in splitted:
			bob.append(int(i))
		lineNumber += 1
		
#################Functon Defenitions ##############
def inputFileGeneration(inputFile, fileName, char):
        varIndex = 1;
        fileXwrite = open(fileName,'w')
        for i in inputFile:
                fileXwrite.write('%s%d %d \n'%(char,varIndex,i))
                varIndex += 1
        if(char == 'a'):
                fileXwrite.write('threshold %d\n'%(threshold))
        fileXwrite.close()

def inputVarGeneration(fileName, index):
        global varNumber
        fileXread = open(fileName,'r')
        for line in fileXread:
                splitted=line.split()
                if( splitted[0] != 'threshold'):
                        circuit.write('.input %s %d %d \n'%(splitted[0],index,domainSize))
                        varNumber += 1
        fileXread.close()
###################################################




inputFileGeneration(alice, client, 'a')
inputFileGeneration(bob, server, 'b')

inputVarGeneration(client, 1)
inputVarGeneration(server, 2)
circuit.write('.input threshold 1 %d\n'%(2*domainSize))
circuit.write('.output result\n')


resXk = 1
for i in range(len(bob)):
        for j in range(domainSize):
                circuit.write('b%dXbit%d select b%d %d %d\n'%((i+1),j,(i+1),j,(j+1)))
        for j in range(domainSize):
                circuit.write('repeatXb%dXbit%d concat '%((i+1),j))
                for k in range(domainSize):
                        circuit.write('b%dXbit%d '%((i+1),j))
                circuit.write('\n')
        for j in range(domainSize):
                circuit.write('mulXb%dXbit%d and repeatXb%dXbit%d a%d\n'%((i+1),j,(i+1),j,(i+1)))

        for j in range(domainSize):
                if (j == 0):
                        circuit.write('concatXb%dXbit%d concat 0:%d  mulXb%dXbit%d\n'%((i+1),j,(domainSize-j),(i+1),j))
                else:
                        circuit.write('concatXb%dXbit%d concat 0:%d  mulXb%dXbit%d 0:%d\n'%((i+1),j,(domainSize-j),(i+1),j,j))
                

        k = 0
        
        for j in range(int(domainSize/2)):
                circuit.write('addXpart%dXb%d add concatXb%dXbit%d concatXb%dXbit%d\n'%((j+1),(i+1),(i+1),(j+k),(i+1),(j+1+k)))
                k += 1
        if((domainSize%2) != 0):
                j += 1
                circuit.write('addXpart%dXb%d or concatXb%dXbit%d concatXb%dXbit%d\n'%((j+1),(i+1),(i+1),(j+k),(i+1),(j+k)))
                k += 1
                rangeSize = int(domainSize/2)
        else:
                rangeSize = int(domainSize/2) - 1

        part = 1
        
        for j in range(rangeSize):
                circuit.write('addXpart%dXb%d add addXpart%dXb%d addXpart%dXb%d\n'%((k+1),(i+1),(part),(i+1),(part+1),(i+1)))
                k += 1       
                part += 2

                
        if(i != 0):
                if (resXk == 1):
                        circuit.write('res%d add addXpart%dXb%d addXpart%dXb%d\n'%((resXk),(k),(i),(k),(i+1)))
                        resXk += 1
                else:
                       circuit.write('res%d add res%d addXpart%dXb%d\n'%((resXk),(resXk-1),(k),(i+1)))
                       resXk += 1

circuit.write('result gteu res%d threshold\n'%(vectorSize-1))                      
                        
file.close()
circuit.close()

