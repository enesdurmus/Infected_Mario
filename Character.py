import pygame


class Character():
    def __init__(self, width, height, image_path, x=0, y=0):
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.isMarioOnTheGround = True
        self.move_to(x,y)
        self.face_way="right"
        self.gravity = 0.20
        self.down_speed2 = 1
        self.down_speed = -10
        self.hero_right_animation = []
        self.hero_left_animation = []
        self.hero_jump_right_animations = []
        self.hero_jump_left_animations = []
        self.hero_stand_left_animation = []
        self.hero_stand_right_animation = []
        self.hero_throwing_animations_right = []
        self.hero_throwing_animations_left = []

        x = 1
        while x <= 12:
            self.hero_right_animation.append(pygame.transform.scale(pygame.image.load("images/character_animations"
                                                                                 "/hero_right_movement_animation"
                                                                                 "/hero_right_movement_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 12:
            self.hero_left_animation.append(pygame.transform.scale(pygame.image.load("images/character_animations"
                                                                                "/hero_left_movement_animation"
                                                                                "/hero_left_movement_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 18:
            self.hero_stand_left_animation.append(pygame.transform.scale(pygame.image.load(
                "images/character_animations/hero_stand/hero_stand_left/hero_stand_left_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 18:
            self.hero_stand_right_animation.append(pygame.transform.scale(pygame.image.load(
                "images/character_animations/hero_stand/hero_stand_right/hero_stand_right_" + str(x) + ".png"),
                                                                     (40, 80)))
            x += 1
        x = 1
        while x <= 6:
            self.hero_jump_right_animations.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/hero_jump_right/hero_jump_start_" + str(x) + ".png"),
                (40, 80)))
            x += 1
        x = 1
        while x <= 6:
            self.hero_jump_right_animations.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/hero_jump_right/hero_jump_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 6:
            self.hero_jump_left_animations.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/hero_jump_left/hero_jump_start_" + str(x) + ".png"),
                (40, 80)))
            x += 1
        x = 1
        while x <= 6:
            self.hero_jump_left_animations.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/hero_jump_left/hero_jump_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 12:
            self.hero_throwing_animations_right.append(pygame.transform.scale(pygame.image.load("images/character_animations"
                                                                                    "/hero_throwing"
                                                                                    "/hero_throwing_" + str(x) + ".png"), (40, 80)))
            self.hero_throwing_animations_right.append(pygame.transform.scale(pygame.image.load("images/character_animations"
                                                                                    "/hero_throwing"
                                                                                    "/hero_throwing_" + str(x) + ".png"), (40, 80)))
            x += 1
        x = 1
        while x <= 12:
            self.hero_throwing_animations_left.append(
                pygame.transform.scale(pygame.image.load("images/character_animations"
                                                         "/hero_throwing"
                                                         "/hero_throwing_left/hero_throwing_" + str(x) + ".png"), (40, 80)))
            self.hero_throwing_animations_left.append(
                pygame.transform.scale(pygame.image.load("images/character_animations"
                                                         "/hero_throwing"
                                                         "/hero_throwing_left/hero_throwing_" + str(x) + ".png"), (40, 80)))
            x += 1

    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def apply_gravity(self):
        self.move_down(2.40)


    def jump(self):
        if not self.isMarioOnTheGround:
            self.move_down(self.down_speed)
            self.down_speed += self.gravity

    def move_animations_right(self, display, mario_current_image, scroll):
        display.blit(self.hero_right_animation[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image

    def move_animations_left(self, display, mario_current_image, scroll):
        display.blit(self.hero_left_animation[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image

    def stand_animations_left(self, display, mario_current_image, scroll):
        display.blit(self.hero_stand_left_animation[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 17:
            mario_current_image = 0
        if not mario_current_image == 17:
            mario_current_image += 1
        return mario_current_image

    def stand_animations_right(self, display, mario_current_image, scroll):
        display.blit(self.hero_stand_right_animation[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 17:
            mario_current_image = 0
        if not mario_current_image == 17:
            mario_current_image += 1
        return mario_current_image

    def hero_jump_right_animation(self ,display, mario_current_image, scroll):
        display.blit(self.hero_jump_right_animations[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image

    def hero_jump_left_animation(self ,display, mario_current_image, scroll):
        display.blit(self.hero_jump_left_animations[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image


    def hero_throwing_animation_right(self ,display, mario_current_image, scroll):
        display.blit(self.hero_throwing_animations_right[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if not mario_current_image == 23:
            mario_current_image += 1
        return mario_current_image

    def hero_throwing_animation_left(self ,display, mario_current_image, scroll):
        display.blit(self.hero_throwing_animations_left[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if not mario_current_image == 23:
            mario_current_image += 1
        return mario_current_image

    def move_right(self, pixels=5):
        self.rect.x += pixels
        self.face_way="right"

    def move_left(self, pixels=5):
        self.rect.x -= pixels
        self.face_way="left"

    def move_down(self, pixels=5):
        self.rect.y += pixels

    def move_up(self, pixels=5):
        self.rect.y -= pixels

class Bat(Character):
    def __init__(self, width, height, image_path, x=0, y=0):
        super().__init__(width, height, image_path, x=0, y=0)
        self.move_to(x,y)
        self.bat_animations = []
        self.is_enemy_exist = 0

        x = 1
        while x <= 4:
            self.bat_animations.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/bat_flies/bat_" + str(x) + ".png"), (40, 40)))
            x += 1

    def fly_animation(self, display, mario_current_image, scroll):
        display.blit(self.bat_animations[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 3:
            mario_current_image = 0
        if not mario_current_image == 3:
            mario_current_image += 1
        return mario_current_image

class Rat (Character):
    def __init__(self,width, height, image_path, x=0, y=0):
        super().__init__(width, height, image_path, x=0, y=0)
        self.move_to(x, y)
        self.rat_animations_right = []
        self.rat_animations_left = []
        self.is_enemy_exist = 0

        x = 1
        while x <= 6:
            self.rat_animations_right.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/rat_animation/Screenshot_" + str(x) + ".png"), (60, 40)))
            self.rat_animations_right.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/rat_animation/Screenshot_" + str(x) + ".png"), (60, 40)))
            x+=1
        x = 1
        while x <= 6:
            self.rat_animations_left.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/rat_animation/rat_animation_left/Screenshot_left_" + str(x) + ".png"), (60, 40)))
            self.rat_animations_left.append(pygame.transform.scale(
                pygame.image.load("images/character_animations/rat_animation/rat_animation_left/Screenshot_left_" + str(x) + ".png"), (60, 40)))
            x += 1

    def run_animation_right(self, display, mario_current_image, scroll):
        display.blit(self.rat_animations_right[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image

    def run_animation_left(self, display, mario_current_image, scroll):
        display.blit(self.rat_animations_left[mario_current_image], (self.rect.x - scroll, self.rect.y))
        if mario_current_image == 11:
            mario_current_image = 0
        if not mario_current_image == 11:
            mario_current_image += 1
        return mario_current_image
