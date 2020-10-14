import pygame
import pygame.gfxdraw

# Setup
pygame.init()

win = pygame.display.set_mode(size=(1280,720),flags=pygame.RESIZABLE|pygame.DOUBLEBUF)
pygame.display.set_caption("DeMsg")

light = pygame.font.Font('fonts/Roboto-Light.ttf', 16)
regular = pygame.font.Font('fonts/Roboto-Regular.ttf', 16)
medium = pygame.font.Font('fonts/Roboto-Medium.ttf', 24)
bold = pygame.font.Font('fonts/Roboto-Bold.ttf', 36)

run = True
while run:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode(size=(event.w,event.h),flags=pygame.RESIZABLE)

    # Update some variables
    width, height = pygame.display.get_surface().get_size()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Fill background
    win.fill((127,127,127))

    # GUI
    # Left section
    chatsTitle = bold.render('Chats', 1, (25,25,25))
    sideBar = pygame.draw.rect(win, (255,255,255), (0,0,max(chatsTitle.get_width()+160,width//4),height))

    topSideBar = pygame.draw.rect(win, (220,220,220), (0,0,sideBar[2], 70))
    pygame.draw.line(win, (140,140,140), (0,70), (sideBar[2],70), 2)

    # Text
    win.blit(chatsTitle, (sideBar[2]//2-chatsTitle.get_width()//2, 15))

    # Right section
    pygame.draw.rect(win, (255,255,255), (sideBar[2]+20, height-80, width-sideBar[2]-40, 60))

    # Update display
    pygame.display.update()

# Exit
pygame.quit()
exit()
