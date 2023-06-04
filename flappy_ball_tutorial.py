import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 1350
WIN_HEIGHT = 660

BALL_IMGS = [
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball1.png"))), 
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball2.png"))), 
pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "ball3.png")))
]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe3.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base1.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg7.png")))
MBG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "mbg2.png")))
STAT_FONT = pygame.font.SysFont("azonix", 50)

class Ball:
	IMGS = BALL_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIMATION_TIME = 5

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
	VEL = 3
	GAP = 400

	def __init__(self, y):
		self.y = y
		self.width = 0
		self.left = 0
		self.right = 0
		self.PIPE_LEFT = pygame.transform.flip(PIPE_IMG, True, False)
		self.PIPE_RIGHT = PIPE_IMG
		self.passed = False
		self.set_width()

	def set_width(self):
		self.width = random.randrange(250, 650)
		self.left = self.width - self.PIPE_LEFT.get_width()
		self.right = self.width + self.GAP

	def move(self):
		self.y += self.VEL

	def draw(self, win):
		win.blit(self.PIPE_LEFT, (self.left, self.y))
		win.blit(self.PIPE_RIGHT, (self.right, self.y))

	def collide(self, ball):
		ball_mask = ball.get_mask()
		left_mask = pygame.mask.from_surface(self.PIPE_LEFT)
		right_mask = pygame.mask.from_surface(self.PIPE_RIGHT)

		left_offset = (self.y - ball.x, self.left - round(ball.y))
		right_offset = (self.y - ball.x, self.right - round(ball.y))

		r_point = ball_mask.overlap(right_mask, right_offset)
		l_point = ball_mask.overlap(left_mask, left_offset)

		if l_point or r_point:
			return True

		return False

class Base1:
	VEL = 5
	HEIGHT = BASE_IMG.get_height()
	IMG = BASE_IMG

	def __init__(self, x):
		self.x = x
		self.y1 = 0
		self.y2 = self.HEIGHT

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL

		if self.y1 >= WIN_HEIGHT:
			self.y1 = self.y2 - self.HEIGHT

		if self.y2 >= WIN_HEIGHT:
			self.y2 = self.y1 - self.HEIGHT

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y1))
		win.blit(self.IMG, (self.x, self.y2))

class Base2:
	VEL = 5
	HEIGHT = BASE_IMG.get_height()
	IMG = pygame.transform.flip(BASE_IMG, True, False)

	def __init__(self, x):
		self.x = x
		self.y1 = 0
		self.y2 = self.HEIGHT

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL

		if self.y1 >= WIN_HEIGHT:
			self.y1 = self.y2 - self.HEIGHT

		if self.y2 >= WIN_HEIGHT:
			self.y2 = self.y1 - self.HEIGHT

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y1))
		win.blit(self.IMG, (self.x, self.y2))

class BG1:
	VEL = 1/4
	HEIGHT = BG_IMG.get_height()
	IMG = BG_IMG

	def __init__(self, x):
		self.x = x
		self.y1 = 0
		self.y2 = self.HEIGHT

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL

		if self.y1 >= WIN_HEIGHT:
			self.y1 = self.y2 - self.HEIGHT

		if self.y2 >= WIN_HEIGHT:
			self.y2 = self.y1 - self.HEIGHT

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y1))
		win.blit(self.IMG, (self.x, self.y2))

class BG2:
	VEL = 1/4
	HEIGHT = BG_IMG.get_height()
	IMG = BG_IMG

	def __init__(self, x):
		self.x = x
		self.y1 = 0
		self.y2 = self.HEIGHT

	def move(self):
		self.y1 += self.VEL
		self.y2 += self.VEL

		if self.y1 >= WIN_HEIGHT:
			self.y1 = self.y2 - self.HEIGHT

		if self.y2 >= WIN_HEIGHT:
			self.y2 = self.y1 - self.HEIGHT

	def draw(self, win):
		win.blit(self.IMG, (self.x, self.y1))
		win.blit(self.IMG, (self.x, self.y2))


def draw_window(win, ball, bg1, bg2, pipes, base1, base2, score):

	win.blit(MBG_IMG, (120,-160))
	win.blit(MBG_IMG, (600,-160))

	bg1.draw(win)
	bg2.draw(win)

	for pipe in pipes:
		pipe.draw(win)

	base1.draw(win)
	base2.draw(win)


	STAT_FONT = pygame.font.Font(None, 30)
	text = STAT_FONT.render("Score: " + str(score), True, (255,255,255))
	win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

	ball.draw(win)
	pygame.display.update()

def main():
	ball = Ball(630,400)
	bg1 = BG1(130)
	bg2 = BG2(600)
	base1 = Base1(1150)
	base2 = Base2(-30)
	pipes = [Pipe(-100)]
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

		bg1.move()
		bg2.move()

		for pipe in pipes:
			if pipe.collide(ball):
				pass

			if pipe.y >= 700:
				rem.append(pipe)

			if not pipe.passed and pipe.y > 300:
				pipe.passed = True
				add_pipe = True

			pipe.move()

		if add_pipe:
			score += 1
			pipes.append(Pipe(-100))

		for r in rem:
			pipes.remove(r)

		if ball.y + ball.img.get_height() >= 730:
			pass

		base1.move()
		base2.move()
		
		draw_window(win, ball, bg1, bg2, pipes, base1, base2, score)

	pygame.quit()
	quit()

main()