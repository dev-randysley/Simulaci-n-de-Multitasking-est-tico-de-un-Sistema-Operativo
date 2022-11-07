from enum import Enum
from contexto import Contexto
from util import parse_csv
import re
import curses
import time
import sys

FILE_NAME = "prog.asm"
FILE_NAME_TEST_FUNCIONES = "test_llamado_funciones.asm"

def main(archivos):
    ejecutables = [Ensamblador.ensamblar(archivo) for archivo in archivos]
    sistemaOperativo = SistemaOperativo(ejecutables,Procesador())
    sistemaOperativo.procesar()

def is_label(instruction):
    return re.search('^([\w_]+):', instruction)

def parse_instruction(instruction):
    match = re.search('(mov|add|jmp|jz|cmp|inc|dec|pop|push|ret|mult|call)(.*)', instruction)
    if match:
        params = re.search('\s*(\w*),\s*(\w*)', instruction)
        if (match.group(1) in ["cmp", "add", "mov", "mult"]):
            if (match.group(1) == "mov"):
                return Mov(params.group(1).strip(),params.group(2).strip())

            elif (match.group(1) == "add"):
                return Add(params.group(1).strip(),params.group(2).strip())

            elif (match.group(1) == "cmp"):
                return Cmp(params.group(1).strip(),params.group(2).strip())

            elif (match.group(1) == "mult"):
                return Multi(params.group(1).strip(),params.group(2).strip())

        elif (match.group(1) in ["dec", "inc", "jz", "jmp", "pop", "push", "ret", "call"]):
            if (match.group(1) == "dec"):
                return Dec(match.group(2).strip())

            elif (match.group(1) == "inc"):
                return Inc(match.group(2).strip())

            elif (match.group(1) == "jz"):
                return Jz(match.group(2).strip())
            
            elif (match.group(1) == "jmp"):
                return Jmp(match.group(2).strip())
            
            elif (match.group(1) == "pop"):
                return Pop(match.group(2).strip())

            elif (match.group(1) == "push"):
                return Push(match.group(2).strip())

            elif (match.group(1) == "ret"):
                return Ret()
            
            elif (match.group(1) == "call"):
                return Call(match.group(2).strip())
        else:
            raise Exception("El comando ingresado en el codigo es incorrecto")

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
        entry_point = getEntryPoint(codigo_fuente,instrucciones_con_includes)
        return Ejecutable(instrucciones=lista_instrucciones,
                          entryPoint=entry_point,
                          lookupTable=lookupTable,
                          codigoFuente = [instruccion[0] for instruccion in instrucciones_con_includes])
    @staticmethod
    def addInclude(file_name):
        codigo_fuente = parse_csv(file_name)
        lista_con_includes = []
        for line in codigo_fuente:
            if "Include" in line:
                lista_con_includes.extend(Ensamblador.addInclude(line.split(" ")[1]))
            else:
                lista_con_includes.append((line,file_name))
        return lista_con_includes

def getEntryPoint(main_instructions, lista_instrucciones):
    entryPoint = ""
    for line in main_instructions:
        if not "Include" in line:
            entryPoint = line
            break
    return [index for index,line in enumerate(lista_instrucciones) if line[0] == entryPoint][0] - 1

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

class Visualizador:
    def __init__(self):
        self.pantalla = curses.initscr()

    def mostrar(self,ejecutable, procesador):
        try:
            self.pantalla.clear()
            self.mostrarInstrucciones(ejecutable, procesador)
            self.mostrarRegistros(procesador)
            self.pantalla.refresh()

            time.sleep(0.5)
        except:
            pass

    def mostrarInstrucciones(self, ejecutable, procesador):
        
        totalMostrado = 0

        if(procesador.ip <= 1):
            for indice in range(len(ejecutable.getCodigoFuente())):
                if(indice == procesador.ip):
                    self.pantalla.addstr(indice, 0, "->")
                    self.pantalla.addstr(indice, 3, ejecutable.getCodigoFuente()[indice].strip())
                else:
                    self.pantalla.addstr(indice, 3, ejecutable.getCodigoFuente()[indice].strip())
                
                totalMostrado += 1
                if(totalMostrado == 5):
                    if(totalMostrado != len(ejecutable.getCodigoFuente())):
                        self.pantalla.addstr(indice + 1, 3, "...")
                    break
        
        elif(procesador.ip + 1 >= (len(ejecutable.getCodigoFuente()) - 1)):
            rango = range(len(ejecutable.getCodigoFuente()))
            if(len(rango) > 5):
                rango = rango[len(rango) - 5: len(rango)]
                self.pantalla.addstr(0, 3, "...")
                totalMostrado += 1

            for indice in rango:
                if(indice == procesador.ip):
                    self.pantalla.addstr(totalMostrado, 0, "->")
                    self.pantalla.addstr(totalMostrado, 3, ejecutable.getCodigoFuente()[indice].strip())
                else:
                    self.pantalla.addstr(totalMostrado, 3, ejecutable.getCodigoFuente()[indice].strip())
                
                totalMostrado += 1
        
        else:
            indice = 0
            if(procesador.ip - 2 > 0):
                self.pantalla.addstr(indice, 3, "...")
                indice += 1

            self.pantalla.addstr(indice, 3, ejecutable.getCodigoFuente()[procesador.ip - 2].strip())
            self.pantalla.addstr(indice + 1, 3, ejecutable.getCodigoFuente()[procesador.ip - 1].strip())

            self.pantalla.addstr(indice + 2, 0, "->")
            self.pantalla.addstr(indice + 2, 3, ejecutable.getCodigoFuente()[procesador.ip].strip())

            self.pantalla.addstr(indice + 3, 3, ejecutable.getCodigoFuente()[procesador.ip + 1].strip())
            self.pantalla.addstr(indice + 4, 3, ejecutable.getCodigoFuente()[procesador.ip + 2].strip())

            self.pantalla.addstr(indice + 5, 3, "...")

    def mostrarRegistros(self, procesador):
        self.pantalla.addstr(0, 25, "ax: " + str(procesador.ax))
        self.pantalla.addstr(1, 25, "bx: " + str(procesador.bx))
        self.pantalla.addstr(2, 25, "cx: " + str(procesador.cx))
        self.pantalla.addstr(3, 25, "dx: " + str(procesador.dx))
        self.pantalla.addstr(4, 25, "ip: " + str(procesador.ip))
        self.pantalla.addstr(5, 25, "flag: " + str(procesador.flag))



    def mostrarFin(self,procesador):
        print("\n Ejecución terminada")
        print("Los registros terminaron con los siguientes valores: ", end="\n\n")

        print("AX:", procesador.getAx())
        print("BX:", procesador.getBx())
        print("CX:", procesador.getCx())
        print("DX:", procesador.getDx())
        print("IP:", procesador.getIP())
        print("FLAG:", procesador.getFlag())
                

class Procesador:
    def __init__(self):
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.ip = 0
        self.flag = 0
        self.proceso = None
        self.estado = ProcesadorEstado.ACTIVO
        self.sistema = None

    def procesar(self):
        while (self.estado == ProcesadorEstado.ACTIVO):
            self.setIP(self.proceso.getContexto()["ip"])
            visualizador = Visualizador()
            while (self.getIP() < len(self.proceso.ejecutable.getListaInstrucciones())):
                try:
                    self.proceso.ejecutable.getListaInstrucciones()[self.getIP()].procesar(self)
                    self.sistema.clockHandler()      #Llamamos al sistema operativo para evaluar si hay que pasar a otro proceso
                    visualizador.mostrar(self.proceso.ejecutable,self)
                except Exception:
                    self.proceso.estado = ProcesoEstado.FINALIZADO
                    self.sistema.cambiarProceso()

        #Si termino el ejecutable
            self.proceso.estado = ProcesoEstado.FINALIZADO
            self.sistema.cambiarProceso()

        visualizador.mostrarFin(self)
    
    def setSistema(self,sistemaOperativo):
        self.sistema = sistemaOperativo

    def getProceso(self):
        return self.proceso

    def setProceso(self,proceso):
        self.proceso = proceso

    def setRegistro(self,registro,nuevoValor):
        self.setRegistros[registro](self,nuevoValor)

    def getRegistro(self,registro):
        return self.getRegistros[registro](self)

    def getEstado(self):
        return self.estado
    
    def setEstado(self, estado):
        self.estado = estado

    def getContexto(self):
        return {"ax":self.getAx(),"bx":self.getBx(), "cx":self.getCx(),
                "dx":self.getDx(), "ip":self.getIP(), "flag":self.getFlag()}

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


class ProcesadorEstado(Enum):
    ACTIVO = 0,
    INACTIVO = 1
    
class SistemaOperativo:
    def __init__(self,ejecutables, procesador):
        self.ejecutables = ejecutables
        self.procesador = procesador
        self.listaProcesos = list()
        self.procesoActivo = 0
        self.contadorInstrucciones = 0
        self.INSTRUCCIONES_MAXIMAS = 5

        for ejecutable in ejecutables:
            proceso = Proceso(ejecutable)
            proceso.getContexto()["ip"] = proceso.ejecutable.entryPoint
            self.listaProcesos.append(proceso)
        
        self.procesador.setSistema(self)
        self.procesador.setProceso(self.listaProcesos[self.procesoActivo])
    
    def procesar(self):
        self.procesador.procesar()
    
    def getProcesador(self):
        return self.procesador
    
    def clockHandler(self):
        self.contadorInstrucciones += 1
        if(self.contadorInstrucciones >= self.INSTRUCCIONES_MAXIMAS):
            self.cambiarProceso()
    
    def cambiarProceso(self):
        contexto = self.procesador.getContexto()
        self.listaProcesos[self.procesoActivo].setContexto(contexto)
        self.listaProcesos[self.procesoActivo].setStack(self.procesador.proceso.getStack()) 
        self.listaProcesos[self.procesoActivo].setEstado(self.procesador.proceso.getEstado()) 
        if(self.listaProcesos[self.procesoActivo].getEstado() == ProcesoEstado.EJECUTANDO):
            self.listaProcesos[self.procesoActivo].setEstado(ProcesoEstado.BLOQUEADO) 

        self.procesoActivo = self.obtenerProximoProceso()

        if(self.procesoActivo != -1):
            self.listaProcesos[self.procesoActivo].setEstado(ProcesoEstado.EJECUTANDO)
            self.procesador.setProceso(self.listaProcesos[self.procesoActivo])
            self.contadorInstrucciones = 0
        else:
            self.procesador.setEstado(ProcesadorEstado.INACTIVO) 

    def obtenerProximoProceso(self):        
        NOT_FOUND = -1
        for index, proceso in enumerate(self.listaProcesos):
            if(proceso.estado == ProcesoEstado.BLOQUEADO):
                return index
        return NOT_FOUND


class Proceso:
    def __init__(self, ejecutable):
        self.ejecutable = ejecutable
        self.stack = []
        self.estado = ProcesoEstado.BLOQUEADO
        self.contexto = {}
    
    def getEjecutable(self):
        return self.ejecutable
    
    def getStack(self):
        return self.stack
    
    def setStack(self, stack):
        self.stack = stack
    
    def getContexto(self):
        return self.contexto

    def setContexto(self, contexto):
        self.contexto["ax"] = contexto["ax"]
        self.contexto["bx"] = contexto["bx"]
        self.contexto["cx"] = contexto["cx"]
        self.contexto["dx"] = contexto["dx"]
        self.contexto["ip"] = contexto["ip"]
        self.contexto["flag"] = contexto["flag"]

    def getEstado(self):
        return self.estado

    def setEstado(self, estado):
        self.estado = estado

class ProcesoEstado(Enum):
    BLOQUEADO = 0,
    EJECUTANDO = 1,
    FINALIZADO = 2

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

class Push(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    
    def procesar(self,procesador):
        if self.param1 in ["ax", "bx", "cx", "dx"]:
           procesador.getProceso().getStack().append(procesador.getRegistro(self.param1))
        else:
            procesador.getProceso().getStack().append(self.param1)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
        
    def __str__(self):
        string = "push {}".format(self.param1)
        return string

class Pop(Instruccion):
    def __init__(self, param1):
        self.param1 = param1
    
    def procesar(self,procesador):
        procesador.setRegistro(self.param1,procesador.getProceso().getStack().pop())
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar
        
    def __str__(self):
        string = "pop {}".format(self.param1)
        return string

class Call(Instruccion):
    def __init__(self, label):
        self.param1 = label

    def procesar(self, procesador):
        lookupTable = procesador.getProceso().getEjecutable().getLookupTable()
        indiceProximaInstruccion = lookupTable[self.param1]
        procesador.getProceso().getStack().append(procesador.getIP() + 1) # agregamos al stack la IP donde debe retornar al terminar la ejecucion de la funcion
        procesador.setIP(indiceProximaInstruccion) # seteamos directamente el indice segun la etiqueta
        
        
    def __str__(self):
        string = "call {}".format(self.param1)
        return string


class Ret(Instruccion):
    
    def procesar(self,procesador):
        proxima_instruccion = procesador.getProceso().getStack().pop()
        procesador.setIP(proxima_instruccion)
        
    def __str__(self):
        string = "ret "
        return string


class Multi(Instruccion):
    
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

    def procesar(self, procesador):
        if self.param2 in ["ax", "bx", "cx", "dx"]:
            procesador.setRegistro(self.param1, 
            int(procesador.getRegistro(self.param1)) * int(procesador.getRegistro(self.param2)))
        else:
            procesador.setRegistro(self.param1, 
            procesador.getRegistro(self.param1) * self.param2)
        procesador.setIP(procesador.getIP() + 1) # pasamos a la siguiente instruccion despues de ejecutar

    def __str__(self):
        string = "multi {}, {}".format(self.param1,self.param2)
        return string

if __name__ == '__main__':
    main([archivo for archivo in sys.argv if archivo != sys.argv[0]])
