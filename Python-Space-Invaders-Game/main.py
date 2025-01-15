import pygame, sys, random
from game import Game

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

GREY = (29, 29, 27)
YELLOW = (243, 216, 63)

# Pygame'ı başlat
pygame.init()

# Ekranı oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("SPACE INVADERS GAME")

# Font yükle
font = pygame.font.Font("Font/monogram.ttf", 60)

class Button:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    start_button = Button('Graphics/start.png', 280, 300)
    background = pygame.image.load('Graphics/background (1).jpg')
    image = pygame.image.load('Graphics/Spacelogo.png')
    image_x = 120
    image_y = 100

    while True:
        screen.blit(background, (0, 0))

        screen.blit(image, (image_x, image_y))
        draw_text('PRESS "ESC" BUTTON TO EXIT', font, YELLOW, screen, 100, 500)

        start_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    start_game()

        pygame.display.update()

def start_game():
    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 700
    OFFSET = 50
    screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
    running = True
    paused = False
    back_button = Button('Graphics/geri.png', 40, 70)
    background = pygame.image.load('Graphics/background (1).jpg')
    screen.blit(background, (0, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                if event.key == pygame.K_RETURN:
                    paused = False
                if event.key == pygame.K_RETURN and paused:
                    paused = False
                if event.key == pygame.K_RETURN and not paused:
                    paused = True

        screen.blit(background, (0, 0))


        if not paused:

            SCREEN_WIDTH = 750
            SCREEN_HEIGHT = 700
            OFFSET = 50

            GREY = (29, 29, 27)
            YELLOW = (243, 216, 63)

            pygame.init()

            screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2 * OFFSET))
            pygame.display.set_caption("Python Space Invaders")




            running = True
            paused = False
            back_button = Button('Graphics/geri.png', 40, 80)
            background = pygame.image.load('Graphics/background (1).jpg')
            screen.blit(background, (0, 0))



            font = pygame.font.Font("Font/monogram.ttf", 40)
            level_surface = font.render("LEVEL", False, YELLOW)
            game_over_surface = font.render("GAME OVER", False, YELLOW)
            score_text_surface = font.render("SCORE", False, YELLOW)
            highscore_text_surface = font.render("HIGH-SCORE", False, YELLOW)




            clock = pygame.time.Clock()

            game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

            SHOOT_LASER = pygame.USEREVENT
            pygame.time.set_timer(SHOOT_LASER, 300)

            MYSTERYSHIP = pygame.USEREVENT + 1
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == SHOOT_LASER and game.run:
                        game.alien_shoot_laser()

                    if event.type == MYSTERYSHIP and game.run:
                        game.create_mystery_ship()
                        pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] and game.run == False:
                        game.reset()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if back_button.is_clicked(event.pos):
                            return main_menu()

                if game.run:
                    game.spaceship_group.update()
                    game.move_aliens()
                    game.alien_lasers_group.update()
                    game.mystery_ship_group.update()
                    game.check_for_collisions()





                screen.fill(GREY)

                pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
                pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

                if game.run:
                    screen.blit(level_surface, (570, 740, 50, 50))
                else:
                    screen.blit(game_over_surface, (570, 740, 50, 50))

                x = 50
                for life in range(game.lives):
                    screen.blit(game.spaceship_group.sprite.image, (x, 745))
                    x += 50

                screen.blit(score_text_surface, (50, 15, 50, 50))
                formatted_score = str(game.score).zfill(5)
                score_surface = font.render(formatted_score, False, YELLOW)
                screen.blit(score_surface, (50, 40, 50, 50))
                screen.blit(highscore_text_surface, (550, 15, 50, 50))
                formatted_highscore = str(game.highscore).zfill(5)
                highscore_surface = font.render(formatted_highscore, False, YELLOW)
                screen.blit(highscore_surface, (625, 40, 50, 50))

                game.spaceship_group.draw(screen)
                game.spaceship_group.sprite.lasers_group.draw(screen)
                for obstacle in game.obstacles:
                    obstacle.blocks_group.draw(screen)

                game.aliens_group.draw(screen)
                game.alien_lasers_group.draw(screen)
                game.mystery_ship_group.draw(screen)
                game.create_aliens_if_empty()

                back_button.draw(screen)

                pygame.display.update()
                clock.tick(60)


if __name__ == '__main__':
    main_menu()
