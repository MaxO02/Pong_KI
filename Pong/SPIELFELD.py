import pygame


pygame.init()
clock = pygame.time.Clock()


#Color
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Resolution
RESOLUTION = (1280, 720)
WIDTH, HEIGHT = RESOLUTION

#Screen
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Pong")

#Font
score_font = pygame.font.SysFont("Clear Sans Regular", 30)

#Rect
left_rect_posX = 50
left_rect_posY = 50

right_rect_posX = 1220
right_rect_posY = 50

left_rect_HEIGHT = 150
right_rect_HEIGHT = 150


left_rect_can_move_upwards = True
left_rect_can_move_downwards = True
right_rect_can_move_upwards = True
right_rect_can_move_downwards = True

#Circle
circle_start_posX = int(WIDTH / 2)
circle_start_posY = int(HEIGHT / 2)

circle_posY = circle_start_posY
circle_posX = circle_start_posX

#Score
score_left = 0
score_right = 0

#Input map
inputMap = [False, False, False, False]

#Rect movement factor
rmf = 10

#Circle movement factor
cmfX = 450
cmfY = 450

#Main Loop
cancel = False

while not cancel:
    pressed_down = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cancel = True
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                inputMap[0] = True
            if event.key == pygame.K_UP:
                inputMap[1] = True
            if event.key == pygame.K_s:
                inputMap[2] = True
            if event.key == pygame.K_w:
                inputMap[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                inputMap[0] = False
            if event.key == pygame.K_UP:
                inputMap[1] = False
            if event.key == pygame.K_s:
                inputMap[2] = False
            if event.key == pygame.K_w:
                inputMap[3] = False

    #Game logic
    if right_rect_posY < 0 - right_rect_HEIGHT / 2:
        right_rect_can_move_upwards   = False
    else:
        right_rect_can_move_upwards   = True
    if right_rect_posY > HEIGHT - right_rect_HEIGHT / 2:
        right_rect_can_move_downwards = False
    else:
        right_rect_can_move_downwards = True
    if left_rect_posY < 0 - left_rect_HEIGHT / 2:
        left_rect_can_move_upwards    = False
    else:
        left_rect_can_move_upwards    = True
    if left_rect_posY > HEIGHT - left_rect_HEIGHT / 2:
        left_rect_can_move_downwards  = False
    else:
        left_rect_can_move_downwards  = True


    if right_rect_can_move_downwards:
        if inputMap[0]: right_rect_posY += rmf
    if right_rect_can_move_upwards:
        if inputMap[1]: right_rect_posY -= rmf
    if left_rect_can_move_downwards:
        if inputMap[2]: left_rect_posY  += rmf
    if left_rect_can_move_upwards:
        if inputMap[3]: left_rect_posY  -= rmf

    #Circle movement
    circle_time_passed = clock.tick(60)
    circle_time_sec = circle_time_passed / 1000.0
    circle_posX += cmfX * circle_time_sec
    circle_posY += cmfY * circle_time_sec

    #Circle collision
    if circle_posY > HEIGHT or circle_posY < 0:
        cmfY = -cmfY
    if circle_posX > right_rect_posX or circle_posX < left_rect_posX:
        if circle_posY > right_rect_posY and circle_posY < right_rect_posY + right_rect_HEIGHT:
            cmfX = -cmfX
        if circle_posY > left_rect_posY and circle_posY < left_rect_posY + left_rect_HEIGHT:
            cmfX = -cmfX

    # Endgame
    if circle_posX > WIDTH:
        score_left += 1
        circle_posX = circle_start_posX
        circle_posY = circle_start_posY

    if circle_posX < 0:
        score_right += 1
        circle_posX = circle_start_posX
        circle_posY = circle_start_posY

    #Clear screen
    screen.fill(GREEN)

    #Drawing code
    pygame.draw.rect(   screen, BLUE, [left_rect_posX, left_rect_posY, 10, left_rect_HEIGHT])
    pygame.draw.rect(   screen, BLUE, [right_rect_posX, right_rect_posY, 10, right_rect_HEIGHT])
    pygame.draw.rect(   screen, RED, [circle_posX, circle_posY, 20, 20])

    screen.blit(score_font.render(str(score_left), True, BLUE), (WIDTH / 4, 50))
    screen.blit(score_font.render(str(score_right), True, BLUE), (WIDTH / 1.25, 50))

    #Update screen
    pygame.display.flip()

    #Frames per second
clock.tick(60)