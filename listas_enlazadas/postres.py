# ============================================================
#  POSTRES - Arreglo + Listas Enlazadas de Ingredientes
#  Estructura: arreglo ordenado alfabéticamente;
#              cada celda apunta a una lista enlazada de ingredientes.
# ============================================================

# --- Nodo de ingrediente (lista enlazada) -------------------
class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None   # NIL cuando no hay más

# --- Nodo del arreglo de postres ----------------------------
class NodoPostre:
    def __init__(self, nombre):
        self.nombre = nombre            # clave del arreglo
        self.ingredientes = None        # cabeza de la lista enlazada (NIL = None)

# --- Arreglo de postres (lista de NodoPostre, orden A-Z) ----
POSTRES = []   # simula el arreglo mostrado en la imagen


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def buscar_postre(nombre):
    """Devuelve el NodoPostre si existe, None si no."""
    nombre = nombre.strip().lower()
    for nodo in POSTRES:
        if nodo.nombre.lower() == nombre:
            return nodo
    return None


def insertar_postre_ordenado(nodo):
    """Inserta un NodoPostre manteniendo el orden alfabético."""
    POSTRES.append(nodo)
    POSTRES.sort(key=lambda n: n.nombre.lower())


# ============================================================
# a) IMPRIMIR INGREDIENTES DE UN POSTRE
# ============================================================

def imprimir_ingredientes(nombre_postre):
    nodo = buscar_postre(nombre_postre)
    if nodo is None:
        print(f"[ERROR] El postre '{nombre_postre}' no existe en POSTRES.")
        return

    print(f"\n  Ingredientes de '{nodo.nombre}':")
    actual = nodo.ingredientes          # empieza en la cabeza
    if actual is None:
        print("    (sin ingredientes)")
        return
    while actual is not None:          # recorre hasta NIL
        print(f"    - {actual.nombre}")
        actual = actual.siguiente


# ============================================================
# b) INSERTAR NUEVO INGREDIENTE A UN POSTRE
# ============================================================

def insertar_ingrediente(nombre_postre, nuevo_ingrediente):
    nodo = buscar_postre(nombre_postre)
    if nodo is None:
        print(f"[ERROR] El postre '{nombre_postre}' no existe en POSTRES.")
        return

    nuevo_ingrediente = nuevo_ingrediente.strip()

    # Verificar duplicado
    actual = nodo.ingredientes
    while actual is not None:
        if actual.nombre.lower() == nuevo_ingrediente.lower():
            print(f"[AVISO] '{nuevo_ingrediente}' ya está en la lista de '{nodo.nombre}'.")
            return
        actual = actual.siguiente

    # Insertar al final de la lista
    nuevo_nodo = NodoIngrediente(nuevo_ingrediente)
    if nodo.ingredientes is None:
        nodo.ingredientes = nuevo_nodo
    else:
        actual = nodo.ingredientes
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo

    print(f"[OK] Ingrediente '{nuevo_ingrediente}' agregado a '{nodo.nombre}'.")


# ============================================================
# c) ELIMINAR UN INGREDIENTE DE UN POSTRE
# ============================================================

def eliminar_ingrediente(nombre_postre, ingrediente_a_eliminar):
    nodo = buscar_postre(nombre_postre)
    if nodo is None:
        print(f"[ERROR] El postre '{nombre_postre}' no existe en POSTRES.")
        return

    ingrediente_a_eliminar = ingrediente_a_eliminar.strip().lower()
    actual = nodo.ingredientes
    anterior = None

    while actual is not None:
        if actual.nombre.lower() == ingrediente_a_eliminar:
            if anterior is None:            # es la cabeza
                nodo.ingredientes = actual.siguiente
            else:
                anterior.siguiente = actual.siguiente
            actual.siguiente = None         # desconectar (NIL)
            print(f"[OK] Ingrediente '{actual.nombre}' eliminado de '{nodo.nombre}'.")
            return
        anterior = actual
        actual = actual.siguiente

    print(f"[ERROR] El ingrediente '{ingrediente_a_eliminar}' no existe en '{nodo.nombre}'.")


# ============================================================
# d) DAR DE ALTA UN POSTRE CON SUS INGREDIENTES
# ============================================================

def alta_postre(nombre_postre, lista_ingredientes):
    nombre_postre = nombre_postre.strip()
    if buscar_postre(nombre_postre) is not None:
        print(f"[AVISO] El postre '{nombre_postre}' ya existe en POSTRES.")
        return

    nuevo_postre = NodoPostre(nombre_postre)
    insertar_postre_ordenado(nuevo_postre)  # insertar en orden A-Z

    for ing in lista_ingredientes:
        insertar_ingrediente(nombre_postre, ing)

    print(f"[OK] Postre '{nombre_postre}' dado de alta con {len(lista_ingredientes)} ingrediente(s).")


# ============================================================
# e) DAR DE BAJA UN POSTRE (elimina postre + toda su lista)
# ============================================================

def baja_postre(nombre_postre):
    nodo = buscar_postre(nombre_postre)
    if nodo is None:
        print(f"[ERROR] El postre '{nombre_postre}' no existe en POSTRES.")
        return

    # Liberar nodos de ingredientes (poner NIL en cada enlace)
    actual = nodo.ingredientes
    while actual is not None:
        siguiente = actual.siguiente
        actual.siguiente = None     # NIL explícito
        actual = siguiente
    nodo.ingredientes = None        # cabeza = NIL

    POSTRES.remove(nodo)
    print(f"[OK] Postre '{nodo.nombre}' dado de baja junto con todos sus ingredientes.")


# ============================================================
# MENÚ INTERACTIVO
# ============================================================

def mostrar_todos():
    if not POSTRES:
        print("  (POSTRES vacío)")
        return
    for i, nodo in enumerate(POSTRES):
        print(f"  [{i}] {nodo.nombre}")


def menu():
    # Datos de ejemplo para comenzar
    alta_postre("Flan",      ["Leche", "Huevos", "Azúcar", "Vainilla"])
    alta_postre("Brownie",   ["Chocolate", "Mantequilla", "Harina", "Huevos", "Azúcar"])
    alta_postre("Cheesecake",["Queso crema", "Galletas", "Mantequilla", "Azúcar"])

    while True:
        print("\n" + "="*50)
        print("         SISTEMA DE POSTRES")
        print("="*50)
        print("  a) Imprimir ingredientes de un postre")
        print("  b) Insertar ingrediente")
        print("  c) Eliminar ingrediente")
        print("  d) Dar de alta un postre")
        print("  e) Dar de baja un postre")
        print("  f) Mostrar todos los postres")
        print("  s) Salir")
        print("="*50)
        opcion = input("  Opción: ").strip().lower()

        if opcion == 'a':
            mostrar_todos()
            p = input("  Nombre del postre: ")
            imprimir_ingredientes(p)

        elif opcion == 'b':
            mostrar_todos()
            p = input("  Nombre del postre: ")
            i = input("  Nuevo ingrediente: ")
            insertar_ingrediente(p, i)

        elif opcion == 'c':
            mostrar_todos()
            p = input("  Nombre del postre: ")
            imprimir_ingredientes(p)
            i = input("  Ingrediente a eliminar: ")
            eliminar_ingrediente(p, i)

        elif opcion == 'd':
            p = input("  Nombre del nuevo postre: ")
            ings = input("  Ingredientes (separados por coma): ").split(",")
            alta_postre(p, [x.strip() for x in ings if x.strip()])

        elif opcion == 'e':
            mostrar_todos()
            p = input("  Nombre del postre a dar de baja: ")
            baja_postre(p)

        elif opcion == 'f':
            print("\n  --- Todos los postres ---")
            mostrar_todos()

        elif opcion == 's':
            print("  Hasta luego.")
            break
        else:
            print("  [AVISO] Opción no válida.")


if __name__ == "__main__":
    menu()
