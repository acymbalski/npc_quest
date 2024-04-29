import os
import pickle
import random
import sys


def loadGame(w: int, game):
    """
    Load game from save/save00X.sav
    Return character object, or None.
    """
    filename = f"save/save00{w}.sav"
    try:
        with open(filename, "rb") as file:
            character = pickle.load(file)
            character.game = game
        return character
    except Exception:
        return None


def delGame(w: int) -> bool:
    """
    Delete game from save/save00X.sav
    Used when player dies.
    Returns True if successful, False if not.
    """
    filename = f"save/save00{w}.sav"
    try:
        os.remove(filename)
        return True
    except Exception:
        return False


def savegame(character) -> bool:
    """
    Save character to save/save00X.sav
    Creates the 'save/' directory if it doesn't exist.
    Returns True if successful, False if not.
    """
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
    """
    Gets an absolute path to a reference. This is here as an attempt to get
    assets working with packaged versions of the game.
    Did it work? I don't even know.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def makeUpName() -> str:
    """
    Generate a random name.
    This algorithm takes a list of name patterns - Cvcvvc, for example -
    and replaces each C or V with a random consonant or vowel, respectively.
    """
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
    vowel = "aeiouy"  # y is not a vowel! >:( But in the original code, it was.
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
