"""
Modulo: mascota

Contiene la definición de la clase Mascota. Esta clase modela una mascota
con atributos simples y métodos para mostrar su información y emitir un sonido.

Se usan comentarios en español para apoyar el aprendizaje de programación orientada a objetos.
"""

class Mascota:
    """Clase que representa una mascota.

    Atributos:
        nombre (str): nombre de la mascota
        especie (str): tipo de animal (por ejemplo: perro, gato)
        edad (int): edad en años

    Métodos:
        mostrar_informacion(): imprime los atributos de la mascota de forma organizada
        hacer_sonido(): imprime un sonido representativo según la especie
    """

    def __init__(self, nombre, especie, edad):
        # El constructor inicializa los atributos del objeto
        self.nombre = nombre
        self.especie = especie
        self.edad = edad

    def mostrar_informacion(self):
        """Muestra la información de la mascota en un formato legible.

        Este método accede a los atributos del objeto (self) y los imprime.
        """
        print("\n" + "-" * 40)
        print(f"Nombre : {self.nombre}")
        print(f"Especie: {self.especie}")
        print(f"Edad   : {self.edad} años")
        print("-" * 40)

    def hacer_sonido(self):
        """Hace que la mascota 'emita' un sonido representativo según su especie.

        Aquí usamos una lógica simple: para especies conocidas (perro/gato)
        imprimimos un onomatopeya típica; para otras especies, mostramos un
        mensaje genérico. Esto demuestra polimorfismo simple mediante
        condicionales (no estamos usando herencia en este ejemplo básico).
        """
        especie_minus = self.especie.strip().lower()
        if especie_minus == "perro":
            sonido = "Guau guau!"
        elif especie_minus == "gato":
            sonido = "Miau"
        elif especie_minus == "pajaro" or especie_minus == "ave":
            sonido = "Pío pío"
        else:
            sonido = "(sonido desconocido)"

        print(f"{self.nombre} dice: {sonido}")

