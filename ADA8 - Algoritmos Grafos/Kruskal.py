class UnionFind:
    """
    Estructura Union-Find (Conjuntos Disjuntos) para detectar ciclos.
    Usa compresion de rutas y union por rango para mayor eficiencia.
    """
    def __init__(self, nodos):
        self.padre = {n: n for n in nodos}
        self.rango = {n: 0 for n in nodos}

    def encontrar(self, nodo):
        """Encuentra la raiz del conjunto al que pertenece nodo."""
        if self.padre[nodo] != nodo:
            self.padre[nodo] = self.encontrar(self.padre[nodo])  # Compresion de rutas
        return self.padre[nodo]

    def unir(self, u, v):
        """Une los conjuntos de u y v. Retorna False si ya estaban unidos."""
        raiz_u = self.encontrar(u)
        raiz_v = self.encontrar(v)
        if raiz_u == raiz_v:
            return False  # Mismo conjunto -> habria ciclo
        # Union por rango
        if self.rango[raiz_u] < self.rango[raiz_v]:
            raiz_u, raiz_v = raiz_v, raiz_u
        self.padre[raiz_v] = raiz_u
        if self.rango[raiz_u] == self.rango[raiz_v]:
            self.rango[raiz_u] += 1
        return True


def kruskal(nodos, aristas):
    """
    Algoritmo de Kruskal para encontrar el Arbol de Expansion Minima (MST).
    
    Estrategia greedy: ordena las aristas por peso de menor a mayor
    y agrega cada arista que no forme un ciclo.
    
    Args:
        nodos: lista de nodos del grafo
        aristas: lista de tuplas (peso, nodo_u, nodo_v)
    
    Returns:
        mst: lista de aristas del arbol de expansion minima
        costo_total: suma de pesos del MST
    """
    aristas_ordenadas = sorted(aristas, key=lambda x: x[0])
    uf = UnionFind(nodos)
    mst = []
    costo_total = 0

    for peso, u, v in aristas_ordenadas:
        if uf.unir(u, v):
            mst.append((peso, u, v))
            costo_total += peso
            if len(mst) == len(nodos) - 1:
                break  # MST completo

    return mst, costo_total


if __name__ == "__main__":
    nodos = ['A', 'B', 'C', 'D', 'E']

    # Aristas: (peso, nodo_u, nodo_v)
    aristas = [
        (1, 'A', 'B'),
        (3, 'A', 'C'),
        (4, 'B', 'C'),
        (2, 'B', 'D'),
        (5, 'C', 'D'),
        (6, 'C', 'E'),
        (4, 'D', 'E'),
    ]

    mst, costo = kruskal(nodos, aristas)

    print("=" * 48)
    print("  Algoritmo de Kruskal - Arbol de Expansion Minima")
    print("=" * 48)
    print()
    print("  Aristas disponibles (ordenadas por peso):")
    print("  " + "-" * 30)
    for peso, u, v in sorted(aristas):
        print(f"    {u} -- {v}  (peso: {peso})")
    print()
    print("  Aristas incluidas en el MST:")
    print("  " + "-" * 30)
    for paso, (peso, u, v) in enumerate(mst, 1):
        print(f"  Paso {paso}: {u} -- {v}  (peso: {peso})")
    print()
    print(f"  Costo total del MST: {costo}")
    print("=" * 48)
