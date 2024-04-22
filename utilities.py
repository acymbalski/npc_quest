import os
import pickle
import random
import sys


def loadGame(w: int, game):
    # load game from save/save00X.sav
    filename = f"save/save00{w}.sav"
    try:
        with open(filename, "rb") as file:
            character = pickle.load(file)
            character.game = game
        return character
    except Exception:
        return None


def delGame(w: int) -> bool:
    # delete game from save/save00X.sav
    filename = f"save/save00{w}.sav"
    try:
        os.remove(filename)
        return True
    except Exception:
        return False


def savegame(character) -> bool:
    # save game to save/save00X.sav
    saveDir = "save"
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    filename = f"{saveDir}/save00{character.slot}.sav"
    try:
        with open(filename, "wb") as file:
            pickle.dump(character, file)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def makeUpName() -> str:
    name_format = [
        "Cvcvvc",
        "Cvvcv Cvccv",
        "Cvv C'Cvcc",
        "Cvcvcv",
        "Cvvcvv",
        "Vcvvcv",
        "Vvcv",
        "Vccvcvv",
        "Vcvcvv",
        "Vccvv Cvcv",
    ]
    vowel = "aeiouy"
    consonant = "bcdfghjklmnpqrstvwxz"

    name = random.choice(name_format)

    for character in name:
        if character == "C":
            name = name.replace("C", random.choice(consonant).upper(), 1)
        elif character == "c":
            name = name.replace("c", random.choice(consonant), 1)
        elif character == "V":
            name = name.replace("V", random.choice(vowel).upper(), 1)
        elif character == "v":
            name = name.replace("v", random.choice(vowel), 1)
        elif character == " ":
            name = name.replace(" ", " ", 1)
        elif character == "'":
            name = name.replace("'", "'", 1)
    return name
