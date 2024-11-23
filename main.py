import pygame
import time
import random
SIZE = 24
BACKGROUND_COLOR = (110,110,5)

class Apple:
  def __init__(self,parent_screen):
    self.image = pygame.image.load("resources/apple (1).png").convert()
    self.parent_screen = parent_screen
    self.x = SIZE*3
    self.y = SIZE*3

  def draw(self):
    self.parent_screen.blit(self.image,(self.x,self.y))
    pygame.display.flip()   
   
  def move (self):
     self.x = random.randint(0,25)*SIZE
     self.y = random.randint(0,20)*SIZE

class Snake:
  def __init__(self,parent_screen,length):
    self.length= length
    self.parent_screen = parent_screen
    self.block = pygame.image.load("resources/block (1).png").convert()
    self.x = [SIZE]*length
    self.y = [SIZE]*length
    self.direction = "down"

  def increase_length(self):
     self.length+=1
     self.x.append(-1)
     self.y.append(-1)

  def move_left(self):
      self.direction = "left"
  def move_right(self):
     self.direction = "right"
  def move_up(self):
     self.direction = "up"
  def move_down(self):
     self.direction = "down"
  
  
  def draw(self):
    for i in range (self.length):
       self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
    pygame.display.flip()

  

  def walk(self):
     for  i in range(self.length-1,0,-1):
       self.x[i]= self.x[i-1]
       self.y[i]= self.y[i-1]
     
     if self.direction == "up":
      self.y[0] -= SIZE
     if self.direction == "down":
      self.y[0] += SIZE
     if self.direction == "left":
      self.x[0] -= SIZE
     if self.direction == "right":
      self.x[0] += SIZE
     self.draw()

class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()
        pygame.display.set_caption("Snake Game")
        self.surface= pygame.display.set_mode((1000,800))
        self.surface.fill((110,110,5))
        self.snake = Snake(self.surface,1)
        self.snake.walk()
        self.apple = Apple(self.surface)
        self.apple.draw()
      
    def display_score(self):
       font = pygame.font.SysFont("arial",30)
       score = font.render(f"Score:{self.snake.length}",True,(2, 26, 237))
       self.surface.blit(score,(700,10))
       

    def is_collision(self,x1,y1,x2,y2):
       if x1 >= x2 and x1 < x2 + SIZE:
          if y1 >= y2 and y1 < y2 + SIZE:
             return True
          
       return False
   
    def play_background_music(self):
       pygame.mixer.music.load("resources/bgmu.mp3")
       pygame.mixer.music.play(-1)
       
       

     
    def render_background(self):
       bg = pygame.image.load("resources/bg.jpg") 
       self.surface.blit(bg,(0,0))
    def play(self):
       self.render_background()
       self.snake.walk()
       self.apple.draw()
       self.display_score()
       pygame.display.flip()
      #snake colliding with apple
       if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
          sound = pygame.mixer.Sound("resources\eat.mp3")
          pygame.mixer.Sound.play(sound)
          self.snake.increase_length()
          self.apple.move()
      #snake colliding with itself   
       for i in range(3,self.snake.length):
          if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
             sound = pygame.mixer.Sound("resources\crash.mp3")
             pygame.mixer.Sound.play(sound)
             raise  "Collision Occured"
             exit(0)

         # check for snake out of bounds
       if self.snake.x[0] < 0 or self.snake.x[0] > self.surface.get_width() or self.snake.y[0] < 0 or self.snake.y[0] > self.surface.get_height():
        sound = pygame.mixer.Sound("resources\crash.mp3")
        pygame.mixer.Sound.play(sound)
        raise "Collision Occured"
        exit(0)

    def show_game_over(self):
       self.render_background()
       font = pygame.font.SysFont("arial",30)
       line1 = font.render(f"Score:{self.snake.length}",True,(2, 26, 237))
       self.surface.blit(line1,(200,300))
       line2 = font.render("to play again press Enter.to exit press Escape",True,(2, 26, 237))
       self.surface.blit(line2,(200,350))
       pygame.display.flip()
    def reset(self):
      self.snake = Snake(self.surface,1)
      self.apple = Apple(self.surface)
      pygame.mixer.music.pause()
    def run(self):
        running = True
        pause = False
        while running:
         for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                     
                if event.key == pygame.K_RETURN:
                   pygame.mixer.music.unpause()
                   pause = False
                if not pause: 

                 if event.key== pygame.K_UP:
                    self.snake.move_up()

                if event.key== pygame.K_DOWN:
                    self.snake.move_down()

                if event.key== pygame.K_LEFT:
                    self.snake.move_left()

                if event.key== pygame.K_RIGHT:
                    self.snake.move_right()

            elif event.type == pygame.QUIT:
                running = False
         try:
           if not pause:
              self.play()
         except Exception as e:
          self.show_game_over() 
          pause  = True
          self.reset()
         time.sleep(0.2)
if __name__=="__main__":
    game = Game()
    game.run()