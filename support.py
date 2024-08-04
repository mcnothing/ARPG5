import pygame
from csv import reader
from os import walk

def import_csv_layout(path) -> list:
    map_data = []
    with open(path) as f:
        layout = reader(f, delimiter=',')
        for row in layout:
            map_data.append(list(row))
    return map_data

def import_folder(path) -> list:
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            surface_list.append(pygame.image.load(full_path).convert_alpha())
    return surface_list

def wrap_text(surface, text, color, rect, font, aa=False, bkg=None) -> None:
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2
    font_height = font.size('Tg')[1]
    while text:
        i = 1
        if y + font_height > rect.bottom:
            break
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        if i < len(text):
            i = text.rfind(' ', 0, i) + 1

        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_color_key(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        text = text[i:]
    return text