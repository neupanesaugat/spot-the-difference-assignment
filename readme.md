# Spot the Difference Game

A desktop application built with Python that lets players find hidden differences between two images.

## Team Members
- Member 1: Bibek kumar Chaudhary (S395751)
- Member 2: Name (Student ID)
- Member 3: Name (Student ID)
- Member 4: Name (Student ID)

## How to Install

Make sure you have Python 3 installed, then run:
## How to Run
python main.py

## How to Play

1. Click "Load Image" to choose any JPG, PNG, or BMP image
2. The original image appears on the left, the modified image on the right
3. Look carefully and click on the right image where you see a difference
4. Found differences are marked with a red circle on both images
5. You have a maximum of 3 mistakes per image
6. Click "Reveal" to show all unfound differences in blue
7. Load a new image to keep playing

## Project Structure

- main.py - Entry point that launches the application
- image_processor.py - Image loading and alteration classes using OpenCV
- game_logic.py - Game state management and click detection
- gui.py - Tkinter GUI for displaying images and handling interactions

## OOP Concepts Used

- Encapsulation: All class attributes use underscore prefix for protection
- Inheritance: ColorShiftAlteration, BlurAlteration, and BrightnessAlteration inherit from Alteration
- Polymorphism: Each alteration subclass overrides the apply() method differently
- Class Interaction: GUI class uses both DifferenceGenerator and GameLogic

## Image Alteration Types

1. Color Shift - Changes the hue of a region using HSV conversion
2. Blur - Applies Gaussian blur to make a region out of focus
3. Brightness - Increases the brightness of a region

## Technologies Used

- Python 3
- OpenCV - Image processing and manipulation
- Tkinter - GUI framework
- Pillow - Image format conversion for display# spot-the-difference-assignment
