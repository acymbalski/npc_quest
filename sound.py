import random

import numpy
import pygame
from constants import SFX

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


def change_frequency(sound_array, factor):
    """Adjust the frequency of a sound array."""
    indices = numpy.round(numpy.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices]


def makeSound(sound: SFX):
    # play sound effect
    print(f"Playing {sound}")

    # get a random number between 0 and 255
    freq_mod = random.randint(0, 255)
    freq = (1000 - 127 + freq_mod) / 1000

    pygame.mixer.init()
    sound = pygame.mixer.Sound(f"sound/{SOUNDS[sound]}")

    # Convert the sound to a NumPy array
    sound_array = pygame.sndarray.samples(sound)

    # Adjust the frequency
    adjusted_sound_array = change_frequency(sound_array, freq)

    # Convert the adjusted sound array back to a Pygame sound
    adjusted_sound = pygame.sndarray.make_sound(adjusted_sound_array)

    # Play the adjusted sound
    adjusted_sound.play()


if __name__ == "__main__":
    import main

    main.main()
