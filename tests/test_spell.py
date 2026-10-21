"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 30, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: test_spell.py
Purpose: Houses all functions necessary for proper spell testing logic in the game
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
import domain_library as dl
import spell
from game_state import GameState


class TestSpell(unittest.TestCase):

    # Repeated Test Functions
    # Saves repeated setup code while keeping individual tests readable

    # Create Test Spell
    # Creates a generic spell for testing
    # Params: None
    # Returns: test_spell - Spell - Generic test spell
    def create_test_spell(self):
        return spell.Spell(
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

    # Create Caster And Target
    # Creates a Mage and a target entity for spell testing
    # Params: target_type - str - Type of entity to target
    # Returns: caster, target, game_state - Game state and entities used in spell tests
    def create_caster_and_target(self, target_type="Goblin"):
        # Create game state and grid
        game_state = GameState()
        game_state.create_grid(5, 5)

        # Spawn caster and target
        game_state.spawn_entity(0, 0, "Mage")
        game_state.spawn_entity(1, 0, target_type)

        # Get spawned entities
        caster = game_state.get_entity_from_list(1)
        target = game_state.get_entity_from_list(2)

        # Return game state and entities
        return caster, target, game_state

    # Create Frostbolt Effects
    # Returns the expected Frostbolt temporary effects
    # Params: None
    # Returns: effects - dict - Expected temporary effects
    def create_frostbolt_effects(self):
        return {
            "Flat_modifiers": {"Speed": -2},
            "Percent_modifiers": {},
        }

    # Calculate Expected Damage
    # Calculates expected damage from an offensive spell
    # Params: caster - Entity - Entity casting the spell
    #         target - Entity - Entity receiving the spell
    #         test_spell - Spell - Spell being cast
    # Returns: damage - float - Expected damage
    def calculate_expected_damage(self, caster, target, test_spell):
        caster_info = caster.get_info()
        target_info = target.get_info()
        spell_info = test_spell.get_info()

        return max(
            1,
            (caster_info.spell_power * spell_info.spell_power_modifier)
            - target_info.defence,
        )

    # Get Temporary Buffs
    # Converts temporary buff information into dictionaries for testing
    # Params: entity_object - Entity - Entity whose buffs are being checked
    # Returns: temp_buffs - list - Temporary buffs converted to dictionaries
    def get_temp_buffs(self, entity_object):
        # Get entity information
        entity_info = entity_object.get_info()

        # Convert each temporary buff into dictionaries
        return [dict(temp_buff) for temp_buff in entity_info.temp_buffs]

    # Assert Temporary Buff
    # Checks that a temporary buff matches the expected values
    # Params: entity_object - Entity - Entity whose buff is being checked
    #         index - int - Index of the temporary buff
    #         name - str - Expected buff name
    #         effects - dict - Expected temporary effects
    #         turns - int - Expected remaining turns
    # Returns: None
    def assert_temp_buff(self, entity_object, index, name, effects, turns):
        # Get temporary buffs
        temp_buffs = self.get_temp_buffs(entity_object)

        # Get temporary buff information
        temp_buff = temp_buffs[index]

        # Verify buff name
        self.assertEqual(temp_buff["Name"], name)

        # Convert effect information into dictionaries
        actual_effects = dict(temp_buff["Effects"])
        actual_flat_modifiers = dict(actual_effects["Flat_modifiers"])
        actual_percent_modifiers = dict(actual_effects["Percent_modifiers"])

        # Verify flat modifiers
        self.assertDictEqual(
            actual_flat_modifiers,
            effects["Flat_modifiers"],
        )

        # Verify percentage modifiers
        self.assertDictEqual(
            actual_percent_modifiers,
            effects["Percent_modifiers"],
        )

        # Verify remaining turns
        self.assertEqual(temp_buff["Turns"], turns)

    # Assert Spell Attributes
    # Checks that a spell contains the expected attributes
    # Params: test_spell - Spell - Spell being checked
    #         name - str - Expected spell name
    #         spell_type - str - Expected spell type
    #         mana_cost - int - Expected mana cost
    #         spell_range - int - Expected spell range
    #         target_type - str - Expected target type
    #         spell_power_modifier - float - Expected spell power modifier
    # Returns: None
    def assert_spell_attributes(
        self,
        test_spell,
        name,
        spell_type,
        mana_cost,
        spell_range,
        target_type,
        spell_power_modifier,
    ):
        # Get spell information
        spell_info = test_spell.get_info()

        # Verify spell attributes
        self.assertEqual(spell_info.name, name)
        self.assertEqual(spell_info.spell_type, spell_type)
        self.assertEqual(spell_info.mana_cost, mana_cost)
        self.assertEqual(spell_info.spell_range, spell_range)
        self.assertEqual(spell_info.target_type, target_type)
        self.assertEqual(
            spell_info.spell_power_modifier,
            spell_power_modifier,
        )

    # Assert Get Spell Returns
    # Checks that get_spell returns an instance of the expected spell class
    # Params: spell_name - str - Name of the spell to retrieve
    #         spell_class - class - Expected spell class
    # Returns: None
    def assert_get_spell_returns(self, spell_name, spell_class):
        # Get spell
        test_spell = spell.get_spell(spell_name)

        # Verify spell type
        self.assertIsInstance(test_spell, spell_class)

    # Spell Initialization Tests

    # Test generic spell initialization
    def test_spell_initialization(self):
        test_spell = self.create_test_spell()
        self.assert_spell_attributes(
            test_spell,
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

    # Test get_range returns the spell range
    def test_spell_get_range(self):
        test_spell = self.create_test_spell()
        self.assertEqual(test_spell.get_info().spell_range, 5)

    # Test Fireball initialization
    def test_fireball_initialization(self):
        fireball = spell.Fireball()
        self.assert_spell_attributes(
            fireball,
            "Fireball",
            dl.SpellTypes.OFFENSIVE.value,
            25,
            4,
            "Enemy",
            1.5,
        )

    # Test Heal initialization
    def test_heal_initialization(self):
        heal = spell.Heal()
        self.assert_spell_attributes(
            heal,
            "Heal",
            dl.SpellTypes.SUPPORT.value,
            30,
            2,
            "All",
            1.2,
        )

    # Test EffectSpell initialization
    def test_effect_spell_initialization(self):
        test_effects = {
            "Flat_modifiers": {"Speed": -2},
            "Percent_modifiers": {},
        }

        test_spell = spell.EffectSpell(
            "Test Effect",
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
            test_effects,
            2,
        )

        self.assert_spell_attributes(
            test_spell,
            "Test Effect",
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
        )
        self.assertEqual(test_spell.over_time_effects, test_effects)
        self.assertEqual(test_spell.duration, 2)

    # Test Frostbolt initialization
    def test_frostbolt_initialization(self):
        frostbolt = spell.Frostbolt()
        self.assert_spell_attributes(
            frostbolt,
            "Frostbolt",
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
        )
        self.assertDictEqual(
            frostbolt.over_time_effects,
            self.create_frostbolt_effects(),
        )
        self.assertEqual(frostbolt.duration, 1)

    # Offensive Spell Tests

    # Test casting an offensive spell
    def test_cast_offensive_spell(self):
        caster, target, game_state = self.create_caster_and_target()
        starting_health = target.get_info().health
        fireball = spell.Fireball()

        effect = fireball.cast_spell(caster, target, game_state)

        self.assertLess(target.get_info().health, starting_health)
        self.assertIn("Dealt", effect)
        self.assertIn(str(target.get_info().id), effect)

    # Test offensive spell damage calculation
    def test_cast_offensive_spell_returns_correct_damage(self):
        caster, target, game_state = self.create_caster_and_target()
        fireball = spell.Fireball()

        expected_damage = self.calculate_expected_damage(caster, target, fireball)
        starting_health = target.get_info().health

        fireball.cast_spell(caster, target, game_state)

        self.assertEqual(
            target.get_info().health,
            max(0, starting_health - expected_damage),
        )

    # Test offensive spell minimum damage
    def test_cast_offensive_spell_minimum_damage(self):
        caster, target, game_state = self.create_caster_and_target()
        target.update_single_stat("defence", 1000)
        fireball = spell.Fireball()
        starting_health = target.get_info().health

        fireball.cast_spell(caster, target, game_state)

        self.assertEqual(
            target.get_info().health,
            max(0, starting_health - 1),
        )

    # Test offensive spell cannot reduce health below zero
    def test_cast_offensive_spell_health_cannot_go_below_zero(self):
        caster, target, game_state = self.create_caster_and_target()
        target.update_single_stat("health", 1)
        fireball = spell.Fireball()

        fireball.cast_spell(caster, target, game_state)

        self.assertEqual(target.get_info().health, 0)

    # Test offensive spell damage message
    def test_offensive_spell_returns_damage_message(self):
        caster, target, game_state = self.create_caster_and_target()
        fireball = spell.Fireball()
        expected_damage = self.calculate_expected_damage(caster, target, fireball)

        effect = fireball.cast_spell(caster, target, game_state)

        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.get_info().id}!",
        )

    # Test offensive spell death message
    def test_offensive_spell_returns_death_message(self):
        caster, target, game_state = self.create_caster_and_target()
        target.update_single_stat("health", 1)
        fireball = spell.Fireball()
        expected_damage = self.calculate_expected_damage(caster, target, fireball)

        effect = fireball.cast_spell(caster, target, game_state)
        target_info = target.get_info()

        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target_info.id}! "
            f"{target_info.id} has died!",
        )
        self.assertFalse(target.is_alive())

    # Healing Spell Tests

    # Test casting a healing spell
    def test_cast_heal_spell(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", target.get_info().health - 20)
        damaged_health = target.get_info().health
        heal = spell.Heal()

        effect = heal.cast_spell(caster, target, game_state)

        self.assertGreater(target.get_info().health, damaged_health)
        self.assertIn("Healed", effect)
        self.assertIn(str(target.get_info().id), effect)

    # Test healing spell restores the expected amount
    def test_cast_heal_spell_correct_amount(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", target.get_info().health - 20)
        starting_health = target.get_info().health
        heal = spell.Heal()

        expected_healing = max(
            1,
            caster.get_info().spell_power * heal.get_info().spell_power_modifier,
        )
        expected_health = min(
            target.get_info().max_health,
            starting_health + expected_healing,
        )

        heal.cast_spell(caster, target, game_state)

        self.assertEqual(target.get_info().health, expected_health)

    # Test healing spell cannot exceed max health
    def test_cast_heal_spell_cannot_exceed_max_health(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat(
            "health",
            target.get_info().max_health - 1,
        )
        heal = spell.Heal()

        heal.cast_spell(caster, target, game_state)

        self.assertEqual(
            target.get_info().health,
            target.get_info().max_health,
        )

    # Test healing spell minimum healing
    def test_cast_heal_spell_minimum_healing(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        caster.update_single_stat("spell_power", 0)
        self.assertEqual(caster.get_info().spell_power, 0)

        target.update_single_stat("health", target.get_info().health - 20)
        starting_health = target.get_info().health
        heal = spell.Heal()

        heal.cast_spell(caster, target, game_state)

        self.assertEqual(
            target.get_info().health,
            min(target.get_info().max_health, starting_health + 1),
        )

    # Test healing a dead entity does not revive it
    def test_heal_dead_entity_does_not_revive(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", 0)
        target.handle_death()
        self.assertFalse(target.is_alive())

        heal = spell.Heal()
        heal.cast_spell(caster, target, game_state)

        self.assertFalse(target.is_alive())

    # Test healing a dead entity does not restore health
    def test_heal_dead_entity_does_not_restore_health(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", 0)
        target.handle_death()

        heal = spell.Heal()
        heal.cast_spell(caster, target, game_state)

        self.assertEqual(target.get_info().health, 0)

    # Test healing a dead entity does not remove its dead status
    def test_heal_dead_entity_does_not_remove_dead_status(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", 0)
        target.handle_death()

        heal = spell.Heal()
        heal.cast_spell(caster, target, game_state)

        self.assertFalse(target.is_alive())
        temp_buffs = self.get_temp_buffs(target)
        self.assertTrue(any(temp_buff["Name"] == "Dead" for temp_buff in temp_buffs))

    # Test healing an alive entity returns the healed message
    def test_heal_alive_entity_returns_healed_message(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", target.get_info().health - 20)
        heal = spell.Heal()

        expected_healing = max(
            1,
            caster.get_info().spell_power * heal.get_info().spell_power_modifier,
        )
        expected_healing = min(
            expected_healing,
            target.get_info().max_health - target.get_info().health,
        )

        effect = heal.cast_spell(caster, target, game_state)

        self.assertEqual(
            effect,
            f"Healed {target.get_info().id} for {int(expected_healing)} health!",
        )

    # Test healing a dead entity returns the dead message
    def test_heal_dead_entity_returns_dead_message(self):
        caster, target, game_state = self.create_caster_and_target("Warrior")
        target.update_single_stat("health", 0)
        target.handle_death()
        heal = spell.Heal()

        effect = heal.cast_spell(caster, target, game_state)

        self.assertEqual(
            effect,
            f"Healed {target.get_info().id} for 0 health! - Cannot heal a dead entity!",
        )

    # Temporary Effect Spell Tests

    # Test casting a spell without a temporary effect
    def test_cast_spell_without_over_time_effect(self):
        caster, target, game_state = self.create_caster_and_target()
        fireball = spell.Fireball()

        self.assertEqual(len(self.get_temp_buffs(target)), 0)

        effect = fireball.cast_spell(caster, target, game_state)

        self.assertEqual(len(self.get_temp_buffs(target)), 0)
        self.assertIn("Dealt", effect)
        self.assertNotIn("Applied", effect)

    # Test casting a spell with a temporary effect
    def test_cast_spell_with_over_time_effect(self):
        caster, target, game_state = self.create_caster_and_target()
        frostbolt = spell.Frostbolt()

        effect = frostbolt.cast_spell(caster, target, game_state)

        self.assertEqual(len(self.get_temp_buffs(target)), 1)
        self.assert_temp_buff(
            target,
            0,
            frostbolt.get_info().name,
            frostbolt.over_time_effects,
            frostbolt.duration,
        )
        self.assertIn("Dealt", effect)
        self.assertIn("Applied", effect)

    # Test Frostbolt deals damage and applies its effect
    def test_frostbolt_deals_damage_and_applies_effect(self):
        caster, target, game_state = self.create_caster_and_target()
        starting_health = target.get_info().health
        frostbolt = spell.Frostbolt()
        expected_damage = self.calculate_expected_damage(caster, target, frostbolt)

        frostbolt.cast_spell(caster, target, game_state)

        self.assertEqual(
            target.get_info().health,
            max(0, starting_health - expected_damage),
        )
        self.assertEqual(len(self.get_temp_buffs(target)), 1)

    # Test EffectSpell returns damage and effect message
    def test_effect_spell_returns_damage_and_effect_message(self):
        caster, target, game_state = self.create_caster_and_target()
        frostbolt = spell.Frostbolt()
        expected_damage = self.calculate_expected_damage(caster, target, frostbolt)

        effect = frostbolt.cast_spell(caster, target, game_state)

        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.get_info().id}! "
            f"Applied {frostbolt.get_info().name} effect to {target.get_info().id}!",
        )

    # Test EffectSpell returns damage, effect, and death message
    def test_effect_spell_returns_damage_effect_and_death_message(self):
        caster, target, game_state = self.create_caster_and_target()
        target.update_single_stat("health", 1)
        frostbolt = spell.Frostbolt()
        expected_damage = self.calculate_expected_damage(caster, target, frostbolt)

        effect = frostbolt.cast_spell(caster, target, game_state)

        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.get_info().id}! "
            f"Applied {frostbolt.get_info().name} effect to {target.get_info().id}! "
            f"{target.get_info().id} has died!",
        )
        self.assertFalse(target.is_alive())

    # Test EffectSpell applies its temporary effect
    def test_effect_spell_applies_temporary_effect(self):
        caster, target, game_state = self.create_caster_and_target()
        frostbolt = spell.Frostbolt()

        frostbolt.cast_spell(caster, target, game_state)

        self.assertEqual(len(self.get_temp_buffs(target)), 1)
        self.assert_temp_buff(
            target,
            0,
            frostbolt.get_info().name,
            frostbolt.over_time_effects,
            frostbolt.duration,
        )

    # Get Spell Tests

    # Test get_spell returns Fireball
    def test_get_spell_returns_fireball(self):
        self.assert_get_spell_returns("Fireball", spell.Fireball)

    # Test get_spell returns Heal
    def test_get_spell_returns_heal(self):
        self.assert_get_spell_returns("Heal", spell.Heal)

    # Test get_spell returns Frostbolt
    def test_get_spell_returns_frostbolt(self):
        self.assert_get_spell_returns("Frostbolt", spell.Frostbolt)

    # Test get_spell is case-insensitive
    def test_get_spell_name_is_case_insensitive(self):
        self.assert_get_spell_returns("fireball", spell.Fireball)
        self.assert_get_spell_returns("HEAL", spell.Heal)
        self.assert_get_spell_returns("fRoStBoLt", spell.Frostbolt)

    # Test get_spell raises ValueError for an invalid spell
    def test_get_spell_with_invalid_spell(self):
        with self.assertRaises(ValueError):
            spell.get_spell("NotASpell")

    # Test get_spell raises ValueError for an empty name
    def test_get_spell_with_empty_name(self):
        with self.assertRaises(ValueError):
            spell.get_spell("")


if __name__ == "__main__":
    unittest.main()
