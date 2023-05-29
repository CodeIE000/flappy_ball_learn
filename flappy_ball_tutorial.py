import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 1000
WIN_HEIGHT = 670

BALL_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball3.png")))]
PIPE_IMG = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe3.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe4.png")))]
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("azonix", 50)

class Pipe:
	GAP = 200
	VEL = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 0

		self.left = 0
		self.right = 0
		self.PIPE_LEFT = PIPE_IMG[1]
		self.PIPE_RIGHT = PIPE_IMG[0]

		self.passed = False
		self.self_width()

	def self_width(self):
		self.width = random.randrange(60, 350)
		self.left = self.width - self.PIPE_LEFT.get_width()
		self.right = self.width + self.GAP

	def move(self):
		self.y += self.VEL

	def draw(self, win, y):
	    win.blit(self.PIPE_TOP, (self.x, y))
	    win.blit(self.PIPE_BOTTOM, (self.x, y + self.GAP))



class Base:
	VEL = 5
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, x):
		self.x = x
		self.y1 = 0
		self.y2 = self.WIDTH
		self.y3 = self.WIDTH + self.y1

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL
		self.y3 += self.VEL

		if self.y1 + self.WIDTH < 0:
			self.y1 = self.y2 + self.WIDTH

		if self.y2 + self.WIDTH < 0:
			self.y2 = self.y3 + self.WIDTH

		if self.y3 + self.WIDTH < 0:
			self.y3 = self.y2 + self.WIDTH

	def draw(self, win):
		win.blit(self.IMG, (self.y1, self.x))
		win.blit(self.IMG, (self.y2, self.x))


def draw_window(win, pipes, base):
	win.blit(BG_IMG, (0,-160))
	win.blit(BG_IMG, (550, -160))

	for pipe in pipes:
		pipe.draw(win)
		self.y(win)


	base.draw(win)

	pygame.display.update()

def main():
	base = Base(600)
	pipes = [Pipe(200, 300)]
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
		pipe_vel = 5
		for pipe in pipes:

			pipe.move()


		base.move()
		draw_window(win, pipes, base)

	pygame.quit()
	quit()

main()