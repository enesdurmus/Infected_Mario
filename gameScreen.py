import pygame,sys
import Character, Elements

pygame.init()
mario = Character.Character(40, 80,"images/character_animations/hero_stand/hero_stand_right/hero_stand_right_1.png",150,200)
bat1 = Character.Bat(40,40,"images/character_animations/bat_flies/bat_1.png")
bat2 = Character.Bat(40,40,"images/character_animations/bat_flies/bat_1.png")
rat1 = Character.Rat(60,40,"images/character_animations/rat_animation/Screenshot_1.png")
wall = Elements.Element(40, 40,"images/ground_with_grass.png")
ground = Elements.Element(40, 40, "images/ground_without_grass.png")
top_ground = Elements.Element(40, 40, "images/ground_with_grass.png")
bullet = Elements.Bullet(20,20,"images/rock.png",500,500)
background = pygame.image.load("images/background.jpg")
flag = Elements.Element(40, 200,"images/flag.png",20,100)
nurse = Character.Character(40,80,"images/nurse.png")
tomb = Elements.Element(20,40,"images/tomb.png")  # We put tombs to the top of the gold walls so we can understand there is a gold.
gold_coin = Elements.Element(40, 40, "images/gold_coin.png")

FPS = 60
scroll=0

mario_current_image=0
hero_stand_image = 0
hero_jump_image = 0
hero_throwing_image = 0
bat_current_image = 0
rat_current_image = 0
is_animation_end = True

virus_bar = 10
healt = 3
level = 1

is_mario_shoot = False
running = True
running_menu = True
game_over = False
jump=False
bullet_distance=0
enemy_exist = False
is_map_uploaded = False

## Game map

game_map = Elements.Map.getMap("map1.txt")

## Colours that ı need.
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
font = pygame.font.SysFont("comicsans", 100, True)

## Sounds that ı need.
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
#JUMP_EFFECT = pygame.mixer.Sound("quake-jump-sound-effect.mp3.mp3") #pygame sound isn't working
music = pygame.mixer.music.load("game_music.mp3")
pygame.mixer.music.play(-1)



##Collecting gold
used_gold_walls = []
our_golds = 0
def collecting_gold(gold_walls,mario_rect,our_golds,used_gold_walls):
    ## Kullandığımız altın duvarlarını siliyoruz
    for used_gold_wallss in used_gold_walls:
        for gold_wallss in gold_walls:
            if used_gold_wallss == gold_wallss:
                gold_walls.remove(gold_wallss)
    for gold_wallsa in gold_walls:    # We check here if we hit gold walls. if we hit one of them we increase our golds.
        if gold_wallsa.bottom >= mario_rect.top - 5 and \
            abs(gold_wallsa.x - mario_rect.x) <= 38 and \
            gold_wallsa.x - mario_rect.x >= 0 and \
            mario_rect.top >= gold_wallsa.top:
            used_gold_walls.append(gold_wallsa)
            display.blit(gold_coin.image, (gold_wallsa.x - scroll, gold_wallsa.top - 40))
            our_golds+=1
    return our_golds
## Game over detecter
def game_over_detecter(mario_rect,game_over,enemy_rect=pygame.Rect(0,0,0,0)):
      if mario_rect.y>600:  # if we fall or we crash to enemy we return game over as true
          game_over=True
      if abs(mario_rect.x-enemy_rect.x) <=20 and abs(mario_rect.y-enemy_rect.y) <80:
          game_over=True
      return game_over
#Shows this screen before the start game
def main_menu_display():
    display.blit(pygame.image.load("images/start_screen.jpg"),(0,0))
    main_screen.blit(display, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    waiting = False
                    running_menu = False
    return running_menu
##Shows this screen when game over.
def game_over_display():
    if healt == 0:
        display.blit(pygame.transform.scale(
            pygame.image.load("images/game_over_screen.jpg"),(800, 600)), (0, 0))
        main_screen.blit(display, (0, 0))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        sys.exit()
    else:
        display.blit(pygame.transform.scale(
            pygame.image.load("images/you_died_screen.jpg"), (800, 600)), (0, 0))
        main_screen.blit(display, (0, 0))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        waiting = False
# For find where should we move our character.
def the_closest_check_point():
    closest_check_point=[0,0]
    for check_point in check_points:
        if check_point.x<mario.rect.x:
            if check_point.x >= closest_check_point[0]:
                closest_check_point[0] = check_point.x
                closest_check_point[1] = check_point.y
    return closest_check_point
## Enemy movement
def enemy_movement(enemy,rects):
    if enemy.face_way == "right":
        if move_test(enemy.rect, enemy.face_way, rects) == "stop":
            enemy.face_way="left"
            enemy.move_left(2)
        else:
            enemy.move_right(2)
    else:
        if move_test(enemy.rect, enemy.face_way, rects) == "stop":
            enemy.face_way="right"
            enemy.move_right(2)
        else:
            enemy.move_left(2)
## Collesion detecter
def collesion_test(character_rect,element_rect):
    colliding_objects=[]
    for rects in element_rect:
        if rects.colliderect(character_rect):
            colliding_objects.append(rects)
    return colliding_objects
# Return stop if we hit something
def move_test(character_rect,movement_way,sprite_rect):
    if collesion_test(character_rect,sprite_rect) != []:
        if(movement_way == "right"):
            return "stop"
        if(movement_way == "left"):
            return "stop"
        if (movement_way == "up"):
            return "stop"
        if (movement_way == "down"):
            return "stop"
# It checks if we hit enemy. if we hit enemy goes to out of screen.
def shooting(bullet,rects,is_mario_shoot,character_face_way,enemy,bullet_distance):
    display.blit(bullet.image, (bullet.rect.x - scroll, bullet.rect.y))
    if character_face_way == "right":
        if move_test(bullet.rect,character_face_way, rects) == "stop":
            bullet.move_to(0,900)
            is_mario_shoot =False
        elif move_test(bullet.rect,character_face_way, [pygame.Rect(enemy.rect.x, enemy.rect.y, enemy.width, enemy.height)]) == "stop":
            bullet.move_to(0, 900)
            enemy.move_to(0, 900)
            enemy.is_enemy_exist = 2
            is_mario_shoot =False
        else:
            bullet.move_right(3)
            bullet_distance+=3
    else:
        if move_test(bullet.rect,character_face_way, rects) == "stop":
            bullet.move_to(0,900)
            is_mario_shoot =False
        elif move_test(bullet.rect,character_face_way, [pygame.Rect(enemy.rect.x, enemy.rect.y, enemy.width, enemy.height)]) == "stop":
            bullet.move_to(0, 900)
            enemy.move_to(0, 900)
            enemy.is_enemy_exist = 2
            is_mario_shoot =False
        else:
            bullet.move_left(3)
            bullet_distance+=3
    if bullet_distance >= 200:
        bullet.move_to(0,900)
        is_mario_shoot = False
    return [is_mario_shoot,bullet_distance]
 # We draw virus bar top of our character.If we get medicine green bar will get smaller.
def draw_virus_bar():
    pygame.draw.rect(display, (0 ,0 ,255), (mario.rect.x - scroll - 20, mario.rect.y - 20, 80, 10))
    pygame.draw.rect(display, (0 ,100 ,0), (mario.rect.x - scroll - 20, mario.rect.y - 20, 8 * virus_bar, 10))
 # We draw our lives top left corner.
def draw_healt():
    heart1 = pygame.transform.scale(pygame.image.load("images/heart.png"), (30, 30))
    if healt==1:
        display.blit(heart1, (0, 0))
    elif healt==2:
        display.blit(heart1, (0, 0))
        display.blit(heart1, (40, 0))
    else:
        display.blit(heart1, (0, 0))
        display.blit(heart1, (40, 0))
        display.blit(heart1, (80,0))
 # Read game map matris and draw them to the screen.
def draw_game_map():
    y = 0
    for column in game_map:
        x = 0
        for row in column:
            if (row == "1"):
                display.blit(top_ground.image, (x * 40 - scroll, y * 40))
                rects.append(pygame.Rect(x * 40, y * 40, 40, 40))
            if (row == "2"):
                display.blit(ground.image, (x * 40 - scroll, y * 40))
                rects.append(pygame.Rect(x * 40, y * 40, 40, 40))
            if (row == "3"):
                display.blit(wall.image, (x * 40 - scroll, y * 40))
                rects.append(pygame.Rect(x * 40, y * 40, 40, 40))
                gold_walls.append(pygame.Rect(x * 40, y * 40, 40, 40))
            if (row == "4"):
                display.blit(ground.image, (x * 40 - scroll, y * 40))
                rects.append(pygame.Rect(x * 40, y * 40, 40, 40))
            if (row == "6"):
                check_points.append(pygame.Rect(x * 40, y * 40, 40, 40))
            if (row == "7"):
                flag_rects.append(pygame.Rect(x * 40, y * 40, 40, 200))
                display.blit(flag.image,(x * 40 - scroll, y * 40))
            if (row == "9"):
                display.blit(nurse.image, (x * 40 - scroll, y * 40))
                flag_rects.append(pygame.Rect(x * 40, y * 40, 40, 80))
            if (row == "t"):
                display.blit(tomb.image, (x * 40 - scroll, y * 40))
            x += 1
        y += 1
 # Read game map matris and draw the enemies to the screen.
def draw_enemies(bat_current_image,game_over,rat_current_image):
    y = 0
    for column in game_map:
        x = 0
        for row in column:
            if (row == "5"):
                if bat1.is_enemy_exist == 1:
                    bat_current_image = bat1.fly_animation(display, bat_current_image, scroll)
                    enemy_rects.append(pygame.Rect(bat1.rect.x - scroll, bat1.rect.y, 40, 40))
                    enemy_movement(bat1, rects)
                    game_over = game_over_detecter(mario.rect, game_over, bat1.rect)
                elif bat1.is_enemy_exist == 0:
                    bat1.move_to(x*40,y*40)
                    bat1.is_enemy_exist = 1
            if (row == "8"):
                if  bat2.is_enemy_exist == 1:
                    bat_current_image = bat2.fly_animation(display, bat_current_image, scroll)
                    enemy_rects.append(pygame.Rect(bat2.rect.x - scroll, bat2.rect.y, 40, 40))
                    enemy_movement(bat2, rects)
                    game_over = game_over_detecter(mario.rect, game_over, bat2.rect)
                elif bat2.is_enemy_exist == 0:
                    bat2.move_to(x * 40, y * 40)
                    bat2.is_enemy_exist = 1
            if (row == "z"):
                if rat1.is_enemy_exist == 1:
                    if rat1.face_way == "right":
                        rat_current_image = rat1.run_animation_right(display, rat_current_image, scroll)
                    else:
                        rat_current_image = rat1.run_animation_left(display, rat_current_image, scroll)
                    enemy_rects.append(pygame.Rect(rat1.rect.x - scroll, rat1.rect.y, 60, 40))
                    enemy_movement(rat1, rects)
                    game_over = game_over_detecter(mario.rect, game_over, rat1.rect)
                elif rat1.is_enemy_exist == 0:
                    rat1.move_to(x * 40, y * 40)
                    rat1.is_enemy_exist = 1
            x += 1
        y += 1
    return enemy_rects, bat_current_image, game_over, rat_current_image
 # Shows this screen when you reach to the flag you buy some medicine here.
def level_end_display(level,is_map_uploaded,virus_bar,our_golds):
    if collesion_test(mario.rect,flag_rects) != []:
        if level == 4:
            wait = True
            if virus_bar == 0:
                display.blit(pygame.transform.scale(
                pygame.image.load("images/level_end_congr_screen.jpg"), (800, 600)), (0, 0))
            else:
                display.blit(pygame.transform.scale(
                    pygame.image.load("images/level_end_dw_screen.jpg"), (800, 600)), (0, 0))
            main_screen.blit(display, (0, 0))
            pygame.display.flip()
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_RETURN:
                            pygame.quit()
                            sys.exit()
        elif level == 3:
            wait = True
            level += 1
            is_map_uploaded = False
            text = font.render(str(our_golds), 1, BLACK)
            display.blit(pygame.transform.scale(
                pygame.image.load("images/level_end_screen.jpg"), (800, 600)), (0, 0))
            display.blit(text, (1500, 190))
            main_screen.blit(display, (0, 0))
            pygame.display.flip()
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_1:
                            if our_golds >= 2 and virus_bar >= 1:
                                our_golds -= 2
                                virus_bar -= 1
                        elif event.key == pygame.K_2:
                            if our_golds >= 5 and virus_bar >= 2:
                                our_golds -= 5
                                virus_bar -= 2
                        elif event.key == pygame.K_RETURN:
                            wait = False
                            mario.move_to(5300, 0)

        else:
            wait = True
            level += 1
            is_map_uploaded = False
            text = font.render(str(our_golds), 1, BLACK)
            display.blit(pygame.transform.scale(
                pygame.image.load("images/level_end_screen.jpg"), (800, 600)), (0, 0))
            display.blit(text, (530, 190))
            main_screen.blit(display, (0, 0))
            pygame.display.flip()
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_1:
                            if our_golds >= 2 and virus_bar >= 1:
                                our_golds -= 2
                                virus_bar -= 1
                        elif event.key == pygame.K_2:
                            if our_golds >= 5 and virus_bar >= 2:
                                our_golds -= 5
                                virus_bar -= 2
                        elif event.key == pygame.K_RETURN:
                            wait = False
                            mario.move_to(150, 0)

    return level,is_map_uploaded,virus_bar, our_golds
## My screen size
screen_x=800
screen_y=600

## My screen
main_screen=pygame.display.set_mode((screen_x,screen_y),0,32)
pygame.display.set_caption("Mario")

## The screen that we will see in the moment
display = pygame.Surface((800,600))
clock = pygame.time.Clock()

while running:

    if running_menu:
        running_menu=main_menu_display()

    scroll += int((mario.rect.x - scroll - 150)/20)  ## Bu değerleri karakteri kameranın orasına getirmek için
    ##koyuyoruz yoksa kameranın dışında kalıyor.

    display.blit(background,(0,0))


 ## We draw the elements to the display.

    draw_virus_bar()
    draw_healt()
    flag_rects=[]
    rects = []
    gold_walls = []
    check_points = []
    enemy_rects = []

    draw_game_map()
    enemy_rects, bat_current_image, game_over, rat_current_image = draw_enemies(bat_current_image,game_over, rat_current_image)
    display.blit(font.render("Gold: " + str(our_golds),1,BLACK), (480, 2)) # We draw our golds.



    if game_over:  # If game over becomes True we goes into here.
        healt -= 1 # We decrease our healt.
        game_over_display() # We show game over display.
        closest_check_point=the_closest_check_point() #We find game over display.
        mario.move_to(closest_check_point[0],closest_check_point[1]) # And we bring mario to the point that we find.
        game_over=False

## Movements being here.
    mario.apply_gravity()

    if jump: # if we press space jump becomes True.
        mario.jump()
        if mario.face_way == "right":  # We control this because there are two different animation for jump.
            hero_jump_image = mario.hero_jump_right_animation(display, hero_jump_image, scroll)
        else:
            hero_jump_image = mario.hero_jump_left_animation(display, hero_jump_image, scroll)

        if move_test(mario.rect, "up", rects) == "stop":
            our_golds = collecting_gold(gold_walls, mario.rect, our_golds, used_gold_walls)
            mario.move_down(mario.rect.top % 40)  # I put this because sometimes mario goes into wall.
            jump=False

    if move_test(mario.rect, "down", rects) == "stop":
        mario.move_up(1)
        mario.move_up(mario.rect.bottom % 40)  # ı put these because sometimes mario goes into ground.
        mario.isMarioOnTheGround = True

    if is_mario_shoot: # if we press x. And if there are enemies and we control them if we hit them.
        if bat1.is_enemy_exist == 1:
            is_mario_shoot, bullet_distance = shooting(bullet, rects, is_mario_shoot, character_face_way, bat1, bullet_distance)
        if bat2.is_enemy_exist == 1:
            is_mario_shoot, bullet_distance = shooting(bullet, rects, is_mario_shoot, character_face_way, bat2, bullet_distance)
        if rat1.is_enemy_exist == 1:
            is_mario_shoot, bullet_distance = shooting(bullet, rects, is_mario_shoot, character_face_way, rat1, bullet_distance)

        if mario.face_way == "right":  # throwing animations according to face way.
            hero_throwing_image = mario.hero_throwing_animation_right(display, hero_throwing_image, scroll)
        else:
            hero_throwing_image = mario.hero_throwing_animation_left(display, hero_throwing_image, scroll)

    game_over = game_over_detecter(mario.rect, game_over) # We update game over property

    level, is_map_uploaded, virus_bar, our_golds = level_end_display(level,is_map_uploaded,virus_bar, our_golds)

    if is_map_uploaded == False: # if we finish a map is_map_uploaded goes false and we find what map we should upload.
        if level == 2:
            game_map = Elements.Map.getMap("map2.txt")
            rat1.is_enemy_exist = 0  # we bring them alive again.
            bat1.is_enemy_exist = 0
            bat2.is_enemy_exist = 0
            is_map_uploaded = True
        if level == 3:
            game_map = Elements.Map.getMap("map3.txt")
            rat1.is_enemy_exist = 0
            bat1.is_enemy_exist = 0
            bat2.is_enemy_exist = 0
            is_map_uploaded = True

    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                if mario.isMarioOnTheGround:
                    mario.down_speed = -11
                    jump=True
                    hero_jump_image = 0
                    mario.isMarioOnTheGround = False
                    #jump_effect.play()
            elif event.key == pygame.K_x:  # if we press x button we start the shooting actions.
                if not is_mario_shoot == True:
                    if bullet.rect.y == 900:
                        bullet.move_to(mario.rect.x, mario.rect.y + 40)  # We bring the bullet to the character.
                    is_mario_shoot = True
                    hero_throwing_image = 0
                    character_face_way = mario.face_way
                    bullet_distance = 0




    keys = pygame.key.get_pressed() #that's listen key pressed.

    if keys[pygame.K_LEFT]:   # If we press left button we goes left and we hit something we stop.
                               # but the stop comes a bit late that's why we goes
                                 # 5 pixel to the opposite direction same as right.
        if not move_test(mario.rect, "left", rects) == "stop":
            mario.move_left(5)
            if not jump:
                if not is_mario_shoot:
                    mario_current_image=mario.move_animations_left(display,mario_current_image,scroll)
            mario.face_way="left"
            if move_test(mario.rect, "left", rects)=="stop":
                mario.move_right(5)
                mario.face_way = "left"
    if keys[pygame.K_RIGHT]:
        if not move_test(mario,"right",rects)=="stop":
            mario.move_right(5)
            if not jump:
                if not is_mario_shoot:
                    mario_current_image = mario.move_animations_right(display, mario_current_image, scroll)
            mario.face_way="right"
            if move_test(mario,"right",rects)=="stop":
                mario.move_left(5)
                mario.face_way = "right"

    if not keys[pygame.K_RIGHT]:   # When mario doesn't do anything we draw him according to face way.
        if not  keys[pygame.K_LEFT]:
            if not is_mario_shoot:
                if not jump:
                    if mario.face_way == "right":
                        hero_stand_image = mario.stand_animations_right(display, hero_stand_image, scroll)
                    else:
                        hero_stand_image = mario.stand_animations_left(display, hero_stand_image, scroll)


    main_screen.blit(display,(0,0))
    pygame.display.update()
    clock.tick(FPS)