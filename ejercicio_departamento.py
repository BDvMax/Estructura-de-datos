import numpy as np 
import time

# 1. Configuración de datos
departamentos = ["Ropa", "Deportes", "Juguetería"]
meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# 2. Generar arreglo bidimensional (3 departamentos x 12 meses)
np.random.seed(42)
ventas = np.random.randint(10000, 50000, size=(len(departamentos), len(meses)))

def mostrar_reporte(matriz):
    inicio_tiempo = time.time()
    print("\nREPORTE DE VENTAS POR DEPARTAMENTO")
    print("-" * 110)
    header = f"{'Departamento':<15}" + "".join([f"{mes:>8}" for mes in meses])
    print(header)
    print("-" * 110)
    for i in range(len(departamentos)):
        fila = f"{departamentos[i]:<15}" + "".join([f"{matriz[i, j]:>8}" for j in range(len(meses))])
        print(fila)
    print("-" * 110)
    fin_tiempo = time.time()
    print(f"Tiempo de ejecución: {fin_tiempo - inicio_tiempo:.6f} segundos.")

# --- MÉTODO PARA BUSCAR VALOR ---
def buscar_valor(matriz):
    print("\n--- BÚSQUEDA DE VALOR ESPECÍFICO ---")
    for i, dept in enumerate(departamentos):
        print(f"{i}: {dept}")
    id_dept = int(input("Seleccione el índice del departamento a buscar: "))
    
    for i, mes in enumerate(meses):
        print(f"{i}: {mes}")
    id_mes = int(input("Seleccione el índice del mes a buscar: "))
    
    valor = matriz[id_dept, id_mes]
    print(f"\n>> El valor de ventas para {departamentos[id_dept]} en {meses[id_mes]} es: ${valor}")

# --- MÉTODO PARA ELIMINAR UNA VENTA ---
def eliminar_venta(matriz):
    print("\n--- ELIMINAR UNA VENTA ---")
    for i, dept in enumerate(departamentos):
        print(f"{i}: {dept}")
    id_dept = int(input("Seleccione el índice del departamento: "))
    
    for i, mes in enumerate(meses):
        print(f"{i}: {mes}")
    id_mes = int(input("Seleccione el índice del mes: "))
    
    matriz[id_dept, id_mes] = 0
    print(f"\n>> Venta eliminada para {departamentos[id_dept]} en {meses[id_mes]}.")

# --- FLUJO DEL PROGRAMA ---

# Mostrar tabla inicial
mostrar_reporte(ventas)

# Método para insertar monto manual
print("\n--- ACTUALIZACIÓN MANUAL DE VENTAS ---")
for i, dept in enumerate(departamentos):
    print(f"{i}: {dept}")
id_dept = int(input("Seleccione el índice del departamento: "))

for i, mes in enumerate(meses):
    print(f"{i}: {mes}")
id_mes = int(input("Seleccione el índice del mes: "))

nuevo_monto = int(input(f"Ingrese el nuevo monto para {departamentos[id_dept]} en {meses[id_mes]}: "))

ventas[id_dept, id_mes] = nuevo_monto
print("\n¡Monto actualizado con éxito!")

# Volver a mostrar la tabla
mostrar_reporte(ventas)

# Llamada al nuevo método de búsqueda
buscar_valor(ventas)

# Llamada al método para eliminar venta
eliminar_venta(ventas)

# Mostrar tabla final
mostrar_reporte(ventas)
