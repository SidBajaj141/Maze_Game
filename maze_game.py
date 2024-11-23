import sys
import pygame
import textwrap

# Constants for directions and room

ASCEND, DESCEND, RIGHT_PASSAGE, LEFT_PASSAGE = 0, 1, 2, 3
WHITE, BLACK, BLUE, GREEN, GREY = (255, 255, 255), (0, 0, 0), (0, 0, 255), (0, 255, 0), (100, 100, 100)

# Node structure (Room)
class Node:
    def __init__(self, room_desc, treasure=0):
        self.room_desc = room_desc
        self.treasure = treasure
        self.adj_room = [None] * 4  # [Ascend, Descend, Right Passage, Left Passage]

# Graph structure (Map)
class Graph:
    def __init__(self):
        self.rooms = [
            Node("The Entrance: You stand before a massive stone gateway, "
                 "its edges worn from centuries of sandstorms. The air feels ancient, "
                 "and faint torchlight flickers, casting long shadows against the walls."),

            Node("A Narrow Hallway: The corridor twists in unnatural ways. The walls are etched with carvings "
                 "depicting ancient rituals, and the ground feels uneven underfoot. It seems as though many "
                 "adventurers lost their way here."),

            Node("A Dark Room: Shadows move eerily in the dim torchlight, as if watching you. A musty odor fills the air, "
                 "and every sound you make echoes endlessly, creating the illusion that you're not alone."),

            Node("An Armory: You find broken weapons and shattered shields littering the floor. Rusted blades hang precariously "
                 "from the walls. The air is thick with dust, and it feels as though a great battle was fought here long ago."),

            Node("A Sacred Shrine: The walls are covered in ancient glyphs that glow faintly. A large statue of a forgotten god "
                 "sits at the center, and incense burners rest in each corner, though they haven't been lit for centuries. "
                 "The silence here feels heavy, as if the shrine itself guards a long-lost secret."),

            Node("A Hidden Chamber: You crawl through a narrow passage to find yourself in a low-ceilinged chamber. The walls "
                 "seem to close in, and strange runes pulse faintly in the dark. The temperature drops, and it feels like the room "
                 "is waiting for something—or someone."),

            Node("The Treasure Room: At last, you find yourself in a grand chamber. In the center, a gleaming golden chest sparkles "
                 "in the torchlight. Piles of jewels and coins surround it, and the room hums with an aura of ancient magic. This is the "
                 "treasure that many sought but never lived to tell about.")
        ]
        self.rooms[6].treasure = 1  # Room 6 has the treasure
        self.setup_rooms()

    def setup_rooms(self):
        self.rooms[0].adj_room[LEFT_PASSAGE] = self.rooms[1]
        self.rooms[0].adj_room[ASCEND] = self.rooms[2]
        self.rooms[1].adj_room[DESCEND] = self.rooms[0]
        self.rooms[1].adj_room[RIGHT_PASSAGE] = self.rooms[2]
        self.rooms[1].adj_room[ASCEND] = self.rooms[3]
        self.rooms[2].adj_room[DESCEND] = self.rooms[0]
        self.rooms[2].adj_room[LEFT_PASSAGE] = self.rooms[1]
        self.rooms[2].adj_room[RIGHT_PASSAGE] = self.rooms[4]
        self.rooms[2].adj_room[ASCEND] = self.rooms[5]
        self.rooms[3].adj_room[DESCEND] = self.rooms[1]
        self.rooms[3].adj_room[ASCEND] = self.rooms[5]
        self.rooms[4].adj_room[LEFT_PASSAGE] = self.rooms[2]
        self.rooms[4].adj_room[ASCEND] = self.rooms[6]
        self.rooms[5].adj_room[DESCEND] = self.rooms[3]
        self.rooms[5].adj_room[RIGHT_PASSAGE] = self.rooms[2]
        self.rooms[5].adj_room[ASCEND] = self.rooms[6]
        self.rooms[6].adj_room[DESCEND] = self.rooms[4]

def wrap_text(text, font, max_width):
    """Wrap the text to fit within a given width."""
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        if font.size(' '.join(current_line))[0] > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line))
    return lines

def draw_text(screen, text, font, color, x, y, max_width):
    """Render wrapped text on the screen."""
    lines = wrap_text(text, font, max_width)
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x, y + i * 30))

def draw_room(screen, current_room, font, small_font):
    screen.fill(BLACK)
    draw_text(screen, current_room.room_desc, font, WHITE, 50, 50, screen.get_width() - 100)
    draw_text(screen, "Exits:", font, BLUE, 50, 350, screen.get_width() - 100)
    exit_y = 400
    if current_room.adj_room[ASCEND]:
        draw_text(screen, "Ascend", small_font, WHITE, 50, exit_y, screen.get_width() - 100)
        exit_y += 30
    if current_room.adj_room[DESCEND]:
        draw_text(screen, "Descend", small_font, WHITE, 50, exit_y, screen.get_width() - 100)
        exit_y += 30
    if current_room.adj_room[RIGHT_PASSAGE]:
        draw_text(screen, "Right Passage", small_font, WHITE, 50, exit_y, screen.get_width() - 100)
        exit_y += 30
    if current_room.adj_room[LEFT_PASSAGE]:
        draw_text(screen, "Left Passage", small_font, WHITE, 50, exit_y, screen.get_width() - 100)

def main():
    pygame.init()

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_width - 100, screen_height - 100))
    pygame.display.set_caption("Pyramid Adventure Game")

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 28)

    graph = Graph()
    current_room = graph.rooms[0]


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and current_room.adj_room[ASCEND]:
                    current_room = current_room.adj_room[ASCEND]
                elif event.key == pygame.K_DOWN and current_room.adj_room[DESCEND]:
                    current_room = current_room.adj_room[DESCEND]
                elif event.key == pygame.K_LEFT and current_room.adj_room[LEFT_PASSAGE]:
                    current_room = current_room.adj_room[LEFT_PASSAGE]
                elif event.key == pygame.K_RIGHT and current_room.adj_room[RIGHT_PASSAGE]:
                    current_room = current_room.adj_room[RIGHT_PASSAGE]

        if current_room.treasure:
            screen.fill(BLACK)
            draw_text(screen, "You found the treasure!", font, GREEN, 200, 200, screen.get_width() - 100)
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        draw_room(screen, current_room, font, small_font)
        pygame.display.flip()

if __name__ == "__main__":
    main()
