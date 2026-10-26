import pygame, sys

width, height = 1000, 1000
screen = pygame.display.set_mode(size=(width, height), flags=pygame.SCALED)
pygame.display.set_caption("Cornell College Engineering Club Robot Controller")


DARK_GRAPHITE = (50, 48, 49)
GRAPHITE = (61, 59, 60)
STRONG_CYAN = (89, 195, 195)
PLATINUM = (235, 235, 235)
BUBBLEGUM_PINK = (244, 91, 105)

screen.fill(DARK_GRAPHITE)

while True:

    # Analog stick boxes
    pygame.draw.rect(screen, GRAPHITE, (175, 100, 300, 300))
    pygame.draw.rect(screen, GRAPHITE, (width//2 + 25, 100, 300, 300))

    pygame.draw.line(screen, PLATINUM, (175 + 300/2, 100), (175 + 300/2, 100 + 300))
    pygame.draw.line(screen, PLATINUM, (175, 100 + 300/2), (175 + 300, 100 + 300/2))
    
    pygame.draw.line(screen, PLATINUM, (width//2 + 25 + 300/2, 100), (width//2 + 25 + 300/2, 100 + 300))
    pygame.draw.line(screen, PLATINUM, (width//2 + 25, 100 + 300/2), (width//2 + 25 + 300, 100 + 300/2))

    # Triggers
    pygame.draw.rect(screen, GRAPHITE, (50, 200, 100, 200))
    pygame.draw.rect(screen, GRAPHITE, (width-50-100, 200, 100, 200))

    # Bumpers
    pygame.draw.rect(screen, GRAPHITE, (50, 100, 100, 75))
    pygame.draw.rect(screen, GRAPHITE, (width-50-100, 100, 100, 75))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()