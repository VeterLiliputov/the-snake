from random import randint

import pygame as pg

Pointer = tuple[int, int]
Color = tuple[int, int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: Pointer = (0, -1)
DOWN: Pointer = (0, 1)
LEFT: Pointer = (-1, 0)
RIGHT: Pointer = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: Color = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR: Color = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: Color = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: Color = (0, 255, 0)

# Скорость движения змейки:
SPEED: int = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


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
        raise NotImplementedError('Метод не реализован в наследнике класса!')


class Apple(GameObject):
    """Класс хранит цвет яблока и случайную позицию."""

    def __init__(self, body_color: Color = APPLE_COLOR) -> None:
        super().__init__(body_color=body_color)

    # Pytest требует следующее: Если в конструктор класса `Apple` помимо
    # параметра `self` передаются какие-то ещё параметры - убедитесь, что
    # для них установлены значения по умолчанию.
    # Написал бы так:
    # def __init__(self, occupied_positions: list[Pointer],
    #              body_color: Color = APPLE_COLOR) -> None:
    #     super().__init__(body_color=body_color)
    #     self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions: list[Pointer]) -> None:
        """Метод определяет случайное положение Apple на игровом поле."""
        while True:
            random_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            random_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            candidate_position = (random_x, random_y)
            if candidate_position not in occupied_positions:
                self.position = candidate_position
                break

    def draw(self) -> None:
        """Метод отрисовывает Apple."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс отвечает за хранение сегментов змейки, движение,
    изменение направления, рост после съеденного яблока, проверку столкновений
    и отрисовку змейки.
    """

    def __init__(self, body_color: Color = SNAKE_COLOR) -> None:
        super().__init__(body_color=body_color)
        self.length: int = 1
        self.direction: Pointer = RIGHT
        self.next_direction: Pointer | None = None
        self.last: Pointer | None = None
        self.positions = [self.position]

    def get_head_position(self) -> Pointer:
        """Метод возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Метод реализует движение змейки"""
        head_x, head_y = self.get_head_position()
        head_x = (head_x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH
        head_y = (head_y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT
        new_head_position = (head_x, head_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
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
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента змейки
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основной цикл игры, проверяет съедено ли яблоко и столкновение головы
    змейки с хвостом.
    """
    pg.init()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    # См. комментарий в Apple. Тут бы написал так:
    # snake = Snake()
    # apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            apple.randomize_position(snake.positions)
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
