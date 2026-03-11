class Cola:
    """Implementación básica de una estructura de datos tipo Cola (Queue)."""
    def __init__(self):
        self.items = []

    def esta_vacia(self):
        return len(self.items) == 0

    def encolar(self, item):
        self.items.append(item)

    def desencolar(self):
        if not self.esta_vacia():
            return self.items.pop(0)
        return 0 # Retorna 0 si está vacía para no afectar la suma

    def __str__(self):
        return str(self.items)


def sumar_colas(cola_a, cola_b):
    """
    Recibe dos Colas de números enteros y devuelve una nueva Cola 
    con sus elementos sumados uno a uno.
    """
    cola_resultado = Cola()
    
    # Se ejecuta mientras al menos una de las colas tenga elementos
    while not cola_a.esta_vacia() or not cola_b.esta_vacia():
        # Desencolamos un elemento de cada cola. 
        # Si una cola ya está vacía, el método desencolar devolverá 0.
        valor_a = cola_a.desencolar()
        valor_b = cola_b.desencolar()
        
        # Sumamos y encolamos en el resultado
        suma = valor_a + valor_b
        cola_resultado.encolar(suma)
        
    return cola_resultado

# ==========================================
# Pruebas con el ejemplo de la imagen
# ==========================================

# 1. Crear e inicializar Cola A
cola_a = Cola()
for num in [3, 4, 2, 8, 12]:
    cola_a.encolar(num)

# 2. Crear e inicializar Cola B
cola_b = Cola()
for num in [6, 2, 9, 11, 3]:
    cola_b.encolar(num)

# 3. Llamar a la función
cola_resultado = sumar_colas(cola_a, cola_b)

# 4. Mostrar los resultados
print(f"Cola Resultado: {cola_resultado}")
# Salida esperada: [9, 6, 11, 19, 15]
