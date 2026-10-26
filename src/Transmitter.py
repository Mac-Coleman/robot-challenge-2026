import pygame, sys

# Really, really bad controller visualizer to assist in using the robots.

pygame.init()
label_font = pygame.font.SysFont('lucidaconsole', 12)
button_font = pygame.font.SysFont('lucidaconsole', 32)

width, height = 1000, 1000
screen = pygame.display.set_mode(size=(width, height), flags=pygame.SCALED)
pygame.display.set_caption("Cornell College Engineering Club Robot Controller")


DARK_GRAPHITE = (25, 23, 24)
GRAPHITE = (61, 59, 60)
BLUE = (64, 64, 255)
PLATINUM = (235, 235, 235)
RED = (255, 64, 64)

yb_label = button_font.render('Y', True, PLATINUM)
bb_label = button_font.render('B', True, PLATINUM)
ab_label = button_font.render('A', True, PLATINUM)
xb_label = button_font.render('X', True, PLATINUM)

ybl_rect = yb_label.get_rect()
bbl_rect = bb_label.get_rect()
abl_rect = ab_label.get_rect()
xbl_rect = xb_label.get_rect()

lb_label = button_font.render('LB', True, PLATINUM)
rb_label = button_font.render('RB', True, PLATINUM)
lt_label = button_font.render('LT', True, PLATINUM)
rt_label = button_font.render('RT', True, PLATINUM)

lbl_rect = lb_label.get_rect()
rbl_rect = rb_label.get_rect()
ltl_rect = lt_label.get_rect()
rtl_rect = rt_label.get_rect()

back_label = button_font.render("BACK", True, PLATINUM)
start_label = button_font.render("START", True, PLATINUM)
bl_rect = back_label.get_rect()
sl_rect = start_label.get_rect()

screen.fill(DARK_GRAPHITE)

while True:
    # Read current input state
    keys = pygame.key.get_pressed()

    # Analog stick boxes
    left_stick_box = pygame.draw.rect(screen, GRAPHITE, (175, 100, 300, 300))
    right_stick_box = pygame.draw.rect(screen, GRAPHITE, (width//2 + 25, 100, 300, 300))

    pygame.draw.aaline(screen, PLATINUM, (175 + 300/2, 100), (175 + 300/2, 100 + 300))
    pygame.draw.aaline(screen, PLATINUM, (175, 100 + 300/2), (175 + 300, 100 + 300/2))
    
    pygame.draw.aaline(screen, PLATINUM, (width//2 + 25 + 300/2, 100), (width//2 + 25 + 300/2, 100 + 300))
    pygame.draw.aaline(screen, PLATINUM, (width//2 + 25, 100 + 300/2), (width//2 + 25 + 300, 100 + 300/2))

    la_label = label_font.render("Left Analog Stick", True, PLATINUM)
    la_label_rect = la_label.get_rect()
    la_label_rect.center = (left_stick_box[0] + left_stick_box[2]//2, 90)
    screen.blit(la_label, la_label_rect)

    ra_label = label_font.render("Right Analog Stick", True, PLATINUM)
    ra_label_rect = ra_label.get_rect()
    ra_label_rect.center = (right_stick_box[0] + right_stick_box[2]//2, 90)
    screen.blit(ra_label, ra_label_rect)

    # Triggers
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_2] else GRAPHITE, (48, 198, 104, 204))
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_9] else GRAPHITE, (width-50-102, 198, 104, 204))
    left_trigger_box = pygame.draw.rect(screen, BLUE if keys[pygame.K_2] else GRAPHITE, (50, 200, 100, 200))
    right_trigger_box = pygame.draw.rect(screen, RED if keys[pygame.K_9] else GRAPHITE, (width-50-100, 200, 100, 200))

    # Bumpers
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_1] else GRAPHITE, (48, 98, 104, 79))
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_0] else GRAPHITE, (width-50-102, 98, 104, 79))
    left_bumper_box = pygame.draw.rect(screen, BLUE if keys[pygame.K_1] else GRAPHITE, (50, 100, 100, 75))
    right_bumper_box = pygame.draw.rect(screen, RED if keys[pygame.K_0] else GRAPHITE, (width-50-100, 100, 100, 75))

    # Start and Back
    
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_3] else GRAPHITE, (48, 200 + 200 + 23, 104, 79))
    pygame.draw.rect(screen, PLATINUM if keys[pygame.K_8] else GRAPHITE, (width-50-102, 200 + 200 + 23, 104, 79))
    back_box = pygame.draw.rect(screen, BLUE if keys[pygame.K_3] else GRAPHITE, (50, 200 + 200 + 25, 100, 75))
    start_box = pygame.draw.rect(screen, RED if keys[pygame.K_8] else GRAPHITE, (width-50-100, 200 + 200 + 25, 100, 75))

    # Buttons
    buttons_centroid = (
        right_stick_box[0] + right_stick_box[2]//2,
        right_stick_box[1] + right_stick_box[3] + 50 + 100
    )

    pygame.draw.circle(screen, PLATINUM if keys[pygame.K_UP] else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]-75), 42)
    pygame.draw.circle(screen, PLATINUM if keys[pygame.K_DOWN] else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]+75), 42)
    pygame.draw.circle(screen, PLATINUM if keys[pygame.K_LEFT] else GRAPHITE, (buttons_centroid[0]-75, buttons_centroid[1]), 42)
    pygame.draw.circle(screen, PLATINUM if keys[pygame.K_RIGHT] else GRAPHITE, (buttons_centroid[0]+75, buttons_centroid[1]), 42)

    yb_box = pygame.draw.circle(screen, RED if keys[pygame.K_UP] else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]-75), 40)
    ab_box = pygame.draw.circle(screen, RED if keys[pygame.K_DOWN] else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]+75), 40)
    xb_box = pygame.draw.circle(screen, RED if keys[pygame.K_LEFT] else GRAPHITE, (buttons_centroid[0]-75, buttons_centroid[1]), 40)
    bb_box = pygame.draw.circle(screen, RED if keys[pygame.K_RIGHT] else GRAPHITE, (buttons_centroid[0]+75, buttons_centroid[1]), 40)

    # D-pad
    dpad_centroid = (
        left_stick_box[0] + left_stick_box[2]//2,
        left_stick_box[1] + left_stick_box[3] + 50 + 100
    )



    pygame.draw.circle(screen, GRAPHITE, dpad_centroid, 125)

    # Analog stick indicators
    left_stick_pos = (
        left_stick_box[0] + 0 * left_stick_box[2]//2 + left_stick_box[2]//2,
        left_stick_box[1] + 0 * left_stick_box[3]//2 + left_stick_box[3]//2
    )
    right_stick_pos = (
        right_stick_box[0] + 0 * right_stick_box[2]//2 + right_stick_box[2]//2,
        right_stick_box[1] + 0 * right_stick_box[3]//2 + right_stick_box[3]//2
    )
    
    pygame.draw.circle(screen, PLATINUM, left_stick_pos, 12)
    pygame.draw.circle(screen, BLUE if keys[pygame.K_4] else GRAPHITE, left_stick_pos, 10)
    pygame.draw.circle(screen, PLATINUM, right_stick_pos, 12)
    pygame.draw.circle(screen, RED if keys[pygame.K_7] else GRAPHITE, right_stick_pos, 10)

    ybl_rect.center = yb_box.center
    bbl_rect.center = bb_box.center
    abl_rect.center = ab_box.center
    xbl_rect.center = xb_box.center

    screen.blit(yb_label, ybl_rect)
    screen.blit(bb_label, bbl_rect)
    screen.blit(ab_label, abl_rect)
    screen.blit(xb_label, xbl_rect)

    lbl_rect.center = left_bumper_box.center
    rbl_rect.center = right_bumper_box.center
    ltl_rect.center = left_trigger_box.center
    rtl_rect.center = right_trigger_box.center

    screen.blit(lb_label, lbl_rect)
    screen.blit(rb_label, rbl_rect)
    screen.blit(lt_label, ltl_rect)
    screen.blit(rt_label, rtl_rect)

    bl_rect.center = back_box.center
    sl_rect.center = start_box.center

    screen.blit(back_label, bl_rect)
    screen.blit(start_label, sl_rect)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()