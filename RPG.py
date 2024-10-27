#setup:
#packages
import random
import pandas as pd
import os
import time
from colorama import Fore, Back, Style, init
init()

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

#Level Up
def level_up(player_name, player_xp, player_xptolevel, player_level, player_health, player_maxhealth, player_strength, player_speed):
    while player_xp >= player_xptolevel:
        player_xp -= player_xptolevel
        player_level += 1
        player_health += 5
        player_maxhealth += 5
        player_strength += 1
        player_speed += 1
        print(Fore.GREEN + f"{player_name}" + Fore.WHITE +" is now " + Fore.YELLOW +f"[level {player_level}]" + Fore.WHITE +"! Exp needed for " + Fore.YELLOW + f"level {player_level+1}" + Fore.WHITE + f": {player_xptolevel}exp. " + Fore.YELLOW + f"Current exp: " + Fore.WHITE + f"{player_xp}exp.")
    return player_xp, player_level, player_health, player_maxhealth, player_strength, player_speed

#Combat system.
def combat(player_name, player_health, player_maxhealth, player_strength, player_speed, enemy_name, enemy_health, enemy_maxhealth, enemy_strength, enemy_speed, items_dict):
    print(Fore.GREEN + f"{player_name} " + Fore.WHITE + f"encountered a " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ", health: " + Fore.RED + f"{enemy_health}/{enemy_maxhealth}" + Fore.WHITE +"!")


    #Escape
    while True:
        attack = input(f"What will you do? " + Fore.RED +"<engage/escape>"+ Fore.WHITE + ": ").lower()
        if attack == "escape":
        #RNG
            rng1 = random.uniform(0,1)
        #Success
            if rng1 >= 0.8:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE +"got away safely!")
                return player_health, True, items_dict
                
        #Fail
            else:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE +"failed to run away! The "+ Fore.MAGENTA +f"{enemy_name} "+ Fore.WHITE + "attacks " + Fore.GREEN + f"{player_name} " + Fore.WHITE +"anyways!")
                break

        elif attack == "engage":
            break
        else:
            print("Invalid input.")

    #While one opponent is still alive...
    while player_health > 0 and enemy_health > 0:
        attack = input(f"What will you do? " + Fore.RED + "<attack/item>" + Fore.WHITE +": ").lower()
        
        #Item:
        if attack == "item":
            remove_zero_quantity_items(items_dict)
            print_dict_with_newlines(items_dict)
            item = input("Which " + Fore.YELLOW +"item " + Fore.WHITE +"would you like to use? "+ Fore.RED +"<c to cancel>" + Fore.WHITE +": ")


            #Potion:
            if item == "potion":

                #If potion is in inventory and potions are greater than 0:
                if "potion" in items_dict and items_dict["potion"] > 0:

                    #Heal:
                    print(Fore.GREEN + f"{player_name} " + Fore.WHITE +"used a " + Fore.YELLOW +"potion" + Fore.WHITE + "!")
                    player_health = player_health + 10
                    items_dict['potion'] -= 1
                    #If players health exceeds maxhealth after heal:
                    if player_health > player_maxhealth:
                        player_health = player_maxhealth
                    print(Fore.GREEN + f"{player_name} "+ Fore.WHITE + "healed 10hp, "+ Fore.GREEN+ f"{player_name}s " + Fore.WHITE +"health is now: " + Fore.RED + f"{player_health}/{player_maxhealth}" + Fore.WHITE + ".")
                    print(f"{player_name} now has {items_dict['potion']} " + Fore.YELLOW + "potions" + Fore.WHITE + ".")


                    #combat:
                    enemy_damage = round(enemy_strength*random.uniform(0,1))
                    #Enemy Miss:
                    if enemy_damage == 0:
                        time.sleep(1)
                        print(Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE +"missed!")

                    #Enemy Hit:
                    else:
                        time.sleep(1)
                        print("The " + Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE+ "delt " + Fore.RED + f"{enemy_damage} " + Fore.WHITE +"damage to " + Fore.GREEN +f"{player_name}" + Fore.WHITE + ".")
                        player_health = player_health - enemy_damage

                    #Player Death
                    if player_health <= 0:
                        time.sleep(1)
                        print("Your health is 0.")
                        time.sleep(1)
                        print(f"Oh no! " + Fore.GREEN + f"{player_name} " + Fore.WHITE+ "was slain by the " + Fore.MAGENTA+ f"{enemy_name}" + Fore.WHITE+ ".")
                        return player_health, False, items_dict


                    #Player Health Update  
                    else:
                        time.sleep(1)
                        print(Fore.GREEN + f"{player_name}s " + Fore.WHITE + "health is " + Fore.RED +  f"{player_health}/{player_maxhealth}" + Fore.WHITE + ".")
                        print("")
                    continue

                #No potions:
                else:
                    print("You have no " + Fore.YELLOW +"potions" + Fore.WHITE+ ".")
                    continue

            #Cancel
            if item == "c":
                continue

            #invalid input:
            else:
                print("This item is not in your inventory.")
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
                print(Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE + "missed!")

            #Enemy Hit:
            else:
                time.sleep(1)
                print("The " + Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE + "delt " + Fore.RED + f"{enemy_damage} " + Fore.WHITE + "damage to " + Fore.GREEN + f"{player_name}" + Fore.WHITE + ".")
                player_health = player_health - enemy_damage

            #Player death:
            if player_health <= 0:
                time.sleep(1)
                print("Your health is 0.")
                time.sleep(1)
                print(f"Oh no! " + Fore.GREEN + f"{player_name} " + Fore.WHITE + "was slain by the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                return player_health, False, items_dict

            #Player Health Update
            else:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name}s " + Fore.WHITE + "health is " + Fore.RED + f"{player_health}/{player_maxhealth}" + Fore.WHITE + ".")
                print("")

            #Player miss:
            if damage == 0:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "missed!")

            #Player Hit:
            else:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "delt " + Fore.RED + f"{damage} " + Fore.WHITE + "damage to the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                enemy_health = enemy_health - damage

            #Enemy death:
            if enemy_health <= 0:
                time.sleep(1)
                print("The enemies health is 0.")
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "killed the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                return player_health, False, items_dict

            #Enemy Health Update:
            else:
                time.sleep(1)
                print("The " + Fore.MAGENTA + f"{enemy_name}s " + Fore.WHITE + "health is " + Fore.RED + f"{enemy_health}/{enemy_maxhealth}" + Fore.WHITE + ".")
                print("")
                time.sleep(1)


        #Player is faster than enemy:
        else:

            #Player miss:
            if damage == 0:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "missed!")

            #Player Hit:
            else:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "delt " + Fore.RED + f"{damage} " + Fore.WHITE + "damage to the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                enemy_health = enemy_health - damage

            #Enemy death:
            if enemy_health <= 0:
                time.sleep(1)
                print("The enemies health is 0.")
                time.sleep(1)
                print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "killed the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                return player_health, False, items_dict

            #Enemy Health Update:
            else:
                time.sleep(1)
                print("The " + Fore.MAGENTA + f"{enemy_name}s " + Fore.WHITE + "health is " + Fore.RED + f"{enemy_health}/{enemy_maxhealth}" + Fore.WHITE + ".")
                print("")
                time.sleep(1)

            #Enemy miss:
            if enemy_damage == 0:
                time.sleep(1)
                print(Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE + "missed!")

            #Enemy Hit:
            else:
                time.sleep(1)
                print("The " + Fore.MAGENTA + f"{enemy_name} " + Fore.WHITE + "delt " + Fore.RED + f"{enemy_damage} " + Fore.WHITE + "damage to " + Fore.GREEN + f"{player_name}" + Fore.WHITE + ".")
                player_health = player_health - enemy_damage

            #Player Death:
            if player_health <= 0:
                time.sleep(1)
                print("Your health is 0.")
                time.sleep(1)
                print(f"Oh no! " + Fore.GREEN + f"{player_name} " + Fore.WHITE + "was slain by the " + Fore.MAGENTA + f"{enemy_name}" + Fore.WHITE + ".")
                return player_health, False, items_dict

            #Player Health Update:
            else:
                time.sleep(1)
                print(Fore.GREEN + f"{player_name}s " + Fore.WHITE + "health is " + Fore.RED + f"{player_health}/{player_maxhealth}" + Fore.WHITE + ".")
                print("")


#Remove inventory items with 0:
def remove_zero_quantity_items(items_dict):
    keys_to_remove = [key for key, value in items_dict.items() if value == 0]

    for key in keys_to_remove:
        del items_dict[key]

    return items_dict

#Inventory formatting:
def print_dict_with_newlines(items_dict):
    for key, value in items_dict.items():

        print(Fore.YELLOW + f"{key}: " + Fore.WHITE+f"{value}")

#Game:
#Intro:
player_name = input(Fore.WHITE + "What is your " + Fore.GREEN + "characters name"+ Fore.WHITE+"?: ")
starting_items = {'potion':3,'gold':50}
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
    choice = input(Fore.WHITE + "What would you like to do?" + Fore.RED + " <combat/stats/inventory/finish>" + Fore.WHITE + ": ").lower()

    #Combat:
    if choice == "combat":

        #Combat:
        zone1monster.generate(zone1monsters)        
        player1.health,escaped,player1.items_dict = combat(player1.name, player1.health, player1.maxhealth, player1.strength, player1.speed, zone1monster.name, zone1monster.health, zone1monster.maxhealth, zone1monster.strength, zone1monster.speed, player1.items_dict)
        print(f"{player1.name}s current health is {player1.health}/{player1.maxhealth}")

        #If did not run:
        if not escaped and player1.health > 0:

            #Money and drops
            coins = random.choices(zone1coinvalues, weights = zone1coinweights, k=1)[0]
            zone1loot.generate(zone1loots, coins, player1.items_dict)
            remove_zero_quantity_items(player1.items_dict)

            #Exp gain:
            player1.xp = xp_gain(
                player1.name, 
                player1.level, 
                player1.xp, 
                player1.xptolevel(), 
                zone1monster.xp)
                
            #Level Up:
            player1.xp, player1.level,player1.health,player1.maxhealth,player1.strength,player1.speed = level_up(
                player1.name, 
                player1.xp, 
                player1.xptolevel(), 
                player1.level, 
                player1.health, 
                player1.maxhealth, 
                player1.strength, 
                player1.speed)



    #Stats:
    elif choice =="stats":
        print("")
        print(Fore.BLUE + f"============" + Fore.GREEN +f"\nHero" + Fore.WHITE + f": {player1.name} "+ Fore.RED +f"\nHealth" + Fore.WHITE + f": {player1.health}/{player1.maxhealth}" + Fore.YELLOW +f"\nLevel"+ Fore.WHITE+ f": {player1.level}"+ Fore.YELLOW + f"\nEXP" + Fore.WHITE +f": {player1.xp}/{player1.xptolevel()}\n"+ Fore.MAGENTA + f"Strength" + Fore.WHITE +f": {player1.strength}\n"+ Fore.CYAN + f"Speed" + Fore.WHITE +f": {player1.speed}" + Fore.BLUE +"\n============" + Fore.WHITE)
        print("")


    #Inventory:        
    elif choice =="inventory":
        while True:
            remove_zero_quantity_items(player1.items_dict)
            #Show inventory:
            print("")
            print(Fore.BLUE + "=========="+ Fore.WHITE)
            print_dict_with_newlines(player1.items_dict)
            print(Fore.BLUE + "==========" + Fore.WHITE)
            #Item selection:
            print("")
            time.sleep(1)
            item = input("What " + Fore.YELLOW + "item" + Fore.WHITE + " would you like to use? " + Fore.RED + "<c to cancel>" + Fore.WHITE + ": ")

            #Potion
            if item == "potion":
                if "potion" in player1.items_dict and player1.items_dict["potion"] > 0:
                    print(Fore.GREEN + f"{player1.name} " + Fore.WHITE +"used a " + Fore.YELLOW + "potion"+ Fore.WHITE + "!")
                    time.sleep(1)
                    player1.health = player1.health + 10
                    player1.items_dict['potion'] -= 1

                    if player1.health > player1.maxhealth:
                        player1.health = player1.maxhealth
                    print(Fore.GREEN + f"{player_name} " + Fore.WHITE + "healed " + Fore.RED + "10hp" + Fore.WHITE +", " + Fore.GREEN + f"{player_name} " + Fore.WHITE+"health is now " + Fore.RED + f"{player1.health}/{player1.maxhealth}"+ Fore.WHITE+ ".")
                    time.sleep(1)
                else:
                    print("That item is not in your inventory. ")    
        
        #Cancel
            elif item == "c":
                break
        
        #Error
            else:
                print("That item is not in your inventory. ")

    
    #Exit:
    elif choice == "finish":
        break


    #Error:
    else:
        print("Invalid input.")




#Exit (will include save later.):