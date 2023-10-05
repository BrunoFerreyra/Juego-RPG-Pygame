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
        self.animation_loop = 1
        
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
        self.animate()
        #cargamos los cambios de movimiento sobre "el jugador" (es decir el cuadrado)
        #recordemos que x_change es la variable temporal que nacio en 0 , luego movement() la cambia en funcion
        #de lo que apretemos, y aca es donde efectuamos ese movimiento
        self.rect.x += self.x_change
        self.collide_blocks('x')  #CHEQUEAMOS COLISION
        self.rect.y += self.y_change
        self.collide_blocks('y')  #CHEQUEAMOS COLISION
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
    
    #Metodo que se ocupa de controlar colisiones
    def collide_blocks(self, direction):
        #self es el personaje
        if direction =='x':
            # hits: variable booleana
            # spritecollide() va a chequear si un cuadrado esta dentro de otro
            #en este caso, self(player) dentro de un block (en el que no debemos entrar)
            #entonces cuando este se ponga en true (porque hiteo)
            #entonces hay que volver a poner al jugador en el limite
            #recordar que self.game.blocks contiene CADA bloque del juego (los de colision )
            #Ultimo parametro (false) es para deletear el sprite cuando colisione
            #como no queremos que pase ponemos false, probaremos luego con true
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0: #es decir estamos yendo a la derecha (si no entendes fijate la asignacion de teclas en movement())
                    self.rect.x = hits[0].rect.left - self.rect.width
                    #coloca al personaje justo a la izquierda del bloque
                if self.x_change < 0: #izquierda
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0: #esta bajando
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    
    #Metodo que se ocupa de colocar animaciones segun la direccion de movimiento
    def animate(self):
        #las siguientes listas contienen los recortes de la animacion (3 por direccion)
        down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        if self.facing == "down":
            if self.y_change == 0: # si estamos quietos
                #si esta mirando para abajo, mostrar una de las 3 animaciones que miran para abajo
                self.image = self.game.character_spritesheet.get_sprite(3,2,self.width, self.height)
            else: #si no estamos quietos:
                #animation_loop es solo una variable que va aumentando en 0.1 con la linea de abajo
                #entonces cada 10 frames pasara de 0 a 1 entonces cambiara la animacion
                #hasta que llegue a 3 y entonces vuelva a 1
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing =="up":
            if self.y_change == 0: # si estamos quietos
                self.image = self.game.character_spritesheet.get_sprite(3,34,self.width, self.height)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "right":
            if self.x_change == 0: # si estamos quietos
                    self.image = self.game.character_spritesheet.get_sprite(3, 66,self.width, self.height)
            else:                 
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
            
        if self.facing == "left":    
            if self.x_change == 0: # si estamos quietos
                self.image = self.game.character_spritesheet.get_sprite(3, 98,self.width, self.height)
            else: 
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
            
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