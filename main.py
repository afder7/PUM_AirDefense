from ingame_objects import *
import pygame
import time
fps = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


def rectRotated(surface, color, pos, fill, border_radius, rotation_angle, rotation_offset_center=(0, 0),
                nAntialiasingRatio=1):
    """
    - rotation_angle: in degree
    - rotation_offset_center: moving the center of the rotation: (-100,0) will turn the rectangle around a point 100 above center of the rectangle,
                                         if (0,0) the rotation is at the center of the rectangle
    - nAntialiasingRatio: set 1 for no antialising, 2/4/8 for better aliasing
    """
    nRenderRatio = nAntialiasingRatio

    sw = pos[2] + abs(rotation_offset_center[0]) * 2
    sh = pos[3] + abs(rotation_offset_center[1]) * 2

    surfcenterx = sw // 2
    surfcentery = sh // 2
    sy = pygame.Surface((sw * nRenderRatio, sh * nRenderRatio))
    sy = sy.convert_alpha()
    sy.fill((0, 0, 0, 0))

    rw2 = pos[2] // 2  # halfwidth of rectangle
    rh2 = pos[3] // 2

    pygame.draw.rect(sy, color, ((surfcenterx - rw2 - rotation_offset_center[0]) * nRenderRatio,
                                 (surfcentery - rh2 - rotation_offset_center[1]) * nRenderRatio, pos[2] * nRenderRatio,
                                 pos[3] * nRenderRatio), fill * nRenderRatio,
                     border_radius=border_radius * nRenderRatio)
    sy = pygame.transform.rotate(sy, rotation_angle)
    if nRenderRatio != 1: sy = pygame.transform.smoothscale(sy, (
        sy.get_width() // nRenderRatio, sy.get_height() // nRenderRatio))
    incfromrotw = (sy.get_width() - sw) // 2
    incfromroth = (sy.get_height() - sh) // 2
    surface.blit(sy, (pos[0] - surfcenterx + rotation_offset_center[0] + rw2 - incfromrotw,
                      pos[1] - surfcentery + rotation_offset_center[1] + rh2 - incfromroth))
    return (pos[0] - surfcenterx + rotation_offset_center[0] + rw2 + incfromrotw + 15,
                      pos[1] - surfcentery + rotation_offset_center[1] + rh2 - incfromroth - 15)


pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("air defense")
clock = pygame.time.Clock()
screen.fill(BLACK)

pygame.draw.circle(screen, BLUE, (300, H), 150)
pygame.draw.rect(screen, BLUE, (700, 500, 100, H))
# pygame.draw.rect(screen, RED, (450, 550, 100, 100))
# pygame.draw.polygon(screen, BLUE, )   ДОДЕЛАТЬ ПУШКУ
gun = rectRotated(screen, RED, (275, 320, 50, 130), 0, 0, 0, (0, 150))
pygame.draw.circle(screen, YELLOW, (750, 550), 10)

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

last_spawn = 0
a = 0
diff = 0.1
current_time = pygame.time.get_ticks() / 1000
counter = 0
counterm = 0
killed = set()
radar = Radar(750)
temp = 1
auto = 0
while True:
    screen.fill(BLACK)
    pygame.draw.circle(screen, BLUE, (300, H), 150)
    pygame.draw.rect(screen, BLUE, (700, 500, 100, H))

    data = radar.scan()
    if auto and temp:
        for i in data:
            gun_pos = rectRotated(screen, RED, (275, 320, 50, 130), 0, 0, i[1] - 7, (0, 220))
            if i[1] < 0:
                pygame.draw.circle(screen, GREEN, (gun_pos[0] + 10, gun_pos[1] - 10), 20)
                bullet_list.append(Bullet(gun_pos[0] + 10, gun_pos[1] - 10, current_time, i[1] - 7))
            else:
                pygame.draw.circle(screen, GREEN, (gun_pos[0] - 20, gun_pos[1] - 10), 20)
                bullet_list.append(Bullet(gun_pos[0] - 20, gun_pos[1] - 10, current_time, i[1] - 7))
            temp = 0
            a = data[0][1] - 7
    gun_pos = rectRotated(screen, RED, (275, 320, 50, 130), 0, 0, a, (0, 220))
    text_surface = my_font.render(f'Score: {counter}', False, (255, 255, 255))
    text_surfacem = my_font.render(f'Missed: {counterm}', False, (255, 255, 255))
    text_surfacek = my_font.render("Press 'K' for auto-pilot mode", False, (255, 255, 255))
    text_surfaceq = my_font.render("Press 'Q' to return to game mode", False, (255, 255, 255))
    screen.blit(text_surface, (0, 0))
    screen.blit(text_surfacem, (0, 40))
    screen.blit(text_surfacek, (0, 80))
    screen.blit(text_surfaceq, (0, 120))

    rm_list = []
    bm_list = []
    for rocket in rocket_list:
        if rocket.y > 500:
            print("Uletel")
            rm_list.append(rocket)
            killed.add(rocket)
            counterm += 1
        for bullet in bullet_list:
            if ((rocket.x - bullet.x) ** 2 + (bullet.y - rocket.y) ** 2) ** 0.5 <= 50 and rocket not in killed:
                print("Popal")
                rm_list.append(rocket)
                bm_list.append(bullet)
                killed.add(rocket)
                counter += 1
    # print(rm_list, bullet_list)
    for rocket in rm_list:
        try:
            rocket_list.remove(rocket)
        except ValueError:
            pass
    for bullet in bm_list:
        try:
            bullet_list.remove(bullet)
        except ValueError:
            pass

    if last_spawn == int(current_time):
        rocket_list.append(Rocket())
        last_spawn += 1
        temp = 1
        # print("Rocket spawned ", 180 * rocket_list[-1].angle / math.pi)
        # print(rocket_list[-1].vx, rocket_list[-1].vy)

    for rocket in rocket_list:
        # 270 + 180 * rocket.angle / math.pi
        # rectRotated(screen, YELLOW, (rocket.x - 10, rocket.y, rocket.x + 10, rocket.y), 0, 0, 0,
        #                 (0, 0))
        img = pygame.image.load("Rocket_2.png")
        im_1 = pygame.transform.rotate(img, 180 + 180 * rocket.angle / math.pi)
        screen.blit(im_1, (rocket.x, rocket.y))
        rocket.move()

    for bullet in bullet_list:
        pygame.draw.circle(screen, GREEN, (bullet.x, bullet.y), 20)
        bullet.change_speed()
        bullet.move()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if not auto:
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and a < 5:
                    a += 4
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and a > -60:
                    a -= 4
                if event.key == pygame.K_SPACE:
                    # print(gun_pos)
                    if a < 0:
                        pygame.draw.circle(screen, GREEN, (gun_pos[0] + 10, gun_pos[1] - 10), 20)
                        bullet_list.append(Bullet(gun_pos[0] + 10, gun_pos[1] - 10, current_time, a))
                    else:
                        pygame.draw.circle(screen, GREEN, (gun_pos[0] - 20, gun_pos[1] - 10), 20)
                        bullet_list.append(Bullet(gun_pos[0] - 20, gun_pos[1] - 10, current_time, a))
                if event.key == pygame.K_k:
                    auto = 1
            if event.key == pygame.K_q:
                auto = 0
        if event.type == pygame.QUIT:
            exit()

    current_time = pygame.time.get_ticks() / 1000
    pygame.display.flip()
