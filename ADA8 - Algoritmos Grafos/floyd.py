INF = float('inf')

def floyd(grafo):
    """
    Algoritmo de Floyd-Warshall para encontrar los caminos
    mas cortos entre todos los pares de nodos.
    
    Args:
        grafo: matriz de adyacencia n x n con pesos
               (INF si no hay arista directa)
    
    Returns:
        dist: matriz de distancias minimas entre todos los pares
        next_node: matriz para reconstruir caminos
    """
    n = len(grafo)
    dist = [fila[:] for fila in grafo]  # Copia de la matriz
    next_node = [[None] * n for _ in range(n)]

    # Inicializar next_node
    for i in range(n):
        for j in range(n):
            if i != j and grafo[i][j] != INF:
                next_node[i][j] = j

    # Relajacion de distancias usando cada nodo como intermediario
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node


def reconstruir_camino(next_node, u, v):
    """Reconstruye el camino entre nodo u y nodo v."""
    if next_node[u][v] is None:
        return []
    camino = [u]
    while u != v:
        u = next_node[u][v]
        camino.append(u)
    return camino


if __name__ == "__main__":
    # Representacion: indices 0=A, 1=B, 2=C, 3=D
    nodos = ['A', 'B', 'C', 'D']

    grafo = [
        #  A    B    C    D
        [  0,   3, INF,   7],  # A
        [  8,   0,   2, INF],  # B
        [  5, INF,   0,   1],  # C
        [  2, INF, INF,   0],  # D
    ]

    dist, next_node = floyd(grafo)
    n = len(nodos)

    print("=" * 55)
    print("  Algoritmo de Floyd - Distancias minimas entre pares")
    print("=" * 55)
    print(f"{'':>4}", end="")
    for nd in nodos:
        print(f"{nd:>8}", end="")
    print()
    for i in range(n):
        print(f"  {nodos[i]}:", end="")
        for j in range(n):
            val = dist[i][j]
            print(f"{'INF':>8}" if val == INF else f"{val:>8}", end="")
        print()

    print()
    print("  Caminos reconstruidos:")
    print("-" * 55)
    for i in range(n):
        for j in range(n):
            if i != j:
                camino = reconstruir_camino(next_node, i, j)
                nombres = " -> ".join(nodos[x] for x in camino)
                d = dist[i][j]
                print(f"  {nodos[i]} -> {nodos[j]}: {nombres}  (dist={d})")
    print("=" * 55)
