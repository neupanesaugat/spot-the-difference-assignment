"""
game_logic.py
Handles all game state and logic for the Spot the Difference game.
Tracks found differences, mistakes, and cumulative scoring.
This class works with the GUI and image processor classes,
demonstrating class interaction in OOP.
"""


class GameLogic:
    """
    Manages the game state including found differences,
    mistake tracking, and score keeping.
    
    Attributes are encapsulated using underscore prefix.
    The cumulative remaining count persists across multiple images.
    Mistakes reset each time a new image is loaded.
    """
    
    def __init__(self):
        # List of difference region coordinates
        self._regions = []
        # Tracks which differences have been found
        self._found = []
        # Mistake counter - resets per image
        self._mistakes = 0
        # Cumulative count across all images
        self._total_remaining = 0
        # Maximum mistakes allowed per image
        self._max_mistakes = 3
    
    def load_new_image(self, regions):
        """
        Sets up game state for a new image.
        Resets mistakes but adds to cumulative remaining count.
        
        Parameters:
            regions: List of (x, y, w, h) tuples for each difference
        """
        self._regions = regions
        # All differences start as not found
        self._found = [False] * len(regions)
        # Reset mistakes for new image
        self._mistakes = 0
        # Add 5 new differences to cumulative total
        self._total_remaining += len(regions)
    
    def check_click(self, click_x, click_y):
        """
        Checks if a click is close enough to any unfound difference.
        Uses distance from click to center of each region.
        
        Parameters:
            click_x: X coordinate of the click
            click_y: Y coordinate of the click
        Returns:
            Index of the found difference, or -1 if no match
        """
        for i, (x, y, w, h) in enumerate(self._regions):
            # Skip already found differences
            if self._found[i]:
                continue
            
            # Calculate center of the region
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Calculate distance from click to center
            distance = ((click_x - center_x) ** 2 + (click_y - center_y) ** 2) ** 0.5
            
            # Use half the region size as the tolerance radius
            radius = max(w, h) // 2
            
            # If click is within radius, mark as found
            if distance <= radius:
                self._found[i] = True
                self._total_remaining -= 1
                return i
        
        # No match found
        return -1
    
    def record_mistake(self):
        """
        Records a wrong click as a mistake.
        
        Returns:
            The updated mistake count
        """
        self._mistakes += 1
        return self._mistakes
    
    def is_game_over(self):
        """
        Checks if the player has used all allowed mistakes.
        
        Returns:
            True if mistakes reached the maximum (3)
        """
        return self._mistakes >= self._max_mistakes
    
    def all_found(self):
        """
        Checks if all differences in the current image are found.
        
        Returns:
            True if every difference has been found
        """
        return all(self._found)
    
    def get_mistakes(self):
        """Returns the current mistake count for this image"""
        return self._mistakes
    
    def get_total_remaining(self):
        """Returns the cumulative remaining differences across all images"""
        return self._total_remaining
    
    def get_unfound_regions(self):
        """
        Returns a list of regions that have not been found yet.
        Used by the reveal feature to show blue circles.
        
        Returns:
            List of (x, y, w, h) tuples for unfound differences
        """
        unfound = []
        for i, region in enumerate(self._regions):
            if not self._found[i]:
                unfound.append(region)
        return unfound