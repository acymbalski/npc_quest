class Monster:
    """
    Monster class. Just holds values for the monster.
    """

    def __init__(self, strength, speed, accuracy, maxLife, defense, xp, gold):
        self.strength = strength
        self.speed = speed
        self.accuracy = accuracy
        self.maxLife = maxLife
        self.defense = defense
        self.xp = xp
        self.gold = gold


# Monsters defined here. Not even with their names!
# This should be really cleaned up and defined elsewhere.
# The first two blank values are a quirk of the original code I think,
# possibly a fixed array thing.
monsters = [
    None,
    None,
    # gnome
    Monster(strength=1, speed=3, accuracy=1, maxLife=2, defense=0, xp=1, gold=3),
    # fatbird
    Monster(strength=7, speed=1, accuracy=1, maxLife=5, defense=2, xp=2, gold=3),
    # dolphin
    Monster(strength=20, speed=1, accuracy=3, maxLife=20, defense=10, xp=20, gold=10),
    # hotdog
    Monster(strength=15, speed=5, accuracy=10, maxLife=13, defense=4, xp=10, gold=20),
    # reindeer
    Monster(strength=6, speed=3, accuracy=5, maxLife=5, defense=2, xp=5, gold=6),
    # bluey
    Monster(strength=2, speed=10, accuracy=1, maxLife=1, defense=2, xp=7, gold=4),
]
