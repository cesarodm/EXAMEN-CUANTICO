# menu.py

from repositorio import RepositorioDeEstados
from operador_cuantico import OperadorCuantico

class Menu:
    """
    Clase que gestiona el menú de interacción por consola con el usuario.
    Se encarga de mostrar opciones, leer entradas y ejecutar operaciones.
    """

    def __init__(self):
        # Instanciamos el repositorio y tratamos de cargar los datos
        self.repo = RepositorioDeEstados()
        self.archivo = "estados.json"
        self.repo.cargar(self.archivo)

        # Definimos algunos operadores estándar
        self.operadores = {
            "X": OperadorCuantico("X", [[0, 1], [1, 0]]),
            "H": OperadorCuantico("H", [[1/2**0.5, 1/2**0.5], [1/2**0.5, -1/2**0.5]])
        }

    def mostrar_menu(self):
        """
        Muestra las opciones disponibles.
        """
        print("\n--- MENÚ CUÁNTICO ---")
        print("1. Listar estados")
        print("2. Agregar nuevo estado")
        print("3. Aplicar operador a estado")
        print("4. Medir estado")
        print("5. Guardar estados")
        print("6. Cargar estados")
        print("0. Salir")

    def ejecutar(self):
        """
        Bucle principal de ejecución del menú.
        """
        while True:
            self.mostrar_menu()
            opcion = input("Elige una opción: ")

            if opcion == "1":
                for estado_str in self.repo.listar_estados():
                    print(estado_str)

            elif opcion == "2":
                id = input("ID del nuevo estado: ")
                base = input("Base (ej: computacional): ")
                vector_str = input("Vector de amplitudes (ej: 1,0): ")
                try:
                    vector = [complex(x.strip()) for x in vector_str.split(",")]
                    self.repo.agregar_estado(id, vector, base)
                except Exception as e:
                    print(f"[Error] Formato de vector inválido: {e}")

            elif opcion == "3":
                id_estado = input("ID del estado original: ")
                print("Operadores disponibles: ", list(self.operadores.keys()))
                nombre_op = input("Nombre del operador: ")
                nuevo_id = input("ID para el nuevo estado transformado: ")

                op = self.operadores.get(nombre_op)
                if op:
                    self.repo.aplicar_operador(id_estado, op, nuevo_id)
                else:
                    print(f"[Error] Operador '{nombre_op}' no reconocido.")

            elif opcion == "4":
                id = input("ID del estado a medir: ")
                self.repo.medir_estado(id)

            elif opcion == "5":
                self.repo.guardar(self.archivo)

            elif opcion == "6":
                self.repo.cargar(self.archivo)

            elif opcion == "0":
                print("Saliendo. ¡Hasta pronto!")
                break

            else:
                print("[Error] Opción inválida.")
