from tkinter import * #libreria para generacion de interfaces graficas
from datetime import datetime #libreria para tomar hora del sistema, necesaria para el cronometro
import random #libreria para generacion de numeros aleatorios

programas = 0 #numero de programas a procesar por lotes, se modifica posteriormente
programadores = ("José","Carlos","Carolina","Juan") #lista de los distintos programadores a asignar en los programas
operadores = ("+","-","*","/") #operaciones aritmeticas que se pueden realizar
hora_inicio = datetime.now() #declaracion del inicio del cronometro
INTERVALO_REFRESCO = 1000 #tiempo para actualizar el cronometro
op = 0 #variable para la activacion del cronometro, cuando sea igual a 1 este iniciará
pendientes = 0 #numero de procesos pendientes de realizar
lista = [] #lista de procesos a realizar

validate_entry = lambda text: text.isdecimal() #funcion de validacion para entrada de numeros unicamente

class proceso: #clase para almacenar los datos de los procesos
    #atributos de un proceso
    nprog=0
    prog = ""
    n1 = 0
    op = ''
    n2 = 0
    tiempo = 0
    nlot = 0

    def set(self, np, pr, num1, oper, num2, times, nlote): #setter de la clase
        self.nprog = np
        self.prog = pr
        self.n1 = num1
        self.op = oper
        self.n2 = num2
        self.tiempo = times
        self.nlot = nlote

    def solve(self): #funcion para resolver las operaciones del proceso
        operacion = str(self.n1)+str(self.op)+str(self.n2) #creamos una cadena que contenga la oepracion
        return eval(operacion) #devolvemos el resultado del calculo, la funcion eval retorna el resultado de
        # una operacion expresada en una cadena

    def toString(self): #metodo para devolver una cadena con el formato requerido, utilizada para escribir en
        # datos.txt
        s='\t'+str(self.nprog)+'. '+self.prog+'\n'+'\t'+str(self.n1)+str(self.op)+str(self.n2)+'\n'+'\tTME: ' \
          + str(self.tiempo) + '\n\n'
        return s

    def toStringSolved(self): #metodo para devolver una cadena con el formato requerido, utilizada para
        # escribir en Resultados.txt
        s = '\t' + str(self.nprog) + '. ' + self.prog + '\n' + '\t' + str(self.n1) + str(self.op) + \
            str(self.n2) +'='+str(self.solve()) + '\n\n'
        return s

def generar(n): #funcion para la generacion de procesos
    global programas, op, hora_inicio,pendientes  # variable globales que modifica la función
    op = 1  # cambiamos el valor de op para iniciar el cronometro
    pendientes = n #numero de procesos pendientes de procesar
    f = open('datos.txt', 'w')  # abrimos el archivo datos.txt en modo escritura
    hora_inicio = datetime.now()  # contamos el tiempo de ejecucion a partir de este momento
    for programa in range(1, n + 1):  # for para la generacion de procesos a asignar por lotes
        programador = programadores[random.randint(0, 3)]  # asigna un programador aleatorio de los contenidos en el arreglo
        n1 = random.randint(1, 9)  # asigna un valor entre 1 y 9 a la variable n1 para su posterior procesamiento
        operacion = operadores[random.randint(0, 3)]  # asigna un operador aritmetico de los contenidos en el arreglo
        n2 = random.randint(1, 9)  # asigna un valor entre 1 y 9 a la variable n2 para su posterior procesamiento
        TME = random.randint(4, 13)  # asigna un tiempo de ejcucion a los procesos entre 4 y 13 segundos
        proc = proceso() #creamos un proceso
        proc.set(programa, programador, n1, operacion, n2, TME,int(programa/5+0.8)) #asignamos valores al proceso
        if programa % 5 == 1: #si el programa es el primero del lote
            lot = "Lote "+str(int(programa/5+0.8))+'\n' #imprimimos el numero del lote en consola y el archivo con esta cadena
            print(lot)
            f.write(lot)
        print(proc.toString()) #imprimimos los datos del proceso en la consola
        f.write(proc.toString()) #escribimos lo mismo en el archivo datos.txt
        lista.append(proc) #agregamos el proceso a la lista
    f.close() #cerramos el archivo
    programas = n #establecemos la cantidad de programas para su analisis

def obtener_resultados(): #funcion para la escritura de informacion en el archivo Resultados.txt
    f = open ('Resultados.txt', 'w') #abrimos el archivo
    f.write(txtTerminados.get(1.0,END)) #escribimos los resultados en el archivo
    f.close() #cerramos el archivo

def obtener_tiempo_transcurrido(): #esta funcion obtiene la cantidad de segundos transcurridos para convertirlos
    segundos_transcurridos= (datetime.now() - hora_inicio).total_seconds() # se usa la funcion anterior contando el tiempo desde la activacion del cronometro hasta el momento actual
    return int(segundos_transcurridos) #devuelve el tiempo resultante

def refrescar_tiempo_transcurrido(): #funcion central, para la actualizacion del reloj y el procesamiento de
    # los programas sin necesidad de hilos
    global op, pendientes, lista, programas #se llama a la variable global op
    if op==1 : #condicion con la variable global op
        print("Refrescando!")  # impresion de control, permite verificar que el programa hace uso de la funcion
        variable_hora_actual.set('Reloj General: '+str(obtener_tiempo_transcurrido())) #almacena el valor de los
        # segundos transcurridos
        lblRelojGeneral.config(text=variable_hora_actual.get()) #actualizacion del cronometro
        nLotes = int(((pendientes-1) / 5) + 0.2) #definimos la catidad de lotes pendientes en cada ejecucion basados
        # en los programas en espera
        lotesP = '# de Lotes pendientes: '+ str(nLotes) #imprimimos los lotes pendientes
        print(lotesP) #impresion de monitoreo
        lblNLotes.config(text=lotesP) #actualizamos la etiqueta
        if len(lista) > 0: #si la lista no esta vacia
            if len(lista) >=1: #si la lista tiene por lo menos un elemento
                if lista[0].tiempo >0: #y ese elemento aun no termina su TME
                    txtEjecucion.delete(1.0,END) #vaciamos la caja de texto
                    txtEjecucion.insert(1.0,lista[0].toString()) #la llenamos con el valor del proceso
                    lista[0].tiempo-=1 #disminuimos el TME
                elif lista[0].tiempo == 0: #si ya paso el TME
                    txtEjecucion.delete(1.0, END) #vaciamos la caja del programa en ejecucion
                    if len(lista) >=2: #si hay un programa en espera
                        txtEjecucion.insert(1.0, lista[1].toString()) #lo ponemos en la caja de ejecucion
                        lista[1].tiempo -= 1 #reducimos su primer segundo
                    if lista[0].nprog%5==1:
                        s = 'Lote '+ str(lista[0].nlot) +'\n'
                        txtTerminados.insert(END,s)
                    txtTerminados.insert(END,lista[0].toStringSolved()) #ponemos el proceso terminado en la caja
                    # correspondiente con su resultado
                    lista.remove(lista[0]) #eliminamos el primer elemento para que no este en la siguiente
                    # ejecucion
                    pendientes-=1 #lo quitamos de los programas pendientes
            if len(lista) >=2: #si has 2 o mas procesos en la lista (uno en ejecucion y uno pendiente)
                txtEspera.delete(1.0,END) #vaciamos la caja de espera
                txtEspera.insert(1.0,lista[1].toString()) #insertamos la informacion del proceso en espera
                if 5*lista[1].nlot <= programas: #si el lote presente no es el ultimo
                    txtEspera.insert(END, ((5*lista[1].nlot)-lista[1].nprog)) #obtenemos los procesos pendietes
                    # del lote
                else: #sino
                    txtEspera.insert(END, pendientes-2) #imprimimos los programas pendientes menos 2 (el
                    # ejecutado y el que espera)
                txtEspera.insert(END, " programas pendientes") #agregamos la etiqueta para hacerlo comprensible
            elif len(lista) <=1: #si la condicion anterior se cumplio y solo hay un programa en ejecucion
                txtEspera.delete(1.0, END) #vaciamos la caja de espera
                txtEspera.insert(1.0, "0 programas pendientes") #indicamos que no hay mas programas pendientes
        else:
            op = 0 #paramos el cronometro y toda la funcion
    root.after(INTERVALO_REFRESCO, refrescar_tiempo_transcurrido) #esta funcion se cicla para funcionar de nuevo
    # cada tiempo determinado, en este caso el valor de la variable intervalo


root= Tk()
root.title("Procesamineto pot lotes")#titulamos la ventana
root.geometry("850x450") #ingresamos las dimensiones que tendra la ventana

#declaracion de componentes
variable_hora_actual = StringVar(root, value='Reloj general: '+str(obtener_tiempo_transcurrido())) #le damos valor al cronometro, con esto llenaremos el valor del label cuando activemos la funcion
lblNProc = Label(root, text="# Procesos")
inpNProc = Entry(root, width=20, validate="key", validatecommand=(root.register(validate_entry), "%S"))
btnGenerar = Button(root, text="Generar", width=10, command= lambda: generar(int(inpNProc.get())))
lblRelojGeneral = Label(root, text='Reloj general: ')
lblEspera = Label(root, text="EN ESPERA")
txtEspera= Text(root, width=25, height=20)
lblEjecucion = Label(root, text="EN EJECUCION")
txtEjecucion= Text(root, width=25, height=10)
lblTerminados = Label(root, text="TERMINADOS")
txtTerminados= Text(root, width=25, height=20)
lblNLotes = Label(root, text="# de Lotes pendientes:")
btnResultados = Button(root, text="OBTENER RESULTADOS", command= lambda: obtener_resultados())

#colocacion de componentes
lblNProc.place(anchor=N, x=50, y=10)
inpNProc.place(anchor=N, x=150, y=10)
btnGenerar.place(anchor=N, x=265, y=7)
lblRelojGeneral.place(anchor=N, x=700, y=5)
lblEspera.place(anchor=N, x=150, y=50)
txtEspera.place(anchor=N, x=150, y=70)
lblEjecucion.place(anchor=N, x=420, y=90)
txtEjecucion.place(anchor=N, x=420, y=120)
lblTerminados.place(anchor=N, x=700, y=50)
txtTerminados.place(anchor=N, x=700, y=70)
lblNLotes.place(anchor=N, x=120, y=400)
btnResultados.place(anchor=N, x=700, y=410)
app = Frame() #declaramos un frame para el funcionamiento del cronometro
refrescar_tiempo_transcurrido() #esta linea activara el cronometro siempre y cuando op sea igual a 1
app.pack() #esta linea nos permitira actualizar la interfaz para visualizar los cambios del cronometro

root.mainloop()