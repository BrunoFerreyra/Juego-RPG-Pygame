WIN_WIDTH = 640
WIN_HEIGHT= 480
TILESIZE = 32
FPS = 60

PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
#tilemap = mapa de mosaicos
#como cada mosaico es de 32x32 y la altura es de 480 px:
#480 / 32 = 15 mosaicos
#640 / 32 = 20 mosaicos (ancho)

tilemap = [
    #Cada fila es un string
    #cada columna es un caracter
    'BBBBBBBBBBBBBBBBBBBB',
    'B..................B',
    'B..................B',
    'B...B.B............B',
    'B...B..............B',
    'B...B...B..........B',
    'B.......B..........B',
    'B...BBBB...........B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B..................B',
    'B.........p........B',
    'B..................B',
    'BBBBBBBBBBBBBBBBBBBB'
    
]