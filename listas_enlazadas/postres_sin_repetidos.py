# ============================================================
#  PROGRAMA 2 – Eliminar postres repetidos de POSTRES
#
#  ¿Qué sucede con las listas de ingredientes?
#  Cuando dos entradas del arreglo tienen el MISMO nombre de postre,
#  sus listas enlazadas son independientes (distintas cabezas).
#  Al eliminar el duplicado, SU lista también se pierde (se borra).
#  El programa detecta esto, avisa al usuario y da la opción
#  de FUSIONAR los ingredientes antes de eliminar el duplicado.
# ============================================================

# Reutilizamos las clases y funciones del programa 1
# (en un proyecto real harías: from postres import ...)

# --- Clases ------------------------------------------------

class NodoIngrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

class NodoPostre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ingredientes = None

# --- Arreglo global ----------------------------------------
POSTRES = []

# --- Utilidades --------------------------------------------

def buscar_postre(nombre):
    nombre = nombre.strip().lower()
    for nodo in POSTRES:
        if nodo.nombre.lower() == nombre:
            return nodo
    return None

def insertar_postre_ordenado(nodo):
    POSTRES.append(nodo)
    POSTRES.sort(key=lambda n: n.nombre.lower())

def _ingredientes_a_lista(cabeza):
    """Devuelve una lista Python con los nombres de los ingredientes."""
    resultado = []
    actual = cabeza
    while actual:
        resultado.append(actual.nombre)
        actual = actual.siguiente
    return resultado

def _agregar_ingrediente_unico(nodo_postre, nombre_ing):
    """Agrega un ingrediente al final si no está ya en la lista."""
    actual = nodo_postre.ingredientes
    while actual:
        if actual.nombre.lower() == nombre_ing.lower():
            return  # ya existe
        actual = actual.siguiente
    nuevo = NodoIngrediente(nombre_ing)
    if nodo_postre.ingredientes is None:
        nodo_postre.ingredientes = nuevo
    else:
        actual = nodo_postre.ingredientes
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo

def alta_postre(nombre, ingredientes):
    """Alta rápida para pruebas."""
    p = NodoPostre(nombre.strip())
    for ing in ingredientes:
        nuevo = NodoIngrediente(ing.strip())
        if p.ingredientes is None:
            p.ingredientes = nuevo
        else:
            actual = p.ingredientes
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
    POSTRES.append(p)   # sin ordenar, para permitir duplicados manuales

def imprimir_postres():
    print("\n  Arreglo POSTRES:")
    for i, nodo in enumerate(POSTRES):
        ings = _ingredientes_a_lista(nodo.ingredientes)
        print(f"  [{i}] {nodo.nombre}  →  {ings}")

# ============================================================
# NÚCLEO: eliminar duplicados
# ============================================================

def eliminar_repetidos(fusionar=True):
    """
    Recorre POSTRES y elimina entradas con nombre repetido.

    fusionar=True  → antes de borrar el duplicado, combina sus
                     ingredientes con la primera aparición.
    fusionar=False → borra el duplicado junto con su lista
                     (se pierden los ingredientes únicos del duplicado).
    """
    print("\n" + "="*55)
    print("  Eliminando postres repetidos  (fusionar=%s)" % fusionar)
    print("="*55)

    vistos = {}          # nombre_lower → primer índice encontrado
    indices_a_borrar = []

    for i, nodo in enumerate(POSTRES):
        clave = nodo.nombre.strip().lower()
        if clave not in vistos:
            vistos[clave] = i
        else:
            primer_idx = vistos[clave]
            primer_nodo = POSTRES[primer_idx]
            ings_dup = _ingredientes_a_lista(nodo.ingredientes)

            print(f"\n  DUPLICADO encontrado: '{nodo.nombre}'  (índice {i})")
            print(f"    Sus ingredientes: {ings_dup}")

            if fusionar:
                # Fusionar ingredientes únicos al nodo original
                nuevos = []
                for ing in ings_dup:
                    actual = primer_nodo.ingredientes
                    existe = False
                    while actual:
                        if actual.nombre.lower() == ing.lower():
                            existe = True
                            break
                        actual = actual.siguiente
                    if not existe:
                        _agregar_ingrediente_unico(primer_nodo, ing)
                        nuevos.append(ing)
                if nuevos:
                    print(f"    → Ingredientes fusionados al original: {nuevos}")
                else:
                    print(f"    → No hay ingredientes nuevos; lista original sin cambios.")
            else:
                # Sin fusión: se pierden los ingredientes del duplicado
                print(f"    ⚠  ADVERTENCIA: los ingredientes del duplicado se PERDERÁN.")
                # Liberar la lista enlazada del duplicado
                actual = nodo.ingredientes
                while actual:
                    sig = actual.siguiente
                    actual.siguiente = None
                    actual = sig
                nodo.ingredientes = None

            indices_a_borrar.append(i)

    # Borrar en orden inverso para no alterar índices
    for idx in sorted(indices_a_borrar, reverse=True):
        del POSTRES[idx]

    # Re-ordenar alfabéticamente
    POSTRES.sort(key=lambda n: n.nombre.lower())

    if indices_a_borrar:
        print(f"\n  [OK] Se eliminaron {len(indices_a_borrar)} postre(s) duplicado(s).")
    else:
        print("  [INFO] No se encontraron duplicados.")


# ============================================================
# DEMO
# ============================================================

def demo():
    print("="*55)
    print("  DEMO – Arreglo con postres repetidos")
    print("="*55)

    # Cargamos postres, incluyendo duplicados intencionados
    alta_postre("Flan",       ["Leche", "Huevos", "Azúcar"])
    alta_postre("Brownie",    ["Chocolate", "Harina", "Mantequilla"])
    alta_postre("Flan",       ["Caramelo", "Vainilla"])        # duplicado de Flan
    alta_postre("Cheesecake", ["Queso crema", "Galletas"])
    alta_postre("Brownie",    ["Nueces", "Chocolate"])         # duplicado de Brownie
    alta_postre("Brownie",    ["Azúcar glass"])                # otro duplicado de Brownie

    imprimir_postres()

    # -------------------------------------------------------
    # CASO 1: eliminar duplicados FUSIONANDO ingredientes
    # -------------------------------------------------------
    print("\n\n>>> CASO 1: Eliminar duplicados con FUSIÓN de ingredientes")
    eliminar_repetidos(fusionar=True)
    imprimir_postres()

    # -------------------------------------------------------
    # CASO 2: simular qué pasaría SIN fusión
    # -------------------------------------------------------
    print("\n\n>>> CASO 2: Eliminar duplicados SIN fusión (se pierden listas)")

    # Recargamos POSTRES con duplicados de nuevo
    POSTRES.clear()
    alta_postre("Flan",    ["Leche", "Huevos"])
    alta_postre("Flan",    ["Caramelo", "Vainilla", "Leche condensada"])
    alta_postre("Suspiro", ["Clara de huevo", "Azúcar"])

    imprimir_postres()
    eliminar_repetidos(fusionar=False)
    imprimir_postres()

    # -------------------------------------------------------
    # CONCLUSIÓN
    # -------------------------------------------------------
    print("\n" + "="*55)
    print("  CONCLUSIONES")
    print("="*55)
    print("""
  Al eliminar un postre repetido del arreglo, también se pierde
  su lista enlazada de ingredientes (pasa a NIL / None).

  Sin precaución → PÉRDIDA DE DATOS: los ingredientes únicos
  del duplicado desaparecen sin posibilidad de recuperarlos.

  Solución recomendada → FUSIONAR las listas antes de borrar:
  se recorre la lista del duplicado y se agregan al nodo
  original sólo los ingredientes que todavía no existen,
  preservando toda la información del arreglo.
""")

if __name__ == "__main__":
    demo()
