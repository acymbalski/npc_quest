import pygame
from enums import SFX
import random

SOUNDS = {
    SFX.HUZZAH: "huzzah.wav",
    SFX.WHIFF: "whiff.wav",
    SFX.HITBADGUY: "hitbadguy.wav",
    SFX.HITPLAYER: "hitplayer.wav",
    SFX.DEADGUY: "deadbadguy.wav",
    SFX.NEEDFOOD: "needfood.wav",
    SFX.PLAYERDIE: "playerdie.wav",
    SFX.EAT: "eat.wav",
    SFX.LEVELUP: "levelup.wav",
    SFX.VICTORY: "victory.wav",
    SFX.CHACHING: "chaching.wav",
    SFX.HEAVY: "heavy.wav",
    SFX.PRICEY: "pricey.wav",
    SFX.DRINK: "drink.wav",
    SFX.CIRCLE: "circlestrike.wav",
    SFX.ARROW: "arrow.wav",
    SFX.ZAP: "zap.wav",
    SFX.CHOMP: "chomp.wav",
    SFX.CHICKEN: "chicken.wav",
    SFX.CRITICAL: "critical.wav",
    SFX.BERSERK: "berserk.wav",
}


def makeSound(sound: SFX):
    # play sound effect

    # get a random number between 0 and 255
    freq_mod = random.randint(0, 255)
    freq = 1000 - 127 + freq_mod
    # TODO: Modify sound by frequency modifier

    pygame.mixer.init()
    sound = pygame.mixer.Sound(f"sound/{SOUNDS[sound]}")
    sound.play()


if __name__ == "__main__":
    import main

    main.main()
