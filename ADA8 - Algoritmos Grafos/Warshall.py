def warshall(matriz):
    """
    Algoritmo de Warshall para calcular el cierre transitivo
    de un grafo dirigido.
    
    Determina si existe un camino (de cualquier longitud) entre
    cada par de nodos i y j.
    
    Args:
        matriz: matriz de adyacencia n x n booleana (0/1)
                1 si hay arista directa de i a j
    
    Returns:
        tc: matriz de cierre transitivo
            tc[i][j] = 1 si existe algun camino de i a j
    """
    n = len(matriz)
    tc = [fila[:] for fila in matriz]  # Copia de la matriz

    # Cada nodo puede ser alcanzado desde si mismo
    for i in range(n):
        tc[i][i] = 1

    # Para cada nodo intermediario k
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Si existe camino i->k y k->j, entonces existe i->j
                tc[i][j] = tc[i][j] or (tc[i][k] and tc[k][j])

    return tc


def imprimir_matriz(matriz, nodos, titulo):
    """Imprime una matriz de forma legible."""
    n = len(nodos)
    print(f"\n  {titulo}")
    print("  " + "-" * (n * 6 + 4))
    print(f"{'':>6}", end="")
    for nd in nodos:
        print(f"  {nd:>3}", end="")
    print()
    for i in range(n):
        print(f"  {nodos[i]:>3} |", end="")
        for j in range(n):
            print(f"  {matriz[i][j]:>3}", end="")
        print()
    print("  " + "-" * (n * 6 + 4))


if __name__ == "__main__":
    nodos = ['A', 'B', 'C', 'D']

    # Matriz de adyacencia del grafo dirigido
    #        A  B  C  D
    matriz = [
        [0, 1, 0, 0],  # A -> B
        [0, 0, 1, 0],  # B -> C
        [0, 0, 0, 1],  # C -> D
        [0, 0, 0, 0],  # D (sin salidas)
    ]

    print("=" * 42)
    print("  Algoritmo de Warshall - Cierre Transitivo")
    print("=" * 42)

    imprimir_matriz(matriz, nodos, "Matriz de Adyacencia (original):")

    tc = warshall(matriz)

    imprimir_matriz(tc, nodos, "Cierre Transitivo:")

    print()
    print("  Interpretacion:")
    n = len(nodos)
    for i in range(n):
        for j in range(n):
            if i != j and tc[i][j]:
                print(f"  Existe camino de {nodos[i]} a {nodos[j]}")
    print("=" * 42)
