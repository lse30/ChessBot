import sys, pygame
pygame.init()
MARGIN = 10
size = width, height = 820, 820
black = 0, 0, 0

square_colours = [(240, 217, 181), (181,136,99)]

game_display = pygame.display.set_mode(size)
pygame.display.set_caption("Chess")
pieces = pygame.image.load("pieces.png")
pieces = pygame.transform.scale(pieces, (600,200))
#king = pieces.subsurface((100, 100, 200, 200))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    game_display.fill(black)

    for i in range(8):
        for j in range(8):
            colour = square_colours[(i+j)%2]
            pygame.draw.rect(game_display, colour, [(i*100) + MARGIN,(j*100) + MARGIN,100,100])
    game_display.blit(pieces, (210,210))
    pygame.display.update()