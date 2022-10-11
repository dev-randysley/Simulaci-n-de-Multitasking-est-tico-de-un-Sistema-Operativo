from multiprocessing import Value
from util import parse_csv
import re

FILE_NAME = "prog.asm"

def main():
    ejecutable = Ensamblador.ensamblar(FILE_NAME)
    print(ejecutable.getListaInstrucciones())
    print(ejecutable.getLookupTable())
    #sistemaOperativo = SistemaOperativo(ejecutable,Procesador())
    #sistemaOperativo.procesar()

def is_label(instruction):
    return re.search('^([\w_]+):', instruction)

def parse_instruction(instruction):
    match = re.search('(mov|add|jmp|jz|cmp|inc|dec)(.*)', instruction)
    if match:
        params = re.search('\s*(\w*),\s*(\w*)', instruction)
        if (match.group(1) in ["cmp", "add", "mov"]):
            if (match.group(1) == "mov"):
                return Mov(params.group(1).strip(),params.group(2).strip())

            elif (match.group(1) == "add"):
                return Add(params.group(1).strip(),params.group(2).strip())

            elif (match.group(1) == "cmp"):
                return Cmp(params.group(1).strip(),params.group(2).strip())

        elif (match.group(1) in ["dec", "inc", "jz", "jmp"]):
            if (match.group(1) == "dec"):
                return Dec(match.group(2).strip())

            elif (match.group(1) == "inc"):
                return Inc(match.group(2).strip())

            elif (match.group(1) == "jz"):
                return Jz(match.group(2).strip())
            
            elif (match.group(1) == "jmp"):
                return Jmp(match.group(2).strip())
        else:
            pass

def parsear_instrucciones(instructions : list):
    list_instrucciones = []
    lookupTable = {}

    for index, instruction in enumerate(instructions):
        match = is_label(instruction[0])
        if match:
            lookupTable[match.group(1)] = index    
        else:
            list_instrucciones.append(parse_instruction(instruction[0]))

    return list_instrucciones,lookupTable

class Ensamblador:
    @staticmethod
    def ensamblar(file_name):
        codigo_fuente = parse_csv(file_name)
        instrucciones_con_includes = Ensamblador.addInclude(file_name)
        lista_instrucciones,lookupTable = parsear_instrucciones(instrucciones_con_includes)
        entry_point = 0
        
        return Ejecutable(instrucciones=lista_instrucciones,
                          entryPoint=entry_point,
                          lookupTable=lookupTable,
                          codigoFuente = [linea.replace("\n","") for linea in codigo_fuente])
    @staticmethod
    def addInclude(file_name):
        codigo_fuente = parse_csv(file_name)
        lista_con_includes = []
        for line in [linea.replace("\n","") for linea in codigo_fuente]:
            if "Include" in line:
                lista_con_includes.extend(Ensamblador.addInclude(line.split(" ")[1]))
            else:
                lista_con_includes.append((line,file_name))
        return lista_con_includes



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
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.ip = 0
        self.flag = 0
        self.proceso = None

    def procesar(self, proceso):
        ejecutable = proceso.getEjecutable()
        self.setProceso(proceso)
        self.setIP(ejecutable.getEntryPoint())
        punteroInstruccion = self.getIP()
        cantidadInstrucciones = len(ejecutable.getListaInstrucciones())
        while (punteroInstruccion < cantidadInstrucciones):
            ejecutable.getListaInstrucciones()[punteroInstruccion].procesar(self)
            punteroInstruccion = self.getIP()
            #visualizador.mostrar(ejecutable, procesador)
            #procesador.mostrar()
        
    def getProceso(self):
        return self.proceso

    def setProceso(self,proceso):
        self.proceso = proceso

    def setRegistro(self,registro,nuevoValor):
        self.setRegistros[registro](self,nuevoValor)

    def getRegistro(self,registro):
        return self.getRegistros[registro](self)

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

class Jz(Instruccion):
    def __init__(self, label):
        self.param1 = label

    def procesar(self, procesador):
        lookupTable = procesador.getProceso().getEjecutable().getLookupTable()
        indiceProximaInstruccion = lookupTable[self.param1]
        if procesador.getFlag() == 0:
            procesador.setIP(indiceProximaInstruccion) # seteamos directamente el indice segun la etiqueta
        else:
             procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
    def __str__(self):
        string = "jz {}".format(self.param1)
        return string

class Cmp(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            if int(procesador.getRegistro(self.param1)) == int(procesador.getRegistro(self.param2)):
                procesador.setRegistro("flag",1)
        else:
            if int(procesador.getRegistro(self.param1)) == int(self.param2):
                procesador.setRegistro("flag",1)
            else:
                procesador.setRegistro("flag",0)

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
