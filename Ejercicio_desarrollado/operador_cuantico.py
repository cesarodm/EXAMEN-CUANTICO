# operador_cuantico.py

import numpy as np
from estado_cuantico import EstadoCuantico

class OperadorCuantico:
    """
    Clase que representa un operador cuántico (puerta unitaria).
    Se define por:
    - un nombre identificador (como 'X', 'H', 'Z')
    - una matriz cuadrada (2x2, 4x4, etc.), representada con numpy.
    """

    def __init__(self, nombre, matriz):
        """
        Inicializa el operador con un nombre y una matriz.
        La matriz debe ser cuadrada.
        """
        self.nombre = nombre
        self.matriz = np.array(matriz, dtype=complex)

        if self.matriz.shape[0] != self.matriz.shape[1]:
            raise ValueError("La matriz del operador cuántico debe ser cuadrada.")

    def aplicar(self, estado):
        """
        Aplica este operador a un estado cuántico.
        Realiza la multiplicación matriz * vector.
        Devuelve un nuevo objeto EstadoCuantico con el vector transformado.
        """
        if len(estado.vector) != self.matriz.shape[1]:
            raise ValueError(f"La dimensión del operador '{self.nombre}' no coincide con la del estado '{estado.id}'.")

        # Convertimos el vector de amplitudes a un array numpy
        vector = np.array(estado.vector, dtype=complex)
        resultado = self.matriz @ vector  # Producto matricial

        # Creamos nuevo estado con nuevo vector, manteniendo la base
        nuevo_id = f"{estado.id}_{self.nombre}"
        return EstadoCuantico(nuevo_id, list(resultado), estado.base)

    def __str__(self):
        """
        Representación legible del operador cuántico.
        """
        return f"Operador '{self.nombre}':\n{self.matriz}"
