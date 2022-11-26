import Project as pj
import pygame as pg

def main():
    # Initializing
    pg.init()

    pj.initial_screen()

    # Initial the game
    gm = pj.game_2048()

    # Refresh the screen
    pg.display.flip()

    pj.game_start(gm)


if __name__ == "__main__":
    main()

