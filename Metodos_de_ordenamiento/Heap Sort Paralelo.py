import multiprocessing
import math
import random
import time

# --- 1. Función de Combinación (Merge) de sublistas ya ordenadas ---
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

# --- 2. Heap Sort base para cada Proceso ---
def heapify(arr, n, i):
    """Hunde el elemento en i para mantener la propiedad de max-heap (iterativo)."""
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        if largest == i:
            return
        arr[i], arr[largest] = arr[largest], arr[i]
        i = largest

def heap_sort(arr):
    """Ordena la lista con Heap Sort (O(n log n)). Modifica y devuelve arr."""
    n = len(arr)
    # Construir max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extraer el máximo repetidamente
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        heapify(arr, end, 0)
    return arr

# --- 3. Ordenamiento Paralelo (Heap Sort por chunk + merge final) ---
def heap_sort_parallel(data, pool, processes):
    """Divide la lista entre los núcleos, cada uno aplica Heap Sort,
    y luego se combinan los resultados con merge."""

    # 1. DIVIDIR
    size = int(math.ceil(float(len(data)) / processes))
    data_chunks = [data[i * size:(i + 1) * size] for i in range(processes)]

    # 2. PARALELIZAR: cada núcleo ordena su chunk con Heap Sort
    data_sorted_chunks = pool.map(heap_sort, data_chunks)

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

    # Mismos exponentes que el secuencial (10^7 tarda minutos; 10^8 requiere varios GB de RAM)
    EXPONENTES = [1, 2, 3, 4, 5, 6, 7]

    num_procesos = multiprocessing.cpu_count()

    resultados = []

    print("--- Prueba de Rendimiento de Heap Sort PARALELO (10^N) ---")
    print(f"Ejecutando en {num_procesos} núcleos de procesador")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")

    pool = multiprocessing.Pool(processes=num_procesos)

    for exponente in EXPONENTES:
        N = 10 ** exponente

        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")

        unsorted_data = generar_datos_aleatorios(N)

        start_time = time.perf_counter()
        sorted_data = heap_sort_parallel(unsorted_data, pool, num_procesos)
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
