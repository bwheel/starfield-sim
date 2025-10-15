
import pygame
import esper

from starfield_sim import constants
from starfield_sim import processors
from starfield_sim import entities


def main():
    try:
        pygame.init()
        screen: pygame.Surface = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        width = screen.get_width()
        height = screen.get_height()
        pygame.display.set_caption("Starfield Simulation")

        esper.add_processor(processors.MovementProcessor())
        esper.add_processor(processors.BoundsProcessor(screen=screen))
        esper.add_processor(processors.RenderProcessor(screen=screen))
        esper.add_processor(processors.VelocityUpdateProcessor(screen=screen))

        for _i in range(500):
            entities.init_star(width, height)
        
        clock = pygame.time.Clock()
        delta_time = 0
        running = True
        while running:
            # Delta time in seconds
            delta_time = clock.tick(60) / 1000.0  # Converts milliseconds to seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            screen.fill(constants.BACKGROUND_COLOR)
            esper.process(delta_time)
            pygame.display.flip()

    finally:
        pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(str(ex))
