import numpy as np
import time  # Importado para medir el tiempo

# 1. Definir dimensiones
TOTAL_ALUMNOS = 100 
TOTAL_MATERIAS = 100

# 2. Crear la matriz con calificaciones aleatorias (0.0 a 10.0)
np.random.seed(42) 
matriz_calificaciones = np.round(np.random.uniform(0, 10, (TOTAL_ALUMNOS, TOTAL_MATERIAS)), 1)

# --- NUEVA SECCIÓN: Entrada de usuario ---
print("--- CONSULTA DE CALIFICACIONES ---")
alumno_input = int(input(f"Ingrese el número del alumno (1-{TOTAL_ALUMNOS}): "))
materia_input = int(input(f"Ingrese el número de la materia (1-{TOTAL_MATERIAS}): "))

# Iniciar medición de tiempo
inicio_tiempo = time.time()

# Ajuste de índices (el usuario ingresa 1-500, Python usa 0-499)
fila_alumno = alumno_input - 1
columna_materia = materia_input - 1

# 3. Realizar la búsqueda
calificacion = matriz_calificaciones[fila_alumno, columna_materia]

print(f"\n--- BÚSQUEDA ESPECÍFICA ---")
print(f"La calificación del Alumno {alumno_input} en la Materia {materia_input} es: {calificacion}")
print(f"---------------------------\n")

# 4. Mostrar la tabla
print("TABLA DE CALIFICACIONES:")
print("Alumno  | Mat 1 | Mat 2 | Mat 3 | Mat 4 | Mat 5 | Mat 6")
print("-" * 55)

# Función para imprimir filas formateadas
def imprimir_fila(id_alumno):
    notas = matriz_calificaciones[id_alumno]
    fila_str = " | ".join([f"{n:5.1f}" for n in notas])
    print(f"ID {id_alumno+1:03d}  | {fila_str}")

# Mostrar todos los alumnos
for i in range(500):
    imprimir_fila(i)

print("...") # Salto visual

# Mostrar específicamente el alumno consultado
imprimir_fila(fila_alumno)

# Finalizar medición de tiempo
fin_tiempo = time.time()
tiempo_ejecucion = fin_tiempo - inicio_tiempo

print("...")
print(f"\nEl programa tardó {tiempo_ejecucion:.6f} segundos en procesar la búsqueda y mostrar la tabla.")
