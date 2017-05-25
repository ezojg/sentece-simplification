import copy
import sys
import requests

class Simp(object):
  def __init__(self):
    self.TYPE=""
    self.TYPEx=0
    self.TYPEy=0
    self.TEXT=""
    self.COMP=[]
  def agregarTYPE(self,Type):
    self.TYPE=Type
  def agregarTEXT(self,text):
    self.TEXT=text
  def agregarCOMP(self,comp):
    self.COMP.append(comp)

class Frase(object):
  def __init__(self):
    self.TYPE=""
    self.TEXT=""
    self.POS=""
    self.TREE=""
    self.SIMP=[]
  def agregarTYPE(self,Type):
    self.TYPE=Type
  def agregarTEXT(self,text):
    self.TEXT=text
  def agregarPOS(self,Pos):
    self.POS=Pos
  def agregarTREE(self,Tree):
    self.TREE=Tree
  def agregarSIMP(self):
    self.SIMP.append(Simp())

class Sentence(object):
  def __init__(self):
    self.FLAG=True
    self.TEXT=""
    self.TREE=""
    self.SIMP=[]
  def agregarTEXT(self,text):
    self.TEXT=text
  def agregarTREE(self,Tree):
    self.TREE=Tree
  def agregarSIMP(self):
    self.SIMP.append(Simp())


MEMORIAB=[]
MEMORIAA=[]


#----lectura de datos desde archivo
arch=(sys.argv[1])
f = open(arch)
dato = f.read().splitlines()
f.close
frase=Frase()
for i in range(len(dato)):
  if 'TYPE: ' in dato[i][0:6]:
    frase.agregarTYPE(dato[i][6:])
  elif 'TEXT: ' in dato[i][0:6]:
    frase.agregarTEXT(dato[i][6:])
  elif 'POS : ' in dato[i][0:6]:
    frase.agregarPOS(dato[i][6:])
  elif 'TREE: ' in dato[i][0:6]:
    frase.agregarTREE(dato[i][6:])
  elif 'SIMP:' in dato[i]:
    frase.agregarSIMP()
  elif '  TYPE: ' in dato[i][0:8]:
    frase.SIMP[-1].agregarTYPE(dato[i][8:])
  elif '  TEXT: ' in dato[i][0:8]:
    frase.SIMP[-1].agregarTEXT(dato[i][8:])
  elif '  COMP: ' in dato[i]:
    frase.SIMP[-1].agregarCOMP(dato[i][8:])
#------------


#-------Programa principal
#Algoritmo v4


if ((frase.TYPE.find('sentence')) !=- 1) and (frase.SIMP!=[]) and (frase.SIMP[0].TYPE != ''):
  y=1
  w=1
  SIMPworkspace=[]
  # copia TREE y cada SIMP a SENTENCE.1
  Sentence1=Sentence()
  Sentence1.TREE=copy.deepcopy(frase.TREE)
  Sentence1.TEXT=copy.deepcopy(frase.TEXT)
  for i in range(len(frase.SIMP)):
    #Sentence1.SIMP.append(Simp())
    #Sentence1.SIMP[i]=copy.deepcopy(frase.SIMP[i])
    SIMPworkspace.append(Simp())
    SIMPworkspace[i]=copy.deepcopy(frase.SIMP[i])
  
## ORDENAMIENTO DE SIMPs
  for i in range(len(SIMPworkspace)):
    #print SIMPworkspace[i].TEXT
    #print SIMPworkspace[i].TYPE
    SIMPworkspace[i].TYPEx = int(SIMPworkspace[i].TYPE[SIMPworkspace[i].TYPE.find('[')+1:SIMPworkspace[i].TYPE.find('..')])
    SIMPworkspace[i].TYPEy = int(SIMPworkspace[i].TYPE[SIMPworkspace[i].TYPE.find('..')+2:SIMPworkspace[i].TYPE.find(']')])
    if 'parenthesis' in SIMPworkspace[i].TYPE:
      SIMPworkspace[i].TYPEy = SIMPworkspace[i].TYPEy + 2
    #print SIMPworkspace[i].TYPEx
    #print SIMPworkspace[i].TYPEy


  SIMPworkspace.sort(key=lambda x: x.TYPEy, reverse=True)
  SIMPworkspace.sort(key=lambda x: x.TYPEx)

 
 # for i in range(len(SIMPworkspace)):
 #   print "\nSIMP " + str(i) + " :"
 #   print SIMPworkspace[i].TYPE 
 #   print SIMPworkspace[i].TYPEx
 #   print SIMPworkspace[i].TYPEy
 # print "\n"  

  for i in range(len(SIMPworkspace)):
    Sentence1.SIMP.append(Simp())
    Sentence1.SIMP[i]=copy.deepcopy(SIMPworkspace[i])  
   

  # Agrega la oracion original Sentence1 a la memoria como primer objeto en ser analizado
  MEMORIAB.append(Sentence())
  MEMORIAB[0]=copy.deepcopy(Sentence1)



  # 1 entrada al bucle A por cada SIMP diferente en Sentence1
  numSimp=len(Sentence1.SIMP)
  s = 0
  #bucle A
  while s < numSimp :
    #print "\nEntro por vez " + str(s) + " al bucle A"
    #print "Analizando todos los SIMP de tipo: " + MEMORIAB[0].SIMP[s].TYPE
    #Entra al bucle B el numero de veces igual al numerode elementos en MEMORIAB
    numMEM = len(MEMORIAB)
    t = 0
    #bucle B
    while t < numMEM :
      #print "Entro por vez " + str(t) + " al bucle B"
      #Entra si la oracion no ha sido analizada antes (FLAG==True) y si el texto del simp esta presente en la oracion.
      #print "CONDICIONES:"
      #print "SIMP " + MEMORIAB[0].SIMP[s].TEXT
      #print "SIMP " + MEMORIAB[0].SIMP[s].TYPE
      #print "MEMB " + str(MEMORIAB[t].FLAG)
      #print "MEMB " + MEMORIAB[t].TEXT
      if ( MEMORIAB[0].SIMP[s].TEXT in MEMORIAB[t].TEXT ) and ( MEMORIAB[t].FLAG == True ):
        MEMORIAB[t].FLAG = False
	#print "False to: " + MEMORIAB[t].TEXT
        #print "Entro a condicional"
        #Reglas de simplificacion
        if ( 'coordination' in MEMORIAB[t].SIMP[s].TYPE ) and ( not ('sentence coordination' in MEMORIAB[t].SIMP[s].TYPE ) ) :
          #print "Aplico regla coord"
          TEMPORALES = []
          c = len(MEMORIAB[t].SIMP[s].COMP)
          #print "Hay " + str(c) + " COMP en este SIMP"
          tt = 0
          while c > 0 :
            c = c - 1
            if ( 'conjunct' in MEMORIAB[0].SIMP[s].COMP[c] ) and ( not ( 'conjunction' in MEMORIAB[0].SIMP[s].COMP[c] ) ) :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t])
              replaced = MEMORIAB[0].SIMP[s].TEXT
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              replacer = MEMORIAB[0].TEXT[indice1:indice2]
              TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
              tt = tt + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'parenthesis' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla par"
          TEMPORALES = []
          c = len(MEMORIAB[t].SIMP[s].COMP)
          #print "Hay " + str(c) + " COMP en este SIMP"
          tt = 0
          while c > 0 :
            #print "entro al while de par"
            c = c - 1
            TEMPORALES.append(Sentence())
            TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t])
            replaced = MEMORIAB[0].SIMP[s].TEXT + ' )'
            indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
            indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
            replacer = MEMORIAB[0].TEXT[indice1:indice2]
            #print "replaced: " + replaced
            #print "replacer: " + replacer
            TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
            tt = tt + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'apposition' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla Apposition"
          TEMPORALES = []
          c = len(MEMORIAB[t].SIMP[s].COMP)
          #print "Hay " + str(c) + " COMP en este SIMP"
          tt = 0
          while c > 0 :
            #print "entro al while de par"
            c = c - 1
            TEMPORALES.append(Sentence())
            TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t])
            replaced = MEMORIAB[0].SIMP[s].TEXT
            indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
            indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
            replacer = MEMORIAB[0].TEXT[indice1:indice2]
            #print "replaced: " + replaced
            #print "replacer: " + replacer
            TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
            tt = tt + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print "Copio a memoria: " + MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'member-collection' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla member-collection"
          TEMPORALES = []
          c = len(MEMORIAB[t].SIMP[s].COMP)
          #print "Hay " + str(c) + " COMP en este SIMP"
          tt = 0
          while c > 0 :
            #print "entro al while de mem"
            c = c - 1
            TEMPORALES.append(Sentence())
            TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t])
            replaced = MEMORIAB[0].SIMP[s].TEXT
            indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
            indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
            replacer = MEMORIAB[0].TEXT[indice1:indice2]
            #print "replaced: " + replaced
            #print "replacer: " + replacer
            TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
            tt = tt + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print "Copio a memoria: " + MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'sentence coordination' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla Verb"
          TEMPORALES = []
          c = len(MEMORIAB[t].SIMP[s].COMP)
          #print "Hay " + str(c) + " COMP en este SIMP"
          tt = 0
          while c > 0 :
            c = c - 1
            if ( 'conjunct' in MEMORIAB[0].SIMP[s].COMP[c] ) and ( not ( 'conjunction' in MEMORIAB[0].SIMP[s].COMP[c] ) ) :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t])
              #sustituye todo el contenido de TEMPORAL.r/TREE, por el contenido la oracion coordinada
              #replaced = MEMORIAB[0].SIMP[s].TEXT
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              replacer = MEMORIAB[0].TEXT[indice1:indice2]
              #print replacer
              TEMPORALES[tt].TEXT = replacer 
              ## si la oracion no termina en punto o ! 
              tt = tt + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'full relative clause' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla RelCl"
          TEMPORALES = []
          c = 0
          tt = 0
          while c < 2 :
            if 'referred noun phrase' in MEMORIAB[0].SIMP[s].COMP[c] :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t]) #ok
              if MEMORIAB[0].TEXT[MEMORIAB[0].TEXT.index(TEMPORALES[tt].SIMP[s].TEXT)+len(TEMPORALES[tt].SIMP[s].TEXT)-1] == ',':
                replaced = MEMORIAB[0].SIMP[s].TEXT + ',' #posible error, si es asi probar con ' ,'
              else:
                replaced = MEMORIAB[0].SIMP[s].TEXT
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              replacer = MEMORIAB[0].TEXT[indice1:indice2]
              TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
              indice3 = indice1
              indice4 = indice2
            if 'clause' in MEMORIAB[0].SIMP[s].COMP[c] :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t]) #ok
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              TEMPORALES[tt].TEXT = copy.deepcopy(MEMORIAB[0].TEXT[indice3:indice4]+' '+MEMORIAB[0].TEXT[indice1:indice2] ) ##
              cad3 = MEMORIAB[0].TEXT[indice1:indice2]
              cad4 = cad3.split()
              if (cad4[0]+'_WDT') in frase.POS:
                TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(' '+cad4[0],'')
            tt = tt + 1
            c = c + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'reduced relative clause' in MEMORIAB[t].SIMP[s].TYPE:
          #print "Aplico regla RelCl"
          TEMPORALES = []
          c = 0
          tt = 0
          while c < 2 :
            if 'referred noun phrase' in MEMORIAB[0].SIMP[s].COMP[c] :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t]) #ok
              replaced = MEMORIAB[0].SIMP[s].TEXT
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              replacer = MEMORIAB[0].TEXT[indice1:indice2]
              #subj = MEMORIAB[0].TEXT[indice1:(indice2+1)]
              subj = MEMORIAB[0].TEXT[indice1:(indice2)]
              TEMPORALES[tt].TEXT = TEMPORALES[tt].TEXT.replace(replaced,replacer)
            if 'clause' in MEMORIAB[0].SIMP[s].COMP[c] :
              TEMPORALES.append(Sentence())
              TEMPORALES[tt] = copy.deepcopy(MEMORIAB[t]) #el referente debera estar antes que la clausula para tener orden correcto
              indice1 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('[')+1:TEMPORALES[tt].SIMP[s].COMP[c].find('..')])
              indice2 = (int)(TEMPORALES[tt].SIMP[s].COMP[c][TEMPORALES[tt].SIMP[s].COMP[c].find('..')+2:TEMPORALES[tt].SIMP[s].COMP[c].find(']')])
              replacer = MEMORIAB[0].TEXT[indice1:indice2]
              TEMPORALES[tt].TEXT = subj + " _ " + replacer #en este punto para ingresar copula necesitas info de numero y tiempo
            tt = tt + 1
            c = c + 1
          #copiar simplificaciones de memoria temporal a MEMORIAB
          indtempamem = 0
          while indtempamem < len(TEMPORALES) :
            MEMORIAB.append(Sentence())
            MEMORIAB[-1]=copy.deepcopy(TEMPORALES[indtempamem])
            MEMORIAB[-1].FLAG = True
            #print MEMORIAB[-1].TEXT
            indtempamem = indtempamem + 1
        elif 'hypernymy' in MEMORIAB[t].SIMP[s].TYPE:
	  print "**hypernymy detected**"
	  #print "True to: " + MEMORIAB[t].TEXT
	  MEMORIAB[t].FLAG = True
        else:
	  print "Error: Unknown simplification construct detected."
	  #print "True to: " + MEMORIAB[t].TEXT
	  MEMORIAB[t].FLAG = True
      t = t + 1
    s = s + 1

  #CONDICIONES PARA IMPRESION DE SIMPLIFICACIONES EN ARCHIVO DE TEXTO
  print "Sentence simplificated. New sentences generated:"
  for i in range(len(MEMORIAB)):
    #se reutiliza flag para marcar las oraciones finales
    MEMORIAB[i].FLAG = True
    for j in range(len(MEMORIAB[0].SIMP)):   
      #NOTA: si se agrega un constructo simplificable, anadirlo tambien a esta lista:
      if ( ('member-collection' in MEMORIAB[0].SIMP[j].TYPE) or ('apposition' in MEMORIAB[0].SIMP[j].TYPE) or ('coordination' in MEMORIAB[0].SIMP[j].TYPE) or ('parenthesis' in MEMORIAB[0].SIMP[j].TYPE) or ('sentence coordination' in MEMORIAB[0].SIMP[j].TYPE) or ('full relative clause' in MEMORIAB[0].SIMP[j].TYPE) or ('reduced relative clause' in MEMORIAB[0].SIMP[j].TYPE) ) and (MEMORIAB[0].SIMP[j].TEXT in MEMORIAB[i].TEXT) :
        MEMORIAB[i].FLAG = False

  ##areglar numeracion archivos salida ej 011
  arcsalnum = 0
  for i in range(len(MEMORIAB)):
    if MEMORIAB[i].FLAG == True:
      arcsalnum = arcsalnum + 1
      print MEMORIAB[i].TEXT#Salida 
      archSalNombre = sys.argv[2]
      archSalNombre=archSalNombre[:-8] + "_" + (str)(arcsalnum)+ '.alg.txt'
      archivoSalida=open(archSalNombre,"w")
      archivoSalida.write(MEMORIAB[i].TEXT)
      archivoSalida.close()
else:
  print frase.TEXT #----Salida si no habia constructos simplificables
  archSalNombre = sys.argv[2]
  archSalNombre = archSalNombre[:-8] + ".alg.txt"
  archivoSalida = open(archSalNombre,"w")
  archivoSalida.write(frase.TEXT)
  archivoSalida.close()


#FIN



















