import multiprocessing
import math
import random
import time

# --- 1. Función de Combinación de sublistas ya ordenadas ---
def merge(left, right):
    """Combina dos listas ordenadas en una sola lista ordenada."""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# --- 2. Selection Sort base para cada Proceso ---
def selection_sort(data):
    """Selection Sort (O(n^2)) utilizado por cada núcleo sobre su chunk."""
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
    return data

# --- 3. Ordenamiento Paralelo (Selection Sort por chunk + merge final) ---
def selection_sort_parallel(data, pool, processes):
    """Divide la lista entre los núcleos, cada uno aplica Selection Sort,
    y luego se combinan los resultados con merge."""

    # 1. DIVIDIR
    size = int(math.ceil(float(len(data)) / processes))
    data_chunks = [data[i * size:(i + 1) * size] for i in range(processes)]

    # 2. PARALELIZAR: cada núcleo ordena su chunk con Selection Sort
    data_sorted_chunks = pool.map(selection_sort, data_chunks)

    # 3. COMBINAR: mezclar secuencialmente las sublistas ordenadas
    while len(data_sorted_chunks) > 1:
        new_chunks = []
        for i in range(0, len(data_sorted_chunks) - 1, 2):
            new_chunks.append(merge(data_sorted_chunks[i], data_sorted_chunks[i + 1]))

        if len(data_sorted_chunks) % 2 != 0:
            new_chunks.append(data_sorted_chunks[-1])

        data_sorted_chunks = new_chunks

    return data_sorted_chunks[0]

# --- 4. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000):
    """Genera una lista de números enteros aleatorios."""
    return [random.randint(0, max_value) for _ in range(cantidad)]

# --- 5. Bloque de Ejecución Principal ---
if __name__ == '__main__':

    # Mismos exponentes que el secuencial (Selection Sort es O(n^2))
    EXPONENTES = [1, 2, 3, 4, 5]

    num_procesos = multiprocessing.cpu_count()

    resultados = []

    print("--- Prueba de Rendimiento de Selection Sort PARALELO (10^N) ---")
    print(f"Ejecutando en {num_procesos} núcleos de procesador")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")

    pool = multiprocessing.Pool(processes=num_procesos)

    for exponente in EXPONENTES:
        N = 10 ** exponente

        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")

        unsorted_data = generar_datos_aleatorios(N)

        start_time = time.perf_counter()
        sorted_data = selection_sort_parallel(unsorted_data, pool, num_procesos)
        end_time_total = time.perf_counter() - start_time

        resultados.append({
            "Exponente": exponente,
            "N": N,
            "Tiempo (s)": end_time_total
        })

        print(f"✅ Prueba de N={N:,} completada. Tiempo: {end_time_total:.6f} segundos.")

    pool.close()
    pool.join()

    # --- TABLA DE RESUMEN ---
    print("\n\n========================================================")
    print("📊 RESUMEN DE TIEMPOS DE EJECUCIÓN PARALELO (N = 10^Exponente)")
    print("========================================================")
    print(f"| {'Exponente':<10} | {'N (Cantidad)':<15} | {'Tiempo (segundos)':<20} |")
    print(f"| {'-'*10:<10} | {'-'*15:<15} | {'-'*20:<20} |")

    for res in resultados:
        print(f"| 10^{res['Exponente']:<7} | {res['N']:<15,} | {res['Tiempo (s)']:.6f}{'':<14} |")

    print("========================================================")
