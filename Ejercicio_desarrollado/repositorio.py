# repositorio.py

import json
from estado_cuantico import EstadoCuantico
from operador_cuantico import OperadorCuantico

class RepositorioDeEstados:
    """
    Clase que gestiona todos los estados cuánticos del sistema.
    Permite agregarlos, listarlos, medirlos, transformarlos y guardar/cargar a archivo.
    """

    def __init__(self):
        # Diccionario con clave = id del estado, valor = objeto EstadoCuantico
        self.estados = {}

    def agregar_estado(self, id, vector, base):
        """
        Crea y registra un nuevo estado cuántico.
        Evita duplicados por ID.
        """
        if id in self.estados:
            print(f"[Error] Ya existe un estado con identificador '{id}'.")
            return False

        estado = EstadoCuantico(id, vector, base)
        self.estados[id] = estado
        return True

    def listar_estados(self):
        """
        Devuelve una lista con la representación string de todos los estados registrados.
        """
        if not self.estados:
            return ["[Info] No hay estados registrados."]
        return [str(estado) for estado in self.estados.values()]

    def obtener_estado(self, id):
        """
        Devuelve el estado con el ID dado, o None si no existe.
        """
        return self.estados.get(id, None)

    def aplicar_operador(self, id_estado, operador, nuevo_id=None):
        """
        Aplica un operador cuántico al estado con id_estado.
        Registra el nuevo estado con nuevo_id, o uno generado automáticamente.
        """
        estado_original = self.obtener_estado(id_estado)
        if not estado_original:
            print(f"[Error] No existe el estado '{id_estado}'.")
            return False

        estado_transformado = operador.aplicar(estado_original)

        # Si no se especifica nuevo_id, usamos el que viene con el estado transformado
        estado_transformado.id = nuevo_id or estado_transformado.id

        if estado_transformado.id in self.estados:
            print(f"[Error] Ya existe un estado con ID '{estado_transformado.id}'. No se puede sobrescribir.")
            return False

        self.estados[estado_transformado.id] = estado_transformado
        return True

    def medir_estado(self, id):
        """
        Mide el estado cuántico indicado y devuelve sus probabilidades.
        """
        estado = self.obtener_estado(id)
        if not estado:
            print(f"[Error] No existe el estado '{id}' para medir.")
            return None

        probabilidades = estado.medir()
        print(f"Medición del estado '{id}' en base '{estado.base}':")
        for i, p in enumerate(probabilidades):
            porcentaje = round(p * 100, 2)
            print(f" - Estado base {i}: {porcentaje}%")
        return probabilidades

    def guardar(self, archivo):
        """
        Guarda todos los estados actuales en un archivo JSON.
        """
        try:
            with open(archivo, "w") as f:
                datos = [estado.to_dict() for estado in self.estados.values()]
                json.dump(datos, f, indent=4)
            print(f"[OK] Estados guardados en '{archivo}'.")
        except Exception as e:
            print(f"[Error] No se pudo guardar en '{archivo}': {e}")

    def cargar(self, archivo):
        """
        Carga estados desde un archivo JSON.
        Reemplaza completamente el conjunto actual de estados.
        """
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                self.estados = {}
                for item in datos:
                    estado = EstadoCuantico.from_dict(item)
                    self.estados[estado.id] = estado
            print(f"[OK] Se cargaron {len(self.estados)} estados desde '{archivo}'.")
        except FileNotFoundError:
            print(f"[Aviso] El archivo '{archivo}' no existe. Se inicia sin estados.")
        except Exception as e:
            print(f"[Error] No se pudo cargar desde '{archivo}': {e}")
