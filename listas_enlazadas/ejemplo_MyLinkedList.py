# ejemplo_uso.py
# Asegúrate de tener MyLinkedList.py en el mismo directorio

from MyLinkedList import MyLinkedList

# -------------------------------------------------------
# 1. Crear una lista e insertar elementos
# -------------------------------------------------------
lista = MyLinkedList()

lista.append(10)
lista.append(20)
lista.append(30)
lista.prepend(5)       # Agrega al inicio

print("Lista inicial:")
print(lista)           # 5 -> 10 -> 20 -> 30 -> NULL

# -------------------------------------------------------
# 2. Insertar en posición específica
# -------------------------------------------------------
lista.insert(2, 99)    # Inserta 99 en el índice 2

print("\nDespués de insert(2, 99):")
print(lista)           # 5 -> 10 -> 99 -> 20 -> 30 -> NULL

# -------------------------------------------------------
# 3. Buscar y acceder a elementos
# -------------------------------------------------------
idx = lista.search(99)
print(f"\nÍndice de 99: {idx}")          # 2

valor = lista.get(0)
print(f"Primer elemento: {valor}")       # 5

print(f"¿Contiene 20?: {20 in lista}")  # True
print(f"¿Contiene 77?: {77 in lista}")  # False

# -------------------------------------------------------
# 4. Eliminar elementos
# -------------------------------------------------------
lista.delete(99)        # Elimina por valor
lista.delete_at(0)      # Elimina por índice (el 5)

print("\nDespués de eliminar 99 y el índice 0:")
print(lista)            # 10 -> 20 -> 30 -> NULL

# -------------------------------------------------------
# 5. Invertir la lista
# -------------------------------------------------------
lista.reverse()

print("\nDespués de reverse():")
print(lista)            # 30 -> 20 -> 10 -> NULL

# -------------------------------------------------------
# 6. Iterar con un for
# -------------------------------------------------------
print("\nIterando con for:")
for valor in lista:
    print(f"  → {valor}")

# -------------------------------------------------------
# 7. Convertir a lista de Python
# -------------------------------------------------------
python_list = lista.to_list()
print(f"\nComo lista Python: {python_list}")

# -------------------------------------------------------
# 8. Longitud y estado
# -------------------------------------------------------
print(f"Longitud: {len(lista)}")
print(f"¿Está vacía?: {lista.is_empty()}")

# -------------------------------------------------------
# 9. Inicializar directamente desde un iterable
# -------------------------------------------------------
lista2 = MyLinkedList([100, 200, 300])
print(f"\nLista2 desde iterable: {lista2}")

# -------------------------------------------------------
# 10. Limpiar la lista
# -------------------------------------------------------
lista2.clear()
print(f"Lista2 después de clear(): {lista2}")
print(f"¿Está vacía?: {lista2.is_empty()}")
