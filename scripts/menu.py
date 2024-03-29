import pygame
from scripts import visual
from scripts import constants as const
from webbrowser import open


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, text, image_button, shift, font_normal=visual.font.render,
                 font_min=visual.font_text.render, color='black'):
        pygame.sprite.Sprite.__init__(self)

        self.image = image_button
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.text = [font_normal(text, 1, pygame.Color(color)),
                     font_min(text, 1, pygame.Color(color))]
        self.shift = shift

    def update(self, surface):
        surface.blit(self.image, self.rect)
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            surface.blit(self.text[1], (self.rect.x + 5 + self.shift[0], self.rect.y + 5 + self.shift[1]))
        else:
            surface.blit(self.text[0], (self.rect.x + self.shift[0], self.rect.y + self.shift[1]))


button_group = pygame.sprite.Group()

size_button = const.SIZE_BUTTON
image_buttons = visual.load_image('fon/cantbuy.png', transforms=size_button)

# создаём кнопки
start = Button((180, 250), 'Играть', image_buttons, (size_button[0] // 4.5, size_button[1] // 5))
exit_in_menu = Button((180, 337), 'Выйти', image_buttons, (size_button[0] // 4.5, size_button[1] // 5))
reference = Button((180, 425), 'Справка', image_buttons, (size_button[0] // 5, size_button[1] // 4),
                   font_normal=visual.font_text.render, font_min=visual.font_text_min.render)
exit_in_pause = Button((185, 260), 'Выйти', image_buttons, (size_button[0] // 4.5, size_button[1] // 5), color='white')

for but in [start, exit_in_menu, reference]:
    button_group.add(but)


def menu(surface):
    # создаём рамку кнопок

    visual.music_fon_menu.play(-1)

    # создаём фон
    fon = pygame.transform.scale(visual.load_image('fon/logo.png'), (const.SCREEN_WIDTH, const.SCREEN_HEIGHT))

    hooked = False  # если навелись на кнопку

    running = True
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                # если кликнули по кнопке начать, начинаем игру
                if start.rect.collidepoint(event.pos):
                    visual.music_click.play()
                    return True
                # если кликнули по кнопке выйти, заканчиваем игру
                elif exit_in_menu.rect.collidepoint(event.pos):
                    return False
                # если кликнули по кнопке, то открываем меню настроек
                elif reference.rect.collidepoint(event.pos):
                    open('https://github.com/jamkinder/towerdefense/blob/main/README.md')
        # показываем фон
        surface.blit(fon, (0, 0))
        # показываем кнопки и все остальное
        button_group.update(surface)
        # если навелись на кнопку, то изменяем её размер
        for button in button_group:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if not hooked:
                    visual.music_hooked.play()
                    hooked = True

        if not (start.rect.collidepoint(pygame.mouse.get_pos()) or
                exit_in_menu.rect.collidepoint(pygame.mouse.get_pos()) or reference.rect.collidepoint(pygame.mouse.get_pos())):
            hooked = False
        pygame.display.flip()
