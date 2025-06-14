import argparse
import os

from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="enable debug printing", action="store_true")
args = parser.parse_args()
DEBUG = args.debug

TITLE = "Asteroids"

SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 1280))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 720))
TARGET_FPS = int(os.getenv("TARGET_FPS", 60))

PLAYER_RADIUS = 20
PLAYER_ROTATION_SPEED = 0.2
PLAYER_MOVE_SPEED = 0.2
PLAYER_RELOAD_SPEED = 300  # milliseconds

ASTEROID_MOVE_SPEED = 0.1
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 800  # milliseconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

MISSILE_SPEED = 0.5
MISSILE_RADIUS = 5
