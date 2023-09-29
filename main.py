from tkinter import * #libreria para generacion de interfaces graficas
from datetime import datetime #libreria para tomar hora del sistema, necesaria para el cronometro
import random #libreria para generacion de numeros aleatorios

programas = 0 #numero de programas a procesar por lotes, se modifica posteriormente
programadores = ("José","Carlos","Carolina","Juan") #lista de los distintos programadores a asignar en los programas
operadores = ("+","-","*","/") #operaciones aritmeticas que se pueden realizar
hora_inicio = datetime.now() #declaracion del inicio del cronometro
INTERVALO_REFRESCO = 500 #tiempo para actualizar el cronometro
op = 0 #variable para la activacion del cronometro, cuando sea igual a 1 este iniciará

validate_entry = lambda text: text.isdecimal() #funcion de validacion para entrada de numeros unicamente

def generar(n): #funcion para generar los programas a procesar por lotes, genera n programas segun el parametro que reciba
    global programas, op, hora_inicio #variable globales que modifica la función
    op = 1 #cambiamos el valor de op para iniciar el cronometro
    f = open ('datos.txt', 'w') #abrimos el archivo datos.txt en modo escritura
    hora_inicio = datetime.now() #contamos el tiempo de ejecucion a partir de este momento
    for programa in range(1,n+1): #for para la generacion de procesos a asignar por lotes
        programador = programadores[random.randint(0,3)] #asigna un programador aleatorio de los contenidos en el arreglo
        n1 = random.randint(1,9) #asigna un valor entre 1 y 9 a la variable n1 para su posterior procesamiento
        operacion = operadores[random.randint(0,3)]#asigna un operador aritmetico de los contenidos en el arreglo
        n2 = random.randint(1,9) #asigna un valor entre 1 y 9 a la variable n2 para su posterior procesamiento
        TME = random.randint(4,13) #asigna un tiempo de ejcucion a los procesos entre 4 y 13 segundos
        if programa%5==1: #en caso de que el programa a escribirse en el archivo, sea el primero del lote:
            lot = "Lote "+str(int(programa/5+0.8))+ '\n' #asignamos el valor a una cadena para utilizarla en consola y escribirla en el archivo, posteriormente para añadirla al
            # cuadro de texto
            print(lot) #imprime en consola el lote actual
            f.write(lot) #añade al archivo el lote actual
        lin1 = '\t'+str(programa)+ '. ' + programador+ '\n' #asignamos valores a la cadena para imprimirlo y añadirlo al archivo
        print(lin1) #imprimimos
        f.write(lin1) #escribimos en el archivo
        lin2 = '\t'+str(n1) + str(operacion) + str(n2)+ '\n'#asignamos valores a la cadena para imprimirlo y añadirlo al archivo
        print(lin2) #imprimimos
        f.write(lin2) #escribimos en el archivo
        lin3 = '\tTME: ' + str(TME) + '\n\n'#asignamos valores a la cadena para imprimirlo y añadirlo al archivo
        print(lin3) #imprimimos
        f.write(lin3) #escribimos en el archivo
    f.close() #cerramos el archivo
    programas = n #cambiamos el valor de programas para sus usos posteriores




def obtener_tiempo_transcurrido(): #esta funcion obtiene la cantidad de segundos transcurridos para convertirlos
    segundos_transcurridos= (datetime.now() - hora_inicio).total_seconds() # se usa la funcion anterior contando el tiempo desde la activacion del cronometro hasta el momento actual
    print(segundos_transcurridos) #imprimimos el valor para visualizar el funcionamiento, esta linea no afecta el funcionamiento escencial de la funcion
    return int(segundos_transcurridos) #devuelve el tiempo resultante

def refrescar_tiempo_transcurrido(): #funcion para la actualizacion del reloj
    global op #se llama a la variable global op
    if op==1: #condicion con la variable global op
        #segundos_transcurridos = (datetime.now() - hora_inicio).total_seconds()
        print("Refrescando!")  # impresion de control, permite verificar que el programa hace uso de la funcion
        variable_hora_actual.set('Reloj general: '+str(obtener_tiempo_transcurrido())) #almacena el valor de los segundos transcurridos
        lblRelojGeneral.config(text=variable_hora_actual.get()) #modificamos el valor del cronometro en la interfaz grafica
        # set de numero de lotes
        nLotes = int((programas / 5) + 0.8) #calculamos la cantidad de lotes pendientes a procesar
        lotesP = '# de Lotes pendientes: ' + str(nLotes) #cargamos la cadena para su uso posterior
        print(lotesP) #imprimimos el valor en consola para visualizar el funcionamiento, linea no indispensable
        lblNLotes.config(text=lotesP) #cambiamos la cantidad en la interfaz

    root.after(INTERVALO_REFRESCO, refrescar_tiempo_transcurrido) #esta funcion se cicla para funcionar de nuevo cada tiempo determinado, en este caso el valor de la variable intervalo



root= Tk()
root.title("Procesamineto pot lotes")#titulamos la ventana
root.geometry("850x450") #ingresamos las dimensiones que tendra la ventana

#declaracion de componentes
variable_hora_actual = StringVar(root,value='Reloj general: '+str(obtener_tiempo_transcurrido())) #le damos valor al cronometro, con esto llenaremos el valor del label cuando
# activemos la funcion
#print("tiempo: ",variable_hora_actual)
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
btnResultados = Button(root, text="OBTENER RESULTADOS")

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
#generar()

root.mainloop()
