"""
image_processor.py
Handles all image processing operations using OpenCV.
Contains the base Alteration class, three alteration subclasses,
and the DifferenceGenerator class that creates the modified image.
"""

import cv2
import numpy as np
import random


class Alteration:
    """
    Base class for all image alterations.
    Uses inheritance - subclasses must override the apply() method.
    This demonstrates polymorphism as each subclass applies a different effect.
    """
    
    def __init__(self, name):
        # Encapsulation - name is protected with underscore
        self._name = name
    
    def get_name(self):
        """Returns the name of this alteration type"""
        return self._name
    
    def apply(self, image, x, y, w, h):
        """
        Apply the alteration to a region of the image.
        Must be overridden by subclasses.
        
        Parameters:
            image: The image array to modify
            x, y: Top-left corner of the region
            w, h: Width and height of the region
        """
        raise NotImplementedError("Subclasses must implement apply()")


class ColorShiftAlteration(Alteration):
    """
    Inherits from Alteration.
    Shifts the hue/color of a rectangular region.
    The change is noticeable but not too obvious.
    """
    
    def __init__(self):
        # Call parent constructor
        super().__init__("Color Shift")
    
    def apply(self, image, x, y, w, h):
        """
        Converts region to HSV color space, shifts the hue by 30,
        then converts back to BGR. This changes the color subtly.
        """
        region = image[y:y+h, x:x+w]
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        # Shift hue by 30 degrees, wrap around at 180
        hsv[:, :, 0] = (hsv[:, :, 0] + 30) % 180
        image[y:y+h, x:x+w] = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


class BlurAlteration(Alteration):
    """
    Inherits from Alteration.
    Applies a Gaussian blur effect to a rectangular region.
    Makes the region look slightly out of focus.
    """
    
    def __init__(self):
        super().__init__("Blur")
    
    def apply(self, image, x, y, w, h):
        """
        Uses OpenCV GaussianBlur with a 15x15 kernel
        to blur the selected region.
        """
        region = image[y:y+h, x:x+w]
        blurred = cv2.GaussianBlur(region, (15, 15), 0)
        image[y:y+h, x:x+w] = blurred


class BrightnessAlteration(Alteration):
    """
    Inherits from Alteration.
    Increases the brightness of a rectangular region.
    Makes the region appear lighter than the original.
    """
    
    def __init__(self):
        super().__init__("Brightness")
    
    def apply(self, image, x, y, w, h):
        """
        Uses convertScaleAbs to increase brightness by 60.
        beta parameter controls the brightness offset.
        """
        region = image[y:y+h, x:x+w]
        bright = cv2.convertScaleAbs(region, alpha=1, beta=60)
        image[y:y+h, x:x+w] = bright


class DifferenceGenerator:
    """
    Loads an image, creates a clone, and generates exactly 5
    non-overlapping differences using random alteration types.
    
    This class interacts with the Alteration subclasses,
    demonstrating class interaction in OOP.
    """
    
    def __init__(self):
        # Encapsulated attributes - all private
        self._original = None
        self._modified = None
        self._regions = []
        # Create one instance of each alteration type
        self._alterations = [
            ColorShiftAlteration(),
            BlurAlteration(),
            BrightnessAlteration()
        ]
    
    def load_image(self, file_path):
        """
        Loads an image from the given file path using OpenCV.
        Creates an exact clone and generates 5 differences.
        
        Parameters:
            file_path: Path to the image file (JPG, PNG, or BMP)
        """
        self._original = cv2.imread(file_path)
        if self._original is None:
            raise ValueError("Could not load image")
        # Create exact clone of the original
        self._modified = self._original.copy()
        self._regions = []
        self._generate_differences()
    
    def _generate_differences(self):
        """
        Creates exactly 5 non-overlapping difference regions.
        Each region gets a randomly chosen alteration type.
        Region size is 1/10th of the image dimensions.
        """
        height, width = self._original.shape[:2]
        # Each region is about 1/10th of image size
        region_w = width // 10
        region_h = height // 10
        
        for i in range(5):
            # Keep trying until we find a non-overlapping position
            while True:
                x = random.randint(0, width - region_w)
                y = random.randint(0, height - region_h)
                new_region = (x, y, region_w, region_h)
                
                if not self._overlaps(new_region):
                    break
            
            # Pick a random alteration and apply it - polymorphism in action
            alteration = random.choice(self._alterations)
            alteration.apply(self._modified, x, y, region_w, region_h)
            self._regions.append(new_region)
    
    def _overlaps(self, new_region):
        """
        Checks if a new region overlaps with any existing regions.
        Uses rectangle intersection logic.
        
        Parameters:
            new_region: Tuple of (x, y, width, height)
        Returns:
            True if overlap exists, False otherwise
        """
        nx, ny, nw, nh = new_region
        for (rx, ry, rw, rh) in self._regions:
            if (nx < rx + rw and nx + nw > rx and
                ny < ry + rh and ny + nh > ry):
                return True
        return False
    
    def get_original(self):
        """Returns the original unmodified image"""
        return self._original
    
    def get_modified(self):
        """Returns the modified image with 5 differences"""
        return self._modified
    
    def get_regions(self):
        """Returns the list of difference region coordinates"""
        return self._regions