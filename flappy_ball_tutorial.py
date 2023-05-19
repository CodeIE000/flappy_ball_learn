import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 670

BALL_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("azonix", 50)

class Ball:
	IMGS = BALL_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 20

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y

	def move(self):
		self.tick_count += 1

		d = self.vel*self.tick_count + 1.5*self.tick_count**2

		if d >= 16:
			d = 16

		if d < 0:
			d -= 20

		self.y = self.y + d

		if d < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL

	def draw(self, win):
		self.img_count += 1

		if self.img_count < self.ANIMATION_TIME:                                                                            
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count < self.ANIMATION_TIME*3:
			self.img = self.IMGS[0]
		elif self.img_count < self.ANIMATION_TIME*4:
			self.img = self.IMGS[2]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.imgcount = self.ANIMATION_TIME*2

		rotated_image = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
		win.blit(rotated_image, new_rect.topleft) 

	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Pipe:
	GAP = 200
	VEL = 5

	def __init__(self, y):
		self.y = y
		self.height = 0

		self.left = 0
		self.right = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):
		self.height = self.y
		self.left = self.height - self.PIPE_TOP.get_height()
		self.right = self.height + self.GAP

	def move(self):
		self.y -= self.VEL

	def draw(self, win):
		win.blit(self.PIPE_TOP, (self.y, self.left))
		win.blit(self.PIPE_BOTTOM, (self.y, self.right))

	def collide(self, ball):
		ball_mask = ball.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		top_offset = (self.y + ball.x, self.left + round(ball.y))
		bottom_offset = (self.y + ball.x, self.right + round(ball.y))

		b_point = ball_mask.overlap(bottom_mask, bottom_offset)
		t_point = ball_mask.overlap(top_mask, top_offset)

		if t_point or b_point:
			return True

		return False

class Base:
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH

		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.x1, self.y))
		win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, ball, pipes, base, score):
	win.blit(BG_IMG, (0,-160))

	for pipe in pipes:
		pipe.draw(win)

	text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

	base.draw(win)

	ball.draw(win)
	pygame.display.update()

def main():
	ball = Ball(230,300)
	base = Base(600)
	pipes = [Pipe(700)]
	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	score = 0

	run = True
	while run:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		#ball.move()
		add_pipe = False
		rem = []
		for pipe in pipes:
			if pipe.collide(ball):
				pass

			if pipe.y + pipe.PIPE_TOP.get_width() < 0:
				rem.append(pipe)

			if not pipe.passed and pipe.y < ball.x:
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe:
			score += 1
			pipes.append(Pipe(550))

		for r in rem:
			pipes.remove(r)

		if ball.y + ball.img.get_height() >= 730:
			pass

		base.move()
		draw_window(win, ball, pipes, base, score)

	pygame.quit()
	quit()

main()