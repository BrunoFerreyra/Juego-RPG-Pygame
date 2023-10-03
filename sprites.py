import pygame
from config import *
import math
import random


class Spritesheet:
    """Como las cada imagen no es estatica sino que tiene animaciones
    esta clase va a cargar cada animacion de cada png , ya que 
    hacer con cada animacion el " pygame.image.load("img/single.png ") "
    no solo llevara mucho tiempo de codigo sino que tambien realentizara mucho el programa
    
    Dicho con mejor vocabulario:
    cada imagen es un "spritesheet", es decir, todas las animaciones de un mismo personaje
    ahora el metodo get_sprite va a acceder a un sprite particular del spritesheet
    
    """
    #file es el png que estemos cargando
    def __init__(self,file):
        self.sheet = pygame.image.load(file).convert()
        # "el convert() carga la imagen mas rapidamente para que el juego no se realentize" 

    def get_sprite(self, x, y, width, height):
        #var sprite crea la superficie del tamaño deseado 
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        #la ultima tupla "(x, y, width, height)" va a cortar puntualmente el sprite que desea del spriteSheet

        #como el fondo es BLACK le seteamos black asi es transparente
        sprite.set_colorkey(BLACK)
        return sprite
    
    
    
    
    
#pygame.sprite.Sprite es una clase del modulo pygame, de la que heredamos para crear el personaje
#para hacerlo  mucho mas facil 
class Player(pygame.sprite.Sprite):
    #"Agregando game vamos a poder acceder a la clase Game de main.py"
    #x e y van a ser el punto de la pantalla en el que va a aparecer nuestrop personajef
    def __init__(self, game, x, y):
        
        self.game = game
        #layer(capa) se usa para indicar el orden en que se muestra cada cosa
        #por ejemplo el cesped va a ser una capa por debajo del personaje
        #para que el personaje sea lo ultimo en ser dibujado
        self._layer = PLAYER_LAYER
        #con "self.goup" estamos agregando al jugador  al grupo "all_sprites" (main, clase Game)
        #podemos acceder a "all_sprites" porque le pasamos el objeto game como parametro
        self.groups = self.game.all_sprites
        #se llama al constructor de la clase heredada 
        #y pasandole self.groups le estamos añadiendo el jugador al grupo "all_sprites"
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #Como es un juego de cuadrados (tail based) tenemos que definir el tamaño del cuadrado
        # (todo es un cuadrado) objetos personajes enemigos etc
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        #VARIABLES TEMPORALES
        #sirven para que se instancie el player con ese valor, luego se van
        #a ir cambiando segun el movimiento en el game loop
        #dicho de otra manera los cambios sobre estas variables (movimiento) van a estar durante un loop
        self.x_change = 0
        self.y_change = 0
        
        #la animacion tiene un conjunto de imagenes, que "miran" a distintos lados
        #vamos a instanciar con la predeterminada hacia abajo
        self.facing = 'down'
        
        
        #Ahora seteamos la imagen del jugador
        #lo que creamos aca es solo un rectangulo, "la superficie"
        #nuestro personaje va a ser un rectangulo de 32x32
        # ya no necesitamos pygame.surface  porque traemos la imagen del spritsheet
        #self.image =  pygame.Surface([self.width, self.height])
        #x,y van con 3y2 porque la imagen puntualmente empieza a dibujar ahi
        self.image = self.game.character_spritesheet.get_sprite(132,80, self.width, self.height)
        
        #self.image.fill(RED) 
        #" el image es como se ve, el rect es donde esta posicionado"
        # es el hitbox  
        #tiene que ser igual a la imagen ( preferentemente obvio) asique seteamos eso:
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def update(self):
        self.movement()
        
        #cargamos los cambios de movimiento sobre "el jugador" (es decir el cuadrado)
        #recordemos que x_change es la variable temporal que nacio en 0 , luego movement() la cambia en funcion
        #de lo que apretemos, y aca es donde efectuamos ese movimiento
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        
        #seteamos denuevo en 0 a las variables temporales para que el cuadrado no se quede moviendo eternamente
        self.x_change = 0
        self.y_change = 0
        
    def movement(self):
        # escucha cada tecla apretada en el teclado
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED 
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys [pygame.K_UP]:
            #en pygame el eje Y arranca arriba en 0 y baja aumentando
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
        # LO MISMO PARA EL KIT WASD
        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED 
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys [pygame.K_w]:
            #en pygame el eje Y arranca arriba en 0 y baja aumentando
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'
            
class Block (pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        #cada bloque va a tener una posicion en x e y
        #traigo el objeto game (clase Game() de main)_ 
        self.game = game
        #hay que decirle a pygame en que capa va a aparecer
        #para manejar las prioridades
        self._layer = BLOCK_LAYER
        
        self.groups = self.game.all_sprites, self.game.blocks
        #esto es como un Super() de la clase padre pygame.sprite.sprite 
        #a la que le agregamos el grupo creado de bloques
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        #definino el tamaño del bloque
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        #seteamos la superficie del bloque terrain_spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(960, 448, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
#La clase "Ground" va a contener y dibujar el cesped,
#llamara a la clase spritesheet para que corte la imagen del cesped que deseemos

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y):
        
        self.game = game
        
        self._layer = GROUND_LAYER
        
        self.groups = self.game.all_sprites
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.image = self.game.terrain_spritesheet.get_sprite(400,290, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y