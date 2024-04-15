import json
import random

class Player:
    def __init__(self, name, player_type, items):
        self.name = name
        self.player_type = player_type
        self.inventory = []
        self.equipped_items = []
        self.attributes = {
            'health': 100,
            'damage': 10,
            'armor': 5
        }
        self.items = items
        self.assign_loadout()

    def assign_loadout(self):
        # Dictionary mapping player types to item types
        loadouts = {
            'titan': ['Assault rifle', 'Helmet', 'Chest armor', 'Leg armor', 'Gauntlets', 'Boots'],
            'warlock': ['Submachine gun', 'Helmet', 'Chest armor', 'Leg armor', 'Gauntlets', 'Boots'],
            'hunter': ['Pump shotgun', 'Helmet', 'Chest armor', 'Leg armor', 'Gauntlets', 'Boots'],
            'demigod': ['Assault rifle', 'Helmet', 'Chest armor', 'Leg armor', 'Gauntlets', 'Boots']
        }

        # Assigning loadout based on player type
        if self.player_type.lower() in loadouts:
            self.inventory = [item for item in self.items if item["name"] in loadouts[self.player_type.lower()]]
            # Add a random consumable item to the inventory
            consumables = [item for item in self.items if item['type'] == 'Consumable']
            self.inventory.append(random.choice(consumables))

    def attack(self, other_player):
        damage_dealt = random.randint(1, 10) * self.attributes['damage']
        damage_dealt -= other_player.attributes['armor']
        other_player.attributes['health'] -= damage_dealt
        return damage_dealt

    def use_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if 'effect' in item:
                if 'health' in item['effect']:
                    self.attributes['health'] += int(item['effect'].split()[0])
                if 'armor' in item['effect']:
                    self.attributes['armor'] += int(item['effect'].split()[0])
            del self.inventory[item_index]
            return True
        else:
            return False

    def equip_item(self, item_index):
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if 'type' in item and item['type'] == 'Armor':
                self.equipped_items.append(item)
                self.inventory.pop(item_index)
                print(f"{item['name']} equipped successfully.")
                return True
            else:
                print("Cannot equip this item.")
                return False
        else:
            print("Invalid item index.")
            return False

    def display_inventory(self):
        print(f"{self.name}'s Inventory:")
        for i, item in enumerate(self.inventory):
            print(f"{i + 1}. {item['name']}")
            if 'description' in item:
                print("  Description:", item['description'])
            if 'effect' in item:
                print("  Effect:", item['effect'])
            print()

    def display_equipped_items(self):
        print(f"{self.name}'s Equipped Items:")
        for item in self.equipped_items:
            print(f"- {item['name']}")

    def display_attributes(self):
        print(f"{self.name}'s Attributes:")
        for attr, value in self.attributes.items():
            print(f"{attr.capitalize()}: {value}")
        print()


def load_inventory(file_path):
    with open(file_path, 'r') as file:
        inventory = json.load(file)
    return inventory

def main():
    # Load inventory from JSON file
    inventory_file = "ValuedItems.json"
    try:
        items = load_inventory(inventory_file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from '{inventory_file}': {e.msg}")
        print("Exiting game.")
        return

    print("Welcome to Player vs Player Game!\n")

    while True:
        player1_name = input("Enter main character's name: ")
        while True:
            player1_type = input("Enter main character's type (titan, warlock, hunter, demigod): ")
            if player1_type in ['titan', 'warlock', 'hunter', 'demigod']:  
                break
            else:
                print("Invalid character type.")
        player1 = Player(player1_name, player1_type, items)

        player2_name = input("\nEnter Player 2's name: ")
        while True:
            player2_type = input("Enter Player 2's type (titan, warlock, hunter, demigod): ")
            if player2_type in ['titan', 'warlock', 'hunter', 'demigod']:
                break
            else:
                print("Invalid character type.")
        player2 = Player(player2_name, player2_type, items)

        print("\nPlayers created!\n")

        while player1.attributes['health'] > 0 and player2.attributes['health'] > 0:
            print(f"{player1.name}'s turn:")
            print("1. Attack")
            print("2. Use Item")
            print("3. Equip Item")
            print("4. Display Inventory")
            print("5. Display Equipped Items")
            print("6. Display Attributes")
            print("7. End Turn")
            choice = input("Enter your choice: ")
            if choice == '1':
                damage_dealt = player1.attack(player2)
                print(f"{player1.name} attacked {player2.name} and dealt {damage_dealt} damage.")
            elif choice == '2':
                player1.display_inventory()
                item_index = int(input("Enter the index of the item you want to use (1, 2, 3, ...): ")) - 1
                if player1.use_item(item_index):
                    print("Item used successfully.")
                else:
                    print("Invalid item index. Please try again.")
            elif choice == '3':
                player1.display_inventory()
                item_index = int(input("Enter the index of the item you want to equip (1, 2, 3, ...): ")) - 1
                player1.equip_item(item_index)
            elif choice == '4':
                player1.display_inventory()
                input("Press Enter.")
            elif choice == '5':
                player1.display_equipped_items()
                input("Press Enter.")
            elif choice == '6':
                player1.display_attributes()
                input("Press Enter.")
            elif choice == '7':
                print("Ending turn.")
                break
            else:
                print("Invalid choice. Please try again.")

            print(f"{player2.name}'s turn:")
            print("1. Attack")
            print("2. Use Item")
            print("3. Equip Item")
            print("4. Display Inventory")
            print("5. Display Equipped Items")
            print("6. Display Attributes")
            print("7. End Turn")
            choice = input("Enter your choice: ")
            if choice == '1':
                damage_dealt = player2.attack(player1)
                print(f"{player2.name} attacked {player1.name} and dealt {damage_dealt} damage.")
            elif choice == '2':
                player2.display_inventory()
                item_index = int(input("Enter the index of the item you want to use (1, 2, 3, ...): ")) - 1
                if player2.use_item(item_index):
                    print("Item used successfully.")
                else:
                    print("Invalid item index. Please try again.")
            elif choice == '3':
                player2.display_inventory()
                item_index = int(input("Enter the index of the item you want to equip (1, 2, 3, ...): ")) - 1
                player2.equip_item(item_index)
            elif choice == '4':
                player2.display_inventory()
                input("Press Enter.")
            elif choice == '5':
                player2.display_equipped_items()
                input("Press Enter.")
            elif choice == '6':
                player2.display_attributes()
                input("Press Enter.")
            elif choice == '7':
                print("Ending turn.")
                break
            else:
                print("Invalid choice. Please try again.")

        print("\nGame Over!")
        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != 'yes':
            print("Thank you for playing!")
            break

if __name__ == "__main__":
    main()