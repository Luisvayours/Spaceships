import pygame
import os
pygame.font.init()

#Game options and constants
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship fight")
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
FPS = 60
BALAS_TOTALES = 3
FUENTEVIDA = pygame.font.SysFont('comicsans', 40)
FUENTEVICTORIA = pygame.font.SysFont('comicsans', 40)

PLAYER_WIDTH, PLAYER_HEIGHT = 55 ,40
JUGADOR1_GOLPE = pygame.USEREVENT+1
JUGADOR2_GOLPE = pygame.USEREVENT+2
NAVE1_CARGA = pygame.image.load(os.path.join('assets','spaceship_red.png'))
NAVE1 = pygame.transform.rotate(pygame.transform.scale
(NAVE1_CARGA, (PLAYER_WIDTH,PLAYER_HEIGHT)), 90)
NAVE2_CARGA = pygame.image.load(os.path.join('assets','spaceship_yellow.png'))
NAVE2 = pygame.transform.rotate(pygame.transform.scale
(NAVE2_CARGA, (PLAYER_WIDTH,PLAYER_HEIGHT)), 270)
fondo = pygame.transform.scale(pygame.image.load(os.path.join('assets','space.png')), (WIDTH,HEIGHT))

                                
def draw_window (jugador1, jugador2, BALAS1, BALAS2, vida1, vida2):
    WIN.blit(fondo,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    vida_jugador1 = FUENTEVIDA.render("Vida: " + str(vida1), 1, WHITE)
    vida_jugador2 = FUENTEVIDA.render("Vida: " + str(vida2), 1, WHITE)
    WIN.blit(vida_jugador1, (10,10))
    WIN.blit(vida_jugador2, (WIDTH - vida_jugador2.get_width() -10 ,10))
    WIN.blit(NAVE1, (jugador1.x, jugador1.y))
    WIN.blit(NAVE2, (jugador2.x, jugador2.y))
    for bala in BALAS1:
        pygame.draw.rect(WIN, RED, bala)
    for bala in BALAS2:
        pygame.draw.rect(WIN, YELLOW, bala)
    pygame.display.update()
    
def mov_jug_1(tecla_pul, jugador1):
    if tecla_pul[pygame.K_a] and jugador1.x - 5 > 0:
            jugador1.x -= 5
    if tecla_pul[pygame.K_d] and jugador1.x + 5 + jugador1.height < BORDER.x:
            jugador1.x += 5
    if tecla_pul[pygame.K_s] and jugador1.y + 5 < HEIGHT-jugador1.width: 
            jugador1.y += 5
    if tecla_pul[pygame.K_w] and jugador1.y > 5:
            jugador1.y -= 5
            
def mov_jug_2(tecla_pul, jugador2):
    if tecla_pul[pygame.K_LEFT] and jugador2.x - 5 - BORDER.width  > BORDER.x:
            jugador2.x -= 5
    if tecla_pul[pygame.K_RIGHT] and jugador2.x + 5 < WIDTH-jugador2.height:
            jugador2.x += 5
    if tecla_pul[pygame.K_DOWN] and jugador2.y + 5 < HEIGHT-jugador2.width:
            jugador2.y += 5
    if tecla_pul[pygame.K_UP] and jugador2.y > 5:
            jugador2.y -= 5

def colision_balas(BALAS1, BALAS2, jugador1, jugador2):
    for bala in BALAS1:
        bala.x += 10
        if jugador2.colliderect(bala):
            pygame.event.post(pygame.event.Event(JUGADOR2_GOLPE))
            BALAS1.remove(bala)
        if bala.x > WIDTH:
            BALAS1.remove(bala)
    for bala in BALAS2:
        bala.x -= 10
        if jugador1.colliderect(bala):
            pygame.event.post(pygame.event.Event(JUGADOR1_GOLPE))
            BALAS2.remove(bala)
        if bala.x < 0:
            BALAS2.remove(bala)
            
def ganador(texto_vic):
    dibujatexto = FUENTEVICTORIA.render(texto_vic,1,WHITE)
    WIN.blit(dibujatexto, (WIDTH/2 - dibujatexto.get_width()/2, HEIGHT/2-dibujatexto.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    

def main ():
    jugador1 = pygame.Rect(100,300, PLAYER_WIDTH, PLAYER_HEIGHT)
    jugador2 = pygame.Rect(700,300, PLAYER_WIDTH, PLAYER_HEIGHT)
    vida1 = 10 
    vida2 = 10
    BALAS1 = []
    BALAS2 = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(BALAS1)<BALAS_TOTALES:
                    bala = pygame.Rect(jugador1.x + jugador1.height, jugador1.y + jugador1.width//2 -2 ,10,5)
                    BALAS1.append(bala)
                if event.key == pygame.K_RCTRL and len(BALAS2)<BALAS_TOTALES:
                    bala = pygame.Rect(jugador2.x , jugador2.y + jugador2.width//2 -2 ,10,5)
                    BALAS2.append(bala)
           
            if event.type == JUGADOR1_GOLPE:
                vida1 -= 1
            if event.type == JUGADOR2_GOLPE:
                vida2 -= 1
        
        texto_vic =""
        if vida1 <= 0:
            texto_vic="Jugador 2 gana"
            
        if vida2 <= 0:
            texto_vic="Jugador 1 gana"
            
        if texto_vic != "":
            ganador(texto_vic)
            break
        
        tecla_pul = pygame.key.get_pressed()
        mov_jug_1(tecla_pul, jugador1)
        mov_jug_2(tecla_pul, jugador2)
        draw_window(jugador1, jugador2, BALAS1, BALAS2, vida1, vida2)
        colision_balas(BALAS1,BALAS2, jugador1,jugador2)
    main() 
    
if __name__ == "__main__":
    main()