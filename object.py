import pygame
from settings import *

class Object:
   def __init__(self, x, y):
      self.function = None

      self.color = (0, 0, 255)
      self.size = 60
      self.rect = pygame.Rect(x, y, self.size, self.size)

      self.reciever_sock = RecivierSocket()
      self.sender_sock = SenderSocket()
 
   def __get_sender_pos(self):
      return self.rect.center + pygame.Vector2(20, 0)
   
   def __get_reciver_pos(self):
      return  self.rect.center - pygame.Vector2(20, 0)
   
   def draw(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      # Calculate positions for the sockets
      receiver_socket_pos = self.__get_reciver_pos()
      sender_socket_pos = self.__get_sender_pos()

      pygame.draw.circle(surface, (0, 255, 255), receiver_socket_pos, 5)
      pygame.draw.circle(surface, (0, 255, 0), sender_socket_pos, 5)

   
   def draw_connection(self, surface):
      if self.sender_sock.send_to:
         other = self.sender_sock.send_to
         sender_socket_pos = self.__get_sender_pos()
         receiver_socket_pos = other.__get_reciver_pos()

         # Draw a line from sender socket to receiver socket
         pygame.draw.line(surface, RED, sender_socket_pos, receiver_socket_pos, 5)

         # Calculate the direction of the arrow
         direction = pygame.Vector2(receiver_socket_pos) - pygame.Vector2(sender_socket_pos)
         direction.normalize_ip()

         # Calculate the points of the arrowhead
         arrowhead_points = [
               receiver_socket_pos,
               receiver_socket_pos + direction.rotate(135) * 14,  # Left point
               receiver_socket_pos + direction.rotate(-135) * 14,  # Right point
         ]
         # Draw the arrowhead as a polygon
         pygame.draw.polygon(surface, RED, arrowhead_points)

         # Draw data
         if self.sender_sock.connection.data:
            progress =  1 - self.sender_sock.connection.counter / DATA_SEND_TIME
            pos = sender_socket_pos + (receiver_socket_pos - sender_socket_pos )*progress
            rect = pygame.Rect(pos.x, pos.y, 30, 30)
            pygame.draw.rect(surface, BLACK , rect)

   def connect(self, other):
      connection = Connection(other.reciever_sock)
      self.sender_sock.send_to = other
      self.sender_sock.connection = connection
      other.reciever_sock.take_from = self

   def update_connections(self):
      if self.sender_sock.connection:
         self.sender_sock.connection.move_data()

   def send_data(self, data):
      self.sender_sock.connection.send_data(data)

class SenderSocket:
   def __init__(self):
      self.send_to = None
      self.connection = None

class RecivierSocket:
   def __init__(self):
      self.take_from = None
      self.data_current_data = None

class Connection:
   def __init__(self, send_to):
      self.send_to = send_to
      self.data = None
      self.counter = 0
   
   def send_data(self, data):
      self.data = data
      self.counter = DATA_SEND_TIME

   def move_data(self):
      if self.counter <= 0:
         self.send_to.data = self.data
         self.data = None
      else:
         self.counter -= 1
