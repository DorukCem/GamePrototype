import pygame
from settings import *
from object import Object


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def place_object(mouse_pos, objects):
   obj = Object(*(mouse_pos))
   objects.append(obj)

def connect_objects(obj1, obj2):
   obj1.connect(obj2)

def get_selected_object(mouse_pos, objects):
   for obj in objects:
      if obj.rect.collidepoint(mouse_pos):
         return obj
   return None

objects = []
connections = set()
connection_selected_object = None
drag_selected_object = None

while running:

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
      if event.type == pygame.MOUSEBUTTONDOWN: 
         mouse_pos = pygame.mouse.get_pos()
         # Left mouse button
         if event.button == 1:
            drag_selected_object = get_selected_object(mouse_pos, objects)
            if not drag_selected_object:
               place_object(mouse_pos, objects)
               
         # Right mouse button
         if event.button == 3: 
            connection_selected_object = get_selected_object(mouse_pos, objects)
      
      if event.type == pygame.MOUSEBUTTONUP: 
         mouse_pos = pygame.mouse.get_pos()
         if event.button == 3 and connection_selected_object:
            other = get_selected_object(mouse_pos, objects)
            if other:
               connect_objects(connection_selected_object, other)

         if event.button == 1:
            drag_selected_object = None

   screen.fill("white")

   for obj in objects:
      obj.draw(screen)

   for obj in objects:
      obj.draw_connection(screen)

   if drag_selected_object:
      drag_selected_object.rect.center = pygame.mouse.get_pos()

   pygame.display.flip()

   clock.tick(FPS) 

pygame.quit()