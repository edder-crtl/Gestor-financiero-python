from datetime import datetime
import uuid
from models import TipoMovimiento
import os



def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_usuarioNuevo():
    print('bievenido a su gestor financiero, sin usuario existente, cree uno nuevo')

def mensaje_exito(accion):
    input(f'{accion}, ingrese enter para continuar')

def confirmaciones(accion):
    while True:
        decision=input(f'¿desea {accion} ? (s/n): ').upper()
        if decision== 'S':
            return True
        if decision=='N':
            return False
        else:
            print('opcion Invalida, intetelo nuevamente.')
            continue


def mensaje_salida():
    print('gracias por usar nuestro sistema, tega un feliz dia')


###manejo de fechas
def pedir_fecha():
    fecha_minima = datetime.strptime("2000-01-01", "%Y-%m-%d")

    while True:
        try:
            fecha_str = input("Ingrese la fecha en formato YYYY-MM-DD: ")
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")

            if fecha <= fecha_minima:
                print("La fecha debe ser posterior al 2000-01-01")
                continue

            return fecha

        except ValueError:
            print("Fecha inválida, ingrese una nueva")


def mostrar_fecha(fecha):
    print(f"año: {fecha.year} mes: {fecha.month} día: {fecha.day}")



### funciones relacionada con la cuenta
def nombre_usuario():
    while True:
        nombre=input('ingrese el nombre de usuario: ')
        if nombre.strip()=='':
            print('El nombre no puede estar vacio intentelo nuevamente')
            continue
        return nombre


def id_usuario():
    id=uuid.uuid4()
    return id

def saldo_inicial():
    while True:
        try:
            saldo_inicial=int(input('ingrese el saldo inicial de la cuenta: '))
            if saldo_inicial <=0 or saldo_inicial <=999 :
                print('debe ingresar un minimo de 1000')
                continue
            return saldo_inicial
        except ValueError:
            print('debe usar NUMEROS')
            continue

def enlistar_usuario(lista, nuevo):
    lista.append(nuevo)


###funciones ingresos


def llenado_tipo():
    while True:
        try:
            opcion=int(input("""ingrese el tipo de movimiento:
1. = INGRESO 
2. = RETIRO  
OPCION: """))
            if opcion ==1:
                return TipoMovimiento.INGRESO
            elif opcion==2:
                return TipoMovimiento.GASTO
            else: 
                print('Opcion invalida, intentelo nuevamente')
                continue
        except ValueError:
            print('Tipo invalido, intentelo nuevamente')
            continue




def llenado_cantidad():
    while True:
        try:
            cantidad = float(input('Ingrese la cantidad: '))
            if cantidad < 1000:
                print('La cantidad mínima es 1000')
                continue
            return cantidad
        except ValueError:
            print('Debe ingresar un número')

