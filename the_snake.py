from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов.
    Хранит позицию объекта на игровом поле и цвет объекта.
    """

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=BOARD_BACKGROUND_COLOR) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для отрисовки объектов"""
        pass


class Apple(GameObject):
    """Класс хранит цвет яблока и случайную позицию."""

    def __init__(self) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self) -> None:
        """Метод определяет случайное положение Apple на игровом поле."""
        random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (random_x, random_y)

    def draw(self) -> None:
        """Метод отрисовывает Apple."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс отвечает за хранение сегментов змейки, движение,
    изменение направления, рост после съеденного яблока, проверку столкновений
    и отрисовку змейки.
    """

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.length: int = 1
        self.direction: tuple = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.last: tuple[int, int] | None = None
        self.positions = [self.position]

    def get_head_position(self) -> tuple:
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Метод реализует движение змейки"""
        head_position = self.get_head_position()
        new_head_position_x = (head_position[0] + (self.direction[0]
                                                   * GRID_SIZE)) % SCREEN_WIDTH
        new_head_position_y = (head_position[1]
                               + (self.direction[1]
                                  * GRID_SIZE)) % SCREEN_HEIGHT
        new_head_position = (new_head_position_x, new_head_position_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            del self.positions[-1]
        else:
            self.last = None

    def update_direction(self) -> None:
        """Метод отвечает за обновление направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Метод отвечает за отрисовку змейки
        и затирание последнего сегмента.
        """
        for position in self.positions[1:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента змейки
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self) -> None:
        """Метод возвращает змейку в начальное состояние.
        Наличие метода - требование тестов.
        """
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]


def handle_keys(game_object) -> None:
    """Обработка нажатия клавишь, обновление направления движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры, проверяет съедено ли яблоко и столкновение головы
    змейки с хвостом.
    """
    pygame.init()

    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.positions[0] in snake.positions[1:]:
            apple.randomize_position()
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
