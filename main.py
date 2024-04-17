import sys
import os

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

sys.path.insert(0, "src/ai")
sys.path.insert(0, "src/core")
sys.path.insert(0, "src/game")
sys.path.insert(0, "src/utils")
sys.path.insert(0, "src")
resource_path("src/ai")
resource_path("src/core")
resource_path("src/game")
resource_path("src/utils")
resource_path("src")
resource_path("assets/data/oldtrie.dat")
resource_path("assets/data/trie.dat")
resource_path("assets/data/dictionary.txt")
resource_path("assets/data/old-dictionary.txt")
resource_path("assets/data/sm-dictionary.txt")
resource_path("assets/font/pixelfont.ttf")
resource_path("assets/sfx/button.wav")
resource_path("assets/sfx/gamefx.wav")
resource_path("assets/sfx/letter.wav")

import sys


if __name__ == "__main__":
    from src.game.wordwiz import init_game
    init_game()
    # sampleMM()
    # sampleCB("glass", "spadeglass")

