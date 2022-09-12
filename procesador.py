from util import parse_csv


def main():
    print(parse_csv("prog.asm",has_headers=False))

def parsear_instrucciones(intrucciones : list):
    list_instrucciones = []
    lookupTable = {}
    # TODO logic to parse instructions
    return list_instrucciones,lookupTable

class Ensamblador:
    @staticmethod
    def ensamblar(file_name):
        lista_instrucciones,lookupTable = parsear_instrucciones(parse_csv(file_name))
        entry_point = 0
        
        return Ejecutable(instrucciones=lista_instrucciones,entryPoint=entry_point,lookupTable=lookupTable)

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

class Mov(Instruccion):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            procesador.setRegistro(self.param1,procesador.getRegistro(self.param2))
        else:
            procesador.setRegistro(self.param1, int(self.param2))

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

class Jmp(Instruccion):
    def __init__(self, label):
        self.param1 = label
    def procesar(self, procesador):
        pass

class Jnz(Instruccion):
    def __init__(self, label):
        self.param1 = label
    def procesar(self, procesador):
        pass

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

class Inc(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) + 1)

class Dec(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    def procesar(self, procesador):
        procesador.setRegistro(self.param1,procesador.getRegistro(self.param1) - 1)

if __name__ == '__main__':
    main()
