import random
import time

# --- 1. Implementación de Heap Sort Secuencial ---
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

# --- 2. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000):
    """Genera una lista de números enteros aleatorios."""
    return [random.randint(0, max_value) for _ in range(cantidad)]

# --- 3. Bloque de Ejecución Principal ---
if __name__ == "__main__":

    # Heap Sort es O(n log n): 10^7 tarda minutos en Python y 10^8 requiere varios GB de RAM.
    EXPONENTES = [1, 2, 3, 4, 5, 6, 7]

    resultados = []

    print("--- Prueba de Rendimiento de Heap Sort SECUENCIAL (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")

    for exponente in EXPONENTES:
        N = 10 ** exponente

        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")

        # Los datos se generan FUERA de la medición de tiempo
        unsorted_data = generar_datos_aleatorios(N)

        start_time = time.perf_counter()
        sorted_data = heap_sort(unsorted_data.copy())
        end_time_total = time.perf_counter() - start_time

        resultados.append({
            "Exponente": exponente,
            "N": N,
            "Tiempo (s)": end_time_total
        })

        print(f"✅ Prueba de N={N:,} completada. Tiempo: {end_time_total:.6f} segundos.")

    # --- TABLA DE RESUMEN ---
    print("\n\n========================================================")
    print("📊 RESUMEN DE TIEMPOS DE EJECUCIÓN SECUENCIAL (N = 10^Exponente)")
    print("========================================================")
    print(f"| {'Exponente':<10} | {'N (Cantidad)':<15} | {'Tiempo (segundos)':<20} |")
    print(f"| {'-'*10:<10} | {'-'*15:<15} | {'-'*20:<20} |")

    for res in resultados:
        print(f"| 10^{res['Exponente']:<7} | {res['N']:<15,} | {res['Tiempo (s)']:.6f}{'':<14} |")

    print("========================================================")
