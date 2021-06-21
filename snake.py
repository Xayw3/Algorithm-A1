import pygame
import sys
import random


pygame.init()

# цвета
frame_color = (220, 20, 60)
twin_color = (250, 235, 215)
odd_color = (128, 128, 128)
header_color = (128, 0, 0)
snake_color = (0, 250, 154)
eat_color = (25, 25, 112)

# отступы
MARGIN = 1
header_margin = 70


# Размер окна
size = [600, 800]

# размеры
count_blocks = 20
size_block = 20
size = [size_block * count_blocks + 2 * size_block + MARGIN * count_blocks,
        size_block * count_blocks + 2 * size_block + MARGIN * count_blocks + header_margin]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("My first game")

timer = pygame.time.Clock()

courier = pygame.font.SysFont('courier', 36)

# сохранение координат змейки
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Проверка находиться ли голова змейки внутри поля
    def is_inside(self):
        return 0 <= self.x < count_blocks and 0 <= self.y < count_blocks

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y

# появление случайных квадратов
def get_random_empty_block():
    x = random.randint(0, count_blocks-1)
    y = random.randint(0, count_blocks - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, count_blocks-1)
        empty_block.y = random.randint(0, count_blocks - 1)
    return empty_block

# создание игрового поля
def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [size_block + column * size_block + MARGIN * (column + 1),
                                             header_margin + size_block + row * size_block + MARGIN * (row + 1), 
                                             size_block, size_block])


# змейка
snake_blocks = [SnakeBlock(9,10), SnakeBlock(9,11), SnakeBlock(9,12)]
# Яблоко
apple = get_random_empty_block()

d_row = 0
d_col = 1
total = 0
speed = 1

# цыкл что бы не закрывалось окно
while True:
    
    for event  in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Exit")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col !=0:
                d_row = -1
                d_col = 0
            elif event.key == pygame.K_DOWN and d_col !=0:
                d_row = 1
                d_col = 0
            elif event.key == pygame.K_LEFT and d_row !=0:
                d_row = 0
                d_col = -1
            elif event.key == pygame.K_RIGHT and d_row !=0:
                d_row = 0
                d_col = 1

    # изменение цвета экрана
    screen.fill(frame_color)

    # header
    pygame.draw.rect(screen, header_color, [0, 0, size[0], header_margin])

    text_total = courier.render(f"Score: {total}", 0, twin_color)
    text_speed = courier.render(f"Level: {speed}", 0, twin_color)
    screen.blit(text_total, (size_block, size_block))
    screen.blit(text_speed, (size_block + 220, size_block))

    # создание рядов
    for row in range(count_blocks):
        # разделение колонок
        for column in range(count_blocks):
            if (row + column) % 2 == 0:
                color = twin_color
            else:
                color = odd_color
            # Эта функция вызывает игровое поле
            draw_block(color, row, column)

    # выбор головы (последний элемент списка)
    head = snake_blocks[-1]
    if not head.is_inside():
        print("Game Over")
        pygame.quit()
        sys.exit()

    # Яблоко
    draw_block(eat_color, apple.x, apple.y)
    for block in snake_blocks:
        draw_block(snake_color, block.x, block.y)

    if apple == head:
        total += 1
        speed = total // 5 + 1
        snake_blocks.append(apple)
        apple = get_random_empty_block()

    # отрисовка змейки
    for block in snake_blocks:
        draw_block(snake_color, block.x, block.y)

    # передвижение головы
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    snake_blocks.append(new_head)
    # удаление первого элемента списка
    snake_blocks.pop(0)

    pygame.display.flip()
    timer.tick(4 + speed)