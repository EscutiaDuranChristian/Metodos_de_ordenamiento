import random
import time

# --- 1. Implementación de Quick Sort Secuencial ---
def quick_sort(arr):
    """Ordena la lista con Quick Sort (O(n log n) promedio). Modifica y devuelve arr.

    Versión iterativa con partición de Hoare y pivote aleatorio: evita el límite
    de recursión de Python y maneja bien los valores repetidos.
    """
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            pivot = arr[random.randint(lo, hi)]
            i, j = lo, hi
            while i <= j:
                while arr[i] < pivot:
                    i += 1
                while arr[j] > pivot:
                    j -= 1
                if i <= j:
                    arr[i], arr[j] = arr[j], arr[i]
                    i += 1
                    j -= 1
            # Procesar primero la parte menor y apilar la mayor (pila O(log n))
            if j - lo < hi - i:
                stack.append((i, hi))
                hi = j
            else:
                stack.append((lo, j))
                lo = i
    return arr

# --- 2. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000):
    """Genera una lista de números enteros aleatorios."""
    return [random.randint(0, max_value) for _ in range(cantidad)]

# --- 3. Bloque de Ejecución Principal ---
if __name__ == "__main__":

    # Quick Sort es O(n log n) promedio: 10^7 tarda minutos en Python y 10^8 requiere varios GB de RAM.
    EXPONENTES = [1, 2, 3, 4, 5, 6, 7, 8]

    resultados = []

    print("--- Prueba de Rendimiento de Quick Sort SECUENCIAL (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")

    for exponente in EXPONENTES:
        N = 10 ** exponente

        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")

        # Los datos se generan FUERA de la medición de tiempo
        unsorted_data = generar_datos_aleatorios(N)

        start_time = time.perf_counter()
        sorted_data = quick_sort(unsorted_data.copy())
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
