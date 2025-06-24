import pygame
from settings import Settings
from fighters import Kevin

"""Will organize the Dummy class here.
Which is the Test Dummy that will be used for training purposes.
Includes attributes same as the fighters."""


class Dummy(Kevin):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.idle = self.settings.dummy_idle
        self.index_count = len(self.idle)
        
        self.image = self.idle[0]
        
