class Pila:
    """Clase personalizada para representar una estructura de datos de Pila (Stack)."""
    def __init__(self, nombre):
        self.items = []
        self.nombre = nombre

    def esta_vacia(self):
        return len(self.items) == 0

    def apilar(self, item):
        self.items.append(item)

    def desapilar(self):
        if not self.esta_vacia():
            return self.items.pop()
        raise IndexError(f"La pila {self.nombre} está vacía.")

    def cima(self):
        if not self.esta_vacia():
            return self.items[-1]
        return None

    def __str__(self):
        # Muestra la pila de abajo hacia arriba. El último elemento es la cima.
        return f"Torre {self.nombre}: {self.items}"


def imprimir_estado_juego(torre_a, torre_b, torre_c):
    """Función auxiliar para mostrar el estado de las 3 torres."""
    print(torre_a)
    print(torre_b)
    print(torre_c)
    print("-" * 30)


def resolver_hanoi(n, origen, auxiliar, destino, t_a, t_b, t_c):
    """
    Función recursiva para resolver las Torres de Hanói.
    
    n: cantidad de discos a mover en esta llamada.
    origen, auxiliar, destino: objetos Pila que cambian de rol según el paso.
    t_a, t_b, t_c: referencias constantes a las 3 pilas originales para imprimir el estado global.
    """
    if n == 1:
        # Caso base: Mover un solo disco directamente
        disco = origen.desapilar()
        destino.apilar(disco)
        print(f"-> Moviendo disco {disco} de {origen.nombre} a {destino.nombre}")
        imprimir_estado_juego(t_a, t_b, t_c)
        return

    # Paso 1: Mover n-1 discos del origen al poste auxiliar
    resolver_hanoi(n - 1, origen, destino, auxiliar, t_a, t_b, t_c)

    # Paso 2: Mover el disco más grande restante al poste destino
    disco = origen.desapilar()
    destino.apilar(disco)
    print(f"-> Moviendo disco {disco} de {origen.nombre} a {destino.nombre}")
    imprimir_estado_juego(t_a, t_b, t_c)

    # Paso 3: Mover los n-1 discos del poste auxiliar al poste destino
    resolver_hanoi(n - 1, auxiliar, origen, destino, t_a, t_b, t_c)


# ==========================================
# Ejecución del programa
# ==========================================
if __name__ == "__main__":
    # 1. Crear las 3 pilas (Torres)
    torre_a = Pila("A (Origen)")
    torre_b = Pila("B (Auxiliar)")
    torre_c = Pila("C (Destino)")

    # 2. Configurar el estado inicial para 3 discos
    # El disco 3 es el más grande (base), el 1 es el más pequeño (cima)
    # Apilamos en orden inverso para que el 1 quede arriba.
    torre_a.apilar(3)
    torre_a.apilar(2)
    torre_a.apilar(1)

    print("ESTADO INICIAL:")
    imprimir_estado_juego(torre_a, torre_b, torre_c)

    # 3. Resolver el juego
    print("INICIANDO RESOLUCIÓN...\n")
    resolver_hanoi(3, torre_a, torre_b, torre_c, torre_a, torre_b, torre_c)
    
    print("¡JUEGO COMPLETADO!")
    
