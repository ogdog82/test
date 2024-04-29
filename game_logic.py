import random
import emoji

class Game:
    goblin = {"name": "Goblin", "icon": '👺', "health": 20, "attack": 8, "defense": 3}
    skeleton = {"name": "Skeleton", "icon": '💀', "health": 30, "attack": 10, "defense": 2}
    orc = {"name": "Orc", "icon": '👹', "health": 40, "attack": 12, "defense": 5}
    dragon = {"name": "Dragon", "icon": '🐉', "health": 50, "attack": 15, "defense": 8}
    def __init__(self, player):
        self.player = player
        self.game_map = self.generate_map()
        self.player_position = self.get_town_position()
        self.enemies = self.generate_enemies()
        self.items = self.generate_items()
        self.npcs = self.generate_npcs()

    def generate_map(self):
        # Generate a random map for the game with mountains, towns, and grassy terrains
        game_map = []
        terrain_types = [emoji.emojize(':evergreen_tree:'), emoji.emojize(':deciduous_tree:'), emoji.emojize(':seedling:'), emoji.emojize(':herb:'), emoji.emojize(':four_leaf_clover:')]

        for _ in range(20):
            row = []
            for _ in range(20):
                terrain = random.choice(terrain_types)
                row.append(terrain)
            game_map.append(row)

        # Add mountains
        for _ in range(3):
            mountain_x = random.randint(0, 19)
            mountain_y = random.randint(0, 19)
            game_map[mountain_x][mountain_y] = emoji.emojize(':mountain:')

        # Add town
        town_x = random.randint(0, 19)
        town_y = random.randint(0, 19)
        game_map[town_x][town_y] = emoji.emojize(':house:')

        return game_map

    def generate_enemies(self):
        enemy_types = [
            {"name": "Goblin", "icon": '👺', "health": 20, "attack": 8, "defense": 3},
            {"name": "Skeleton", "icon": '💀', "health": 30, "attack": 10, "defense": 2},
            {"name": "Orc", "icon": '👹', "health": 40, "attack": 12, "defense": 5},
            {"name": "Dragon", "icon": '🐉', "health": 50, "attack": 15, "defense": 8}
        ]

        enemies = []

        num_enemies = random.randint(1, 5)
        enemy_positions = [(random.randint(0, 20), random.randint(0, 20)) for _ in range(num_enemies)]

        for position in enemy_positions:
            random_enemy = random.choice(enemy_types)
            enemies.append({"name": random_enemy["name"], "icon": random_enemy["icon"], "x": position[0], "y": position[1]})

        return enemies
    def generate_items(self):
        # Generate items for the game
        items = [
            {"name": "Potion", "healing": 20},
            {"name": "Sword", "attack": 15},
            {"name": "Shield", "defense": 10}
        ]
        return items

    def generate_npcs(self):
        # Generate NPCs for the game
        npcs = [
            {"name": "Tony", "dialogue": "Hello, traveller!", "quest": "Find the lost treasure"},
            {"name": "Jane", "dialogue": "Welcome to the town!", "quest": "None"}
        ]
        return npcs

    def play(self):
        while True:
            self.print_map()
            direction = input("Enter a direction (w/a/s/d): ")
            self.move_player(direction)
            self.check_encounter()
            self.check_item()
            self.check_npc()

    def print_map(self):
        for y in range(20):
            for x in range(20):
                if (x, y) == self.player_position:
                    print("😎", end=" ")  # Print the player emoji
                elif any(enemy["x"] == x and enemy["y"] == y for enemy in self.enemies):
                    for enemy in self.enemies:
                        if enemy["x"] == x and enemy["y"] == y:
                            print(enemy["icon"], end=" ")  # Print enemy emoji
                        else:
                            print(self.game_map[y][x], end=" ")  # Print the terrain symbol
                else:
                    print(self.game_map[y][x], end=" ")  # Print the terrain symbol
            print()
            
    def update_player_position(self, direction):
        x, y = self.player_position

        if direction == "w" and x > 0:
            x -= 1
        elif direction == "a" and y > 0:
            y -= 1
        elif direction == "s" and x < 19:
            x += 1
        elif direction == "d" and y < 19:
            y += 1

        self.player_position = (x, y)

    def move_player(self, direction):
        self.update_player_position(direction)
        self.move_enemies()

    def check_encounter(self):
        # Check if player encounters an enemy
        player_x, player_y = self.player_position

        for enemy in self.enemies:
            enemy_x = enemy["x"]
            enemy_y = enemy["y"]

            if player_x == enemy_x and player_y == enemy_y:
                self.battle(enemy)
                
    def apply_status_effects(self, player_status_effects):
        # Apply any ongoing status effects on the player
        if "Poison" in player_status_effects:
            poison_damage = 2
            self.player.health -= poison_damage
            player_status_effects["Poison"] -= 1
            print(f"You take {poison_damage} poison damage from being poisoned!")
            if player_status_effects["Poison"] == 0:
                del player_status_effects["Poison"]
        return player_status_effects

    def battle(self, enemy):
        enemy_name = enemy["name"]
        enemy_health = enemy["health"]
        enemy_attack = enemy["attack"]
        
        if 'defense' in enemy:
            enemy_defense = enemy["defense"]
        else:
            enemy_defense = 0

        print(f"You are fighting against {enemy_name}!")
        
        player_turn = True
        player_defending = False
        player_status_effects = {}  # Dictionary to store active status effects on player with durations
        
        while enemy_health > 0 and self.player.health > 0:
            print("\nPlayer Health:", self.player.health)
            print("Enemy Health:", enemy_health)
            print("\nChoose your action:")
            print("1. Attack")
            print("2. Defend")
            print("3. Use Item")
            if len(player_status_effects) > 0:
                print("4. Use Special Ability")
            action = input("Enter your choice: ")
            
            if player_turn:
                if action == "1":  # Attack
                    player_damage = self.calculate_attack_damage(self.player.attack, enemy_defense)
                    if random.random() < 0.1:  # 10% chance of critical hit
                        player_damage *= 2  # Double damage for critical hit
                        print("Critical Hit!")
                    enemy_health -= player_damage
                    print(f"You deal {player_damage} damage to {enemy_name}!")
                elif action == "2":  # Defend
                    self.player.defense += 2
                    player_defending = True
                    print("You brace for impact and increase your defense by 2!")
                elif action == "3":  # Use Item
                    if len(self.player.items) > 0:
                        print("Items:")
                        for i, item in enumerate(self.player.items):
                            print(f"{i+1}. {item['name']}")
                        item_choice = int(input("Choose an item to use: ")) - 1
                        item = self.player.items[item_choice]
                        if item["name"] == "Potion":
                            self.player.health += item["healing"]
                            print(f"You used a Potion and healed for {item['healing']} HP!")
                            del self.player.items[item_choice]
                    else:
                        print("No items available to use.")
                elif action == "4" and len(player_status_effects) > 0:  # Use Special Ability
                    if "special_ability" in self.player and self.player["special_ability"]["cooldown"] == 0:
                        special_ability = self.player.special_ability
                        if special_ability["name"] == "Fireball":
                            player_damage = special_ability["damage"]
                            enemy_health -= player_damage
                            print(f"You cast Fireball and deal {player_damage} damage to {enemy_name}!")
                            self.player.special_ability["cooldown"] = special_ability["max_cooldown"]
                        # Add more special abilities here
                    else:
                        print("Special ability is on cooldown.")
                else:
                    print("Invalid choice. Try again.")
                    continue
                
                player_turn = False
            else:
                if random.random() < 0.3:  # 30% chance of enemy using a special move
                        if "special_moves" in enemy and len(enemy["special_moves"]) > 0:
                            special_move = random.choice(enemy["special_moves"])
                            if special_move["name"] == "Poison Stab":
                                poison_damage = special_move["damage"]
                                self.player.health -= poison_damage
                                print(f"{enemy_name} uses Poison Stab and deals {poison_damage} poison damage!")
                                if random.random() < 0.5:  # 50% chance to apply poison effect
                                    player_status_effects["Poison"] = 3  # Poison effect lasts for 3 turns
                                    print("You have been poisoned!")
                            # Add more special moves here
                else:
                    player_status_effects = self.apply_status_effects(player_status_effects)
                    # Apply any ongoing status effects on the player
                    if "Poison" in player_status_effects:
                        poison_damage = 2
                        self.player.health -= poison_damage
                        player_status_effects["Poison"] -= 1
                        print(f"You take {poison_damage} poison damage from being poisoned!")
                        if player_status_effects["Poison"] == 0:
                            del player_status_effects["Poison"]
                if not player_defending:
                
                    enemy_damage = max(0, enemy_attack - self.player.defense)
                    self.player.health -= enemy_damage
                    print(f"{enemy_name} deals {enemy_damage} damage to you!")
                else:
                    print(f"{enemy_name} attacks, but you defend successfully!")
                    player_defending = False
                
                player_turn = True
            
            # Check for and apply status effects on player and enemy
            # Update health, defense, etc. based on status effects
            
            if enemy_health <= 0:
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                print(f"You have defeated {enemy_name}!")
                break

            if self.player.health <= 0:
                print("You have been defeated!")
                break

        if self.player.health <= 0:
            print("You have been defeated! Game over!")
            exit(0)
    
    def calculate_attack_damage(self, player_attack, enemy_defense):
        base_damage = max(0, player_attack - enemy_defense)
        return random.randint(base_damage // 2, base_damage)
            
    def check_item(self):
        # Check if player encounters an item
        pass  # Implement item logic

    def check_npc(self):
        # Check if player encounters an NPC
        player_x, player_y = self.player_position
        town_x, town_y = self.get_town_position()

        if player_x == town_x and player_y == town_y:
            print("You have entered the town!")
            # Implement special encounter for the town here

    def get_town_position(self):
        for i, row in enumerate(self.game_map):
            for j, terrain in enumerate(row):
                if terrain == emoji.emojize(':house:'):
                    return i, j
    def move_enemies(self):
        player_x, player_y = self.player_position
        
        # Check if there is an enemy that should chase the player
        chasing_enemy = None
        for enemy in self.enemies:
            enemy_x = enemy["x"]
            enemy_y = enemy["y"]
            distance = abs(player_x - enemy_x) + abs(player_y - enemy_y)
            if distance <= 3:
                chasing_enemy = enemy
                break
        
        if chasing_enemy:
            # Move the chasing enemy towards the player
            if chasing_enemy["x"] < player_x:
                chasing_enemy["x"] += 1
            elif chasing_enemy["x"] > player_x:
                chasing_enemy["x"] -= 1
            elif chasing_enemy["y"] < player_y:
                chasing_enemy["y"] += 1
            elif chasing_enemy["y"] > player_y:
                chasing_enemy["y"] -= 1
        else:
            # Move other enemies randomly if no enemy is chasing the player
            for enemy in self.enemies:
                direction = random.choice(["up", "down", "left", "right"])
                if direction == "up":
                    enemy["x"] -= 1 if enemy["x"] > 0 else 0
                elif direction == "down":
                    enemy["x"] += 1 if enemy["x"] < len(self.game_map) - 1 else 0
                elif direction == "left":
                    enemy["y"] -= 1 if enemy["y"] > 0 else 0
                elif direction == "right":
                    enemy["y"] += 1 if enemy["y"] < len(self.game_map[0]) - 1 else 0
    
        # Update the enemy positions and icons
        for enemy in self.enemies:
            enemy_x = enemy["x"]
            enemy_y = enemy["y"]
            
            # Check and update enemy icons based on their type
            for enemy_type in [Game.goblin, Game.skeleton, Game.orc, Game.dragon]:
                if enemy["name"] == enemy_type["name"]:
                    self.game_map[enemy_x][enemy_y] = enemy_type["icon"]
                    
            # Update the enemy position
            enemy["x"], enemy["y"] = enemy_x, enemy_y
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 10
        self.defense = 5
        

# Instantiate the Player and Game classes
player = Player("Hero")
game = Game(player)

# Start the game
game.play()