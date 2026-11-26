#Marcos Altamirano

import math
import pygame

from concurrent.futures import ProcessPoolExecutor

from models import Ant, GameState
from simulation import update, NEST
from parallel import update_parallel, CPU_CORES, WORKERS
from rendering import draw_world

WIDTH = 1000
HEIGHT = 700

def create_initial_state(amount):
    """Crea una colonia inicial de hormigas."""

    ants = tuple(
        Ant(
            id=i,
            x=NEST[0] + math.cos(i * 0.15) * (i % 30),
            y=NEST[1] + math.sin(i * 0.15) * (i % 30),
            carrying=False
        )
        for i in range(amount)
    )

    return GameState(ants=ants)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulador de Colonia de Hormigas")

    clock = pygame.time.Clock()

    amount = 1000
    state = create_initial_state(amount)

    mode = "SECUENCIAL"
    running = True

    print("Núcleos detectados:", CPU_CORES)
    print("Workers configurados:", WORKERS)

    # Se crea el grupo de procesos una sola vez.
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:

        while running:
            dt = min(clock.tick(60) / 1000.0, 0.05)

            events = ()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_1:
                        mode = "SECUENCIAL"

                    elif event.key == pygame.K_2:
                        mode = "PARALELO"

                    elif event.key == pygame.K_F1:
                        amount = 1000
                        state = create_initial_state(amount)

                    elif event.key == pygame.K_F2:
                        amount = 3000
                        state = create_initial_state(amount)

                    elif event.key == pygame.K_F3:
                        amount = 5000
                        state = create_initial_state(amount)

                    elif event.key == pygame.K_r:
                        events = ("reset_score",)

            # Actualizar el estado del juego.
            if mode == "SECUENCIAL":
                state = update(state, events, dt)

            else:
                state = update_parallel(
                    state,
                    events,
                    dt,
                    executor
                )

            # Dibujar el estado nuevo.
            draw_world(
                screen,
                state,
                mode,
                WORKERS if mode == "PARALELO" else 1,
                clock.get_fps()
            )

    pygame.quit()

if __name__ == "__main__":
    main()
