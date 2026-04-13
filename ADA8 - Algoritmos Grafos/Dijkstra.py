import heapq

def dijkstra(grafo, inicio):
    """
    Algoritmo de Dijkstra para encontrar el camino mas corto
    desde un nodo origen hasta todos los demas nodos.
    
    Args:
        grafo: diccionario {nodo: [(vecino, peso), ...]}
        inicio: nodo de partida
    
    Returns:
        distancias: diccionario con la distancia minima a cada nodo
        predecesores: diccionario para reconstruir el camino
    """
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    predecesores = {nodo: None for nodo in grafo}
    
    # Cola de prioridad: (distancia, nodo)
    cola = [(0, inicio)]
    visitados = set()

    while cola:
        dist_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        for vecino, peso in grafo[nodo_actual]:
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola, (nueva_dist, vecino))

    return distancias, predecesores


def reconstruir_camino(predecesores, inicio, destino):
    """Reconstruye el camino desde inicio hasta destino."""
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = predecesores[nodo]
    camino.reverse()
    if camino[0] == inicio:
        return camino
    return []


if __name__ == "__main__":
    # Grafo de ejemplo (lista de adyacencia con pesos)
    grafo = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }

    inicio = 'A'
    distancias, predecesores = dijkstra(grafo, inicio)

    print("=" * 45)
    print(f"  Algoritmo de Dijkstra - Origen: {inicio}")
    print("=" * 45)
    for nodo, dist in distancias.items():
        camino = reconstruir_camino(predecesores, inicio, nodo)
        print(f"  {inicio} -> {nodo}: distancia = {dist}, camino = {' -> '.join(camino)}")
    print("=" * 45)
