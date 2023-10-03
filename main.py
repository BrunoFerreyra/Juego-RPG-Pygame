import pygame

from sprites import *

from config import *
#NOTA: * significa importar todo

import sys

class Game:
    def __init__(self):
        #Se inicializa el modulo pygame
        pygame.init()
        #Se establece el tamaño de la ventana, variables en config.py 
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        #Framerate (tasa de refresco) del juego
        self.clock = pygame.time.Clock()
        #Fuente
        #self.font = pygame.font.Font('Arial', 32)
        #self.running es un booleando que vamos a usar cuando queramos parar el juego
        self.running = True
        
        #instancio el personaje
        self.character_spritesheet = Spritesheet("img/character.png")
        
        #
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        
    # Creo el mapa (metodo que dibuja el mapa, sera llamado en new)
    def createTileMap(self):
        """ i es la posicion de la lista
            row es cada caracter
            entonces:
            for i, row in enumerate(tilemap):
                print(i,row)
            muestra todos los caracteres de cada espacio de la lista
        """
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self,j,i)
                if column == "P":
                    Player(self,j,i)
                # if column == ".":
                #    Grass(self,j,i)
    
    def new(self):
        
        #Empieza un juego nuevo
        self.playing = True
        
        #all_sprites es el grupo de sprites(personaje u objeto) 
        #Es un objeto que contendra todos los sprites del juego (personaje, paredes, enemigos)
        #entonces podemos a actualizar  a todos juntos  
        self.all_sprites = pygame.sprite.LayeredUpdates()
        
        #y despues estan los demas por separado
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates() #no tengo claro que es, dice "la animacin del ataque"
        
        #en la instanciacion player: el self se refiere a esta clase Game y manda el objeto instanciado game 
        #luego para los parametros (x,y) = (1,2) es porque en la clase player lo multiplica por la constante (32)
        #entonces el player va a quedar de 32 de ancho x 64 de alto
        self.player = Player(self, 1, 2)
        
        #dibujo el mapa:
        self.createTileMap()
    def events(self):
        #Todo lo que apretemos en el teclado
        
        #pygame.event.get() va a escuchar CADA evento que pase en pygame
        for event in pygame.event.get(): 
            #Este metodo es para cuando apretamos la X de cerrar, es decir
            #que esta constantemente viendo si apretamos ese boton, y cuando lo hacemos
            #para el juego cambiando las variables booleanas
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                
    def update(self):
        #game loop updates
        #actualiza el juego todo el tiempo para que no sea una imagen estatica
        
        #gracias a esto y al metodo LayeredUpdates del metodo New()
        #va a ir al metodo update de CADA SPRITE y correrlo
        #En español: mantener todo actualziado
        self.all_sprites.update()
    
    def draw(self):
        #va a mostrar todos los objetos en la pantalla 
        
        #seteamos / dibujamos el fondo de pantalla
        #screen lo creamos en el cons tructor te acordas?
        self.screen.fill(BLACK)
        
        #dibuja TODOS los objetos contenidos en all_sprites
        #" se fija enn su image y rectangulo y lo dibuja en la ventana"
        self.all_sprites.draw(self.screen)
        #setea la taza de refresco de dibujo:
        self.clock.tick(FPS)
        #actualiza la pantalla:
        pygame.display.update()

    def main(self):
        # game loop
        #mientras self.playing sea true significa que se esta jugando entonces se corren los metodos en loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
        #una vez se termino de jugar (self.playing += False)se cambia self.running a false
        self.running = False

    def game_over(self):
        pass
    def intro_screen(self):
        pass
    

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()
    
pygame.quit()
sys.exit()