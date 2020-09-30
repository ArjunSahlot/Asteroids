
    import pygame
    import tkinter as tk
    

    # Window Management
    WIDTH, HEIGHT = 900, 600

    screen_width = tk.Tk().winfo_screenwidth()
    screen_height = tk.Tk().winfo_screenheight()

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (screen_width//2-WIDTH//2, screen_height//2-HEIGHT//2)
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    

    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (128, 128, 128)

    
    def draw_window(win):
        win.fill(WHITE)


    def main(win, width, height):
        run = True
        while run:
            draw_window(win)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    # exit()
            pygame.display.update()

    
    main()

    