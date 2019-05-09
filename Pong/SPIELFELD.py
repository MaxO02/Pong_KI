import pygame

from Pong.paddel import PADDEL


class SPIELFELD:

    pygame.init()
    clock = pygame.time.Clock()

    # Color
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    RESOLUTION = (1280, 720)
    WIDTH, HEIGHT = RESOLUTION

    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pong")

    score_font = pygame.font.SysFont("Clear Sans Regular", 30)
    left_paddel = PADDEL(50, 50)
    right_paddel = PADDEL(1220, 50)

    circle_start_posX = int(WIDTH / 2)
    circle_start_posY = int(HEIGHT / 2)

    circle_posY = circle_start_posY
    circle_posX = circle_start_posX

    # Score
    score_left = 0
    score_right = 0

    # Input map
    inputMap = [False, False, False, False]

    # Circle movement factor
    cmfX = 450
    cmfY = 450

    # Main Loop
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

        # Game logic
        if right_paddel.getypos() < 0 - right_paddel.getheight / 2:
            right_paddel.setcmu(False)
        else:
            right_paddel.setcmu(True)
        if right_paddel.getypos() > HEIGHT - right_paddel.getheight / 2:
            right_paddel.setcmd(False)
        else:
            right_paddel.setcmd(True)
        if left_paddel.getypos() < 0 - left_paddel.getheight / 2:
            left_paddel.setcmu(False)
        else:
            left_paddel.setcmu(True)
        if left_paddel.getypos() > HEIGHT - left_paddel.getheight / 2:
            left_paddel.setcmd(False)
            left_paddel.setcmd(True)

        if right_paddel.getcmd() and inputMap[0]:
            right_paddel.moveydown()
        if right_paddel.getcmu() and inputMap[1]:
            right_paddel.moveyup()
        if left_paddel.getcmd() and inputMap[2]:
            left_paddel.moveydown()
        if left_paddel.getcmu() and inputMap[3]:
            left_paddel.moveyup()

        # Circle movement
        circle_time_passed = clock.tick(60)
        circle_time_sec = circle_time_passed / 1000.0
        circle_posX += cmfX * circle_time_sec
        circle_posY += cmfY * circle_time_sec

        # Circle collision
        if circle_posY > HEIGHT or circle_posY < 0:
            cmfY = -cmfY
        if circle_posX > right_paddel.getxpos() or circle_posX < left_paddel.getxpos():
            if circle_posY > right_paddel.getxpos() and circle_posY < right_paddel.getxpos() + right_paddel.getheight:
                cmfX = -cmfX
            if circle_posY > left_paddel.getypos() and circle_posY < left_paddel.getypos() + left_paddel.getheight:
                cmfX = -cmfX

        if circle_posX > WIDTH:
            score_left += 1
            circle_posX = circle_start_posX
            circle_posY = circle_start_posY

        if circle_posX < 0:
            score_right += 1
            circle_posX = circle_start_posX
            circle_posY = circle_start_posY

        def updatescreen(self, scoreleft, scorright):
            self.screen.fill(self.GREEN)

            pygame.draw.rect(self.screen, self.BLUE, [self.left_paddel.getxpos(), self.left_paddel.getypos(), 10, self.left_paddel.getheight])
            pygame.draw.rect(self.screen, self.BLUE, [self.right_paddel.getxpos(), self.right_paddel.getxpos(), 10, self.right_paddel.getheight])
            pygame.draw.rect(self.screen, self.RED, [self.circle_posX, self.circle_posY, 20, 20])

            self.screen.blit(self.score_font.render(str(self.scoreleft), True, self.BLUE), (self.WIDTH / 4, 50))
            self.screen.blit(self.score_font.render(str(self.scoreright), True, self.BLUE), (self.WIDTH / 1.25, 50))

            pygame.display.flip()

