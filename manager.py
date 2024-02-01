from object import * 

class Manager:
   def __init__(self):
      self.objects = []
      self.current_dragged_object = None
      self.connection_selected_object = None

      self.current_func = lambda x : str(int(x) * int(x))

   def place_object(self, mouse_pos):
      obj = Object(*(mouse_pos))
      obj.function = self.current_func
      self.objects.append(obj)

   def connect_objects(self, obj):
      if self.connection_selected_object is not obj:
         self.connection_selected_object.connect(obj)

   def get_selected_object(self, mouse_pos): 
      for obj in self.objects:
         if obj.rect.collidepoint(mouse_pos):
            return obj
      return None 
   
   def select_drag_object(self, object):
      self.current_dragged_object = object

   def select_connect_object(self, object):
      self.connection_selected_object = object

   def release_draged_object(self):
      self.current_dragged_object = None

   def drag_object(self, mouse_pos):
      if self.current_dragged_object:
         self.current_dragged_object.rect.center = mouse_pos
   
   def send_data(self, data): #! Hardcoded
      self.objects[0].send_data(data)