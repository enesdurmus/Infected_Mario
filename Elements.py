import pygame

class Element(pygame.sprite.Sprite):
    def __init__(self, width, height, image_path, x=0, y=0):
        super(Element, self).__init__()
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.move_to(x,y)

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Map:
    def getMap(map_name):

        file = open(map_name)
        data = file.read()
        file.close()
        data = data.split('\n')
        game_map = []
        for x in data:
            a = []
            for y in range(len(x)):
                a.append(x[y])
            game_map.append(a)
        return game_map

class Bullet(Element):
    def __init__(self, width, height, image_path, x=0, y=0):
        super().__init__(width, height, image_path, x=0, y=0)
        self.move_to(x,y)

    def move_up(self, pixels=5):
         self.rect.y -= pixels

    def move_right(self, pixels=5):
        self.rect.x += pixels

    def move_left(self, pixels=5):
          self.rect.x -= pixels


