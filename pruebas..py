from models import Cuenta, Movimiento, TipoMovimiento
from datetime import datetime

def main():
    cuenta2= Cuenta ("ALEX","0101", 23332,"US")
    cuenta = Cuenta ("Edder", "001", 100000, "COP")
    Lista_usuarios=[cuenta, cuenta2]

    ingreso = Movimiento(TipoMovimiento.INGRESO, 20000, datetime.now())
    gasto = Movimiento(TipoMovimiento.GASTO, -5000, datetime.now())

    cuenta.enlistar_movimientos(ingreso)
    cuenta.enlistar_movimientos(gasto)
    Lista_usuarios[0].mostrar_cuenta()
    Lista_usuarios[1].mostrar_cuenta()


    Lista_usuarios[0].mostrar_movimientosTodos()
    Lista_usuarios[1].mostrar_movimiento

if __name__ == "__main__":
    main()

