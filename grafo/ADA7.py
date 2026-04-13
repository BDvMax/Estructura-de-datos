"""
Grafo de 7 Estados de la República Mexicana
============================================
Estados seleccionados:
  1. Ciudad de México (CDMX)
  2. Jalisco
  3. Nuevo León
  4. Yucatán
  5. Veracruz
  6. Puebla
  7. Oaxaca

Conexiones y costos (distancia aproximada en km por carretera):
"""

import heapq
from collections import defaultdict

# ─────────────────────────────────────────────
#  DEFINICIÓN DEL GRAFO
# ─────────────────────────────────────────────

ESTADOS = {
    0: "Ciudad de México",
    1: "Jalisco",
    2: "Nuevo León",
    3: "Yucatán",
    4: "Veracruz",
    5: "Puebla",
    6: "Oaxaca",
}

# Aristas: (nodo_a, nodo_b, costo_km)
ARISTAS = [
    (0, 1, 700),   # CDMX  ↔ Jalisco
    (0, 2, 920),   # CDMX  ↔ Nuevo León
    (0, 4, 420),   # CDMX  ↔ Veracruz
    (0, 5, 130),   # CDMX  ↔ Puebla
    (1, 2, 730),   # Jalisco ↔ Nuevo León
    (2, 4, 870),   # Nuevo León ↔ Veracruz
    (3, 4, 680),   # Yucatán ↔ Veracruz
    (3, 6, 770),   # Yucatán ↔ Oaxaca
    (4, 5, 310),   # Veracruz ↔ Puebla
    (4, 6, 470),   # Veracruz ↔ Oaxaca
    (5, 6, 360),   # Puebla  ↔ Oaxaca
]

# Construir lista de adyacencia
def construir_grafo():
    grafo = defaultdict(list)
    for a, b, costo in ARISTAS:
        grafo[a].append((b, costo))
        grafo[b].append((a, costo))
    return grafo

# ─────────────────────────────────────────────
#  MOSTRAR ESTADOS Y RELACIONES
# ─────────────────────────────────────────────

def mostrar_relaciones(grafo):
    print("\n" + "═" * 55)
    print("   ESTADOS Y SUS RELACIONES (vecinos directos)")
    print("═" * 55)
    for nodo, nombre in ESTADOS.items():
        vecinos = grafo[nodo]
        print(f"\n  [{nodo}] {nombre}")
        if vecinos:
            for v, costo in sorted(vecinos, key=lambda x: x[1]):
                print(f"       → {ESTADOS[v]:<22} {costo:>5} km")
        else:
            print("       (sin conexiones directas)")
    print()

# ─────────────────────────────────────────────
#  DIJKSTRA (camino mínimo entre dos nodos)
# ─────────────────────────────────────────────

def dijkstra(grafo, origen):
    dist = {n: float("inf") for n in ESTADOS}
    prev = {n: None for n in ESTADOS}
    dist[origen] = 0
    heap = [(0, origen)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in grafo[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev

def reconstruir_camino(prev, destino):
    camino = []
    n = destino
    while n is not None:
        camino.append(n)
        n = prev[n]
    return list(reversed(camino))

# ─────────────────────────────────────────────
#  INCISO A: Recorrido SIN repetir nodos
#  Algoritmo: búsqueda exhaustiva (fuerza bruta)
#  sobre todos los caminos Hamiltonianos posibles
# ─────────────────────────────────────────────

def camino_hamiltoniano(grafo):
    """
    Encuentra un camino que visita los 7 estados exactamente
    una vez (camino Hamiltoniano). Devuelve el primero encontrado.
    """
    n = len(ESTADOS)
    mejor = {"camino": None, "costo": float("inf")}

    def bt(nodo_actual, visitados, camino_actual, costo_actual):
        if len(visitados) == n:
            if costo_actual < mejor["costo"]:
                mejor["costo"] = costo_actual
                mejor["camino"] = camino_actual[:]
            return
        for vecino, peso in grafo[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                camino_actual.append(vecino)
                bt(vecino, visitados, camino_actual, costo_actual + peso)
                camino_actual.pop()
                visitados.remove(vecino)

    for inicio in ESTADOS:
        bt(inicio, {inicio}, [inicio], 0)

    return mejor["camino"], mejor["costo"]

# ─────────────────────────────────────────────
#  INCISO B: Recorrido CON al menos una repetición
#  Estrategia: recorrido Euleriano-style usando
#  Dijkstra para "saltar" entre estados no
#  adyacentes, repitiendo nodos intermedios.
# ─────────────────────────────────────────────

def recorrido_con_repeticion(grafo):
    """
    Visita los 7 estados asegurando que AL MENOS uno
    se repita. Parte del camino Hamiltoniano y agrega
    un "retorno" extra a uno de los nodos intermedios.
    """
    camino_h, costo_h = camino_hamiltoniano(grafo)

    # Tomamos el camino Hamiltoniano y añadimos un
    # salto extra: volvemos al segundo nodo del camino.
    nodo_extra = camino_h[1]
    ultimo = camino_h[-1]

    # Costo de ir desde el último nodo hasta nodo_extra (Dijkstra)
    dist, prev = dijkstra(grafo, ultimo)
    costo_extra = dist[nodo_extra]
    sub_camino = reconstruir_camino(prev, nodo_extra)

    camino_completo = camino_h + sub_camino[1:]   # evitar duplicar el nodo de unión
    costo_total = costo_h + costo_extra

    return camino_completo, costo_total

# ─────────────────────────────────────────────
#  DIBUJAR GRAFO EN ASCII / TEXTO
# ─────────────────────────────────────────────

def dibujar_grafo():
    """
    Representación visual del grafo en la terminal
    usando caracteres ASCII.
    """
    print("\n" + "═" * 55)
    print("   VISUALIZACIÓN DEL GRAFO (mapa simplificado)")
    print("═" * 55)

    # Representación artística del mapa
    mapa = r"""
                [2] Nuevo León
               /       \
           730 km      920 km
           /               \
    [1] Jalisco     870 km   \
           \      ─────────── [0] CDMX ── 130 km ── [5] Puebla
        700 km \             /                           |  \
                 \       420 km                       310 km  360 km
                  \      /                              |       \
                  [0] CDMX                          [4] Veracruz [6] Oaxaca
                                                    /       \
                                                680 km     470 km
                                                  /           \
                                          [3] Yucatán ── 770 km ── [6] Oaxaca
    """

    # Versión limpia con tabla de conexiones
    print("""
  Nodos del grafo:
  ┌────┬──────────────────────┐
  │ ID │ Estado               │
  ├────┼──────────────────────┤
  │  0 │ Ciudad de México     │
  │  1 │ Jalisco              │
  │  2 │ Nuevo León           │
  │  3 │ Yucatán              │
  │  4 │ Veracruz             │
  │  5 │ Puebla               │
  │  6 │ Oaxaca               │
  └────┴──────────────────────┘

  Aristas (conexiones directas):
  ┌──────────────────────┬──────────────────────┬──────────┐
  │ Estado A             │ Estado B             │  Costo   │
  ├──────────────────────┼──────────────────────┼──────────┤
  │ Ciudad de México     │ Jalisco              │  700 km  │
  │ Ciudad de México     │ Nuevo León           │  920 km  │
  │ Ciudad de México     │ Veracruz             │  420 km  │
  │ Ciudad de México     │ Puebla               │  130 km  │
  │ Jalisco              │ Nuevo León           │  730 km  │
  │ Nuevo León           │ Veracruz             │  870 km  │
  │ Yucatán              │ Veracruz             │  680 km  │
  │ Yucatán              │ Oaxaca               │  770 km  │
  │ Veracruz             │ Puebla               │  310 km  │
  │ Veracruz             │ Oaxaca               │  470 km  │
  │ Puebla               │ Oaxaca               │  360 km  │
  └──────────────────────┴──────────────────────┴──────────┘

  Diagrama esquemático:

   [1]Jalisco ─730─ [2]NuevoLeón
      |                   |
     700                 920
      |                   |
   [0]CDMX ─420─ [4]Veracruz ─680─ [3]Yucatán
      |          /    |    \\             |
     130      870   310   470          770
      |      /      |      \\            |
   [5]Puebla ─360─ [6]Oaxaca ─────────┘
    """)

# ─────────────────────────────────────────────
#  IMPRIMIR CAMINO CON NOMBRES
# ─────────────────────────────────────────────

def formato_camino(camino):
    partes = []
    for i, nodo in enumerate(camino):
        partes.append(f"[{nodo}]{ESTADOS[nodo]}")
        if i < len(camino) - 1:
            partes.append("→")
    return " ".join(partes)

def costo_camino(grafo, camino):
    """Calcula el costo real de un camino dado (usando adyacencia directa o Dijkstra)."""
    total = 0
    detalles = []
    for i in range(len(camino) - 1):
        a, b = camino[i], camino[i + 1]
        # Buscar arista directa
        costo = None
        for vecino, w in grafo[a]:
            if vecino == b:
                costo = w
                break
        if costo is None:
            # No son adyacentes → usar Dijkstra
            dist, _ = dijkstra(grafo, a)
            costo = dist[b]
        total += costo
        detalles.append(f"  {ESTADOS[a]:<22} → {ESTADOS[b]:<22} = {costo:>5} km")
    return total, detalles

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    grafo = construir_grafo()

    print("\n" + "╔" + "═" * 53 + "╗")
    print("║   GRAFO DE ESTADOS DE LA REPÚBLICA MEXICANA    ║")
    print("╚" + "═" * 53 + "╝")

    # ── 5. Mostrar estados y relaciones
    mostrar_relaciones(grafo)

    # ── 4. Dibujar grafo
    dibujar_grafo()

    # ── A. Recorrido sin repetición
    print("\n" + "═" * 55)
    print("  INCISO A: Recorrido sin repetir estados")
    print("  (Camino Hamiltoniano de menor costo)")
    print("═" * 55)
    camino_a, costo_a = camino_hamiltoniano(grafo)

    if camino_a:
        _, detalles_a = costo_camino(grafo, camino_a)
        print(f"\n  Ruta encontrada:")
        for d in detalles_a:
            print(d)
        print(f"\n  Camino: {formato_camino(camino_a)}")
        print(f"  {'─'*45}")
        print(f"  ✔ Costo total (sin repetición): {costo_a:,} km")
    else:
        print("  ✗ No se encontró camino Hamiltoniano.")

    # ── B. Recorrido con repetición
    print("\n" + "═" * 55)
    print("  INCISO B: Recorrido repitiendo al menos un estado")
    print("═" * 55)
    camino_b, costo_b = recorrido_con_repeticion(grafo)
    _, detalles_b = costo_camino(grafo, camino_b)

    print(f"\n  Ruta encontrada:")
    for d in detalles_b:
        print(d)

    # Marcar el nodo repetido
    repetidos = [ESTADOS[n] for n in camino_b if camino_b.count(n) > 1]
    repetidos_unicos = list(dict.fromkeys(repetidos))

    print(f"\n  Camino: {formato_camino(camino_b)}")
    print(f"  Estado(s) repetido(s): {', '.join(repetidos_unicos)}")
    print(f"  {'─'*45}")
    print(f"  ✔ Costo total (con repetición): {costo_b:,} km")

    # ── Comparativa
    print("\n" + "═" * 55)
    print("  RESUMEN COMPARATIVO")
    print("═" * 55)
    print(f"  Inciso A (sin repetir):  {costo_a:>7,} km")
    print(f"  Inciso B (con repetir):  {costo_b:>7,} km")
    print(f"  Diferencia:              {costo_b - costo_a:>7,} km extra")
    print()

if __name__ == "__main__":
    main()
