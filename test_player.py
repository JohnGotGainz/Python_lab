import unittest
from unittest.mock import patch
from player import Player
from player import load_inventory


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.items = [
            {"name": "Assault rifle", "type": "Weapon"},
            {"name": "Helmet", "type": "Armor"},
            {"name": "Chest armor", "type": "Armor"},
            {"name": "Leg armor", "type": "Armor"},
            {"name": "Gauntlets", "type": "Armor"},
            {"name": "Boots", "type": "Armor"},
            {"name": "Submachine gun", "type": "Weapon"},
            {"name": "Pump shotgun", "type": "Weapon"},
            {"name": "Health Potion", "type": "Consumable", "effect": "20 health"},
            {"name": "Mana Potion", "type": "Consumable", "effect": "20 mana"}
        ]

    def test_assign_loadout(self):
        player = Player("Test Player", "titan", self.items)
        self.assertTrue(any(item["name"] == "Assault rifle" for item in player.inventory))

    def test_attack(self):
        player1 = Player("Player1", "titan", self.items)
        player2 = Player("Player2", "warlock", self.items)
        damage_dealt = player1.attack(player2)
        self.assertTrue(isinstance(damage_dealt, int))

    def test_use_item(self):
        player = Player("Test Player", "titan", self.items)
        player.inventory = [{'name': 'Health Potion', 'type': 'Consumable', 'effect': '20 health'}]
        player.attributes['health'] = 50
        player.use_item(0)
        self.assertEqual(player.attributes['health'], 70)

    def test_equip_item(self):
        player = Player("Test Player", "titan", self.items)
        player.inventory = [{'name': 'Helmet', 'type': 'Armor'}]
        player.equip_item(0)
        self.assertIn({'name': 'Helmet', 'type': 'Armor'}, player.equipped_items)

    def test_display_inventory(self):
        player = Player("Test Player", "titan", self.items)
        with patch('builtins.print') as mocked_print:
            player.display_inventory()
            mocked_print.assert_called()

    def test_display_equipped_items(self):
        player = Player("Test Player", "titan", self.items)
        with patch('builtins.print') as mocked_print:
            player.display_equipped_items()
            mocked_print.assert_called()

    def test_display_attributes(self):
        player = Player("Test Player", "titan", self.items)
        with patch('builtins.print') as mocked_print:
            player.display_attributes()
            mocked_print.assert_called()

if __name__ == "__main__":
    unittest.main()
