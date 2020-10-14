import pygame

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
    sideBar = pygame.draw.rect(win, (255,255,255), (0,0,width//5,height))

    # Chats
    chatsTitle = bold.render('Chats', 10, (25,25,25))
    win.blit(chatsTitle, (, height//2))

    # Update display
    pygame.display.update()

# Exit
pygame.quit()
exit()
