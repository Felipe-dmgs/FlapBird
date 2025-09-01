import pygame
import os
import random


#Inicilizar o mixer de som

pygame.mixer.init()

TELA_WIDTH = 500;

TELA_HEIGHT = 800;# LETRA MAIUSCULA = CONSTANTE, LETRAS MAIUSCULAS E MINUSCULAS OU SO MINUSCULAS = VARIAVVEIS


IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")));

IMAGE_FLOOR = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")));

IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")));

IMAGEM_BIRD = [

    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),

    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),

    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))

];


pygame.font.init()

FONT_POINTS = pygame.font.SysFont('arial', 50);


#Funções da música

def tocar_musica(arquivo, loop=True):

    pygame.mixer.music.stop();

    pygame.mixer.music.load(arquivo);

    pygame.mixer.music.play(-1 if loop else 0);

#o pygame começa o plano cartesiano  no canto superior esquerdo onde o ponto 0,0 e o canto superior esquero e quando mais para baixo maior o número, para cima menor nesse jogo para subirmos temos que colocar -10 assim descemos 10 pixeis mas na tela a gente sobe os 10

class Bird:

    IMGS = IMAGEM_BIRD;

    #rotation animation

    MAX_ROTATION = 25;

    SPEED_ROTATION = 20;

    TIME_ANIM = 5;


    def __init__(self,x,y):

        self.x = x;

        self.y = y;

        self.angle = 0;

        self.speed = 0;

        self.height = self.y;

        self.time = 0;

        self.count_img = 0;

        self.image = self.IMGS[0];


    def jump(self):

        self.speed = -10.5;

        self.time = 0;

        self.height = self.y;
    

    def move(self):

        #Calcula o deslocamento

        self.time += 1;

        deslocamento = 1.5 * (self.time**2) + self.speed * self.time

        #restringir deslocamento

        if deslocamento > 16:

            deslocamento = 16;

        elif deslocamento < 0:

            deslocamento -= 2;

        self.y += deslocamento;


        #Angulo do passaro

        if deslocamento < 0 or self.y < (self.height + 50):

            if self.angle < self.MAX_ROTATION:

                self.angle = self.MAX_ROTATION;

        else:

            if self.angle > -90:

                self.angle -= self.SPEED_ROTATION;

    def desenhar(self, tela):

        #Definir qual imagem o passaro ira aparecer

        self.count_img += 1;


        if self.count_img < self.TIME_ANIM:

            self.image = self.IMGS[0]

        elif self.count_img < self.TIME_ANIM*2:

            self.image = self.IMGS[1]

        elif self.count_img < self.TIME_ANIM*3:

            self.image = self.IMGS[2]

        elif self.count_img < self.TIME_ANIM*4:

            self.image = self.IMGS[1]

        elif self.count_img < self.TIME_ANIM*4 + 1:

            self.image = self.IMGS[0]

            self.count_img = 0


        #Se o passaro estiver caindo não pode bater as asas

        if self.angle <= -80:

            self.image = self.IMGS[1]

            self.count_img = self.TIME_ANIM*2


        #Desenhar a imagem

        rotate_image = pygame.transform.rotate(self.image, self.angle);

        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center;

        rectangle = rotate_image.get_rect(center=pos_center_image);

        tela.blit(rotate_image, rectangle.topleft);
    

    def get_mask(self):

        return pygame.mask.from_surface(self.image);



class Pipe:

    DISTANCE = 200

    SPD = 5


    def __init__(self, x):

        self.x = x;

        self.height = 0;

        self.pos_top = 0;

        self.pos_floor = 0;

        self.TOP_PIPE = IMAGE_PIPE;

        self.FLOOR_PIPE = pygame.transform.flip(IMAGE_PIPE, False, True);

        self.passTrough = False

        self.set_height()


    def set_height(self):

        self.height = random.randint(50, 450)

        self.pos_floor = self.height - self.TOP_PIPE.get_height()

        self.pos_top = self.height + self.DISTANCE


    def move(self):

        self.x -= self.SPD


    def desenhar(self, tela):

        tela.blit(self.TOP_PIPE, (self.x, self.pos_top))

        tela.blit(self.FLOOR_PIPE, (self.x, self.pos_floor))


    def collide(self, bird):

        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.TOP_PIPE)

        floor_mask = pygame.mask.from_surface(self.FLOOR_PIPE)


        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))#o round pega a posição do item

        distance_floor = (self.x - bird.x, self.pos_floor - round(bird.y))


        top_point = bird_mask.overlap(top_mask, distance_top)

        floor_point = bird_mask.overlap(floor_mask, distance_floor)


        if floor_point or top_point:

            return True

        else:

            return False


class Floor:

    SPD = 5

    WIDTH = IMAGE_FLOOR.get_width()

    IMAGE = IMAGE_FLOOR


    def __init__(self, y):

        self.y = y

        self.x1 = 0

        self.x2 = self.WIDTH


    def mover(self):

        self.x1 -= self.SPD

        self.x2 -= self.SPD


        if self.x1 + self.WIDTH <= 0:

            self.x1 = self.x2 + self.WIDTH;

        if self.x2 + self.WIDTH <= 0:

            self.x2 = self.x1 + self.WIDTH;


    def desenhar(self, tela):

        tela.blit(self.IMAGE, (self.x1, self.y));

        tela.blit(self.IMAGE, (self.x2, self.y));


#FUNÇÕES DO SISTEMA DO JOGO


def gameOver(tela):

    tocar_musica(os.path.join('sounds','gameover.ogg'), loop=False);


    font = pygame.font.SysFont('arial', 60)


    text_game_over = font.render('Game Over', True,(255,255,255))

    text_retry = FONT_POINTS.render('Retry', True, (255,255,255))


    #Button retry

    button_width = 200

    button_height = 60

    button_x = (TELA_WIDTH - button_width) // 2

    button_y = (TELA_HEIGHT - button_width) //2 +50

    button_rect = pygame.Rect(button_x,button_y,button_width,button_height)


    while True:

        tela.blit(IMAGE_BACKGROUND, (0,0))

        tela.blit(text_game_over, ((TELA_WIDTH - text_game_over.get_width())//2, 200))


        pygame.draw.rect(tela, (0,100,200), button_rect)

        tela.blit(text_retry, (

            button_x, (button_width - text_retry.get_width()) // 2,

            button_y, (button_height - text_retry.get_height()) // 2,
        ))

        pygame.display.update()


        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button_rect.collidepoint(event.pos):

                    return True


def desenhar_tela(tela, birds, pipes, floor, points):

    tela.blit(IMAGE_BACKGROUND, (0,0))


    for bird in birds:

        bird.desenhar(tela)


    for pipe in pipes:

        pipe.desenhar(tela)


    floor.desenhar(tela)

    texto = FONT_POINTS.render(f'Pontuação {points}',1,(255,255,255));

    tela.blit(texto, (TELA_WIDTH - 10 - texto.get_width(), 10))


    pygame.display.update()


def main():

    tocar_musica(os.path.join('sounds', 'overflow.ogg'), loop= True)


    birds = [Bird(230, 350)]

    floorO = Floor(730)

    pipes = [Pipe(700)]

    tela = pygame.display.set_mode((TELA_WIDTH, TELA_HEIGHT))

    points = 0

    clock = pygame.time.Clock()


    #loop do jogo

    playing = True

    while playing:

        clock.tick(30)

        #Interação com o usuário

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

                playing = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    for bird in birds:

                        bird.jump()

        #Mover coisas

        for bird in birds:

            bird.move()

        floorO.mover()


        add_pipe = False

        remove_pipe = []

        for pipe in pipes:

            for i, bird in enumerate(birds):

                if pipe.collide(bird):

                    if gameOver(tela):
                        main()

                    else:

                        playing = False

                        pygame.quit()

                        quit()

                if not pipe.passTrough and bird.x > pipe.x:

                    pipe.passTrough = True

                    add_pipe = True

            pipe.move()

            if pipe.x + pipe.TOP_PIPE.get_width() < 0:

                remove_pipe.append(pipe)

        if add_pipe:

            points += 1

            pipes.append(Pipe(600))
        

        for pipe in remove_pipe:

            pipes.remove(pipe)


        for i, bird in enumerate(birds):

            if (bird.y + bird.image.get_height()) > floorO.y or bird.y < 0:

                if gameOver(tela):
                    main()

                else:

                    playing = False

                    pygame.quit()

                    quit()

        desenhar_tela(tela, birds, pipes, floorO, points)


if __name__ == '__main__':
    main()

