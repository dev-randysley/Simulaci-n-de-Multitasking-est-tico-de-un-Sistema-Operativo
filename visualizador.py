import curses
import time

class Visualizador:

    def __init__(self):
        self.pantalla = curses.initscr()

    def mostrar(self, ejecutable, procesador):
        try:
            self.pantalla.clear()
            
            self.__mostrarInstrucciones(ejecutable, procesador)

            self.__mostrarRegistros(procesador)

            self.__mostrarMemoriaVideo(procesador)

            self.pantalla.refresh()

            time.sleep(0.5)
        except:
            pass


    def __mostrarInstrucciones(self, ejecutable, procesador):

      for indice in range(len(ejecutable.lista_instrucciones)):
          if(indice == procesador.getIP()):  #Si la instruccion es la ejecutada, se muestra con una flecha
              self.pantalla.addstr(indice, 0, "->")
              self.pantalla.addstr(indice, 3, ejecutable.lista_instrucciones[indice].strip())
          else:
              self.pantalla.addstr(indice, 3, ejecutable.lista_instrucciones[indice].strip())



    def __mostrarRegistros(self, procesador):
        self.pantalla.addstr(0, 25, "ax: " + str(procesador.getAx()))
        self.pantalla.addstr(1, 25, "bx: " + str(procesador.getBx()))
        self.pantalla.addstr(2, 25, "cx: " + str(procesador.getCx()))
        self.pantalla.addstr(3, 25, "dx: " + str(procesador.getDx()))
        self.pantalla.addstr(4, 25, "ip: " + str(procesador.getIP()))
        self.pantalla.addstr(5, 25, "flag: " + str(procesador.getFlag()))

    def mostrarFin(self, listaProcesos):
        print("\n\n", "Ejecucion finalizada")
        print("Los procesos terminaron con los siguientes valores: ", end="\n\n")

        for proceso in listaProcesos:
            if(proceso.error == ""):
                print("AX:", proceso.contexto.ax)
                print("BX:", proceso.contexto.bx)
                print("CX:", proceso.contexto.cx)
                print("DX:", proceso.contexto.dx)
                print("IP:", proceso.contexto.ip)
                print("FLAG:", proceso.contexto.flag)
                
            else:
                print("ERROR:", proceso.error)
            print("----------------", end='\n\n')