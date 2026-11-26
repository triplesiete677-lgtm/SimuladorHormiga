#Marcos Altamirano
import time
from concurrent.futures import ProcessPoolExecutor

from models import Ant, GameState
from simulation import update
from parallel import update_parallel, WORKERS, CPU_CORES
from main import create_initial_state


def medir_secuencial(estado, repeticiones):
    inicio = time.perf_counter()

    for _ in range(repeticiones):
        update(estado, (), 1 / 60)

    fin = time.perf_counter()
    return fin - inicio


def medir_paralelo(estado, repeticiones, executor):
    inicio = time.perf_counter()

    for _ in range(repeticiones):
        update_parallel(estado, (), 1 / 60, executor)

    fin = time.perf_counter()
    return fin - inicio


def main():
    cantidades = (1000, 3000, 5000, 8000)
    repeticiones = 10

    print("======================================")
    print(" BENCHMARK - SIMULADOR DE HORMIGAS")
    print("======================================")
    print("Núcleos detectados:", CPU_CORES)
    print("Workers utilizados:", WORKERS)
    print("Repeticiones:", repeticiones)

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        for cantidad in cantidades:
            estado = create_initial_state(cantidad)

            tiempo_secuencial = medir_secuencial(
                estado, repeticiones
            )

            tiempo_paralelo = medir_paralelo(
                estado, repeticiones, executor
            )

            velocidad_secuencial = (
                repeticiones / tiempo_secuencial
            )

            velocidad_paralela = (
                repeticiones / tiempo_paralelo
            )

            aceleracion = (
                tiempo_secuencial / tiempo_paralelo
            )

            print("\nHormigas:", cantidad)
            print(f"Tiempo secuencial: {tiempo_secuencial:.4f} s")
            print(f"Tiempo paralelo: {tiempo_paralelo:.4f} s")
            print(
                f"Actualizaciones secuenciales/s: "
                f"{velocidad_secuencial:.2f}"
            )
            print(
                f"Actualizaciones paralelas/s: "
                f"{velocidad_paralela:.2f}"
            )
            print(f"Aceleración: {aceleracion:.2f}x")

if _name_ == "_main_":
    main()
