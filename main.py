from models import Cuenta, Movimiento, TipoMovimiento
from utils import mensaje_exito, menu_usuarioNuevo, confirmaciones , nombre_usuario, id_usuario, saldo_inicial, enlistar_usuario, mensaje_salida, llenado_tipo, llenado_cantidad, pedir_fecha, limpiar_pantalla
from datos import guardar_usuarios, cargar_usuarios



def menu_inicial():
    while True:
        try:
            print('''Bienvenido a su gestor financiero, que desea hacer el dia de hoy 
            1.Ver estado de cuenta
            2.Registrar movimiento
            3.Mostrar todos los movimientos ''')
            opcion=int(input('ingrese su opcion, debe ser un NUMERO: '))
            if opcion >= 4 or opcion<=0:
                print('opcion fuera del menu')
                continue
            return opcion
        except ValueError:
            print('tipo de dato erroneo, por favor use un numero')
            continue



def main():
    usuarios = cargar_usuarios()
    if not usuarios:
        menu_usuarioNuevo()
        nombre=nombre_usuario()
        id=id_usuario()
        saldo_inicia=saldo_inicial()
        moneda='cop'##Crear sistema de moneda despues

        nuevo = Cuenta(nombre,id,saldo_inicia,moneda)
        enlistar_usuario(usuarios, nuevo)
        mensaje_exito(accion='creado con exito')
        guardar_usuarios(nuevo)
        limpiar_pantalla()

        if confirmaciones(accion='ver la cuenta nueva'):
            nuevo.mostrar_cuenta()
            mensaje_exito(accion='Mostrado con exito')
            limpiar_pantalla()

    while True:
        Cuenta.calcular_saldo(usuarios[0])
        opcion=menu_inicial()

        if opcion==1:
            Cuenta.mostrar_cuenta(usuarios[0])
            if confirmaciones(accion='continuar'):
                limpiar_pantalla()
                continue
            mensaje_salida()
            if confirmaciones(accion='¿ continuar en el menu?'):
                continue
            break


        elif opcion==2:
            tipo=llenado_tipo()
            if not confirmaciones(accion=f'Crear un nuevo movimiento de tipo {tipo.name}'):
                continue
            cantidad=llenado_cantidad()
            if tipo==TipoMovimiento.GASTO:
                saldo_actual=usuarios[0].calcular_saldo()
                if cantidad>saldo_actual:
                    print('Fondos insuficientes para realizar este gasto')
                    if confirmaciones(accion='intentar de nuevo'):
                        limpiar_pantalla()
                        continue
                    else:
                        break
            fecha=pedir_fecha()
            nuevo_movimiento=Movimiento(tipo, cantidad, fecha)
            usuarios[0].enlistar_movimientos(nuevo_movimiento)
            guardar_usuarios(usuarios)
            limpiar_pantalla()
            if confirmaciones(accion='ver el movimiento'):
                while True:
                    limpiar_pantalla()
                    usuarios[0].mostrar_movimiento(nuevo_movimiento)
                    if confirmaciones(accion='Dejar de ver el movimiento'):
                        break
            continue


        elif opcion==3:
            usuarios[0].mostrar_movimientosTodos()
            if confirmaciones(accion='continuar'):
                limpiar_pantalla()
                continue



if __name__=='__main__':
    main()









