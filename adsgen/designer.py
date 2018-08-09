import pygame, sys
from PIL import Image
import json
from adsgen import pygame_input
from tkinter import Tk, StringVar, Entry, Button, Label
from tkinter.filedialog import askopenfilename
pygame.init()
# Tk().withdraw()

draws=json.load(open("imageoverlays.json"))
basicfont = pygame.font.SysFont(None, 48)


def displayselected(screen, px, topleft, prior):
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()
    return (x, y, width, height)

def AskValue():
    master=Tk()
    master.title("Saving...")
    master.eval('tk::PlaceWindow %s center' % master.winfo_pathname(master.winfo_id()))
    v = StringVar()
    Label(master, text="Name:", font=("Helvetica", 16)).pack(pady=8)
    Entry(master, textvariable=v, font=("Helvetica", 16)).pack(pady=7,padx=15)
    Button(master, text="Save", command=master.destroy, font=("Helvetica", 10)).pack(pady=5)
    master.mainloop()
    return v.get()

def setup(path):
    px = pygame.image.load(path)
    px = pygame.transform.scale(px, (1080, 520))
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def mainLoop(screen, px,filename):
    topleft = bottomright = prior = None
    quit = False
    draws[filename]=draws.get(filename) or {}
    for text,re in draws[filename].items():
        t=basicfont.render(text, True, (0, 0, 0))
        textrect=pygame.draw.rect(screen,(0)*3,re,2)
        surface=t.get_rect()
        surface.centerx=textrect.centerx
        surface.centery=textrect.centery
        screen.blit(t,surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                topleft = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                bottomright = event.pos
                left, upper, right, lower = topleft + bottomright
                if right < left:
                    left, right = right, left
                if lower < upper:
                    lower, upper = upper, lower
                if (abs(left-right)<20 or abs(upper-lower)<20):
                    topleft = bottomright = prior = None
                    break
                right, lower = right-left, lower-upper
                textinput = AskValue()
                draws[filename][textinput]=[left, upper, right, lower]
                for text,re in draws[filename].items():
                    t=basicfont.render(text, True, (0, 0, 0))
                    textrect=pygame.draw.rect(screen,(0)*3,re,2)
                    surface=t.get_rect()
                    surface.centerx=textrect.centerx
                    surface.centery=textrect.centery
                    screen.blit(t,surface)
                pygame.display.update()
                topleft = bottomright = prior = None
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit=True
                break
        if quit:
            break
        if topleft and not quit:
            prior=displayselected(screen, px, topleft, prior)

def design(folder,types):
    p=Tk()
    filename = askopenfilename(initialdir=folder, title="Select Image",filetypes=types)
    p.destroy()
    if filename:
        screen, px = setup(filename)
        mainLoop(screen, px,filename)
        json.dump(draws,open("imageoverlays.json",'w'))
