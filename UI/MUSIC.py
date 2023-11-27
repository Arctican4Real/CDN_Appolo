import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
white = (143, 67, 238)
black = (45, 39, 39)
purple = (65, 53, 67)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Set screen dimensions
screen_width = 1000
screen_height = 500

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the caption
pygame.display.set_caption('Music Player')

# Set up fonts
pygame.font.init()
font = pygame.font.Font("./Roboto-Black.ttf", 36)

# Set up music playback
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# Set up buttons
def draw_button(x, y, w, h, text, color, txtcolor , action=None):
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, black, (x, y, w, h), 2)
    label = font.render(text, 1, txtcolor)
    screen.blit(label, (x + w/2 - label.get_width()/2, y + h/2 - label.get_height()/2))
    return pygame.Rect(x, y, w, h)



# Display area for album art
album_art_x = 365
album_art_y = 20
album_art_width = 300
album_art_height = 300



# Play the music
pygame.mixer.music.load('music.mp3')
#pygame.mixer.music.play()

# Load the album art


# Game loop
running = True
while running:
    screen.fill(purple)
    pygame.draw.rect(screen, black, (100, 335, 800, 2))
    #pygame.draw.rect(screen, black, (100, 400, 800, 2))
    play_button = draw_button(170, 350, 200, 50, 'Play', black, white)
    pause_button = draw_button(420, 350, 200, 50, 'Pause', black, white)
    unpause_button = draw_button(420, 420, 200, 50, 'Unpause', black, white)
    stop_button = draw_button(670, 350, 200, 50, 'Stop', black, white)
    album_art = pygame.image.load('album_art.jpg')
    album_art = pygame.transform.scale(album_art, (album_art_width, album_art_height))

    # Display the album art
    screen.blit(album_art, (album_art_x, album_art_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if play_button.collidepoint(event.pos):
                    pygame.mixer.music.play()
                elif pause_button.collidepoint(event.pos):
                    pygame.mixer.music.pause()
                elif stop_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                elif unpause_button.collidepoint(event.pos):
                    pygame.mixer.music.unpause()

    pygame.display.flip()

pygame.quit()