from enum import Enum
from datetime import datetime


class TipoMovimiento(Enum):
    INGRESO = 1
    GASTO = 2     




class Movimiento:
    def __init__(self,  tipo_movimiento: TipoMovimiento, cantidad: float, fecha: datetime):
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad if tipo_movimiento == TipoMovimiento.INGRESO else -cantidad
        self.fecha= fecha  




class Cuenta:
    def __init__(self, usuario: str, cuenta_id: int, saldo_inicial: float , moneda: str):
        self.usuario = usuario
        self.cuenta_id = cuenta_id
        self.saldo_inicial = saldo_inicial
        self.moneda = moneda
        self.historial = []


    def mostrar_cuenta(self):
        saldo=self.calcular_saldo()
        print(f'Titular de la cuenta: {self.usuario}\n'
        f'Id de la cuenta: {self.cuenta_id}\n')
        print(f'Saldo de la cuenta: {saldo}{self.moneda}')

    def enlistar_movimientos(self, movimiento : Movimiento ):
        self.historial.append(movimiento)


    def calcular_saldo(self):
        try:
            saldo = float(self.saldo_inicial)
        except (ValueError, TypeError):
            saldo = 0.0
        
        for m in self.historial:
            try:
                cantidad_valor = float(m.cantidad)
                saldo += cantidad_valor
            except (ValueError, TypeError):
                continue  
        
        return saldo


    def mostrar_movimiento(self , Movimiento:Movimiento):
        print(f'El tipo de movimiento es: {Movimiento.tipo_movimiento.name} \n'
        f'Cantidad: {Movimiento.cantidad}\n'
        f'fecha: {Movimiento.fecha.year} Mes: {Movimiento.fecha.month} dia: {Movimiento.fecha.day}\n')

    def mostrar_movimientosTodos(self):
        print('lista de movimientos: \n ')
        for m in self.historial:
            print(f'Tipo de movimiento: {m.tipo_movimiento.name} \n' 
f'Cantidad: {m.cantidad} \n'
f'fecha: {m.fecha.year} Mes: {m.fecha.month} dia: {m.fecha.day} \n')











