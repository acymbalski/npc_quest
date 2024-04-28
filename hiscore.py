import os
import pickle

import pygame

import requests

from constants import CLASS_NAME, LEVELS, MAX_SCORES
from display import printMe


class Score:
    """
    A general score object.
    This is what the high score lists are comprised of. It's not much, can
    likely be condensed or cleaned up.
    """

    def __init__(
        self, player_name, name, chrClass, deathCause, deathLevel, maxLevel, score
    ):
        # player name is the name of you, the player at the computer
        # this is used for the global high score list
        self.player_name = player_name.strip()

        # name of the character
        self.name = name

        # had a real problem with these, should they be enums, ints, strings, what?
        # I think it's strings at the moment. But I hate it!
        self.chrClass = chrClass
        self.deathCause = deathCause
        self.deathLevel = deathLevel

        # how far did we get?
        self.maxLevel = maxLevel

        # xp earned
        self.score = int(score)

    def __str__(self):
        """
        String representation of the score object.
        """
        return f"{self.name}, a Level {self.maxLevel} {self.chrClass}. Score: {int(self.score)}"


def rankEarned(game):
    """
    Return the rank earned by the player in the local high score list.
    """
    # hate this whole thing
    score = Score(
        game.player_name,
        game.player.name,
        game.player.chrClass,
        game.player.deathCause,
        game.level,
        game.player.level,
        game.player.xp,
    )
    for i in range(len(game.hiscores)):
        this_score = game.hiscores[i]
        if score.score == this_score.score and score.name == this_score.name:
            return i
    return -1


def addHiScore(game):
    """
    Player must have died. Add their Score to the local and possibly global
    high score lists.
    """

    # Create the Score object
    new_score = Score(
        game.player_name,
        game.player.name,
        CLASS_NAME[game.player.chrClass],  # oof
        game.player.deathCause,
        game.level,
        game.player.level,
        game.player.xp,
    )
    game.hiscores.append(new_score)
    # sort the hiscores by score
    game.hiscores = sorted(game.hiscores, key=lambda x: x.score, reverse=True)
    # remove anything after 10, even if we don't display it
    game.hiscores = game.hiscores[:MAX_SCORES]
    # save scores to file
    save_scores(game)

    # do we have a score URL? And does the player even want to upload scores?
    if game.upload_scores and game.score_url:
        # if this character is eligible to upload...
        if game.player.online_eligible:
            # send the score to the server
            # there's unfortunately no way to actually validate that the score
            # is real. You could send a fake score. It would be nice to fix
            # that although at the moment I just don't know how. There is
            # the possibility to validate a little server-side but nothing
            # ironclad :(
            # if you are reading this, be cool and don't cheat!
            # It's just a game!
            url = game.score_url + "/scores"
            score = new_score
            data = {
                "player_name": score.player_name,
                "character_name": score.name,
                "character_class": score.chrClass,
                "death_cause": score.deathCause,
                "death_level": LEVELS[score.deathLevel],  # oof!
                "level": score.maxLevel,
                "score": score.score,
                "version": game.version,
            }
            try:
                # timeout of 5 seconds, let's not get crazy here
                requests.post(url, json=data, timeout=5)
            except requests.exceptions.Timeout:
                print("Timeout occurred while sending score")
            except Exception as e:
                print(f"Error sending score: {e}")
        else:
            # player cannot upload score. Must have cheated.
            # You can cheat! But we just can't muck up the leaderboard with that
            print("Player not eligible to upload score")


def drawHiScores(game):
    """
    Render the high scores to the screen.
    Currently just used in the Title screen.
    """
    # if we have no scores, don't bother
    if len(game.hiscores) and (game.retrieve_scores and len(game.global_hiscores) == 0):
        return

    printMe(game, "Greatest NPCs In History", 360, 5)

    # if we're going to show global high scores, clear up some room
    show_scores = len(game.hiscores)
    if game.retrieve_scores:
        show_scores = 5

    # draw local scores
    for i in range(show_scores):
        if i < len(game.hiscores):
            score = game.hiscores[i]
            printMe(game, f"{i + 1}. {str(score)}", 360, i * 30 + 30)
            death_text = (
                f"Defeated by {score.deathCause} in {LEVELS[score.deathLevel]}."
            )
            printMe(game, death_text, 380, i * 30 + 40)

    # get networked scores
    if game.retrieve_scores:
        printMe(game, "Global High Scores", 360, 200)
        if len(game.global_hiscores) == 0:
            printMe(game, "No scores found", 360, 230)
        else:
            for i in range(len(game.global_hiscores)):
                score = game.global_hiscores[i]

                # if it's our score, make it yellow!
                color = pygame.Color("WHITE")
                if score.player_name == game.player_name:
                    color = pygame.Color("YELLOW")
                printMe(
                    game,
                    f"{i + 1}. {score.player_name}",
                    360,
                    i * 30 + 230,
                    color=color,
                )
                printMe(
                    game,
                    str(score),
                    360,
                    i * 30 + 240,
                    color=color,
                )
                death_text = f"Defeated by {score.deathCause} in {score.deathLevel}."
                printMe(
                    game,
                    death_text,
                    380,
                    i * 30 + 250,
                    color=color,
                )


def retrieve_scores(game):
    """
    Retrieve the global high scores from the server.
    """
    scores = []
    if game.retrieve_scores and game.score_url:
        url = game.score_url + f"/scores?version={game.version}"
        print(f"Retrieving scores from {url}...")
        try:
            # timeout of 5 seconds
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                scores = response.json()
        except requests.exceptions.Timeout:
            print("Timeout occurred while retrieving scores")
        except Exception as e:
            print(f"Error retrieving scores: {e}")
    print("Retrieved scores!")

    global_hiscores = []
    # save to score objects
    for score in scores:
        global_hiscores.append(
            Score(
                player_name=score["player_name"],
                name=score["character_name"],
                chrClass=score["character_class"],
                deathCause=score["death_cause"],
                deathLevel=score["death_level"],
                maxLevel=int(score["level"]),
                score=int(score["score"]),
            )
        )

    return global_hiscores


def drawDeathScore(game):
    """
    Draw the player's score to the screen when they die.
    Used by Notice
    """
    printMe(
        game,
        f"{rankEarned(game) + 1}. {game.player.name}, a Level {game.player.level} {CLASS_NAME[game.player.chrClass]}. Score {game.player.xp}",
        200,
        400,
    )

    printMe(
        game,
        f"Defeated by {game.player.deathCause} in {LEVELS[game.level]}.",
        220,
        410,
    )


def save_scores(game):
    """
    Save the hiscores to a file.
    We save both global and local to the file so you can see a little something
    even when offline.
    """
    print("Saving hiscores")
    with open("hiscores.dat", "wb") as f:
        hiscores = {"local": game.hiscores, "global": game.global_hiscores}
        pickle.dump(hiscores, f)


def load_scores(game):
    """
    Load the hiscores from a file.
    """
    # if file exists, load it
    if os.path.exists("hiscores.dat"):
        loaded_dict = {}
        with open("hiscores.dat", "rb") as f:
            loaded_dict = pickle.load(f)
        if loaded_dict:
            game.hiscores = loaded_dict["local"]
            game.global_hiscores = loaded_dict["global"]


if __name__ == "__main__":
    import main

    main.main()
