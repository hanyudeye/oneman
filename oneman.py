# 假设你用Python和Pygame来实现
import pygame

# 初始化Pygame
pygame.init()
pygame.mixer.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("孤独的人的花园")

# 定义玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width=800, screen_height=600):
        super().__init__()
           # 加载音效
        try:
         self.footstep_sound = pygame.mixer.Sound('sounds/footstep.wav')
         self.footstep_sound.set_volume(0.3)  # 设置音量为30%
        except pygame.error as e:
            print(f"无法加载脚步声音效: {e}")
            self.footstep_sound = None
    
        self.is_moving = False
        self.sound_cooldown = 0


        # 加载玩家图片
        self.image_default = pygame.image.load('images/man.png')
        self.image_left_down = pygame.image.load('images/man1.png')
        self.image_right_up = pygame.image.load('images/man9.png')
        
        # 调整所有图片尺寸为40x40
        self.image_default = pygame.transform.scale(self.image_default, (40, 40))
        self.image_left_down = pygame.transform.scale(self.image_left_down, (40, 40))
        self.image_right_up = pygame.transform.scale(self.image_right_up, (40, 40))
        
        # 设置默认图片
        self.image = self.image_default
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed = 5
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        keys = pygame.key.get_pressed()
        # 检测是否在移动
        is_moving_now = any([keys[pygame.K_LEFT], keys[pygame.K_RIGHT], 
            keys[pygame.K_UP], keys[pygame.K_DOWN]])
        # 处理移动和声音
        if is_moving_now:
            if not self.is_moving:  # 刚开始移动
             self.is_moving = True
             self.play_footstep()
            elif self.sound_cooldown <= 0:  # 正在移动且冷却时间结束
                self.play_footstep()
        else:
            self.is_moving = False

        # 更新声音冷却时间
        if self.sound_cooldown > 0:
             self.sound_cooldown -= 1
    

        if keys[pygame.K_LEFT] or keys[pygame.K_DOWN]:
            self.image = self.image_left_down
        elif keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
            self.image = self.image_right_up
        else:
            self.image = self.image_default
            
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def play_footstep(self):
     if self.footstep_sound:
        self.footstep_sound.play()
        self.sound_cooldown = 20  # 设置冷却时间（约0.3秒，基于60FPS）


# 假设玩家接触到一个物品时，触发动画或效果
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((50, 50))  # 物品的尺寸
        self.image.fill((0, 255, 0))  # 物品颜色
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def interact(self):
        print(f"你正在与{self.name}互动")
# 设置游戏场景和玩家
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 创建物体并添加到精灵组，碰到桌子会唱歌
table = Object(200, 200, "桌子")
all_sprites.add(table)

# 加载背景图片
try:
    background = pygame.image.load('images/background.png')
    background = pygame.transform.scale(background, (800, 600))
except pygame.error as e:
    print(f"无法加载背景图片: {e}")
    # 使用纯色背景作为备选
    background = pygame.Surface((800, 600))
    background.fill((200, 200, 200))

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新玩家
    all_sprites.update()

    # 绘制背景
    screen.blit(background, (0, 0))

    # 绘制玩家
    all_sprites.draw(screen)

    # 更新屏幕
    pygame.display.flip()
    pygame.time.Clock().tick(60)  # 60帧每秒

pygame.quit()