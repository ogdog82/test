import emoji
from game_logic import *
from player import *

def main():
    player_name = input("Enter your name: ")
    player = Player(player_name)
    game = Game(player)
    
    print(f"Welcome to the dungeon, {player.name}!")
    print("Your adventure begins now...")
    
    game.play()

if __name__ == "__main__":
    main()