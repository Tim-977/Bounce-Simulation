import pygame
import random

WIDTH = 600
HEIGHT = 400
RADIUS = 15
LINE_THICKNESS = 2
GRAVITY = 0.1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Circle:
    def __init__(self, x, y, radius, color, velocity):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity = velocity

    def move(self):
        self.velocity[1] += GRAVITY

        self.x += self.velocity[0]
        self.y += self.velocity[1]

    def check_collision(self, width, height, line_y):
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.velocity[0] = -self.velocity[0]
        if self.y - self.radius < 0 or self.y + self.radius > line_y:
            self.velocity[1] = -self.velocity[1]
        elif self.y + self.radius > line_y and self.velocity[1] > 0:
            self.velocity[1] = -self.velocity[1]

        if self.y + self.radius > line_y:
            self.y = line_y - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


def get_random_color(i):
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def rainbow_color(current_ball, total_balls):
    current_ball = total_balls - current_ball
    rainbow = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (143, 0, 255)]
    num_colors = len(rainbow)
    num_intermediate_colors = total_balls - num_colors
    balls_per_color = num_intermediate_colors // (num_colors - 1)
    remainder = num_intermediate_colors % (num_colors - 1)
    intermediate_colors = []
    for i in range(num_colors - 1):
        r1, g1, b1 = rainbow[i]
        r2, g2, b2 = rainbow[i + 1]
        for j in range(balls_per_color):
            ratio = (j + 1) / (balls_per_color + 1)
            r = int((1 - ratio) * r1 + ratio * r2)
            g = int((1 - ratio) * g1 + ratio * g2)
            b = int((1 - ratio) * b1 + ratio * b2)
            intermediate_colors.append((r, g, b))
        if remainder > i:
            ratio = (balls_per_color + 1) / (balls_per_color + 2)
            r = int((1 - ratio) * r1 + ratio * r2)
            g = int((1 - ratio) * g1 + ratio * g2)
            b = int((1 - ratio) * b1 + ratio * b2)
            intermediate_colors.append((r, g, b))
    colors = rainbow[:1] + intermediate_colors + rainbow[-1:]
    index = min(int((current_ball - 1) / (total_balls - 1) * len(colors)), len(colors) - 1)
    return colors[index]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Simulation")

clock = pygame.time.Clock()

x, y = 100, 100
radius = RADIUS

circles = []
for i in range(10):
    #x = random.randint(RADIUS * 2, WIDTH - RADIUS * 2)
    #y = random.randint(RADIUS * 2, HEIGHT - RADIUS * 2)
    color = rainbow_color(i, 10)
    velocity = [3, 3]
    circle = Circle(x, y, radius, color, velocity)
    circles.append(circle)
    radius += 1
    x += 50
    y += 10

line_y = HEIGHT - RADIUS
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for circle in circles:
        circle.move()
        circle.check_collision(WIDTH, HEIGHT, line_y)

    screen.fill(BLACK)

    pygame.draw.line(screen, WHITE, (0, line_y), (WIDTH, line_y), LINE_THICKNESS)

    for circle in circles:  
        circle.draw(screen)

    pygame.display.flip()

    clock.tick(120)
