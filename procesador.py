from multiprocessing import Value
from util import parse_csv
import re

FILE_NAME = "prog.asm"

def main():
    Ensamblador.ensamblar(FILE_NAME)

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

            elif (match.group(1) == "add"):
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
        if is_label(instruction):
            lookupTable[instruction] = index    
        else:
            list_instrucciones.append(parse_instruction(instruction))

    return list_instrucciones,lookupTable

class Ensamblador:
    @staticmethod
    def ensamblar(file_name):
        codigo_fuente = parse_csv(file_name)
        lista_instrucciones,lookupTable = parsear_instrucciones(codigo_fuente)
        entry_point = 0
        
        return Ejecutable(instrucciones=lista_instrucciones,entryPoint=entry_point,lookupTable=lookupTable,codigoFuente = codigo_fuente)

class Ejecutable:
    def __init__(self, entryPoint, instrucciones : list, lookupTable : dict, codigoFuente):
        self.entryPoint = entryPoint
        self.instrucciones = instrucciones
        self.lookupTable = lookupTable
        self.codigoFuente = codigoFuente

    def procesar(self):
       pass

    def getEntryPoint(self):
        return self.entryPoint

    def getListaInstrucciones(self):
        return self.instrucciones

    def getCodigoFuente(self):
        return self.codigoFuente

    def getLookupTable(self):
        return self.lookupTable

    def run(self):
        pass

class Procesador:
    def __init__(self, ax, bx, cx, dx, ip, flag):
        self.ax = ax
        self.bx = bx
        self.cx = cx
        self.dx = dx
        self.ip = ip
        self.flag = flag

    def ejecutar(self, ejecutable):
        ejecutable.procesar()

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
        self.procesador.procesar(self.ejecutable)

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
    def __str__(self):
        string = "add {}, {}".format(self.param1,self.param2)
        return string

class Jmp(Instruccion):
    def __init__(self, label):
        self.param1 = label
    def procesar(self, procesador):
        pass
     
    def __str__(self):
        string = "jmp {}".format(self.param1)
        return string

class Jnz(Instruccion):
    def __init__(self, label):
        self.param1 = label

    def procesar(self, procesador):
        pass
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
    def __str__(self):
        string = "cmp {}, {}".format(self.param1,self.param2)
        return string

class Inc(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) + 1)
    def __str__(self):
        string = "inc {}".format(self.param1)
        return string

class Dec(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) - 1)
    def __str__(self):
        string = "dec {}".format(self.param1)
        return string

if __name__ == '__main__':
    main()
