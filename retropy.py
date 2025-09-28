import os
import pygame
import time
import json
from pyboy import PyBoy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

pygame.init()
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("RetroPy Launcher")

font_title = pygame.font.SysFont("Arial", 30, bold=True)
font_desc = pygame.font.SysFont("Arial", 20)
font_hint = pygame.font.SysFont("Arial", 16)

settings = {
    "scroll_speed": 0.15,
    "zoom_center": 1.0,
    "zoom_side": 0.6,
    "sound_volume": 1.0,
    "bg_color": (15, 15, 15),
    "highlight_color": (0, 255, 0),
    "normal_color": (200, 200, 200),
    "hint_color": (180, 180, 180),
    "rom_folder": "Roms"
}

SETTINGS_FILE = "settings.json"

def load_settings():
    global settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                loaded = json.load(f)
                settings.update(loaded)
        except Exception as e:
            print("Failed to load settings:", e)

def save_settings():
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        print("Failed to save settings:", e)

load_settings()

settings_options = [
    {"name": "Scroll Speed", "key": "scroll_speed", "min": 0.05, "max": 2.0, "step": 0.05},
    {"name": "Zoom Center", "key": "zoom_center", "min": 0.5, "max": 2.0, "step": 0.1},
    {"name": "Zoom Side", "key": "zoom_side", "min": 0.3, "max": 1.0, "step": 0.05},
    {"name": "Sound Volume", "key": "sound_volume", "min": 0.0, "max": 1.0, "step": 0.1},
    {"name": "ROM Folder", "key": "rom_folder", "min": None, "max": None, "step": None}
]
current_setting_index = 0

def load_roms():
    roms = []
    thumbnails = {}
    descriptions = {}

    rom_folder = settings["rom_folder"]
    if not os.path.exists(rom_folder):
        os.makedirs(rom_folder)

    for file in os.listdir(rom_folder):
        file_path = os.path.join(rom_folder, file)
        if os.path.isfile(file_path) and file.lower().endswith((".gb", ".gbc")):
            name = os.path.splitext(file)[0]
            roms.append({"name": name, "path": file_path})

            cover_path = os.path.join(rom_folder, name + ".png")
            if os.path.exists(cover_path):
                img = pygame.image.load(cover_path)
            else:
                img = pygame.Surface((200, 200))
                img.fill((60, 60, 60))
            thumbnails[name] = img

            desc_path = os.path.join(rom_folder, name + ".txt")
            if os.path.exists(desc_path):
                with open(desc_path, "r", encoding="utf-8") as f:
                    descriptions[name] = f.read().strip()
            else:
                descriptions[name] = ""

    for folder in os.listdir(rom_folder):
        folder_path = os.path.join(rom_folder, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.lower().endswith((".gb", ".gbc")):
                    roms.append({"name": folder, "path": os.path.join(folder_path, file)})

                    cover_path = os.path.join(folder_path, "cover.png")
                    if os.path.exists(cover_path):
                        img = pygame.image.load(cover_path)
                    else:
                        img = pygame.Surface((200, 200))
                        img.fill((60, 60, 60))
                    thumbnails[folder] = img

                    desc_path = os.path.join(folder_path, "desc.txt")
                    if os.path.exists(desc_path):
                        with open(desc_path, "r", encoding="utf-8") as f:
                            descriptions[folder] = f.read().strip()
                    else:
                        descriptions[folder] = ""

    if not roms:
        roms = [{"name": "No ROMs found!", "path": None}]
        thumbnails["No ROMs found!"] = pygame.Surface((200, 200))
        thumbnails["No ROMs found!"].fill((60, 60, 60))
        descriptions["No ROMs found!"] = ""

    roms.append({"name": "Settings", "path": None})
    thumbnails["Settings"] = pygame.Surface((200, 200))
    thumbnails["Settings"].fill((100, 100, 255))
    descriptions["Settings"] = "Configure scroll, zoom, and sound options."

    return roms, thumbnails, descriptions


    roms.append({"name": "Settings", "path": None})
    thumbnails["Settings"] = pygame.Surface((200, 200))
    thumbnails["Settings"].fill((100, 100, 255))
    descriptions["Settings"] = "Configure scroll, zoom, and sound options."

    return roms, thumbnails, descriptions

roms, thumbnails, descriptions = load_roms()

bg_path = r"Assets\background.png" 
if os.path.exists(bg_path):
    background_img = pygame.image.load(bg_path).convert()
    background_img = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
else:
    background_img = None
    print("Background not found!")

scroll_x = 0.0
scroll_target = 0.0
spacing = 300
center_x = screen.get_width() // 2
in_settings = False
running = True
clock = pygame.time.Clock()
easing = 0.1

def draw_carousel():
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(settings["bg_color"])

    for y in range(screen.get_height()):
        color_val = 15 + int(45 * y / screen.get_height())
        pygame.draw.line(screen, (color_val, color_val, color_val, 30), (0, y), (screen.get_width(), y))

    y_img = 250
    y_text = 500
    num_roms = len(roms)
    selected_index = round(scroll_x) % num_roms

    for i, rom in enumerate(roms):
        distance = (i - scroll_x) % num_roms
        if distance > num_roms / 2:
            distance -= num_roms
        if i == selected_index or abs(distance) > 3:
            continue

        scale_factor = max(settings["zoom_side"], settings["zoom_center"] - 0.2 * abs(distance))
        alpha = max(100, 255 - 50 * abs(distance))

        img = pygame.transform.scale(thumbnails[rom["name"]],
                                     (int(200 * scale_factor), int(200 * scale_factor)))
        img.set_alpha(alpha)
        rect = img.get_rect(center=(center_x + distance * spacing, y_img + 20 * abs(distance)))
        screen.blit(img, rect)

        text_color = (150, 150, 150) if distance != 0 else settings["highlight_color"]
        text = font_desc.render(rom["name"], True, text_color)
        text_rect = text.get_rect(center=(rect.centerx, y_text + 20 * abs(distance)))
        screen.blit(text, text_rect)

    rom = roms[selected_index]
    scale_factor = settings["zoom_center"] * 1.2
    img = pygame.transform.scale(thumbnails[rom["name"]],
                                 (int(200 * scale_factor), int(200 * scale_factor)))
    rect = img.get_rect(center=(center_x, y_img))
    screen.blit(img, rect)

    text = font_title.render(rom["name"], True, settings["highlight_color"])
    screen.blit(text, text.get_rect(center=(center_x, y_text)))

    desc = descriptions[rom["name"]]
    for idx, line in enumerate(desc.splitlines()[:5]):
        screen.blit(font_desc.render(line, True, settings["hint_color"]), (50, 550 + idx * 25))

    hint_text = "←/→: Scroll   ENTER: Launch/Settings   ESC: Quit"
    screen.blit(font_hint.render(hint_text, True, settings["hint_color"]), (50, 650))
    pygame.display.flip()

def draw_settings():
    screen.fill(settings["bg_color"])
    screen.blit(font_title.render("Settings", True, settings["highlight_color"]), (400, 50))

    for idx, opt in enumerate(settings_options):
        is_selected = idx == current_setting_index
        color = settings["highlight_color"] if is_selected else settings["normal_color"]

        if opt["key"] != "rom_folder":
            val = settings[opt["key"]]
            value = f"{val:.2f}" if isinstance(val, float) else str(val)
        else:
            value = settings["rom_folder"]

        line = f"{opt['name']}: {value}"
        screen.blit(font_desc.render(line, True, color), (100, 150 + idx * 50))
        if is_selected:
            pygame.draw.rect(screen, (50, 50, 50), (90, 150 + idx * 50 - 5, 400, 30), 2)

    screen.blit(font_hint.render("↑/↓: Select   ←/→: Adjust   ESC: Return",
                                 True, settings["hint_color"]), (50, 650))
    pygame.display.flip()

def handle_settings_input(event):
    global current_setting_index, in_settings
    opt = settings_options[current_setting_index]
    if event.key == pygame.K_UP:
        current_setting_index = (current_setting_index - 1) % len(settings_options)
    elif event.key == pygame.K_DOWN:
        current_setting_index = (current_setting_index + 1) % len(settings_options)
    elif event.key == pygame.K_LEFT:
        if opt["step"] and isinstance(settings[opt["key"]], (int, float)):
            settings[opt["key"]] = max(opt["min"], settings[opt["key"]] - opt["step"])
            save_settings()
    elif event.key == pygame.K_RIGHT:
        if opt["step"] and isinstance(settings[opt["key"]], (int, float)):
            settings[opt["key"]] = min(opt["max"], settings[opt["key"]] + opt["step"])
            save_settings()
    elif event.key == pygame.K_ESCAPE:
        in_settings = False
        save_settings()

while running:
    num_roms = len(roms)
    if not in_settings:
        diff = (scroll_target - scroll_x) % num_roms
        if diff > num_roms / 2:
            diff -= num_roms
        elif diff < -num_roms / 2:
            diff += num_roms

        scroll_x += diff * easing
        scroll_x %= num_roms
        draw_carousel()
    else:
        draw_settings()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if in_settings:
                handle_settings_input(event)
            else:
                if event.key == pygame.K_RIGHT:
                    scroll_target = (scroll_target + 1) % len(roms)
                elif event.key == pygame.K_LEFT:
                    scroll_target = (scroll_target - 1) % len(roms)
                elif event.key == pygame.K_RETURN:
                    selected_index = round(scroll_x) % len(roms)
                    rom_item = roms[selected_index]
                    if rom_item["name"] == "Settings":
                        in_settings = True
                    elif rom_item["path"]:
                        try:
                            pyboy = PyBoy(rom_item["path"],
                                          window="SDL2",
                                          sound_emulated=True,
                                          sound_volume=settings["sound_volume"])
                            running_pyboy = True
                            while running_pyboy:
                                running_pyboy = pyboy.tick()
                                for py_event in pygame.event.get():
                                    if py_event.type == pygame.QUIT:
                                        running_pyboy = False
                                time.sleep(1 / 60.0)
                            pyboy.stop()
                        except Exception as e:
                            print(f"Failed to load ROM: {e}")
                elif event.key == pygame.K_ESCAPE:
                    running = False

    clock.tick(60)

pygame.quit()

