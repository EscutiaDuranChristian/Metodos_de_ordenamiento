import random
import time

# --- 1. Implementación de Merge Sort Secuencial ---
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    return merge(left_sorted, right_sorted)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

# --- 2. Función para Generar Datos Aleatorios ---
def generar_datos_aleatorios(cantidad, max_value=1_000_000):
    """Genera una lista de números enteros aleatorios."""
    return [random.randint(0, max_value) for _ in range(cantidad)]

# --- 3. Bloque de Ejecución Principal ---
if __name__ == "__main__":
    
    # Exponentes base 10: 10^1, 10^2, 10^3, 10^4, 10^5, 10^6
    # Puedes ajustar esta lista según lo que quieras probar (ej. [1, 2, 3, 4, 5, 6])
    EXPONENTES = [1, 2, 3, 4, 5, 6, 7, 8] 
    
    resultados = []
    
    print("--- Prueba de Rendimiento de Merge Sort SECUENCIAL (10^N) ---")
    print(f"Exponentes a probar: {EXPONENTES}")
    print("------------------------------------------------------------")
    
    for exponente in EXPONENTES:
        # CAMBIO 1: Cálculo con base 10 (10^1, 10^2, ...)
        N = 10 ** exponente
        
        print(f"\nGenerando lista para N = 10^{exponente} = {N:,} elementos...")
        
        # ⚠️ Los datos se generan FUERA de la medición de tiempo
        unsorted_data = generar_datos_aleatorios(N)
        
        # CAMBIO 2: Medición correcta del tiempo (Solo del algoritmo)
        start_time = time.perf_counter()

        # Ejecutamos el ordenamiento sobre una copia de los datos
        sorted_data = merge_sort(unsorted_data.copy())

        end_time_total = time.perf_counter() - start_time
        
        # Guardar resultado
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