# Here is our code for our innovative game "Candy Clicker"!
# Please go check out our readme.md to learn more about our game.
# Also, note that all the code below will not work without image, font, and music downloads. :)

import pygame
import math
import os
import sys
import json
import random

# <------------------ Initialization ------------------>

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load("new-dream-background-music.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

WIDTH = 1200
HEIGHT = 800
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# <--------------------------------------------------- Global Variables ------------------------------------------------------>

current_screen = "preferences"

# Preference options
confectionery_name = "ICS 3U1's Confectionery"
difficulty = "medium"
lollipop_colour = "pink-lollipop"
wallpaper_colour = "blue-wallpaper"

game_state = {
    "screen": current_screen,
    "difficulty": difficulty,
    "lollipop_colour": lollipop_colour,
    "wallpaper_colour": wallpaper_colour
}

# Custom fonts
font_path = os.path.join("fonts", "merriweather.ttf")
font_160 = pygame.font.Font(font_path, 160)  # Game over
font_100 = pygame.font.Font(font_path, 100)  # Title
font_80_merr = pygame.font.Font(font_path, 80)  # Subtitle
font_50 = pygame.font.Font(font_path, 50)  # Preferences subtitle
font_40 = pygame.font.Font(font_path, 40)  # Store
font_30_merr = pygame.font.Font(font_path, 30)  # Description
font_25 = pygame.font.Font(font_path, 25)  # Button/text
font_20 = pygame.font.Font(font_path, 20)  # Input box
font_10 = pygame.font.Font(font_path, 10)  # sweetener


# Font colours
title_colour = ""
subtitle_colour = ""
prompt_colour = ""

# Wallpaper images
blue_wallpaper = pygame.image.load("blue_wallpaper.jpg").convert_alpha()
blue_wallpaper = pygame.transform.scale(blue_wallpaper, (WIDTH, HEIGHT))
blue_wallpaper_rect = blue_wallpaper.get_rect()

green_wallpaper = pygame.image.load("green_wallpaper.jpg").convert_alpha()
green_wallpaper = pygame.transform.scale(green_wallpaper, (WIDTH, HEIGHT))
green_wallpaper_rect = green_wallpaper.get_rect()

red_wallpaper = pygame.image.load("red_wallpaper.jpg").convert_alpha()
red_wallpaper = pygame.transform.scale(red_wallpaper, (WIDTH, HEIGHT))
red_wallpaper_rect = red_wallpaper.get_rect()

pink_wallpaper = pygame.image.load("pink_wallpaper.jpg").convert_alpha()
pink_wallpaper = pygame.transform.scale(pink_wallpaper, (WIDTH, HEIGHT))
pink_wallpaper_rect = pink_wallpaper.get_rect()

purple_wallpaper = pygame.image.load("purple_wallpaper.jpg").convert_alpha()
purple_wallpaper = pygame.transform.scale(purple_wallpaper, (WIDTH, HEIGHT))
purple_wallpaper_rect = purple_wallpaper.get_rect()

# <------------------------------ Preference Screen Variables ------------------------------>

# Confectionery name input box
input_box = pygame.Rect(350, 410, 420, 40)
input_color_inactive = pygame.Color("#FF8269")
input_colour_active = pygame.Color("#FF866E9D")
input_colour = input_color_inactive
input_active = False
cursor_visible = True
cursor_timer = 0

# Buttons
buttons = [
    # Difficulty buttons
    {"rect": pygame.Rect(330, 255, 150, 50), "action": lambda s: s | {"difficulty": "easy"}},
    {"rect": pygame.Rect(522, 255, 150, 50), "action": lambda s: s | {"difficulty": "medium"}},
    {"rect": pygame.Rect(715, 255, 150, 50), "action": lambda s: s | {"difficulty": "hard"}},

    # Lollipop buttons
    {"rect": pygame.Rect(315, 555, 150, 50), "action": lambda s: s | {"lollipop_colour": "pink-lollipop"}},
    {"rect": pygame.Rect(500, 555, 150, 50), "action": lambda s: s | {"lollipop_colour": "red-lollipop"}},
    {"rect": pygame.Rect(688, 555, 150, 50), "action": lambda s: s | {"lollipop_colour": "purple-lollipop"}},
    {"rect": pygame.Rect(875, 555, 150, 50), "action": lambda s: s | {"lollipop_colour": "blue-lollipop"}},

    # Wallpaper buttons
    {"rect": pygame.Rect(460, 705, 130, 50), "action": lambda s: s | {"wallpaper_colour": "blue-wallpaper"}},
    {"rect": pygame.Rect(590, 705, 130, 50), "action": lambda s: s | {"wallpaper_colour": "green-wallpaper"}},
    {"rect": pygame.Rect(720, 705, 130, 50), "action": lambda s: s | {"wallpaper_colour": "red-wallpaper"}},
    {"rect": pygame.Rect(850, 705, 130, 50), "action": lambda s: s | {"wallpaper_colour": "pink-wallpaper"}},
    {"rect": pygame.Rect(980, 705, 130, 50), "action": lambda s: s | {"wallpaper_colour": "purple-wallpaper"}},

    # Finish button changes screen
    {"rect": pygame.Rect(WIDTH - 235, 90, 175, 65), "action": lambda s: s | {"screen": "intro"}},
]


start_button_rect = pygame.Rect(425, 580, 350, 100)

difficulty_times = {
    "easy": 300,
    "medium": 180,
    "hard": 120
}

# <------------------------------ Main Screen Variables ------------------------------>

# Lollipop
lollipop_pos = (WIDTH // 5, int(HEIGHT // 2.5))
base_radius = 150
lollipop_circle = pygame.Rect(90, 170, 250, 250)

# Lollipop clicking
lollipop_clicked = False

scale = 1.0
bounce_velocity = 0.0
radius = int(base_radius * scale)

BOUNCE_STRENGTH = -0.08  # How hard it compresses
SPRING = 0.15  # How fast it returns
DAMPING = 0.85  # How bouncy it feels

# Upgrades (x, y) positions
upgrades_x = [500, 530, 560, 590, 620, 650, 680, 710, 740, 770, 800]
upgrades_y = [225, 300, 225, 300, 225, 300, 225, 300, 225, 300, 225]

# Sugar jar
sugar_jar = pygame.image.load("sugar_jar.webp").convert_alpha()
sugar_jar = pygame.transform.scale(sugar_jar, (85, 85))
sugar_jar_rect = sugar_jar.get_rect()

# Honey jar
honey_jar = pygame.image.load("honey_jar.png").convert_alpha()
honey_jar = pygame.transform.scale(honey_jar, (90, 90))
honey_jar_rect = honey_jar.get_rect()

# Maple syrup
maple_syrup = pygame.image.load("maple_syrup.webp").convert_alpha()
maple_syrup = pygame.transform.scale(maple_syrup, (90, 90))
maple_syrup_rect = maple_syrup.get_rect()


WIN_CONDITION = 10000
candies_confected = 0
start_time = 0
last_cps_tick = 0
timer_started = False
paused_time_left = None

####
store_width = 300
store_height = 800
store_x = WIDTH - store_width
store_y = 0

font_title = pygame.font.SysFont(None, 50)
font_size = pygame.font.SysFont(None, 30)

sweeteners = [
    {"name": "Regular Sugar", "cost": 25, "cps": 1, "owned": 0},
    {"name": "Brown Sugar", "cost": 100, "cps": 4, "owned": 0},
    {"name": "Honey", "cost": 300, "cps": 10, "owned": 0},
    {"name": "Maple Syrup", "cost": 500, "cps": 15, "owned": 0},
    {"name": "Molasses", "cost": 1000, "cps": 20, "owned": 0}
]

####

font_30 = pygame.font.SysFont('none', 30)
font_50 = pygame.font.SysFont('none', 50)
font_80 = pygame.font.SysFont('none', 80)


news_prompts = ["You feel like making candy, but no one wants to eat your candy.",
                "Your first batch was burnt to a crisp. Straight to the trash.",
                "Your candy was finally accepted by your baby cousin.",
                "News: Every 6 in 7 children aged 6-7 want to buy your candy.",
                "News: Even 67 year olds are starting to gain interest in your candy.",
                "News: Evidence detected that back in 1967 people breathed!",
                "News: foreign politician involved in candy stealing scandal.",
                "People are starting to talk about your candy.",
                "Your candy is popular in the neighbourhood.",
                "People from all over the country want to buy your candy.",
                "Your candy is gaining international recognition.",
                "YOUR ON THE NEWS!!!",
                "How many pieces of candy could chuck chuck if chuck was a chuck?",
                "News: Potential new candy scam?!?",
                "What do you call a cookie clicker game in disguise? Candy clicker! hahaha... just kidding this is a super original game.",
                "You just found out that using Gallo Extra Virgin Olive Oil improves candy flavor.",
                "You invented a new type of candy.",
                "Are you trying to beat Willy Wonka?!?",
                "Sorry, I think Wonka's still better.",
                "News: Looking to buy some oompa loompas? Dial + 1 (647) 760-6767 for further inquiries. First come first serve!",
                "You consider opening a franchise.",
                "Your franchise shut down due to zero success. womp womp.",
                "Your market is expanding!!",
                "You see people littering on the streets with candy wrappers of YOUR candy.",
                "You're famous!!!"]

news_step = 400
news_index = 0
candy_count = 0

menu_button_rect = pygame.Rect(400, 0, 100, 99)
stats_button_rect = pygame.Rect(400, 100, 100, 99)
x_button_rect = pygame.Rect(1130, 20, 50, 50)

candies_made = 0
sweetener_count = 0
candies_per_second = 0
candies_per_click = 1
aura_candies_clicked = 0


# ---------------------------
# User preference (JSON)

default_user_preference = {
    "difficulty_level": difficulty,
    "confectionery_name": confectionery_name,
    "lollipop_colour": lollipop_colour,
    "wallpaper_colour": wallpaper_colour
}

# How often (ms) candy should spawn
GOLDEN_CANDY_SPAWN_INTERVAL = 10000  # every 10 seconds


# ================= Candy size =================
CANDY_WIDTH = 90
CANDY_HEIGHT = 35
WRAP_SIZE = 25

# ================= Candy state =================
golden_candy = {
    "visible": False,
    "x": 0,
    "y": 0,
    "spawn_time": 0,
    "duration": 5000  # ms
}


# number-guess
font_45 = pygame.font.SysFont('none', 45)
input_box_game = pygame.Rect(300, 370, 600, 50)
color_inactive = pygame.Color('blue')
color_active = pygame.Color('green')
color = color_inactive
active = False
game1_text = ''
exit_button = pygame.Rect(957, 586, 150, 150)

# Create random numbers
game1_answer = random.randrange(500, 550)
game1_answer = 500
text_answer = ""
lives = 7


candies_purple = [
    (464, 744), (477, 671), (509, 711), (549, 738), (566, 686), (520, 638),
    (599, 721), (640, 725), (590, 644), (635, 566), (477, 581), (550, 551),
    (479, 518), (568, 596), (635, 670), (673, 600), (606, 524), (623, 611),
    (471, 621), (674, 530), (684, 702), (517, 590), (673, 648), (503, 542),
    (586, 560), (520, 672), (553, 630), (471, 702), (504, 741), (680, 735),
    (536, 704), (593, 671), (490, 640), (529, 520), (676, 562), (460, 531),
    (473, 553), (538, 654), (565, 661), (619, 640), (540, 580), (532, 610),
    (588, 607), (596, 587), (623, 534), (686, 672), (589, 744), (614, 740),
    (484, 722), (525, 727), (559, 706), (569, 724), (589, 696), (618, 719),
    (617, 690), (643, 696), (657, 669), (651, 745), (551, 513), (581, 536),
    (523, 558), (491, 602), (507, 616), (685, 622), (459, 650), (646, 635),
    (646, 611), (642, 523), (661, 713), (542, 678), (494, 690), (458, 597),
    (498, 571), (655, 585), (651, 546), (611, 662), (608, 557), (620, 585),
    (667, 689), (564, 570), (603, 624), (573, 627), (460, 682), (577, 515),
    (500, 517)
]

candies_blue = [
    (559, 530), (484, 540), (458, 570), (490, 654), (504, 675), (517, 694),
    (458, 720), (480, 739), (523, 744), (564, 744), (657, 728), (654, 625),
    (685, 583), (684, 542), (621, 513), (658, 727), (459, 516), (509, 526),
    (532, 536), (545, 598), (557, 609), (582, 713), (627, 705), (625, 655),
    (656, 519), (596, 538), (652, 563), (542, 560), (517, 571), (507, 600),
    (488, 615), (552, 644), (669, 668), (548, 693), (491, 709), (607, 610),
    (579, 582), (677, 633), (629, 739), (473, 687), (513, 651), (583, 655),
    (576, 675), (601, 681), (636, 590), (461, 631), (608, 573), (621, 553),
    (539, 719), (657, 696), (648, 647), (525, 624), (482, 564), (568, 550),
]

candies_pink = [
    (602, 704), (455, 698), (468, 655), (508, 634), (477, 598), (457, 547),
    (554, 584), (497, 555), (488, 669), (468, 720), (510, 723), (489, 742),
    (573, 732), (532, 733), (567, 639), (572, 608), (604, 591), (632, 545),
    (665, 543), (685, 516), (688, 600), (684, 647), (679, 684), (669, 703),
    (665, 740), (628, 623), (602, 640), (586, 623), (545, 539), (539, 519),
    (470, 530), (628, 684), (599, 735), (527, 679), (454, 612), (669, 576),
    (543, 524), (493, 526), (655, 597), (583, 548), (588, 516), (556, 672),
    (477, 629), (535, 632), (500, 582), (680, 718), (550, 715), (626, 720),
    (629, 574), (523, 579), (637, 656), (686, 552), (501, 696), (516, 604),
    (571, 696), (505, 660), (543, 615), (516, 541), (452, 580), (665, 616)
]



########    game 2
font = pygame.font.SysFont('none', 70)
rock = 1
paper = 2
scissor = 3
result = ""
rock_button = pygame.Rect(90, 450, 250, 250)
paper_button = pygame.Rect(480, 450, 250, 250)
scissor_button = pygame.Rect(860, 450, 250, 250)
current_screen = "rock_paper_scissor"
game2_exit_button = pygame.Rect(1014, 65, 150, 150)
# Create random numbers
game2_answer = random.randrange(1, 4)


# Function to render and display text
def show_text(text, font, color, surface, x, y):
    text_look = font.render(text, True, color)
    surface.blit(text_look, (x, y))





# ---------------------------
# User Preference (JSON)

def load_or_init_user_preference(filename: str = "user_preference.json") -> dict:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(filename, "w") as f:
            json.dump(default_user_preference, f, indent=4)
        return default_user_preference.copy()


def update_user_preference(filename: str, updates: dict) -> None:
    with open(filename, "r") as f:
        data = json.load(f)
        for key in updates:
            if key in data:
                data[key] = updates[key]

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------
# Functions

def text_split(text: str) -> list[str]:
    max_len = 38
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        if current_line == "":
            current_line = word  # first word in the line
        elif len(current_line + " " + word) <= max_len:
            current_line += (" " + word)
        else:
            lines.append(current_line)
            current_line = word  # first word in new line

    if current_line:  # last line
        lines.append(current_line)

    return lines


def text_format(prompt_list: list[str]) -> None:
    for i in range(len(prompt_list)):
        text = font_30.render(prompt_list[i], True, (255, 255, 255))
        text_width = text.get_width()
        screen.blit(text, (400 // 2 + 500 - text_width // 2, 200 // 2 - 42 + i * 21))


def text_printer(stats: dict[str, int]) -> None:
    for i, (key, value) in enumerate(stats.items()):
        label = key.replace("_", " ").title()
        stat = font_20.render(f"{label}: {value}", True, (255, 255, 255))
        screen.blit(stat, (50, 150 + i * 30))


def buttonStats(button_label: str, button_x: int, button_y: int) -> None:
    pygame.draw.rect(screen, "#efefef", (button_x, button_y, 100, 99))
    pygame.draw.rect(screen, "#bababa", (button_x + 5, button_y + 5, 90, 90))
    button_text = font_20.render(button_label, True, (0, 0, 0))
    button_text_width = button_text.get_width()
    screen.blit(button_text, (100 // 2 + button_x - button_text_width // 2, 100 // 2 + button_y - 10))


# <--------------------------------------------------------------- Functions --------------------------------------------------------------------->

# <------------------------------ Wallpaper Functions ------------------------------>

def draw_blue_wallpaper() -> None:
    """
    Draws the blue-striped background.
    """
    blue_wallpaper_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(blue_wallpaper, blue_wallpaper_rect)


def draw_green_wallpaper() -> None:
    """
    Draws the green-striped background.
    """
    green_wallpaper_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(green_wallpaper, green_wallpaper_rect)


def draw_red_wallpaper() -> None:
    """
    Draws the red-striped background.
    """
    red_wallpaper_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(red_wallpaper, red_wallpaper_rect)


def draw_pink_wallpaper() -> None:
    """
    Draws the pink-striped background.
    """
    pink_wallpaper_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(pink_wallpaper, pink_wallpaper_rect)


def draw_purple_wallpaper() -> None:
    """
    Draws the purple-striped background.
    """
    purple_wallpaper_rect.center = (WIDTH // 2, HEIGHT // 2)
    screen.blit(purple_wallpaper, purple_wallpaper_rect)


def draw_wallpaper(wallpaper_colour: str) -> str:
    """
    Draws the wallpaper based on the user's preference (blue is default).
    """
    if wallpaper_colour == "green-wallpaper":
        draw_green_wallpaper()
        return "#EDFFED", "#CCF0CE", "#ABDBAE"

    elif wallpaper_colour == "red-wallpaper":
        draw_red_wallpaper()
        return "#FFD9D9", "#F0BDBD", "#ED9D9D"

    elif wallpaper_colour == "pink-wallpaper":
        draw_pink_wallpaper()
        return "#C94D99", "#DE6AB3", "#E384C1"

    elif wallpaper_colour == "purple-wallpaper":
        draw_purple_wallpaper()
        return "#F0E3FF", "#DCCCF0", "#CBB8DE"

    else:
        draw_blue_wallpaper()
        return "#E8EEFF", "#CCD6F0", "#A5B4D6"


# <------------------------------------------------ Preference Screen Functions ------------------------------------------------>

# TEXT FUNCTIONS

def draw_text() -> None:
    """
    Displays the title, subtitles, and prompts of the preference screen.
    """
    title = font_100.render("PREFERENCES", True, title_colour)
    difficulty_title = font_50.render("Difficulty", True, subtitle_colour)
    difficulty_prompt = font_25.render("Which difficulty?:", True, prompt_colour)
    confectionery_name_title = font_50.render("Confectionery Name", True, subtitle_colour)
    confectionery_name_prompt = font_25.render("Pick a unique name:", True, prompt_colour)
    lollipop_colour_title = font_50.render("Lollipop Colour", True, subtitle_colour)
    lollipop_colour_prompt = font_25.render("Choose a colour:", True, prompt_colour)
    wallpaper_colour_title = font_50.render("Wallpaper Colour", True, subtitle_colour)
    wallpaper_colour_prompt = font_25.render("Style your confectionery:", True, prompt_colour)

    # Names & positions
    texts = [title, difficulty_title, difficulty_prompt, confectionery_name_title, confectionery_name_prompt,
             lollipop_colour_title, lollipop_colour_prompt, wallpaper_colour_title, wallpaper_colour_prompt]
    texts_pos = [50, 190, 265, 340, 415, 490, 565, 640, 715]

    # Iterate through the text to print them out using a loop
    for i in range(len(texts)):
        screen.blit(texts[i], (100, texts_pos[i]))


def draw_input_boxOLD() -> None:
    """
    Draws an text input box where the user can type in their preferred confectionery name.
    """
    text_surface = font_20.render(confectionery_name, True, input_colour)

    # Get box width
    width = max(200, text_surface.get_width() + 10)
    input_box.w = width

    # Blit text & input box
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, input_colour, input_box, 2)

def draw_input_box() -> None:
    global cursor_timer, cursor_visible

    # Text to display
    display_text = confectionery_name

    # Cursor blink logic (simple)
    if input_active:
        cursor_timer += 1
        if cursor_timer % 30 == 0:
            cursor_visible = not cursor_visible
    else:
        cursor_visible = False
        cursor_timer = 0

    # Add cursor
    if input_active and cursor_visible:
        display_text += "|"

    text_surface = font_20.render(display_text, True, input_colour)

    # Border colour
    border_colour = input_colour_active if input_active else input_color_inactive

    # Draw box
    pygame.draw.rect(screen, border_colour, input_box, 2, border_radius=6)

    # Draw text
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 8))


def draw_lines() -> None:
    """
    Draws 3 lines to separate the button choices.
    """
    # Lines variables
    lines_y = [320, 470, 620]
    lines_x_end = [WIDTH - 300, WIDTH - 400, WIDTH - 100]

    # Iterate through y positions of lines to draw in different positions & lengths
    for i in range(len(lines_y)):
        pygame.draw.line(screen, subtitle_colour, (100, lines_y[i]), (lines_x_end[i], lines_y[i]), 2)


# BUTTON FUNCTIONS

def buttonOLD(label: str, x_pos: int, y_pos: int, width: int, height: int, label_colour: str, base_colour: str,
           padding_colour: str) -> None:
    """
    Takes in a bunch of parameters to draw a customized button for the preferences screen.
    """
    button_padding = 5

    # Draw button & border
    pygame.draw.rect(screen, padding_colour, (x_pos, y_pos, width, height))
    pygame.draw.rect(screen, base_colour, (
    x_pos + button_padding, y_pos + button_padding, width - 2 * button_padding, height - 2 * button_padding))

    # Get text ("Finish!" button has a larger font)
    if label == "Finish!":
        button_text = font_40.render(label, True, label_colour)
    else:
        button_text = font_30_merr.render(label, True, label_colour)

    # Display button label
    text_rect = button_text.get_rect(center=(x_pos + width // 2, y_pos + height // 2))
    screen.blit(button_text, text_rect)


def button(label: str, x_pos: int, y_pos: int, width: int, height: int,
           label_colour: str, base_colour: str, padding_colour: str,
           selected: bool = False) -> None:
    """
    Draw a customized button for the preferences screen.
    """
    button_padding = 5

    # -------- Selected effect --------
    if selected:
        scale = 1.08  # 放大 8%
        highlight_colour = (255, 255, 255)
    else:
        scale = 1.0
        highlight_colour = padding_colour

    scaled_width = int(width * scale)
    scaled_height = int(height * scale)

    draw_x = x_pos - (scaled_width - width) // 2
    draw_y = y_pos - (scaled_height - height) // 2

    # Draw button & border
    pygame.draw.rect(
        screen,
        highlight_colour,
        (draw_x, draw_y, scaled_width, scaled_height),
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        base_colour,
        (
            draw_x + button_padding,
            draw_y + button_padding,
            scaled_width - 2 * button_padding,
            scaled_height - 2 * button_padding
        ),
        border_radius=8
    )

    # Get text
    if label == "Finish!":
        button_text = font_40.render(label, True, label_colour)
    else:
        button_text = font_30_merr.render(label, True, label_colour)

    text_rect = button_text.get_rect(
        center=(draw_x + scaled_width // 2, draw_y + scaled_height // 2)
    )
    screen.blit(button_text, text_rect)


def handle_buttons(state: dict, mouse_pos: tuple, buttons: list) -> dict:
    """
    Call the action of the clicked button.
    """
    for button in buttons:
        if button["rect"].collidepoint(mouse_pos):
            return button["action"](state)
    return state


def draw_all_buttons() -> None:
    """
    Draws all buttons on the preference screen with their respective texts, positions, and colours.
    """
    # Draw difficulty buttons
    button(
        "Easy", 330, 255, 150, 50,
        "#0C5928", "#1DF267", "#14A646",
        selected=(game_state["difficulty"] == "easy")
    )

    button(
        "Medium", 522, 255, 150, 50,
        "#7D4915", "#FFB873", "#FF8E1C",
        selected=(game_state["difficulty"] == "medium")
    )

    button(
        "Hard", 715, 255, 150, 50,
        "#8A2315", "#FC7D6F", "#F25644",
        selected=(game_state["difficulty"] == "hard")
    )

    # Draw lollipop colour buttons
    button(
        "Pink", 315, 555, 150, 50,
        "#CF57AE", "#FFB0E4", "#FA8EE1",
        selected=(game_state["lollipop_colour"] == "pink-lollipop")
    )

    button(
        "Red", 500, 555, 150, 50,
        "#A83E34", "#FFB0A8", "#F2887E",
        selected=(game_state["lollipop_colour"] == "red-lollipop")
    )

    button(
        "Purple", 688, 555, 150, 50,
        "#7A2BA1", "#E1A2FA", "#BC65E6",
        selected=(game_state["lollipop_colour"] == "purple-lollipop")
    )

    button(
        "Blue", 875, 555, 150, 50,
        "#375699", "#C3D4F7", "#88ACF7",
        selected=(game_state["lollipop_colour"] == "blue-lollipop")
    )


    # Draw wallpaper colour buttons
    # button("Blue", 425, 705, 115, 50, "#375699", "#C3D4F7", "#88ACF7")
    # button("Green", 564, 705, 115, 50, "#49B871", "#C3F7D2", "#7CE69F")
    # button("Red", 703, 705, 115, 50, "#A83E34", "#FFB0A8", "#F2887E")
    # button("Pink", 842, 705, 115, 50, "#E046BD", "#FAA2E6", "#FF70DF")
    # button("Purple", 980, 705, 115, 50, "#7A2BA1", "#E1A2FA", "#BC65E6")

    button(
        "Blue", 425, 705, 115, 50,
        "#375699", "#C3D4F7", "#88ACF7",
        selected=(game_state["wallpaper_colour"] == "blue-wallpaper")
    )

    button(
        "Green", 564, 705, 115, 50,
        "#49B871", "#C3F7D2", "#7CE69F",
        selected=(game_state["wallpaper_colour"] == "green-wallpaper")
    )

    button(
        "Red", 703, 705, 115, 50,
        "#A83E34", "#FFB0A8", "#F2887E",
        selected=(game_state["wallpaper_colour"] == "red-wallpaper")
    )

    button(
        "Pink", 842, 705, 115, 50,
        "#E046BD", "#FAA2E6", "#FF70DF",
        selected=(game_state["wallpaper_colour"] == "pink-wallpaper")
    )

    button(
        "Purple", 980, 705, 115, 50,
        "#7A2BA1", "#E1A2FA", "#BC65E6",
        selected=(game_state["wallpaper_colour"] == "purple-wallpaper")
    )


    # Draw finish button
    button("Finish!", WIDTH - 235, 90, 175, 75, "#C7A716", "#FFE585", "#EBC134")


# <------------------------------ Main Screen Functions ------------------------------>

# LOLLIPOP FUNCTIONS

def get_lollipop_colours(lollipop_colour: str) -> tuple[str, str, str, str]:
    """
    Takes the parameter lollipop_colour to return four lollipop colours.
    """
    if lollipop_colour == "red-lollipop":
        return "#FF9885", "#FF8770", "#FFF1F0", "#FFF8F7"

    elif lollipop_colour == "purple-lollipop":
        return "#EECCFF", "#E0B1FA", "#F8EBFF", "#FCF7FF"

    elif lollipop_colour == "blue-lollipop":
        return "#C0D5FA", "#B1C9F2", "#E0ECFF", "#F0F6FC"

    else:
        return "#F7ABD8", "#F29DCF", "#FFE5F6", "#FFF2FB"


def draw_lollipop_swirls(swirl_colour: str) -> None:
    """
    Decorates the lollipop with swirls given the parameter swirl_colour.
    """
    spiral_points = []
    turns = 4
    points = 300

    # Draw swirl points
    for i in range(points):
        angle = turns * 2 * math.pi * (i / points)
        r = radius * (i / points)
        x = lollipop_pos[0] + r * math.cos(angle)
        y = lollipop_pos[1] + r * math.sin(angle)
        spiral_points.append((x, y))

    if len(spiral_points) > 1:
        pygame.draw.lines(screen, swirl_colour, False, spiral_points, 5)


def draw_lollipop(lollipop_radius: int, lollipop_colour: str, swirl_colour: str, line_colour: str) -> None:
    pygame.draw.line(screen, line_colour, (WIDTH // 5, 450), (WIDTH // 5, 724), 20)  # Lollipop holder
    pygame.draw.circle(screen, lollipop_colour, lollipop_pos, lollipop_radius)  # Lollipop base
    draw_lollipop_swirls(swirl_colour)


def update_lollipop_bounce(bounce_velocity: float, scale: float, base_radius: int, lollipop_pos: tuple) -> tuple[
    float, float, int, pygame.Rect]:
    """
    Updates the lollipop bounce physics and hitbox.
    Returns updated bounce_velocity, scale, radius, and lollipop_circle.
    """
    bounce_velocity += (1 - scale) * SPRING
    bounce_velocity *= DAMPING
    scale += bounce_velocity

    scale = max(0.9, min(scale, 1.1))  # # Clamp scale

    # Update size and hitbox
    radius = int(base_radius * scale)
    lollipop_circle = pygame.Rect(
        lollipop_pos[0] - radius,
        lollipop_pos[1] - radius,
        radius * 2,
        radius * 2
    )

    return bounce_velocity, scale, radius, lollipop_circle


# UPGRADE FUNCTIONS

def draw_sugar_jar(upgrades_x: int, upgrades_y: int) -> None:
    """
    Draws the sugar jar upgrade on the screen.
    """
    for i in range(len(upgrades_x)):
        sugar_jar_rect.x = upgrades_x[i]
        sugar_jar_rect.y = upgrades_y[i]
        screen.blit(sugar_jar, sugar_jar_rect)


def draw_honey_jar(upgrades_x: int, upgrades_y: int) -> None:
    """
    Draws the honey jar upgrade on the screen.
    """
    for i in range(len(upgrades_x)):
        honey_jar_rect.x = upgrades_x[i]
        honey_jar_rect.y = upgrades_y[i] + 200
        screen.blit(honey_jar, honey_jar_rect)


def draw_maple_syrup(upgrades_x: int, upgrades_y: int) -> None:
    """
    Draws the maple syrup upgrade on the screen.
    """
    for i in range(len(upgrades_x)):
        maple_syrup_rect.x = upgrades_x[i]
        maple_syrup_rect.y = upgrades_y[i] + 400
        screen.blit(maple_syrup, maple_syrup_rect)




def draw_borders() -> None:
    lines = [
        ((900, 0), (900, 800)),  # store
        ((500, 0), (500, 800)),  # lollipop
        ((500, 200), (900, 200)),  # news
        ((500, 400), (900, 400)),  # sweeteners
        ((500, 600), (900, 600)),  # sweeteners
    ]
    for point1, point2 in lines:
        pygame.draw.line(screen, (52, 28, 2), point1, point2, 10)


# Lollipop (by Lilyana)
def draw_lollipop_swirls(swirl_colour) -> None:
    spiral_points = []
    turns = 4
    points = 300

    for i in range(points):
        angle = turns * 2 * math.pi * (i / points)
        r = radius * (i / points)

        x = lollipop_pos[0] + r * math.cos(angle)
        y = lollipop_pos[1] + r * math.sin(angle)

        spiral_points.append((x, y))

    if len(spiral_points) > 1:
        pygame.draw.lines(screen, swirl_colour, False, spiral_points, 5)


def draw_lollipop(lollipop_radius, lollipop_colour, swirl_colour, line_colour) -> None:
    pygame.draw.line(screen, line_colour, (WIDTH // 5, 450), (WIDTH // 5, 724), 20)  # lollipop holder
    pygame.draw.circle(screen, lollipop_colour, lollipop_pos, lollipop_radius)  # lollipop base
    draw_lollipop_swirls(swirl_colour)





def draw_info() -> None:
    bank_text = font_30_merr.render(f"BANK: {candies_confected}", True, (255, 255, 255))
    bank_width = bank_text.get_width()
    screen.blit(bank_text, ((500 - bank_width) / 2, 60))

    cps_text = font_30_merr.render(f"CPS: {total_cps(sweeteners)}", True, (255, 255, 255))
    cps_width = cps_text.get_width()
    screen.blit(cps_text, ((500 - cps_width) / 2, 90))

    confect_text = font_20.render(f"{confectionery_name}", True, (255, 255, 255))
    confect_width = confect_text.get_width()
    screen.blit(confect_text, ((500 - confect_width) / 2, 130))


def draw_pop_up() -> None:
    pygame.draw.rect(screen, (155, 155, 155), (110, 60, 980, 670))
    pygame.draw.rect(screen, (239, 234, 215), (130, 130, 940, 570))
    pygame.draw.rect(screen, (210, 180, 140), start_button_rect)


def timer_white() -> None:
    timer = font_30_merr.render(timer_text, True, (255, 255, 255))
    screen.blit(timer, (220, 20))


def timer_red() -> None:
    timer = font_30_merr.render(timer_text, True, (250, 0, 0))
    screen.blit(timer, (220, 20))


# LOGIC FUNCTIONS


def total_cps(sweeteners: list[dict]) -> int:
    total = 0
    for s in sweeteners:
        total += s["owned"] * s["cps"]
    return total

def update_timer(start_time: int) -> int:
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    return max(0, TOTAL_TIME - elapsed)


# TEXT FUNCTIONS
def game_over_text() -> None:
    game_over = font_160.render("GAME OVER", True, (100, 0, 0))
    game_over_width = game_over.get_width()
    screen.blit(game_over, ((WIDTH - game_over_width) / 2, (HEIGHT - 100) / 3))

    game_over_1 = font_30_merr.render("Uh oh, you ran out of time and your confectionery", True, (0, 0, 0))
    game_over_2 = font_30_merr.render("subsequently combusts. There goes that dream!", True, (0, 0, 0))
    game_over_3 = font_30_merr.render("Press enter to play again or 'Q' to quit the game.", True, (0, 0, 0))

    game_over_text = [game_over_1, game_over_2, game_over_3]
    game_over_pos = [440, 500, 560]

    for text in range(len(game_over_text)):
        text_width = game_over_text[text].get_width()
        screen.blit(game_over_text[text], (WIDTH / 2 - text_width / 2, game_over_pos[text]))


def game_won_text() -> None:
    game_won = font_160.render("CONGRATS!", True, (0, 0, 0))
    game_won_width = game_won.get_width()
    screen.blit(game_won, ((WIDTH - game_won_width) / 2, (HEIGHT - 100) / 3))

    game_won_1 = font_30_merr.render("Press enter to play again or ‘Q’ to quit the game.", True, (0, 0, 0))
    game_won_2 = font_30_merr.render("Thanks for playing!", True, (0, 0, 0))

    game_won_text = [game_won_1, game_won_2]
    game_won_pos = [440, 500]

    for text in range(len(game_won_text)):
        text_width = game_won_text[text].get_width()
        screen.blit(game_won_text[text], (WIDTH / 2 - text_width / 2, game_won_pos[text]))

def draw_store() -> None:
    pygame.draw.rect(screen, "#E6E6E6", (store_x, store_y, store_width, store_height))

    title = font_title.render("STORE", True, (0, 0, 0))
    title_width = title.get_width()
    screen.blit(title, (store_x + store_width // 2 - title_width // 2, 20))

    candy_text = font_size.render("Candies: " + str(candies_confected), True, (0, 0, 0))
    screen.blit(candy_text, (store_x + 20, 80))

    y = 140
    box_height = 110

    for item in sweeteners:
        pygame.draw.rect(
            screen, "#F5F5F5",
            (store_x + 10, y - 10, store_width - 20, box_height)
        )

        if candies_confected >= item["cost"] or item["owned"] > 0:
            display_name = item["name"]
        else:
            display_name = "???"

        name_text = font_size.render(display_name, True, (0, 0, 0))
        screen.blit(name_text, (store_x + 20, y))

        cost_text = font_size.render("Cost: " + str(item["cost"]), True, (60, 60, 60))
        cps_text = font_size.render(
            "CPS: +" + str(item["cps"]) + "  Owned: " + str(item["owned"]),
            True,
            (60, 60, 60)
        )

        screen.blit(cost_text, (store_x + 20, y + 30))
        screen.blit(cps_text, (store_x + 20, y + 55))

        can_afford = False
        if candies_confected >= item["cost"]:
            can_afford = True

        if can_afford:
            button_colour = "#4CAF50"
        else:
            button_colour = "#AAAAAA"

        buy_rect = pygame.Rect(store_x + 150, y + 20, 120, 30)
        pygame.draw.rect(screen, button_colour, buy_rect, border_radius=3)

        buy_text = font_size.render("BUY", True, (255, 255, 255))
        screen.blit(buy_text, (store_x + 185, y + 25))

        item["rect"] = buy_rect

        y += box_height + 15

def handle_store_click(pos) -> None:
    global candies_confected
    global sweetener_count

    for item in sweeteners:
        if "rect" in item:
            if item["rect"].collidepoint(pos):
                if candies_confected >= item["cost"]:
                    candies_confected -= item["cost"]
                    item["owned"] += 1
                    item["cost"] = int(item["cost"] * 1.15)
                    sweetener_count += 1

def draw_golden_candy(surface, x, y):
    pygame.draw.polygon(
        surface,
        "#cfb45c",
        [(x - WRAP_SIZE, y),
         (x - WRAP_SIZE, y + CANDY_HEIGHT),
         (x, y + CANDY_HEIGHT // 2)]
    )
    pygame.draw.polygon(
        surface,
        "#cfb45c",
        [(x + CANDY_WIDTH, y + CANDY_HEIGHT // 2),
         (x + CANDY_WIDTH + WRAP_SIZE, y + CANDY_HEIGHT),
         (x + CANDY_WIDTH + WRAP_SIZE, y)]
    )
    pygame.draw.ellipse(surface, "#cfb45c", (x, y, CANDY_WIDTH, CANDY_HEIGHT))
    pygame.draw.ellipse(surface, "#88b9de", (x + 20, y + 10, 6, 6))
    pygame.draw.ellipse(surface, "#88b9de", (x + 45, y + 18, 6, 6))
    pygame.draw.ellipse(surface, "#88b9de", (x + 65, y + 8, 6, 6))


# <----------------------------------------------------------- Game Loop ----------------------------------------------------------->
user_preference = load_or_init_user_preference()
# Sync global variables with loaded preferences
difficulty = user_preference.get("difficulty_level", difficulty)
confectionery_name = user_preference.get("confectionery_name", confectionery_name)
lollipop_colour = user_preference.get("lollipop_colour", lollipop_colour)
wallpaper_colour = user_preference.get("wallpaper_colour", wallpaper_colour)

# Update game_state accordingly
game_state["difficulty"] = difficulty
game_state["lollipop_colour"] = lollipop_colour
game_state["wallpaper_colour"] = wallpaper_colour

running = True

while running:

    current_screen = game_state["screen"]
    difficulty = game_state["difficulty"]
    lollipop_colour = game_state["lollipop_colour"]
    wallpaper_colour = game_state["wallpaper_colour"]

    # <------------------------------- Draw Wallpaper ------------------------------->

    title_colour, subtitle_colour, prompt_colour = draw_wallpaper(wallpaper_colour)

    # <--------------------------------------- Preferences Screen -------------------------------------------->

    if current_screen == "preferences":

        # Event handling
        for event in pygame.event.get():

            # Detect collision with button/input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                # input_active = input_box.collidepoint(event.pos)
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                if event.button == 1:
                    game_state = handle_buttons(game_state, event.pos, buttons)

            # Update input box text
            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    confectionery_name = confectionery_name[:-1]
                else:
                    # Only allow user to type when the name is less than 20 characters (or the input box will be too long)
                    if len(confectionery_name) < 100:
                        confectionery_name += event.unicode

            # Update input box colour
            if input_active:
                input_colour = input_colour_active
            else:
                input_colour = input_color_inactive

        # Drawing
        draw_text()
        draw_all_buttons()
        draw_input_box()
        draw_lines()

    elif current_screen == "intro":
        # update preference
        updates = {
            "difficulty_level": game_state["difficulty"],
            "confectionery_name": confectionery_name,
            "lollipop_colour": game_state["lollipop_colour"],
            "wallpaper_colour": game_state["wallpaper_colour"]
        }
        update_user_preference("user_preference.json", updates)

        # DRAWING
        screen.fill((0, 0, 0))
        draw_pop_up()

        # TEXT
        title = font_100.render("CANDY CLICKER", True, (0, 0, 0))
        instruct_1 = font_30_merr.render("You, an amateur confectioner, are at risk of eviction! Make", True, (0, 0, 0))
        instruct_2 = font_30_merr.render("10,000 candies from scratch by clicking the lollipop. As you", True, (0, 0, 0))
        instruct_3 = font_30_merr.render("confect, you can buy sweeteners, which increase production.", True, (0, 0, 0))
        instruct_4 = font_30_merr.render("Good luck… beat the game before you get evicted!", True, (0, 0, 0))
        play = font_80_merr.render("PLAY", True, (0, 0, 0))

        text = [title, instruct_1, instruct_2, instruct_3, instruct_4, play]
        text_pos = [200, 340, 390, 440, 490, 580]

        for line in range(len(text)):
            text_width = text[line].get_width()
            screen.blit(text[line], (WIDTH / 2 - text_width / 2, text_pos[line]))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    start_time = pygame.time.get_ticks()
                    last_cps_tick = start_time
                    timer_started = True
                    game_state["screen"] = "main-game"

    # <--------------------------------------- Main Game Screen -------------------------------------------->

    elif current_screen == "main-game":
        TOTAL_TIME = difficulty_times[game_state["difficulty"]]

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # print("Mouse clicked at:", event.pos)
                if lollipop_circle.collidepoint(event.pos):
                    candies_confected += 1
                    candies_made += 1
                    lollipop_clicked = True
                    bounce_velocity = BOUNCE_STRENGTH

                handle_store_click(event.pos)

                if menu_button_rect.collidepoint(event.pos):
                    game_state["screen"] = "preferences"

                if stats_button_rect.collidepoint(event.pos):
                    game_state["screen"] = "stats"

                if golden_candy["visible"]:
                    candy_rect = pygame.Rect(
                        golden_candy["x"], golden_candy["y"], CANDY_WIDTH + 2 * WRAP_SIZE, CANDY_HEIGHT
                    )
                    if candy_rect.collidepoint(event.pos):
                        golden_candy["visible"] = False
                        # trigger mini-games
                        game_state["screen"] = random.choice(["number-guess", "rock_paper_scissor"])

                        # pause timer
                        timer_started = False
                        paused_time_left = time_left

                        # aura_candies_clicked
                        aura_candies_clicked += 1

                        # reset game result
                        game1_answer = random.randrange(500, 550)
                        game1_text = ''
                        text_answer = ""
                        lives = 7

                        result = ""
                        game2_answer = random.randrange(1, 4)

        # Update bounce physics
        bounce_velocity, scale, radius, lollipop_circle = update_lollipop_bounce(
            bounce_velocity, scale, base_radius, lollipop_pos
        )

        # Get lollipop colours
        base_colour_1, base_colour_2, swirl_colour, line_colour = get_lollipop_colours(lollipop_colour)

        if lollipop_clicked:
            current_colour = base_colour_1
        else:
            current_colour = base_colour_2

        # Draw lollipop with animation
        draw_lollipop(radius, current_colour, swirl_colour, line_colour)
        draw_borders()
        draw_store()
        draw_sugar_jar(upgrades_x, upgrades_y)
        draw_honey_jar(upgrades_x, upgrades_y)
        draw_maple_syrup(upgrades_x, upgrades_y)

        news_index = candies_confected // 200
        news_index = min(news_index, len(news_prompts) - 1)

        # DRAWING
        # news

        some_text = font_30.render("News:", True, (255, 255, 255))
        text_width = some_text.get_width()
        screen.blit(some_text, (400 // 2 + 500 - text_width // 2, 10))

        text_format(text_split(news_prompts[news_index]))

        # buttons
        buttonStats("Menu", 400, 0)
        buttonStats("Stats", 400, 100)
        # time_left = update_timer(start_time)
        if timer_started:
            time_left = update_timer(start_time)
        elif paused_time_left is not None:
            time_left = paused_time_left
        else:
            time_left = TOTAL_TIME

        # if timer_started:
        #     time_left = update_timer(start_time)
        # else:
        #     time_left = TOTAL_TIME

        draw_info()

        if time_left == 0:
            game_state["screen"] = "game-over"

        if candies_confected >= WIN_CONDITION:
            game_state["screen"] = "game-won"

        current_time = pygame.time.get_ticks()

        if current_time - last_cps_tick >= 1000:
            candies_confected += total_cps(sweeteners)
            last_cps_tick = current_time

        mins = time_left // 60  # floor division to ONLY get min
        secs = time_left % 60  # mod to get ONLY the remainder after div
        timer_text = f"{mins}:{secs:02d}"  # 02d: d is decimal integer, 2 is make output at least 2 char, 0 is pad w/ zeros

        if time_left > 5:
            timer_white()
        elif time_left == 0:
            game_state["screen"] = "game-over"
        else:
            timer_red()

        # spawn logic
        if not golden_candy["visible"] and current_time - golden_candy.get("last_spawn_attempt",
                                                                           0) > GOLDEN_CANDY_SPAWN_INTERVAL:
            golden_candy["visible"] = True


            golden_candy["x"] = random.randint(50, 200)
            golden_candy["y"] = random.randint(50, 600)

            golden_candy["spawn_time"] = current_time
            golden_candy["last_spawn_attempt"] = current_time

        # despawn
        if golden_candy["visible"] and current_time - golden_candy["spawn_time"] > golden_candy["duration"]:
            golden_candy["visible"] = False

        if golden_candy["visible"]:
            draw_golden_candy(screen, golden_candy["x"], golden_candy["y"])

    elif current_screen == "game-over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    candies_confected = 0

                    start_time = pygame.time.get_ticks()
                    last_cps_tick = start_time
                    timer_started = True
                    scale = 1.0
                    bounce_velocity = 0.0
                    radius = int(base_radius * scale)
                    game_state["screen"] = "main-game"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        game_over_text()

        candies_confected = 0
        for s in sweeteners:
            s["owned"] = 0
        timer_started = False

    elif current_screen == "game-won":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    candies_confected = 0

                    start_time = pygame.time.get_ticks()
                    last_cps_tick = start_time
                    timer_started = True
                    scale = 1.0
                    bounce_velocity = 0.0
                    radius = int(base_radius * scale)
                    game_state["screen"] = "main-game"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        game_won_text()

        candies_confected = 0
        for s in sweeteners:
            s["owned"] = 0
        timer_started = False

    elif current_screen == "stats":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x_button_rect.collidepoint(event.pos):
                    game_state["screen"] = "main-game"

        # draw
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, "#efefef", (1130, 20, 50, 50))
        x_text = font_50.render("X", True, (0, 0, 0))
        screen.blit(x_text, (1144, 30))

        stats_title = font_80.render("STATISTICS", True, (255, 255, 255))
        stats_title_width = stats_title.get_width()
        screen.blit(stats_title, (1200 // 2 - stats_title_width // 2, 35))

        user_progress = {
            "candies_in_bank": candies_confected,
            "candies_made": candies_made,
            "sweetener_count": sweetener_count,
            "candies_per_second": total_cps(sweeteners),
            "candies_per_click": candies_per_click,
            "aura_candies_clicked": aura_candies_clicked
        }

        text_printer(user_progress)

    elif current_screen == "number-guess":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_game.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

                # Exit button
                if exit_button.collidepoint(event.pos):
                    if text_answer == "correct":
                        candies_confected += int(game1_answer)
                        candies_made += int(game1_answer)
                    game_state["screen"] = "main-game"
                    # restart timer
                    timer_started = True
                    start_time = pygame.time.get_ticks() - (TOTAL_TIME - paused_time_left) * 1000

            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(f"User input: {game1_text}")
                        print(f"answer: {game1_answer}")
                        user_input = int(game1_text)
                        if user_input == game1_answer:
                            text_answer = "correct"
                        if user_input >= game1_answer and user_input != game1_answer:
                            text_answer = "big"
                            lives -= 1
                        if user_input <= game1_answer and user_input != game1_answer:
                            text_answer = "small"
                            lives -= 1
                        text = ''  # Clear text after hitting enter
                    elif event.key == pygame.K_BACKSPACE:
                        game1_text = game1_text[:-1]  # Remove last character
                    else:
                        game1_text += event.unicode  # Append character


        screen.fill("#138BAC")  # Always the first drawing command

        # Display static text message
        message = 'You are in the Candy Guessing game!'
        text_surface = font_45.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 200))

        message = 'Guess how many pieces of candy are in this jar (500-550)'
        text_surface = font_45.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))
        # Draw input box
        pygame.draw.rect(screen, color, input_box_game, 2)

        # Show the current text in the input box
        show_text(game1_text, font_45, pygame.Color('black'), screen, input_box_game.x + 5, input_box_game.y + 5)

        # Jar
        pygame.draw.rect(screen, "#546f80", (434, 496, 275, 269), 200)
        pygame.draw.rect(screen, "#546f80", (484, 447, 170, 60), 200)
        pygame.draw.rect(screen, "#91bcd8", (444, 506, 255, 249), 200)
        pygame.draw.rect(screen, "#91bcd8", (494, 457, 150, 40), 200)
        # Candy
        for candy in candies_purple:
            candy_x, candy_y = candy
            pygame.draw.circle(screen, "#AA42A5", (candy_x, candy_y), 10)  # Purple fill

        for candy in candies_blue:
            candy_x, candy_y = candy
            pygame.draw.circle(screen, "#3C90E4", (candy_x, candy_y), 10)

        for candy in candies_pink:
            candy_x, candy_y = candy
            pygame.draw.circle(screen, "#F17AE1", (candy_x, candy_y), 10)

        # Words display
        if text_answer == "correct":
            screen.fill("#138BAC")
            message = f'YOU GOT IT RIGHT! YOU WON {game1_answer} CANDIES!  Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 300))

        if text_answer == "big":
            message = f'Your answer was too big.You have {lives} more lives'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 300))

        if text_answer == "small":
            message = f'Your answer was small.You have {lives} more lives'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 300))

        if lives == 0:
            screen.fill("#138BAC")
            message = 'YOU RAN OUT OF LIVES! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 300))

        # Exit Button
        pygame.draw.rect(screen, "#8DC5EA", (957, 586, 150, 150), 200)
        message = 'Exit'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 1.17 - text_width // 2, HEIGHT // 2 + 240))

    elif current_screen == "rock_paper_scissor":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "rock_paper_scissor":
                if rock_button.collidepoint(event.pos):
                    print(f"answer: {game2_answer}")
                    result = 1
            if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "rock_paper_scissor":
                if paper_button.collidepoint(event.pos):
                    print(f"answer: {game2_answer}")
                    result = 2
            if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "rock_paper_scissor":
                if scissor_button.collidepoint(event.pos):
                    print(f"answer: {game2_answer}")
                    result = 3
            if event.type == pygame.MOUSEBUTTONDOWN and current_screen == "rock_paper_scissor":
                if game2_exit_button.collidepoint(event.pos):
                    if ((result == 2 and game2_answer == 1) or
                            (result == 1 and game2_answer == 3) or
                            (result == 3 and game2_answer == 2)):
                        candies_confected += 500
                        candies_made += 500
                    result = 0
                    game_state["screen"] = "main-game"
                    # restart timer
                    timer_started = True
                    start_time = pygame.time.get_ticks() - (TOTAL_TIME - paused_time_left) * 1000

        screen.fill("#b391d8")  # always the first drawing command

        message = 'Play Rock, Paper, Scissors!'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 200))

        message = 'Click either Rock, Paper, or Scissors'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))
        # Blocks
        pygame.draw.rect(screen, "#91bcd8", (90, 450, 250, 250), 200)
        message = 'Rock'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 5.6 - text_width // 2, HEIGHT // 2 + 150))

        pygame.draw.rect(screen, "#91bcd8", (480, 450, 250, 250), 200)
        message = 'Paper'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 150))

        pygame.draw.rect(screen, "#91bcd8", (860, 450, 250, 250), 200)
        message = 'Scissors'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 1.22 - text_width // 2, HEIGHT // 2 + 150))
        # Win
        if result == 2 and game2_answer == 1:
            screen.fill("#65BDD5")
            message = 'YOU WON 500 CANDIES! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played rock"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))

        if result == 1 and game2_answer == 3:
            screen.fill("#65BDD5")
            message = 'YOU WON 500 CANDIES! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played scissor"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))

        if result == 3 and game2_answer == 2:
            screen.fill("#65BDD5")
            message = 'YOU WON 500 CANDIES! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played paper"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))

        # Lost
        if result == 1 and game2_answer == 2:
            screen.fill("#65BDD5")
            message = 'YOU LOST! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played paper"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))
        if result == 2 and game2_answer == 3:
            screen.fill("#65BDD5")
            message = 'YOU LOST! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played scissor"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))
        if result == 3 and game2_answer == 1:
            screen.fill("#65BDD5")
            message = 'YOU LOST! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))

            message = "Your opponent played rock"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))
        # Tie
        if result == game2_answer:
            screen.fill("#65BDD5")
            message = 'It was a tie! Click the Exit Button'
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - 100))
            if game2_answer == 1:
                word = "Rock"
            if game2_answer == 2:
                word = "Paper"
            if game2_answer == 1:
                word = "Scissor"
            message = f"Your opponent played {word}"
            text_surface = font_30_merr.render(message, True, pygame.Color("black"))
            text_width = text_surface.get_width()
            screen.blit(text_surface, (WIDTH // 2 - text_width // 2, HEIGHT // 2 + 100))
        # Exit Button
        pygame.draw.rect(screen, "#688aa0", (1014, 65, 150, 150), 200)
        message = 'Exit'
        text_surface = font_30_merr.render(message, True, pygame.Color("black"))
        text_width = text_surface.get_width()
        screen.blit(text_surface, (WIDTH // 1.11 - text_width // 2, HEIGHT // 2 - 275))


    # Must be the last two lines of the game loop
    pygame.display.flip()
    clock.tick(100)
    # ---------------------------

pygame.quit()
