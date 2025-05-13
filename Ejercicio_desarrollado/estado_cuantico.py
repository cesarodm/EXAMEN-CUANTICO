# estado_cuantico.py

import math

class EstadoCuantico:
    """
    Clase que representa un estado cuántico individual.
    Un estado cuántico está definido por:
    - un identificador único (string),
    - un vector de amplitudes (lista de números complejos o reales),
    - una base (por ejemplo, 'computacional').
    """

    def __init__(self, id, vector, base):
        """
        Constructor del estado cuántico.
        Verifica que el vector no esté vacío y puede opcionalmente normalizarlo.
        """
        if not vector:
            raise ValueError("El vector de estado no puede estar vacío.")
        
        self.id = id
        self.vector = [complex(v) for v in vector]  # Asegura que todos los elementos sean complejos
        self.base = base

        if not self._esta_normalizado():
            print(f"[Aviso] El vector del estado '{id}' no está normalizado (norma ≠ 1).")

    def _esta_normalizado(self, tolerancia=1e-6):
        """
        Comprueba si la suma de los módulos al cuadrado de las amplitudes es ≈ 1.
        """
        norma_cuadrada = sum(abs(amplitud) ** 2 for amplitud in self.vector)
        return abs(norma_cuadrada - 1.0) <= tolerancia

    def medir(self):
        """
        Calcula las probabilidades de medir cada estado base.
        Devuelve una lista de probabilidades (floats) cuyo total debe ser ≈ 1.
        """
        probabilidades = [abs(amplitud)**2 for amplitud in self.vector]
        suma = sum(probabilidades)

        if suma == 0:
            raise ValueError(f"El estado '{self.id}' tiene norma cero, no se puede medir.")
        
        # Normalizamos por seguridad si la suma es cercana pero no exacta
        probabilidades_normalizadas = [p / suma for p in probabilidades]
        return probabilidades_normalizadas

    def __str__(self):
        """
        Representación legible del estado cuántico.
        """
        return f"{self.id}: vector={self.vector} en base {self.base}"

    def to_dict(self):
        """
        Convierte el estado a un diccionario serializable para guardar en JSON.
        Nota: Los números complejos se convierten a string para compatibilidad.
        """
        return {
            "id": self.id,
            "vector": [str(x) for x in self.vector],
            "base": self.base
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un EstadoCuantico desde un diccionario (cargado de JSON).
        Convierte los strings complejos de vuelta a tipo complex.
        """
        id = data["id"]
        base = data["base"]
        vector = [complex(s) for s in data["vector"]]
        return EstadoCuantico(id, vector, base)
