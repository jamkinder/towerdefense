




class Castle(pygame.sprite.Sprite):
    def __init__(self):
        self.hp = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(color=(255, 0, 0, 0.5))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 50, HEIGHT - 25)

        self.pos = (440, 480)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            loosescreen.start_screen()


    def show(self):
        pass