# Explicación del código de `TAREA-SEMANA-2.py`

Este archivo explica cada parte del programa en Python usando programación orientada a objetos (POO). Está escrito pensando en quien está aprendiendo.

## 1. ¿Qué es una clase?

Una clase es una plantilla o molde para crear objetos. Un objeto representa una cosa del mundo real con propiedades y comportamientos.

En este caso, la clase es:

```python
class CuentaBancaria:
    """Representa una cuenta bancaria simple."""
```

Esto define el tipo `CuentaBancaria` que describe cómo es una cuenta bancaria.

## 2. El constructor `__init__`

Dentro de la clase, `__init__` es una función especial que se ejecuta cuando creamos un nuevo objeto.

```python
    def __init__(self, titular, numero_cuenta, saldo_inicial=0.0):
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.saldo = float(saldo_inicial)
```

- `self` es una referencia al objeto que se está creando.
- `titular`, `numero_cuenta` y `saldo_inicial` son los datos que definimos para cada cuenta.
- `self.titular`, `self.numero_cuenta` y `self.saldo` son atributos del objeto.

## 3. Métodos: acciones del objeto

Los métodos son funciones dentro de la clase. Representan lo que el objeto puede hacer.

### 3.1 `depositar`

```python
    def depositar(self, cantidad):
        """Deposita dinero en la cuenta."""
        if cantidad <= 0:
            raise ValueError('La cantidad a depositar debe ser mayor que cero.')
        self.saldo += cantidad
        return self.saldo
```

- Recibe `cantidad` y la suma al saldo.
- Verifica que no se intente depositar un valor cero o negativo.
- Retorna el saldo nuevo.

### 3.2 `retirar`

```python
    def retirar(self, cantidad):
        """Retira dinero de la cuenta si hay saldo suficiente."""
        if cantidad <= 0:
            raise ValueError('La cantidad a retirar debe ser mayor que cero.')
        if cantidad > self.saldo:
            raise ValueError('Saldo insuficiente para realizar el retiro.')
        self.saldo -= cantidad
        return self.saldo
```

- Resta la `cantidad` del saldo.
- Verifica que la cantidad sea positiva.
- Verifica que haya suficiente dinero antes de retirar.

### 3.3 `mostrar_informacion`

```python
    def mostrar_informacion(self):
        """Devuelve una representación legible de la cuenta."""
        return (
            f'Cuenta bancaria\n'
            f'Titular: {self.titular}\n'
            f'Número de cuenta: {self.numero_cuenta}\n'
            f'Saldo: ${self.saldo:.2f}'
        )
```

- Este método no cambia nada en el objeto.
- Devuelve un texto con los detalles de la cuenta.
- Usamos `f'...'` para incluir los valores de los atributos en el texto.

## 4. La función `main()`

```python
def main():
    cuenta = CuentaBancaria('Erick Yamberla', '1234567890', saldo_inicial=1500.0)

    print('Información inicial de la cuenta:')
    print(cuenta.mostrar_informacion())
    print('\nRealizando operaciones...')

    cuenta.depositar(500.0)
    print('\nDespués de depositar $500:')
    print(cuenta.mostrar_informacion())

    cuenta.retirar(300.0)
    print('\nDespués de retirar $300:')
    print(cuenta.mostrar_informacion())
```

- `main()` es el lugar donde usamos la clase.
- Creamos un objeto `cuenta` con datos iniciales.
- Llamamos a los métodos `depositar`, `retirar` y `mostrar_informacion`.
- Imprimimos resultados para ver cómo cambia el saldo.

## 5. `if __name__ == '__main__':`

```python
if __name__ == '__main__':
    main()
```

- Esto hace que `main()` se ejecute solo si el archivo se ejecuta directamente.
- Si el archivo se importa desde otro programa, no se ejecutará automáticamente.

## 6. Conceptos básicos de POO en este ejemplo

- Objeto: la cuenta bancaria creada con `CuentaBancaria(...)`.
- Clase: el plano `CuentaBancaria` que define cómo es una cuenta.
- Atributos: `titular`, `numero_cuenta`, `saldo`.
- Métodos: `depositar`, `retirar`, `mostrar_informacion`.

## 7. Resumen

Este programa muestra cómo representar un objeto real (una cuenta bancaria) en Python usando POO. La clase contiene los datos de la cuenta y las acciones que se pueden hacer con ella.
