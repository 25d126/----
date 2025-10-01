# import 및 초기화
import pygame
import sys
import random

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('벽돌깨기 게임')

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 패들 설정
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 7

# 공 설정
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5 * random.choice((1, -1))
ball_speed_y = -5

# 벽돌 설정
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
bricks = []
for row in range(BRICK_ROWS):
	for col in range(BRICK_COLS):
		brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 50, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
		bricks.append(brick)

# 점수
score = 0
font = pygame.font.SysFont(None, 36)

# 게임 루프
clock = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# 패들 이동
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and paddle.left > 0:
		paddle.x -= paddle_speed
	if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
		paddle.x += paddle_speed

	# 공 이동
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	# 벽 충돌
	if ball.left <= 0 or ball.right >= WIDTH:
		ball_speed_x *= -1
	if ball.top <= 0:
		ball_speed_y *= -1
	if ball.bottom >= HEIGHT:
		running = False  # 게임 오버

	# 패들 충돌
	if ball.colliderect(paddle):
		ball_speed_y *= -1
		ball.y = paddle.y - BALL_RADIUS * 2

	# 벽돌 충돌
	hit_index = ball.collidelist(bricks)
	if hit_index != -1:
		hit_brick = bricks.pop(hit_index)
		ball_speed_y *= -1
		score += 10

	# 화면 그리기
	screen.fill(BLACK)
	pygame.draw.rect(screen, BLUE, paddle)
	pygame.draw.ellipse(screen, RED, ball)
	for brick in bricks:
		pygame.draw.rect(screen, GREEN, brick)
	score_text = font.render(f'Score: {score}', True, WHITE)
	screen.blit(score_text, (10, 10))

	if not bricks:
		win_text = font.render('축하합니다! 클리어!', True, WHITE)
		screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
		pygame.display.flip()
		pygame.time.wait(2000)
		running = False

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
sys.exit()
