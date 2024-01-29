import pygame
from settings import *
from manager import Manager

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

manager = Manager()

while running:

   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
      if event.type == pygame.MOUSEBUTTONDOWN: 
         mouse_pos = pygame.mouse.get_pos()
         # Left mouse button
         if event.button == 1:
            selected = manager.get_selected_object(mouse_pos)
            if selected:
               manager.select_drag_object(selected)
            else:
               manager.place_object(mouse_pos)
               
         # Right mouse button
         if event.button == 3: 
            manager.select_connect_object(manager.get_selected_object(mouse_pos))
      
      if event.type == pygame.MOUSEBUTTONUP: 
         mouse_pos = pygame.mouse.get_pos()
         if event.button == 3 and manager.connection_selected_object:
            other = manager.get_selected_object(mouse_pos)
            if other:
               manager.connect_objects(manager.connection_selected_object, other) # ! this part is a little wierd

         if event.button == 1:
            manager.release_draged_object()

   screen.fill("white")

   # ! this part also needs refactor
   for obj in manager.objects:
      obj.draw(screen)

   for obj in manager.objects:
      obj.draw_connection(screen)

   if manager.current_dragged_object:
      manager.drag_object(pygame.mouse.get_pos())

   pygame.display.flip()

   clock.tick(FPS) 

pygame.quit()