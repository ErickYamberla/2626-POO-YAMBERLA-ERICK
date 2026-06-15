# -*- coding: utf-8 -*-

class CuentaBancaria:
    """Representa una cuenta bancaria simple."""

    def __init__(self, titular, numero_cuenta, saldo_inicial=0.0):
        self.titular = titular
        self.numero_cuenta = numero_cuenta
        self.saldo = float(saldo_inicial)

    def depositar(self, cantidad):
        """Deposita dinero en la cuenta."""
        if cantidad <= 0:
            raise ValueError('La cantidad a depositar debe ser mayor que cero.')
        self.saldo += cantidad
        return self.saldo

    def retirar(self, cantidad):
        """Retira dinero de la cuenta si hay saldo suficiente."""
        if cantidad <= 0:
            raise ValueError('La cantidad a retirar debe ser mayor que cero.')
        if cantidad > self.saldo:
            raise ValueError('Saldo insuficiente para realizar el retiro.')
        self.saldo -= cantidad
        return self.saldo

    def mostrar_informacion(self):
        """Devuelve una representación legible de la cuenta."""
        return (
            f'Cuenta bancaria\n'
            f'Titular: {self.titular}\n'
            f'Número de cuenta: {self.numero_cuenta}\n'
            f'Saldo: ${self.saldo:.2f}'
        )


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


if __name__ == '__main__':
    main()
