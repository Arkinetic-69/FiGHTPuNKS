import pygame

"""Handles the animations for the game.
This module contains the Animation class, which manages the animations
for characters and other game elements."""

class Animation:
    """Class to handle animations for game elements."""
    
    def __init__(self, image_paths, frame_duration):
        """Initialize the animation with a list of image paths and frame duration."""
        self.images = [pygame.image.load(path) for path in image_paths]
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0

    def update(self, delta_time):
        """Update the current frame based on the elapsed time."""
        self.time_since_last_frame += delta_time
        if self.time_since_last_frame >= self.frame_duration:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.time_since_last_frame = 0

    def get_current_image(self):
        """Return the current image for rendering."""
        return self.images[self.current_frame]