from character import className
from constants import LEVELS, MAX_SCORES
from display import printMe

# TODO: make sure we save this to hiscore.dat somewhere


class Score:
    def __init__(self, name, chrClass, deathCause, deathLevel, maxLevel, score):
        self.name = name
        self.chrClass = chrClass
        self.deathCause = deathCause
        self.deathLevel = deathLevel
        self.maxLevel = maxLevel
        self.score = score

    def __str__(self):
        # TODO: Note this doesn't include the prefix of the actual number of the rank, include that elsewhere
        return f"{self.name}, a Level {self.maxLevel} {className(self.chrClass)}. Score: {self.score}"


def rankEarned(game):
    # TODO: add hiscore list to game, sort it here by score, return rank
    rank = 0
    for i in range(MAX_SCORES):
        if game.player.xp > game.hiscore[i].score:
            pass
    return rank


def drawHiScores(game):
    printMe(game, "Greatest NPCs In History", 360, 5)
    # TODO: the rest


def drawDeathScore(game):
    printMe(
        game,
        f"{rankEarned(game) + 1}. {game.player.name}, a Level {game.player.level} {className(game.player.chrClass)}. Score {game.player.xp}",
        200,
        400,
    )
    if game.level > 9:
        printMe(
            game,
            f"Defeated by {game.monster[game.level].name} in A Very Bad Place.",
            220,
            410,
        )
    else:
        printMe(
            game,
            f"Defeated by {game.monster[game.level].name} in {LEVELS[game.level]}.",
            220,
            410,
        )
