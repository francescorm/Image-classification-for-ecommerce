import os
import shutil






def createDir(matricola,folder):
    dirSerial = os.path.join(folder,matricola)
    #dirBollino = os.path.join(folder,matricola)
    if not os.path.exists(dirSerial):
        os.mkdir(dirSerial)

def copiaFoto(directoryMatricola,foto,folderFinal):
    cartellaFinaleBollino = os.path.join(folderFinal,directoryMatricola)
    #cartellaFinaleSenzaBollino = os.path.join(cartellaClassificateSenzaBollino,directoryMatricola)
    shutil.copy(foto,cartellaFinaleBollino)
    #shutil.copy(foto,cartellaFinaleSenzaBollino)

def rinominaConSeriale(cartellaConBollino):
	for subdir, dirs, files in os.walk(cartellaConBollino):
		matricola = os.path.split(subdir)[1]  #NOME DELLA SOTTOCARTELLA, SERIALE MACCHINA
		i=0
		#VADO SOLO SULLE CARTELLE CHE CONTENGONO FILE
		if files:
			files.sort()
			for file in files:
				nomefile=os.path.splitext(file)[0]
				print (file)
				nuovonome = os.path.join(subdir,matricola + "-"+str(i)+".jpg")
				#print (nuovonome)
				i += 1
				#print (file)
				#nomefile = file+"-"+str(i)+".jpg"
				src = os.path.join(subdir,file)
				os.rename(src,nuovonome)



def rinominaPrimaImmagine(cartellaConBollino):
    for subdir, dirs, files in os.walk(cartellaConBollino):
        matricola = os.path.split(subdir)[1]  #NOME DELLA SOTTOCARTELLA, SERIALE MACCHINA
        #print (matricola)
        #VADO SOLO SULLE CARTELLE CHE CONTENGONO FILE
        if files:
            #print (files)
            files.sort()
            primaImmagine= matricola + "-0.jpg"
            #print (primaImmagine)
            src = os.path.join(subdir,primaImmagine)
            primaImmagineMagento= matricola+".jpg"
            #print (primaImmagineMagento)
            srcNew=os.path.join(subdir,primaImmagineMagento)
            os.rename(src,srcNew)
