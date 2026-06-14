"""
Archivo principal para demostrar el uso de la clase Mascota.

Este script crea al menos dos objetos de la clase Mascota, llama a sus
métodos y muestra por pantalla la información y los sonidos.
"""

from mascota import Mascota


def main():
    # Creamos al menos dos objetos (instancias) de la clase Mascota
    mascota1 = Mascota("Firulais", "Perro", 4)
    mascota2 = Mascota("Misu", "Gato", 2)

    # Podemos crear más objetos si lo deseamos
    mascota3 = Mascota("Tweety", "Pajaro", 1)

    # Ejecutamos los métodos definidos en la clase para cada objeto
    mascotas = [mascota1, mascota2, mascota3]
    for m in mascotas:
        # mostrar_informacion() es un método que imprime los atributos
        m.mostrar_informacion()
        # hacer_sonido() demuestra comportamiento asociado a la instancia
        m.hacer_sonido()


if __name__ == "__main__":
    main()

