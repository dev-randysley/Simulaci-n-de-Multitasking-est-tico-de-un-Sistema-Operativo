from multiprocessing import Value
from util import parse_csv
import re

FILE_NAME = "prog.asm"

def main():
    ejecutable = Ensamblador.ensamblar(FILE_NAME)
    #sistemaOperativo = SistemaOperativo(ejecutable,Procesador())
    #sistemaOperativo.procesar()

def is_label(instruction):
    return re.search('^([\w_]+):', instruction)

def parse_instruction(instruction):
    match = re.search('(mov|add|jmp|jnz|cmp|inc|dec)(.*)', instruction)
    if match:
        params = re.search('\s*(\w*),\s*(\w*)', instruction)
        if (match.group(1) in ["cmp", "add", "mov"]):
            if (match.group(1) == "mov"):
                return Mov(params.group(1),params.group(2))

            elif (match.group(1) == "add"):
                return Add(params.group(1),params.group(2))

            elif (match.group(1) == "cmp"):
                return Cmp(params.group(1),params.group(2))

        elif (match.group(1) in ["dec", "inc", "jnz", "jmp"]):
            if (match.group(1) == "dec"):
                return Dec(match.group(2))

            elif (match.group(1) == "inc"):
                return Inc(match.group(2))

            elif (match.group(1) == "jnz"):
                return Jnz(match.group(2))
            
            elif (match.group(1) == "jmp"):
                return Jmp(match.group(2))
        else:
            pass

def parsear_instrucciones(instructions : list):
    list_instrucciones = []
    lookupTable = {}

    for index, instruction in enumerate(instructions):
        match = is_label(instruction)
        if match:
            lookupTable[match.group(1)] = index    
        else:
            list_instrucciones.append(parse_instruction(instruction))

    return list_instrucciones,lookupTable

class Ensamblador:
    @staticmethod
    def ensamblar(file_name):
        codigo_fuente = parse_csv(file_name)
        lista_instrucciones,lookupTable = parsear_instrucciones(codigo_fuente)
        entry_point = 0
        
        return Ejecutable(instrucciones=lista_instrucciones,
                          entryPoint=entry_point,
                          lookupTable=lookupTable,
                          codigoFuente = [linea.replace("\n","") for linea in codigo_fuente])

class Ejecutable:
    def __init__(self, entryPoint, instrucciones : list, lookupTable : dict, codigoFuente: list):
        self.entryPoint = entryPoint
        self.instrucciones = instrucciones
        self.lookupTable = lookupTable
        self.codigoFuente = codigoFuente

    def getEntryPoint(self):
        return self.entryPoint

    def getListaInstrucciones(self):
        return self.instrucciones

    def getCodigoFuente(self):
        return self.codigoFuente

    def getLookupTable(self):
        return self.lookupTable

class Procesador:
    def __init__(self):
        self.ax = ""
        self.bx = ""
        self.cx = ""
        self.dx = ""
        self.ip = ""
        self.flag = ""
        self.proceso = None

    def procesar(self, proceso):
        self.setProceso(proceso)
        ejecutable = proceso.getEjecutable()
        punteroInstruccion = self.procesador.getIP()
        cantidadInstrucciones = len(ejecutable.getListaInstrucciones())
        while (punteroInstruccion < cantidadInstrucciones):
            indiceInstruccion = self.procesador.getIP()
            ejecutable.getListInstrucciones()[indiceInstruccion].procesar(self.procesador)
            #visualizador.mostrar(ejecutable, procesador)
            print(ejecutable.getCodigoFuente()[indiceInstruccion])
            #procesador.mostrar()
        
    def getProceso(self):
        return self.getProceso

    def setProceso(self,proceso):
        self.proceso = proceso

    def setRegistro(self,registro,nuevoValor):
        self.setRegistros[registro](nuevoValor)

    def getRegistro(self,registro):
        return self.getRegistros[registro]

    def setAx(self,valor):
        self.ax = valor

    def setBx(self,valor):
        self.bx = valor

    def setCx(self,valor):
        self.cx = valor
    
    def setDx(self,valor):
        self.dx = valor
    
    def setIP(self,valor):
        self.ip = valor
    
    def setFlag(self,valor):
        self.flag = valor

    def getAx(self):
        return self.ax 

    def getBx(self):
        return self.bx 

    def getCx(self):
        return self.cx 
    
    def getDx(self):
        return self.dx
    
    def getIP(self):
        return self.ip
    
    def getFlag(self):
        return self.flag
    
    setRegistros = {
        "ax" : setAx,
        "bx" : setBx,
        "cx" : setCx,
        "dx" : setDx,
        "ip" : setIP,
        "flag" : setFlag
    }

    getRegistros = {
        "ax" : getAx,
        "bx" : getBx,
        "cx" : getCx,
        "dx" : getDx,
        "ip" : getIP,
        "flag" : getFlag
    }
    
class SistemaOperativo:
    def __init__(self,ejecutable, procesador):
        self.ejecutable = ejecutable
        self.procesador = procesador
    
    def procesar(self):
        proceso = Proceso(self.ejecutable)
        self.procesador.procesar(proceso)

class Proceso:
    def __init__(self, ejecutable):
        self.ejecutable = ejecutable
        self.stack = []
    
    def getEjecutable(self):
        return self.ejecutable
    
    def getStack(self):
        return self.stack

class Visualizador:

    @staticmethod
    def mostrar(ejecutable,procesador):
        pass

class Instruccion:
    def procesar(procesador):
        pass

    def __str__(self):
        pass

    def __repr__(self):
        return self.__str__()
    

class Mov(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            procesador.setRegistro(self.param1,procesador.getRegistro(self.param2))
        else:
            procesador.setRegistro(self.param1, int(self.param2))
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar

    def __str__(self):
        string = "mov {}, {}".format(self.param1,self.param2)
        return string

class Add(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            procesador.setRegistro(self.param1, 
            procesador.getRegistro(self.param1) + procesador.getRegistro(self.param2))
        else:
            procesador.setRegistro(self.param1, 
            procesador.getRegistro(self.param1) + self.param2)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar

    def __str__(self):
        string = "add {}, {}".format(self.param1,self.param2)
        return string

class Jmp(Instruccion):
    def __init__(self, label):
        self.param1 = label
    def procesar(self, procesador):
        lookupTable = procesador.getProceso().getEjecutable().getLookupTable()
        indiceProximaInstruccion = lookupTable[self.param1]
        procesador.setIP(indiceProximaInstruccion) # seteamos directamente el indice segun la etiqueta
     
    def __str__(self):
        string = "jmp {}".format(self.param1)
        return string

class Jnz(Instruccion):
    def __init__(self, label):
        self.param1 = label

    def procesar(self, procesador):
        lookupTable = procesador.getProceso().getEjecutable().getLookupTable()
        indiceProximaInstruccion = lookupTable[self.param1]
        if procesador.setFlag() == 1:
            procesador.setIP(indiceProximaInstruccion) # seteamos directamente el indice segun la etiqueta
        else:
             procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
    def __str__(self):
        string = "jnz {}".format(self.param1)
        return string

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            if procesador.getRegistro(self.param1) == procesador.getRegistro(self.param2):
                procesador.getRegistro("flag",0)
        else:
             if procesador.getRegistro(self.param1) != procesador.getRegistro(self.param2):
                procesador.getRegistro("flag",1)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
    def __str__(self):
        string = "cmp {}, {}".format(self.param1,self.param2)
        return string

class Inc(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) + 1)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
    def __str__(self):
        string = "inc {}".format(self.param1)
        return string

class Dec(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) - 1)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
    def __str__(self):
        string = "dec {}".format(self.param1)
        return string

if __name__ == '__main__':
    main()
