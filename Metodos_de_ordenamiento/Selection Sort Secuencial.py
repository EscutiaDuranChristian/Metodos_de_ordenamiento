import random
import time

# --- 1. Implementación de Selection Sort Secuencial ---
def selection_sort(arr):
    """Ordena la lista con Selection Sort (O(n^2)). Modifica y devuelve arr."""
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

# --- 2. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000):
    """Genera una lista de números enteros aleatorios."""
    return [random.randint(0, max_value) for _ in range(cantidad)]

# --- 3. Bloque de Ejecución Principal ---
if __name__ == "__main__":

    # Selection Sort es O(n^2): 10^5 tarda minutos y 10^6+ es inviable en Python.
    EXPONENTES = [1, 2, 3, 4, 5]

    resultados = []

    print("--- Prueba de Rendimiento de Selection Sort SECUENCIAL (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")

    for exponente in EXPONENTES:
        N = 10 ** exponente

        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")

        # Los datos se generan FUERA de la medición de tiempo
        unsorted_data = generar_datos_aleatorios(N)

        start_time = time.perf_counter()
        sorted_data = selection_sort(unsorted_data.copy())
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
