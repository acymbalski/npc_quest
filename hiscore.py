from character import className
from constants import LEVELS, MAX_SCORES
from display import printMe


def rankEarned(game):
    # TODO
    for i in range(MAX_SCORES):
        pass


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
