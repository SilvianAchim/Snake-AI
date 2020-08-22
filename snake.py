#####################################
#  SNAKE AI MADE BY SILVIAN ACHIM
# YOUTUBE: https://www.youtube.com/channel/UCWQRzGZa2Owh4U81pEQkObg

import random

import main
import fruit
import math


def distance(xa, xb, ya, yb):
    return int(math.sqrt(pow((xa - xb), 2) + pow((ya - yb), 2))) - 1


def ok(x, y):
    if 0 <= x <= main.LENGTH and 0 <= y <= main.WIDTH:
        return True
    return False


class Pos:
    def __init__(self):
        self.x = 0
        self.y = 0


class Snake:

    def __init__(self):
        self.snake = []
        for i in range(100):
            self.snake.append(Pos())
        self.gameOver = 0
        self.fruct = fruit.Fruit()
        # self.generate()
        self.direction = 0
        self.tail = 4
        self.score = 0
        self.eat = False
        self.loop_tail = 0
        self.food_distance = 5

        self.snake[0].y = 5
        self.snake[1].y = 4
        self.snake[2].y = 3
        self.snake[3].y = 2
        self.snake[4].y = 1

        self.snake[0].x = 5
        self.snake[1].x = 5
        self.snake[2].x = 5
        self.snake[3].x = 5
        self.snake[4].x = 5

    def game(self):
        for i in range(self.tail, 0, -1):
            self.snake[i].x = self.snake[i - 1].x
            self.snake[i].y = self.snake[i - 1].y
        # Move the snake
        if self.direction == 0:
            self.snake[0].y += 1
        if self.direction == 1:
            self.snake[0].x -= 1
        if self.direction == 2:
            self.snake[0].x += 1
        if self.direction == 3:
            self.snake[0].y -= 1
        # The snake has eaten a fruit
        if self.snake[0].x == self.fruct.pos.x and self.snake[0].y == self.fruct.pos.y:
            self.tail += 1
            self.score += 1
            self.eat = True
            self.generate()
        # Game over cases
        if self.snake[0].x >= main.LENGTH:
            self.gameOver = 1
        if self.snake[0].y >= main.WIDTH:
            self.gameOver = 1
        if self.snake[0].x < 0:
            self.gameOver = 1
        if self.snake[0].y < 0:
            self.gameOver = 1

        for i in range(1, self.tail + 1):
            if self.snake[0].x == self.snake[i].x and self.snake[0].y == self.snake[i].y:
                self.gameOver = 2

    def reset(self):
        self.gameOver = 0
        self.generate()
        self.direction = 0
        self.tail = 4
        self.score = 0
        self.eat = False
        for i in range(100):
            self.snake[i].x = 5
            self.snake[i].y = 5
        self.loop_tail = 0
        self.food_distance = 5

        self.snake[0].y = 5
        self.snake[1].y = 4
        self.snake[2].y = 3
        self.snake[3].y = 2
        self.snake[4].y = 1

    def vision2(self):
        output = []
        if self.direction == 0:
            # Distance to the food
            output.append(self.snake[0].x - self.fruct.pos.x - 1)  # Right
            if self.fruct.pos.x <= (self.snake[0].x - 1) and self.fruct.pos.y >= (self.snake[0].y + 1):
                output.append(
                    distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y + 1,
                             self.fruct.pos.y))  # ForwardRight
            else:
                output.append(
                    - distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y + 1,
                               self.fruct.pos.y))  # ForwardRight
            output.append(self.fruct.pos.y - self.snake[0].y - 1)  # Forward
            if self.fruct.pos.x >= (self.snake[0].x + 1) and self.fruct.pos.y >= (self.snake[0].y + 1):
                output.append(
                    distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y + 1,
                             self.fruct.pos.x))  # ForwardLeft
            else:
                output.append(
                    - distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y + 1,
                               self.fruct.pos.x))  # ForwardLeft
            output.append(self.fruct.pos.x - self.snake[0].x - 1)  # Left

            # Distance to nearest obstacle
            # 1(Right)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.snake[0].x))
            # 8(ForwardRight)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                y += 1
                x -= 1
            output.append(min(d, (distance(self.snake[0].x, 0, self.snake[0].y, main.WIDTH))))
            # 7(Forward)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = y - self.snake[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (main.WIDTH - self.snake[0].y - 1)))
            # (ForwardLeft)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                x += 1
                y += 1
            output.append(min(d, (distance(self.snake[0].x, main.LENGTH, self.snake[0].y, main.WIDTH))))
            # (Left)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = x - (self.snake[0].x + 1)
                        run = False
                        break
                x += 1
            output.append(min((main.LENGTH - self.snake[0].x - 1), d))

        if self.direction == 1:
            # Distance to the food
            output.append(self.snake[0].y - self.fruct.pos.y - 1)  # Right
            if self.fruct.pos.x <= (self.snake[0].x - 1) and self.fruct.pos.y <= (self.snake[0].y - 1):
                output.append(
                    distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y - 1,
                             self.fruct.pos.y))  # Forward Right
            else:
                output.append(
                    - distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y - 1,
                               self.fruct.pos.y))  # Forward Right
            output.append(self.snake[0].x - self.fruct.pos.x - 1)  # Forward
            if self.fruct.pos.x <= (self.snake[0].x - 1) and self.fruct.pos.y >= (self.snake[0].y + 1):
                output.append(
                    distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y + 1,
                             self.fruct.pos.y))  # Forward Left
            else:
                output.append(
                    - distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y + 1,
                               self.fruct.pos.y))  # Forward Left
            output.append(self.fruct.pos.y - self.snake[0].y - 1)  # Left

            # Distance to the nearest obstacle
            # (Right)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.snake[0].y))

            # (Forward Right)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.snake[0].x, 0, self.snake[0].y, 0))))

            # (Forward)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.snake[0].x))

            # (Forward Left)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                y += 1
                x -= 1
            output.append(min(d, (distance(self.snake[0].x, 0, self.snake[0].y, main.WIDTH))))

            # (Left)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = y - self.snake[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (main.WIDTH - self.snake[0].y - 1)))

        if self.direction == 2:
            # Distance to the food
            output.append(self.fruct.pos.y - self.snake[0].y - 1)  # Right
            if self.fruct.pos.x >= (self.snake[0].x + 1) and self.fruct.pos.y >= (self.snake[0].y + 1):
                output.append(
                    distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y + 1,
                             self.fruct.pos.y))  # Forward Right
            else:
                output.append(
                    - distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y + 1,
                               self.fruct.pos.y))  # Forward Right
            output.append(self.fruct.pos.x - self.snake[0].x - 1)  # Forward
            if self.fruct.pos.x >= (self.snake[0].x + 1) and self.fruct.pos.y <= (self.snake[0].y - 1):
                output.append(
                    distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y - 1,
                             self.fruct.pos.y))  # Forward left
            else:
                output.append(
                    - distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y - 1,
                               self.fruct.pos.y))  # Forward left
            output.append(self.snake[0].y - self.fruct.pos.y - 1)  # Left

            # Distance to the nearest object
            # 7(Right)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = y - self.snake[0].y - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (main.WIDTH - self.snake[0].y - 1)))

            # 8(Forward Right)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y + 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                y += 1
                x += 1
            output.append(min(d, (distance(self.snake[0].x, 0, self.snake[0].y, main.WIDTH))))

            # 5(Forward)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = x - self.snake[0].x - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (main.LENGTH - self.snake[0].x - 1)))

            # 4(Forward Left)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.snake[0].x, main.LENGTH, self.snake[0].y, 0))))

            # 3(Left)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.snake[0].y))

        if self.direction == 3:
            # Distance to the food
            output.append(self.fruct.pos.x - self.snake[0].x - 1)  # Right
            if self.fruct.pos.x >= (self.snake[0].x + 1) and self.fruct.pos.y <= (self.snake[0].y - 1):
                output.append(
                    distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y - 1,
                             self.fruct.pos.y))  # Forward Right
            else:
                output.append(
                    - distance(self.snake[0].x + 1, self.fruct.pos.x, self.snake[0].y - 1,
                               self.fruct.pos.y))  # Forward Right
            output.append(self.snake[0].y - self.fruct.pos.y - 1)  # Forward
            if self.fruct.pos.x <= (self.snake[0].x - 1) and self.fruct.pos.y <= (self.snake[0].y - 1):
                output.append(
                    distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y - 1,
                             self.fruct.pos.y))  # Forward Left
            else:
                output.append(
                    - distance(self.snake[0].x - 1, self.fruct.pos.x, self.snake[0].y - 1,
                               self.fruct.pos.y))  # Forward Left
            output.append(self.snake[0].x - self.fruct.pos.x - 1)  # Left

            # Distance to the nearest object
            # 5(Right)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = x - self.snake[0].x - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (main.LENGTH - self.snake[0].x - 1)))

            # (Forward Right)
            d = 100
            x = self.snake[0].x + 1
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.snake[0].x, main.LENGTH, self.snake[0].y, 0))))

            # (Forward)
            d = 100
            x = self.snake[0].x
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].y - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.snake[0].y))

            # (Forward Left)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y - 1
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = distance(self.snake[0].x, x, self.snake[0].y, y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.snake[0].x, 0, self.snake[0].y, 0))))

            # (Left)
            d = 100
            x = self.snake[0].x - 1
            y = self.snake[0].y
            run = True

            while ok(x, y) and run:
                for i in range(1, self.tail + 1):
                    if x == self.snake[i].x and y == self.snake[i].y:
                        d = self.snake[0].x - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.snake[0].x))

        return output

    def generate(self):
        k = False
        a = 0
        b = 0
        z = 0
        while not k:
            k = True
            a = random.randrange(0, main.LENGTH)
            b = random.randrange(0, main.WIDTH)
            for i in range(0, self.tail + 1):
                if self.snake[i].x == a and self.snake[i].y == b:
                    k = False
            if k and z <= 200:
                food = self.food_distance
                if self.food_distance > 2:
                    self.food_distance = random.randrange(2, food + 1)
                else:
                    self.food_distance = random.randrange(0, food + 1)
                z += 1
                # Left
                x = a - 1
                y = b
                d = 1
                run = True
                while ok(x, y) and run:
                    for i in range(1, self.tail + 1):
                        if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                            run = False
                            k = False
                            break
                        if d >= self.food_distance:
                            run = False
                            break
                    x -= 1
                    d += 1
                if k:
                    # Top left
                    d = 1
                    x = a - 1
                    y = b - 1
                    run = True
                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        x -= 1
                        y -= 1
                        d += 1
                if k:
                    # Top
                    d = 1
                    x = a
                    y = b - 1
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        y -= 1
                        d += 1
                if k:
                    # Top right
                    d = 1
                    x = a + 1
                    y = b - 1
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        y -= 1
                        x += 1
                        d += 1
                if k:
                    # Right
                    d = 1
                    x = a + 1
                    y = b
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        x += 1
                        d += 1
                if k:
                    # Bottom Right
                    d = 1
                    x = a + 1
                    y = b + 1
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        y += 1
                        x += 1
                        d += 1
                if k:
                    # Bottom
                    d = 1
                    x = a
                    y = b + 1
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        y += 1
                        d += 1
                        d += 1
                if k:
                    # Bottom left
                    d = 1
                    x = a - 1
                    y = b + 1
                    run = True

                    while ok(x, y) and run:
                        for i in range(1, self.tail + 1):
                            if x == self.snake[i].x and y == self.snake[i].y and d < self.food_distance:
                                k = False
                                run = False
                                break
                            if d >= self.food_distance:
                                run = False
                                break
                        y += 1
                        x -= 1
                        d += 1
                self.food_distance = food
            elif z > 100:
                self.food_distance -= 1

        self.fruct.pos.x = a
        self.fruct.pos.y = b
