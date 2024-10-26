#setup:
#packages
import random
import pandas as pd
import os
import time

#Player Character:
class Player:
    def __init__(self, name, health, maxhealth, strength, speed, level, xp, items=None):
        self.name = name
        self.health = health
        self.maxhealth = maxhealth
        self.strength = strength
        self.speed = speed
        self.level = level
        self.xp = xp
        self.items_dict = items if items else {}

    def xptolevel(self):
        return self.level * 8

#Loot
class Item:
    def __init__(self):
        self.items_dict = {}

    def generate(self, df,drop,playerinv):
        weight = df['weight'].tolist()
        index = random.choices([0,1], weights = weight, k=1)[0]
        self.item = df.loc[index, 'item']
        self.amount = int(df.loc[index, 'amount'])
        
        if 'gold' not in playerinv:
            playerinv['gold'] = 0


        if self.item != 'none' and drop != 0:
            
            if self.item in playerinv:
                playerinv['gold'] += drop
                playerinv[self.item] +=self.amount
                print(f"Items Dropped: {self.item}({self.amount}) and {drop}gp")


            elif self.item not in playerinv:
                playerinv['gold'] += drop
                playerinv[self.item] =self.amount
                print(f"Items Dropped: {self.item}({self.amount}) and {drop}gp")
        


        if self.item == 'none' and drop != 0:
            print(f"Items Dropped: {drop}gp.")
            playerinv['gold'] += drop


        if self.item != 'none' and drop == 0:
            if self.item in playerinv:
                playerinv[self.item] +=self.amount
                print(f"Items Dropped: {self.item}({self.amount})")

            else:
                playerinv[self.item] = self.amount
                print(f"Items Dropped: {self.item}({self.amount})")
        
        else:
            ("No drops.")

#Mobs
class Monster:
    def generate(self, df):
        weight = df['weight'].tolist()
        index = random.choices([0,1,2], weights = weight, k=1)[0]
        self.name = df.loc[index, 'enemy_name']
        self.health = int(df.loc[index, 'enemy_health'])
        self.maxhealth = int(df.loc[index, 'enemy_maxhealth'])
        self.speed = int(df.loc[index, 'enemy_speed'])
        self.strength = int(df.loc[index, 'enemy_strength'])
        self.xp = int(df.loc[index, 'enemy_xp'])



#Systems
#xp_gain
def xp_gain(player_name, player_level, player_xp, player_xptolevel, enemy_xp):
    player_xp += enemy_xp
    if player_xp >= player_xptolevel:
        print(f"{player_name} gained {enemy_xp}exp.")
        return player_xp
    else:
        print(f"{player_name} gained {enemy_xp}exp. Exp until level {player_level+1}: {player_xptolevel-player_xp}exp.")
        return player_xp

#Combat system.
def combat(player_name, player_health, player_maxhealth, player_strength, player_speed, enemy_name, enemy_health, enemy_maxhealth, enemy_strength, enemy_speed, items_dict):
    print(f"{player_name} encountered a {enemy_name}, health: {enemy_health}/{enemy_maxhealth}!")


    #Escape
    while True:
        attack = input(f"What will you do? <engage/escape>: ").lower()
        if attack == "escape":
        #RNG
            rng1 = random.uniform(0,1)
        #Success
            if rng1 >= 0.8:
                time.sleep(1)
                print(f"{player_name} got away safely!")
                return player_health, True, items_dict['potion']
                
        #Fail
            else:
                time.sleep(1)
                print(f"{player_name} failed to run away! The {enemy_name} attacks {player_name} anyways!")
                break

        elif attack == "engage":
            break
        else:
            print("Invalid input.")

    #While one opponent is still alive...
    while player_health > 0 and enemy_health > 0:
        attack = input(f"What will you do? <attack/heal>: ").lower()
        
        #Heal:
        if attack == "heal":
            #Heal:
            if "potion" in items_dict and items_dict["potion"] > 0:
                print(f"{player_name} used a potion!")
                player_health = player_health + 10
                items_dict['potion'] -= 1

                if player_health > player_maxhealth:
                    player_health = player_maxhealth
                print(f"{player_name} healed 10hp, players health is now {player_health}/{player_maxhealth}.")
                print(f"{player_name} has {items_dict['potion']} potions left.")
                enemy_damage = round(enemy_strength*random.uniform(0,1))

                #Enemy Miss:
                if enemy_damage == 0:
                    time.sleep(1)
                    print(f"{enemy_name} missed!")

                #Enemy Hit:
                else:
                    time.sleep(1)
                    print(f"The {enemy_name} delt {enemy_damage} damage to {player_name}")
                    player_health = player_health - enemy_damage

                #Player Death
                if player_health <= 0:
                    time.sleep(1)
                    print("Your health is 0.")
                    time.sleep(1)
                    print(f"Oh no! {player_name} was slain by the {enemy_name}.")
                    return player_health, False, items_dict['potion']


                #Player Health Update  
                else:
                    time.sleep(1)
                    print(f"{player_name}s health is {player_health}/{player_maxhealth}.")
                    print("")
                continue
            else:
                print("You have no potions.")
                continue


        #Invalid Input Error:
        elif attack != "attack":
            print("Invalid input.")
            continue


        #Damage Calculation:
        enemy_damage = round(enemy_strength*random.uniform(0,1))
        damage = round(player_strength*random.uniform(0, 1))


        #If enemy is faster than player:
        if enemy_speed > player_speed:

            #Enemy miss:
            if enemy_damage == 0:
                time.sleep(1)
                print(f"{enemy_name} missed!")

            #Enemy Hit:
            else:
                time.sleep(1)
                print(f"The {enemy_name} delt {enemy_damage} damage to {player_name}")
                player_health = player_health - enemy_damage

            #Player death:
            if player_health <= 0:
                time.sleep(1)
                print("Your health is 0.")
                time.sleep(1)
                print(f"Oh no! {player_name} was slain by the {enemy_name}.")
                return player_health, False, items_dict['potion']

            #Player Health Update
            else:
                time.sleep(1)
                print(f"{player_name}s health is {player_health}/{player_maxhealth}.")
                print("")

            #Player miss:
            if damage == 0:
                time.sleep(1)
                print(f"{player_name} missed!")

            #Player Hit:
            else:
                time.sleep(1)
                print(f"{player_name} delt {damage} damage to the {enemy_name}.")
                enemy_health = enemy_health - damage


            #Enemy death:
            if enemy_health <= 0:
                time.sleep(1)
                print(f"The enemies health is 0.")
                time.sleep(1)
                print(f"{player_name} killed the {enemy_name}.")
                return player_health, False, items_dict['potion']
            
            #Enemey Health Update:
            else:
                time.sleep(1)
                print(f"The {enemy_name}s health is {enemy_health}/{enemy_maxhealth}.")
                print("")
                time.sleep(1)


        #Player is faster than enemy:
        else:

            #Player miss:
            if damage == 0:
                time.sleep(1)
                print(f"{player_name} missed!")

            #Player Hit:
            else:
                time.sleep(1)
                print(f"{player_name} delt {damage} damage to the {enemy_name}.")
                enemy_health = enemy_health - damage

            #Enemy death:
            if enemy_health <= 0:
                time.sleep(1)
                print(f"The enemies health is 0.")
                time.sleep(1)
                print(f"{player_name} killed the {enemy_name}.")
                return player_health, False, items_dict['potion']

            #Enemey Health Update:
            else:
                time.sleep(1)
                print(f"The {enemy_name}s health is {enemy_health}/{enemy_maxhealth}.")
                print("")
                time.sleep(1)

                
            #Enemy miss:
            if enemy_damage == 0:
                time.sleep(1)
                print(f"{enemy_name} missed!")


            #Enemy Hit:
            else:
                time.sleep(1)
                print(f"The {enemy_name} delt {enemy_damage} damage to {player_name}")
                player_health = player_health - enemy_damage


            #Player Death:
            if player_health <= 0:
                time.sleep(1)
                print("Your health is 0.")
                time.sleep(1)
                print(f"Oh no! {player_name} was slain by the {enemy_name}.")
                return player_health, False, items_dict['potion']

            #Player Health Update:
            else:
                time.sleep(1)
                print(f"{player_name}s health is {player_health}/{player_maxhealth}.")
                print("")

#Remove inventory items with 0:
def remove_zero_quantity_items(items_dict):
    keys_to_remove = [key for key, value in items_dict.items() if value == 0]

    for key in keys_to_remove:
        del items_dict[key]

    return items_dict

#Inventory formatting:
def print_dict_with_newlines(dictionary):
    for key, value in dictionary.items():

        print(f"{key}: {value}")

#Game:
#Intro:
print("Welcome to the game, Castle! A text based adventure RPG!")
player_name = input("What is your characters name? ")
starting_items = {'potion':3,'gold':50,'turkey':69}
player1 = Player(player_name, 100, 100, 10, 10, 1, 0, starting_items)

zone1monsters = pd.read_csv(os.path.join(os.path.dirname(__file__), "zone1monsters.csv"))
zone1monster = Monster()

zone1loots = pd.read_csv(os.path.join(os.path.dirname(__file__), "zone1loots.csv"))
zone1loot = Item()
zone1coinvalues =  list(range(201))
zone1coinweights = [i for i in range(201,0, -1)]

#Check if player is alive:
while player1.health > 0:
    #Clear players inventory of items with 0:
    player1.items_dict = remove_zero_quantity_items(player1.items_dict)

    #Prompt:
    choice = input("What would you like to do? <combat/stats/inventory/heal/finish>: ").lower()

    #Combat:
    if choice == "combat":

        #Combat:
        zone1monster.generate(zone1monsters)        
        player1.health,escaped,player1.items_dict['potion'] = combat(player1.name, player1.health, player1.maxhealth, player1.strength, player1.speed, zone1monster.name, zone1monster.health, zone1monster.maxhealth, zone1monster.strength, zone1monster.speed, player1.items_dict)
        print(f"{player1.name}s current health is {player1.health}/{player1.maxhealth}")

        #If did not run:
        if not escaped and player1.health > 0:

            #Money and drops
            coins = random.choices(zone1coinvalues, weights = zone1coinweights, k=1)[0]
            zone1loot.generate(zone1loots, coins, player1.items_dict)
            remove_zero_quantity_items(player1.items_dict)

            #Exp gain:
            player1.xp = xp_gain(player1.name, player1.level, player1.xp, player1.xptolevel(), zone1monster.xp)


            #Level Up:
            while player1.xp >= player1.xptolevel():
                player1.xp -= player1.xptolevel()
                player1.level += 1
                player1.health += 5
                player1.maxhealth += 5
                player1.strength += 1
                player1.speed += 1
                print(f"{player1.name} is now [level {player1.level}]! Exp needed for level {player1.level+1}: {player1.xptolevel()}exp. Current exp: {player1.xp}exp.")


    #Stats:
    elif choice =="stats":
        print(f"============\nHero: {player1.name} \nHealth: {player1.health}/{player1.maxhealth}\nLevel: {player1.level}\nEXP: {player1.xp}/{player1.xptolevel()}\nStrength: {player1.strength}\nSpeed: {player1.speed}\n============")


    #Inventory:        
    elif choice =="inventory":
        print("==========")
        print_dict_with_newlines(player1.items_dict)
        print("==========")


    #Heal:
    elif choice == "heal":
        heal = input(f"Potions: {player1.items_dict['potion']}. Current HP: {player1.health}/{player1.maxhealth}hp. Do you want to use one potion to heal 10hp? <yes/<no>: ")
        if player1.items_dict['potion'] == 0:
            print("Sorry you have no potions.")
            continue
        elif heal == "yes":
            if "potion" in player1.items_dict and player1.items_dict["potion"] > 0:
                print(f"{player1.name} used a potion!")
                player1.health = player1.health + 10
                player1.items_dict['potion'] -= 1

                if player1.health > player1.maxhealth:
                    player1.health = player1.maxhealth
                print(f"{player_name} healed 10hp, players health is now {player1.health}/{player1.maxhealth}.")
                print(f"{player_name} has {player1.items_dict['potion']} potions left.")           
        elif heal == "no":
            continue
        else:
            print("Invalid input.")
    
    
    #Exit:
    elif choice == "finish":
        break


    #Error:
    else:
        print("Invalid input.")




#Exit (will include save later.):
print("Gameover! Goodbye!")