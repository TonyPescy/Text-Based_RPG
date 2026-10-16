"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 21, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_item.py
Purpose: Utilizes unittest to test all of the classes and methods in item.py file
"""

"""
NOTE: These commands are written with the idea that they will only be called with
the correct typing or the expected correct parameters from the CLIs process command. 
As such this testing may lack certain cases. This is handled in the CLI, which is
why the CLI test file is far larger than any other test file. To avoid the extra 
redundant code in this file as well as the grid.py, we will only be looking at 
cases that can be tested without an entire refactor of all of the entire game logic.

TLDR: This will primarily test only success cases as any and all error handling of 
these functions are handled within the CLI prior to calling this function.
"""

# Imports
import unittest
import equipment
import domain_library as dl
from game_state import GameState


# Test Equipment
# Utilizes unittest to test equipment and consumable classes
class TestEquipment(unittest.TestCase):

    # Repeated Methods

    # Create Warrior
    # Creates and registers a Warrior entity for testing
    # Params: None
    # Returns: game_state, warrior - GameState and Warrior entity
    def create_warrior(self):
        # Create game state
        game_state = GameState()

        # Create game grid
        game_state.create_grid(25, 25)

        # Spawn Warrior through game state
        game_state.spawn_entity(0, 0, "warrior")

        # Get registered Warrior
        warrior = game_state.get_entity_from_list(1)

        return game_state, warrior

    # Create Mage
    # Creates and registers a Mage entity for testing
    # Params: None
    # Returns: game_state, mage - GameState and Mage entity
    def create_mage(self):
        # Create game state
        game_state = GameState()

        # Create game grid
        game_state.create_grid(25, 25)

        # Spawn Mage through game state
        game_state.spawn_entity(0, 0, "mage")

        # Get registered Mage
        mage = game_state.get_entity_from_list(1)

        return game_state, mage

    # Get Consumable
    # Retrieves a consumable from the equipment types dictionary
    # Params: name - str - Name of the consumable
    # Returns: Consumable - Consumable object
    def get_consumable(self, name):
        return equipment.create_equipment(name)

    # Use Consumable
    # Adds a consumable to the entity backpack and uses it through GameState
    # Params:   name - str - Name of the consumable
    #           entity - Entity - Entity using the consumable
    #           game_state - GameState - Current game state
    # Returns: None
    def use_consumable(self, name, entity, game_state):
        # Create consumable
        consumable = self.get_consumable(name)

        # Add consumable to entity backpack
        entity.add_item_to_backpack(consumable)

        # Use consumable through game state
        game_state.use_consumable(entity.get_info().id, name)
        # entity.update_stats(game_state)

    # Assert Base Warrior Stats
    # Checks that the Warrior has its default stats
    # Params: warrior - Warrior - Warrior entity being checked
    # Returns: None
    def assert_base_warrior_stats(self, warrior):
        self.assertEqual(warrior.attack, 15)
        self.assertEqual(warrior.defence, 10)
        self.assertEqual(warrior.speed, 5)
        self.assertEqual(warrior.max_health, 120)

    # Assert Base Mage Stats
    # Checks that the Mage has its default stats
    # Params: mage - Mage - Mage entity being checked
    # Returns: None
    def assert_base_mage_stats(self, mage):
        mage_info = mage.get_info()
        self.assertEqual(mage_info.health, 70)
        self.assertEqual(mage_info.attack, 8)
        self.assertEqual(mage_info.defence, 4)
        self.assertEqual(mage_info.speed, 5)
        self.assertEqual(mage_info.max_health, 70)
        self.assertEqual(mage_info.max_mana, 100)

    # Assert Consumable Attributes
    # Checks that a consumable has the expected attributes
    # Params:   item - Consumable - Consumable being checked
    #           name - str - Expected consumable name
    #           instant_effects - dict - Expected instant effects
    #           over_time_effects - dict - Expected over-time effects
    #           duration - int - Expected duration
    # Returns: None
    def assert_consumable_attributes(
        self, item, name, instant_effects, over_time_effects, duration
    ):
        self.assertEqual(item.name, name)
        self.assertEqual(item.slot, "Consumable")
        self.assertDictEqual(item.effects, {})
        self.assertDictEqual(item.instant_effects, instant_effects)
        self.assertDictEqual(item.over_time_effects, over_time_effects)
        self.assertEqual(item.duration, duration)

    # Assert Health Potion
    # Checks that a health potion has the expected instant health effect
    # Params:   item - Consumable - Health potion being checked
    #           name - str - Expected potion name
    #           amount - str - Expected health amount
    # Returns: None
    def assert_health_potion(self, item, name, amount):
        self.assert_consumable_attributes(
            item,
            name,
            {"Flat_modifiers": {"Health": amount}, "Percent_modifiers": {}},
            {"Flat_modifiers": {}, "Percent_modifiers": {}},
            0,
        )

    # Assert Temporary Buff
    # Checks that an entity has the expected temporary buff
    # Params:   entity - Entity - Entity being checked
    #           index - int - Index of the temporary buff
    #           name - str - Expected buff name
    #           effects - dict - Expected buff effects
    #           turns - int - Expected number of turns
    # Returns: None
    def assert_temp_buff(
        self,
        entity,
        index,
        name,
        flat_modifiers,
        percent_modifiers,
        turns,
    ):
        # Get entity info
        entity_info = entity.get_info()

        # Get temporary buff info
        temp_buff = dict(entity_info.temp_buffs[index])

        # Check buff name
        self.assertEqual(temp_buff["Name"], name)

        # Get buff effects
        effects = dict(temp_buff["Effects"])

        # Check flat modifiers
        self.assertDictEqual(
            dict(effects["Flat_modifiers"]),
            flat_modifiers["Flat_modifiers"],
        )

        # Check percent modifiers
        self.assertDictEqual(
            dict(effects["Percent_modifiers"]),
            percent_modifiers["Percent_modifiers"],
        )

        # Check remaining turns
        self.assertEqual(temp_buff["Turns"], turns)

    # Equipment Initialization Tests

    # Test Equipment Initialization
    # Checks that an Equipment object is initialized correctly
    def test_item_init(self):
        item = equipment.Equipment("test", "Weapon", {"Attack": "+10"})

        self.assertEqual(item.get_info().name, "test")
        self.assertEqual(item.get_info().slot, "Weapon")
        self.assertEqual(dict(item.get_info().effects), {"Attack": "+10"})

    # Test None Weapon Initialization
    # Checks that a NoneWeapon object is initialized correctly
    def test_none_weapon_init(self):
        item = equipment.NoneWeapon()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "None")
        self.assertEqual(item_info.slot, "Weapon")
        self.assertEqual(dict(item_info.effects), {})

    # Test None Armor Initialization
    # Checks that a NoneArmor object is initialized correctly
    def test_none_armor_init(self):
        item = equipment.NoneArmor()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "None")
        self.assertEqual(item_info.slot, "Armor")
        self.assertEqual(dict(item_info.effects), {})

    # Test None Accessory Initialization
    # Checks that a NoneAccessory object is initialized correctly
    def test_none_accessory_init(self):
        item = equipment.NoneAccessory()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "None")
        self.assertEqual(item_info.slot, "Accessory")
        self.assertEqual(dict(item_info.effects), {})

    # Test Iron Sword Initialization
    # Checks that an IronSword object is initialized correctly
    def test_iron_sword_init(self):
        item = equipment.IronSword()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "IronSword")
        self.assertEqual(item_info.slot, "Weapon")
        self.assertEqual(dict(item_info.effects), {"Attack": "+12"})

    # Test Cursed Dagger Initialization
    # Checks that a CursedDagger object is initialized correctly
    def test_cursed_dagger_init(self):
        item = equipment.CursedDagger()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "CursedDagger")
        self.assertEqual(item_info.slot, "Weapon")
        self.assertEqual(dict(item_info.effects), {"Attack": "+18", "Defence": "-5"})

    # Test Mage Staff Initialization
    # Checks that a MageStaff object is initialized correctly
    def test_mage_staff_init(self):
        item = equipment.MageStaff()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "MageStaff")
        self.assertEqual(item_info.slot, "Weapon")
        self.assertEqual(dict(item_info.effects), {"Spell_power": "+5"})

    # Test Iron Chestplate Initialization
    # Checks that an IronChestplate object is initialized correctly
    def test_iron_chestplate_init(self):
        item = equipment.IronChestplate()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "IronChestplate")
        self.assertEqual(item_info.slot, "Armor")
        self.assertEqual(dict(item_info.effects), {"Defence": "+15", "Speed": "-2"})

    # Test Leather Tunic Initialization
    # Checks that a LeatherTunic object is initialized correctly
    def test_leather_tunic_init(self):
        item = equipment.LeatherTunic()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "LeatherTunic")
        self.assertEqual(item_info.slot, "Armor")
        self.assertEqual(dict(item_info.effects), {"Defence": "+5"})

    # Test Scout Armor Initialization
    # Checks that a ScoutArmor object is initialized correctly
    def test_scout_armor_init(self):
        item = equipment.ScoutArmor()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "ScoutArmor")
        self.assertEqual(item_info.slot, "Armor")
        self.assertEqual(dict(item_info.effects), {"Defence": "+3", "Speed": "+10%"})

    # Test Ring of the Sorcerer Initialization
    # Checks that a RingOfTheSorcerer object is initialized correctly
    def test_ring_of_the_sorcerer_init(self):
        item = equipment.RingOfTheSorcerer()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "RingOfTheSorcerer")
        self.assertEqual(item_info.slot, "Accessory")
        self.assertEqual(dict(item_info.effects), {"Spell_power": "+5", "Mana": "+15%"})

    # Test Amulet of Vitality Initialization
    # Checks that an AmuletOfVitality object is initialized correctly
    def test_amulet_of_vitality_init(self):
        item = equipment.AmuletOfVitality()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "AmuletOfVitality")
        self.assertEqual(item_info.slot, "Accessory")
        self.assertEqual(dict(item_info.effects), {"Health": "+10%", "Defence": "+3"})

    # Test Ring of Haste Initialization
    # Checks that a RingOfHaste object is initialized correctly
    def test_ring_of_haste_init(self):
        item = equipment.RingOfHaste()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "RingOfHaste")
        self.assertEqual(item_info.slot, "Accessory")
        self.assertEqual(dict(item_info.effects), {"Speed": "+2"})

    # Consumable Initialization Tests

    # Test Small Health Potion Initialization
    # Checks that a SmallHealthPotion object is initialized correctly
    def test_small_health_potion_init(self):
        item = equipment.SmallHealthPotion()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "SmallHealthPotion")
        self.assertEqual(item_info.duration, 0)
        self.assertEqual(
            item_info.instant_effects,
            (("Flat_modifiers", (("Health", "20"),)), ("Percent_modifiers", ())),
        )
        self.assertEqual(
            item_info.over_time_effects,
            (("Flat_modifiers", ()), ("Percent_modifiers", ())),
        )

    # Test Greater Health Potion Initialization
    # Checks that a GreaterHealthPotion object is initialized correctly
    def test_greater_health_potion_init(self):
        item = equipment.GreaterHealthPotion()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "GreaterHealthPotion")
        self.assertEqual(item_info.duration, 0)
        self.assertEqual(
            item_info.instant_effects,
            (("Flat_modifiers", (("Health", "50"),)), ("Percent_modifiers", ())),
        )

    # Test Superior Health Potion Initialization
    # Checks that a SuperiorHealthPotion object is initialized correctly
    def test_superior_health_potion_init(self):
        item = equipment.SuperiorHealthPotion()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "SuperiorHealthPotion")
        self.assertEqual(item_info.duration, 0)
        self.assertEqual(
            item_info.instant_effects,
            (("Flat_modifiers", (("Health", "100"),)), ("Percent_modifiers", ())),
        )

    # Test Mana Potion Initialization
    # Checks that a ManaPotion object is initialized correctly
    def test_mana_potion_init(self):
        item = equipment.ManaPotion()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "ManaPotion")
        self.assertEqual(item_info.duration, 0)
        self.assertEqual(
            item_info.instant_effects,
            (("Flat_modifiers", (("Mana", "50"),)), ("Percent_modifiers", ())),
        )

    # Test Turtle Master Potion Initialization
    # Checks that a TurtleMasterPotion object is initialized correctly
    def test_turtle_master_potion_init(self):
        item = equipment.TurtleMasterPotion()
        item_info = item.get_info()

        self.assertEqual(item_info.name, "TurtleMasterPotion")
        self.assertEqual(item_info.duration, 5)
        self.assertEqual(
            item_info.instant_effects,
            (("Flat_modifiers", ()), ("Percent_modifiers", (("Health", "10"),))),
        )
        self.assertEqual(
            item_info.over_time_effects,
            (
                ("Flat_modifiers", (("Speed", "-3"), ("Defence", "10"))),
                ("Percent_modifiers", (("Health", "10"), ("Defence", "20"))),
            ),
        )

    # Consumable Use Tests

    # Test Small Health Potion Use
    # Checks that a SmallHealthPotion restores health correctly
    def test_small_health_potion_use(self):
        game_state, warrior = self.create_warrior()
        warrior.update_single_stat("health", 50)

        self.use_consumable("smallhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 70)
        # self.assert_base_warrior_stats(warrior)

    # Test Greater Health Potion Use
    # Checks that a GreaterHealthPotion restores health correctly
    def test_greater_health_potion_use(self):
        game_state, warrior = self.create_warrior()
        warrior.update_single_stat("health", 50)

        self.use_consumable("greaterhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 100)
        # self.assert_base_warrior_stats(warrior)

    # Test Superior Health Potion Use
    # Checks that a SuperiorHealthPotion restores health correctly
    def test_superior_health_potion_use(self):
        game_state, warrior = self.create_warrior()
        warrior.update_single_stat("health", 50)

        self.use_consumable("superiorhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Health Potion Above Maximum Health
    # Checks that a health potion does not restore health above the maximum
    def test_health_potion_above_max_health(self):
        game_state, warrior = self.create_warrior()
        warrior.update_single_stat("health", 110)

        self.use_consumable("greaterhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Health Potion At Maximum Health
    # Checks that a health potion does not change health when already at maximum
    def test_health_potion_at_max_health(self):
        game_state, warrior = self.create_warrior()

        self.use_consumable("smallhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Turtle Master Potion Instant Effect
    # Checks that the instant health effect is applied correctly
    def test_turtle_master_potion_instant_effect(self):
        game_state, warrior = self.create_warrior()
        warrior.update_single_stat("health", 50)

        self.use_consumable("turtlemasterpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 55)
        # self.assert_base_warrior_stats(warrior)

    # Test Turtle Master Potion At Maximum Health
    # Checks that the instant effect does not exceed maximum health
    def test_turtle_master_potion_at_max_health(self):
        game_state, warrior = self.create_warrior()

        self.use_consumable("turtlemasterpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Mana Potion Use
    # Checks that a ManaPotion restores mana correctly
    def test_mana_potion_use(self):
        game_state, mage = self.create_mage()
        mage.update_single_stat("mana", 25)

        self.use_consumable("manapotion", mage, game_state)
        mage_info = mage.get_info()
        self.assertEqual(mage_info.mana, 75)
        self.assert_base_mage_stats(mage)

    # Test Mana Potion Above Maximum Mana
    # Checks that a mana potion does not restore mana above the maximum
    def test_mana_potion_above_max_mana(self):
        game_state, mage = self.create_mage()
        mage.update_single_stat("mana", 90)

        self.use_consumable("manapotion", mage, game_state)

        mage_info = mage.get_info()
        self.assertEqual(mage_info.mana, 100)
        self.assert_base_mage_stats(mage)

    # Test Mana Potion At Maximum Mana
    # Checks that a mana potion does not change mana when already at maximum
    def test_mana_potion_at_max_mana(self):
        game_state, mage = self.create_mage()

        self.use_consumable("manapotion", mage, game_state)
        mage_info = mage.get_info()
        self.assertEqual(mage_info.mana, 100)
        self.assert_base_mage_stats(mage)

    # Temporary Buff Tests

    # Test Turtle Master Potion Temporary Buff
    # Checks that TurtleMasterPotion adds the expected temporary buff
    def test_turtle_master_potion_temporary_buff(self):
        game_state, warrior = self.create_warrior()

        self.use_consumable("turtlemasterpotion", warrior, game_state)

        self.assert_temp_buff(
            warrior,
            0,
            "TurtleMasterPotion",
            {"Flat_modifiers": {"Speed": "-3", "Defence": "10"}},
            {"Percent_modifiers": {"Health": "10", "Defence": "20"}},
            5,
        )
        warrior_info = warrior.get_info()
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Multiple Turtle Master Potion Buffs
    # Checks that using multiple potions adds multiple temporary buffs
    def test_multiple_turtle_master_potion_buffs(self):
        game_state, warrior = self.create_warrior()

        self.use_consumable("turtlemasterpotion", warrior, game_state)
        self.use_consumable("turtlemasterpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(len(warrior_info.temp_buffs), 4)

        self.assert_temp_buff(
            warrior,
            0,
            "TurtleMasterPotion",
            {"Flat_modifiers": {"Speed": "-3", "Defence": "10"}},
            {
                "Percent_modifiers": {"Health": "10", "Defence": "20"},
            },
            5,
        )

        self.assert_temp_buff(
            warrior,
            1,
            "TurtleMasterPotion",
            {"Flat_modifiers": {"Speed": "-3", "Defence": "10"}},
            {
                "Percent_modifiers": {"Health": "10", "Defence": "20"},
            },
            5,
        )

    # Test Health Potion Does Not Add Temporary Buff
    # Checks that a health potion does not create a temporary buff
    def test_health_potion_no_temporary_buff(self):
        game_state, warrior = self.create_warrior()

        self.use_consumable("smallhealthpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        self.assertEqual(len(warrior_info.temp_buffs), 0)
        self.assertEqual(warrior_info.health, 120)
        # self.assert_base_warrior_stats(warrior)

    # Test Existing Temporary Buff Is Preserved
    # Checks that using TurtleMasterPotion preserves existing buffs
    def test_existing_temporary_buff_is_preserved(self):
        game_state, warrior = self.create_warrior()

        existing_buff = {
            "Name": "ExistingBuff",
            "Effects": {"Flat_modifiers": {"Attack": "5"}, "Percent_modifiers": {}},
            "Turns": 2,
        }

        warrior.add_temp_buff(existing_buff)

        self.use_consumable("turtlemasterpotion", warrior, game_state)
        warrior_info = warrior.get_info()
        # existing buffs = 1, turtle bufff = 2
        self.assertEqual(len(warrior_info.temp_buffs), 3)

        self.assert_temp_buff(
            warrior,
            0,
            "ExistingBuff",
            existing_buff["Effects"],
            existing_buff["Effects"],
            2,
        )

        self.assert_temp_buff(
            warrior,
            1,
            "TurtleMasterPotion",
            {"Flat_modifiers": {"Speed": "-3", "Defence": "10"}},
            {
                "Percent_modifiers": {"Health": "10", "Defence": "20"},
            },
            5,
        )


# Run Unit Tests
if __name__ == "__main__":
    unittest.main()
