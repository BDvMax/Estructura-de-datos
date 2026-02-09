import numpy as np

def memoria_estatica():
    calificaciones = np.zeros(5, dtype=int)

    print("Registro de Calificaciones")
    
    for i in range(5):
        # Solicitamos la entrada al usuario
        entrada = input(f"Captura la calificación {i+1}: ")
        
        calificaciones[i] = int(entrada)

    print("\nArreglo resultante:", calificaciones)
    print("Tipo de objeto:", type(calificaciones))

def memoria_dinamica():
    # En Python, una lista [] equivale al ArrayList de Java
    frutas = []

    frutas.append("Mango")
    frutas.append("Manzana")
    frutas.append("Banana")
    frutas.append("Uvas")

    print("Lista inicial:", frutas)

    # eliminar por índice
    frutas.pop(0) 
    
    # los índices se recorren
    frutas.pop(1)

    frutas.append("sandia")

    print("Lista final:  ", frutas)

def main():
    memoria_estatica()
    memoria_dinamica()

if __name__ == "__main__":
    main()
