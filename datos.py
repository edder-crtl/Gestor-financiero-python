# datos.py
import json
from models import Cuenta, Movimiento, TipoMovimiento
from datetime import datetime
import os

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def cuenta_to_dict(cuenta: Cuenta):
    """Convierte una cuenta a diccionario para JSON"""
    # Manejo seguro de UUID
    cuenta_id_str = str(cuenta.cuenta_id) if hasattr(cuenta.cuenta_id, 'hex') else cuenta.cuenta_id
    
    return {
        "usuario": cuenta.usuario,
        "cuenta_id": cuenta_id_str,
        "saldo_inicial": float(cuenta.saldo_inicial) if cuenta.saldo_inicial is not None else 0.0,
        "moneda": cuenta.moneda,
        "historial": [
            {
                "tipo_movimiento": m.tipo_movimiento.name,
                "cantidad": float(m.cantidad) if m.cantidad is not None else 0.0,
                "fecha": m.fecha.strftime(DATE_FORMAT) if hasattr(m.fecha, 'strftime') else datetime.now().strftime(DATE_FORMAT)
            } for m in cuenta.historial
        ]
    }

def dict_to_cuenta(data: dict):
    """Convierte un diccionario a objeto Cuenta"""
    try:
        cuenta_id = data["cuenta_id"]
        if isinstance(cuenta_id, str):
            try:
                from uuid import UUID
                cuenta_id = UUID(cuenta_id)
            except (ValueError, ImportError):
                pass
        
        cuenta = Cuenta(
            usuario=str(data["usuario"]),
            cuenta_id=cuenta_id,
            saldo_inicial=float(data["saldo_inicial"]) if data.get("saldo_inicial") is not None else 0.0,
            moneda=str(data.get("moneda", "COP"))
        )
        
        historial_data = data.get("historial", [])
        for m_data in historial_data:
            try:
                tipo_str = m_data.get("tipo_movimiento", "INGRESO")
                try:
                    tipo_mov = TipoMovimiento[tipo_str]
                except KeyError:
                    tipo_mov = TipoMovimiento.INGRESO if tipo_str.upper() == "INGRESO" else TipoMovimiento.GASTO
                
                cantidad = float(m_data.get("cantidad", 0.0))
                
                fecha_str = m_data.get("fecha", "")
                if fecha_str:
                    try:
                        fecha = datetime.strptime(fecha_str, DATE_FORMAT)
                    except ValueError:
                        fecha = datetime.now()
                else:
                    fecha = datetime.now()
                
                # Crear el movimiento
                movimiento = Movimiento(tipo_mov, cantidad, fecha)
                cuenta.enlistar_movimientos(movimiento)
                
            except Exception as e:
                print(f"Advertencia: Error al cargar movimiento - {e}")
                continue
                
        return cuenta
        
    except Exception as e:
        print(f"Error crítico al convertir diccionario a cuenta: {e}")
        from uuid import uuid4
        return Cuenta("Usuario por defecto", uuid4(), 0.0, "COP")

def guardar_usuarios(lista_cuentas, filename="usuarios.json"):
    """
    Guarda la lista de cuentas en un archivo JSON
    
    Args:
        lista_cuentas: Puede ser una lista de Cuentas o una sola Cuenta
        filename: Nombre del archivo para guardar
    """
    try:
        if not isinstance(lista_cuentas, list):
            lista_cuentas = [lista_cuentas]
        
        data = []
        for cuenta in lista_cuentas:
            try:
                data.append(cuenta_to_dict(cuenta))
            except Exception as e:
                print(f"Error al convertir cuenta {cuenta.usuario}: {e}")
                continue
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f" Datos guardados exitosamente en '{filename}'")
        return True
        
    except Exception as e:
        print(f" Error al guardar datos: {e}")
        return False

def cargar_usuarios(filename="usuarios.json"):
    """
    Carga la lista de cuentas desde un archivo JSON
    
    Args:
        filename: Nombre del archivo a cargar
        
    Returns:
        Lista de objetos Cuenta, o lista vacía si hay error
    """
    try:
        if not os.path.exists(filename):
            print(f" Archivo '{filename}' no encontrado. Se creará uno nuevo al guardar.")
            return []
        
        if os.path.getsize(filename) == 0:
            print(f" Archivo '{filename}' está vacío.")
            return []
        
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cuentas = []
        for cuenta_data in data:
            try:
                cuenta = dict_to_cuenta(cuenta_data)
                cuentas.append(cuenta)
            except Exception as e:
                print(f"Error al cargar cuenta: {e}")
                continue
        
        print(f" Datos cargados exitosamente desde '{filename}'")
        print(f"  Cuentas cargadas: {len(cuentas)}")
        
        return cuentas
        
    except json.JSONDecodeError as e:
        print(f" Error: Archivo '{filename}' no tiene formato JSON válido")
        print(f"  Detalle: {e}")
        return []
    except Exception as e:
        print(f" Error inesperado al cargar datos: {e}")
        return []