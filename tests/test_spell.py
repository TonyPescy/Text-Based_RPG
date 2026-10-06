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

# imports
import unittest
import entity
import domain_library as dl
import spell


class TestSpell(unittest.TestCase):

    # Repeated Test Functions
    # Saves repeated setup code while keeping individual tests readable

    # Create a generic test spell
    def create_test_spell(self):
        return spell.Spell(
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

    # Create a caster and target for spell tests
    def create_caster_and_target(self, target_type="Goblin"):
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity(target_type, 1, 0, 1)

        return caster, target

    # Create the expected Frostbolt effects
    def create_frostbolt_effects(self):
        return {
            "Flat_modifiers": {"Speed": -2},
            "Percent_modifiers": {},
        }

    # Calculate expected offensive spell damage
    def calculate_expected_damage(self, caster, target, test_spell):
        return max(
            1,
            ((caster.spell_power * test_spell.spell_power_modifier) - target.defence),
        )

    # Verify common spell attributes
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
        self.assertEqual(test_spell.name, name)
        self.assertEqual(test_spell.spell_type, spell_type)
        self.assertEqual(test_spell.mana_cost, mana_cost)
        self.assertEqual(test_spell.spell_range, spell_range)
        self.assertEqual(test_spell.target_type, target_type)
        self.assertEqual(
            test_spell.spell_power_modifier,
            spell_power_modifier,
        )

    # Verify a spell dictionary entry
    def assert_spell_dictionary_entry(self, spell_name, spell_class):
        self.assertIn(spell_name, spell.SPELLS)
        self.assertEqual(
            spell.SPELLS[spell_name],
            spell_class,
        )

    # Verify get_spell returns the expected spell type
    def assert_get_spell_returns(self, spell_name, spell_class):
        test_spell = spell.get_spell(spell_name)

        self.assertIsInstance(
            test_spell,
            spell_class,
        )

    # Spell initialization
    # Tests that a generic Spell correctly assigns all provided attributes
    def test_spell_initialization(self):

        # Create test spell
        test_spell = self.create_test_spell()

        # Verify spell attributes
        self.assert_spell_attributes(
            test_spell,
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

    # success
    def test_spell_get_range(self):

        # Create test spell
        test_spell = self.create_test_spell()

        # Get spell range
        spell_range = test_spell.get_range()

        # Verify spell range
        self.assertEqual(spell_range, 5)

    # success
    def test_fireball_initialization(self):

        # Create Fireball
        fireball = spell.Fireball()

        # Verify Fireball attributes
        self.assert_spell_attributes(
            fireball,
            dl.SpellNames.FIREBALL.value,
            dl.SpellTypes.OFFENSIVE.value,
            25,
            4,
            "Enemy",
            1.5,
        )

    # success
    def test_heal_initialization(self):

        # Create Heal
        heal = spell.Heal()

        # Verify Heal attributes
        self.assert_spell_attributes(
            heal,
            dl.SpellNames.HEAL.value,
            dl.SpellTypes.SUPPORT.value,
            30,
            2,
            "All",
            1.2,
        )

    # success
    def test_effect_spell_initialization(self):

        # Create test effects
        test_effects = {
            "Flat_modifiers": {"Speed": -2},
            "Percent_modifiers": {},
        }

        # Create EffectSpell
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

        # Verify inherited attributes
        self.assert_spell_attributes(
            test_spell,
            "Test Effect",
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
        )

        # Verify EffectSpell attributes
        self.assertEqual(
            test_spell.over_time_effects,
            test_effects,
        )
        self.assertEqual(test_spell.duration, 2)

    # success
    def test_frostbolt_initialization(self):

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Verify Frostbolt attributes
        self.assert_spell_attributes(
            frostbolt,
            dl.SpellNames.FROSTBOLT.value,
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
        )

        # Verify Frostbolt effects
        self.assertEqual(
            frostbolt.over_time_effects,
            self.create_frostbolt_effects(),
        )
        self.assertEqual(frostbolt.duration, 1)

    # success
    def test_cast_offensive_spell(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Store target's starting health
        starting_health = target.health

        # Create Fireball
        fireball = spell.Fireball()

        # Cast Fireball
        effect = fireball.cast_spell(caster, target)

        # Verify target took damage
        self.assertLess(target.health, starting_health)

        # Verify effect message
        self.assertIn("Dealt", effect)
        self.assertIn(str(target.id), effect)

    # success
    def test_cast_offensive_spell_returns_correct_damage(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Fireball
        fireball = spell.Fireball()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            fireball,
        )

        # Store target's starting health
        starting_health = target.health

        # Cast Fireball
        fireball.cast_spell(caster, target)

        # Verify exact damage
        self.assertEqual(
            target.health,
            max(0, starting_health - expected_damage),
        )

    # success
    def test_cast_offensive_spell_minimum_damage(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Give target extremely high defence
        target.defence = 1000

        # Create Fireball
        fireball = spell.Fireball()

        # Store target's starting health
        starting_health = target.health

        # Cast Fireball
        fireball.cast_spell(caster, target)

        # Verify minimum damage of 1
        self.assertEqual(
            target.health,
            starting_health - 1,
        )

    # success
    def test_cast_offensive_spell_health_cannot_go_below_zero(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Give target very low health
        target.health = 1

        # Create Fireball
        fireball = spell.Fireball()

        # Cast Fireball
        fireball.cast_spell(caster, target)

        # Verify health stops at zero
        self.assertEqual(target.health, 0)

    # success
    def test_cast_heal_spell(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Damage target before healing
        target.health -= 20

        # Store damaged health
        damaged_health = target.health

        # Create Heal
        heal = spell.Heal()

        # Cast Heal
        effect = heal.cast_spell(caster, target)

        # Verify target healed
        self.assertGreater(target.health, damaged_health)

        # Verify effect message
        self.assertIn("Healed", effect)
        self.assertIn(str(target.id), effect)

    # success
    def test_cast_heal_spell_correct_amount(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Damage target
        target.health -= 20

        # Store damaged health
        starting_health = target.health

        # Create Heal
        heal = spell.Heal()

        # Calculate expected healing
        expected_healing = max(
            1,
            caster.spell_power * heal.spell_power_modifier,
        )

        # Cast Heal
        heal.cast_spell(caster, target)

        # Calculate expected final health
        expected_health = min(
            target.max_health,
            starting_health + expected_healing,
        )

        # Verify health
        self.assertEqual(
            target.health,
            expected_health,
        )

    # success
    def test_cast_heal_spell_cannot_exceed_max_health(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Set target below maximum health
        target.health = target.max_health - 1

        # Create Heal
        heal = spell.Heal()

        # Cast Heal
        heal.cast_spell(caster, target)

        # Verify health does not exceed maximum
        self.assertEqual(
            target.health,
            target.max_health,
        )

    # success
    def test_cast_heal_spell_minimum_healing(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Set caster spell power extremely low
        caster.spell_power = 0

        # Damage target
        target.health -= 20

        # Store damaged health
        starting_health = target.health

        # Create Heal
        heal = spell.Heal()

        # Cast Heal
        heal.cast_spell(caster, target)

        # Verify minimum healing of 1
        self.assertEqual(
            target.health,
            starting_health + 1,
        )

    # success
    def test_cast_spell_without_over_time_effect(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Fireball
        fireball = spell.Fireball()

        # Verify target starts with no temporary buffs
        self.assertEqual(target.temp_buffs, [])

        # Cast Fireball
        effect = fireball.cast_spell(caster, target)

        # Verify no temporary effect was added
        self.assertEqual(target.temp_buffs, [])

        # Verify normal damage message
        self.assertIn("Dealt", effect)
        self.assertNotIn("Applied", effect)

    # success
    def test_cast_spell_with_over_time_effect(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Cast Frostbolt
        effect = frostbolt.cast_spell(caster, target)

        # Verify temporary buff was added
        self.assertEqual(len(target.temp_buffs), 1)

        # Verify temporary buff contents
        self.assertEqual(
            target.temp_buffs[0]["Name"],
            frostbolt.name,
        )
        self.assertEqual(
            target.temp_buffs[0]["Effects"],
            frostbolt.over_time_effects,
        )
        self.assertEqual(
            target.temp_buffs[0]["Turns"],
            frostbolt.duration,
        )

        # Verify effect message
        self.assertIn("Dealt", effect)
        self.assertIn("Applied", effect)

    # success
    def test_frostbolt_deals_damage_and_applies_effect(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Store target's starting health
        starting_health = target.health

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            frostbolt,
        )

        # Cast Frostbolt
        frostbolt.cast_spell(caster, target)

        # Verify damage
        self.assertEqual(
            target.health,
            max(0, starting_health - expected_damage),
        )

        # Verify effect was added
        self.assertEqual(len(target.temp_buffs), 1)

    # success
    def test_spell_dictionary_contains_all_spells(self):

        # Verify Fireball exists
        self.assert_spell_dictionary_entry(
            dl.SpellNames.FIREBALL.value,
            spell.Fireball,
        )

        # Verify Heal exists
        self.assert_spell_dictionary_entry(
            dl.SpellNames.HEAL.value,
            spell.Heal,
        )

        # Verify Frostbolt exists
        self.assert_spell_dictionary_entry(
            dl.SpellNames.FROSTBOLT.value,
            spell.Frostbolt,
        )

    # success
    def test_spell_dictionary_returns_correct_fireball_class(self):

        # Verify Fireball class
        self.assert_spell_dictionary_entry(
            dl.SpellNames.FIREBALL.value,
            spell.Fireball,
        )

    # success
    def test_spell_dictionary_returns_correct_heal_class(self):

        # Verify Heal class
        self.assert_spell_dictionary_entry(
            dl.SpellNames.HEAL.value,
            spell.Heal,
        )

    # success
    def test_spell_dictionary_returns_correct_frostbolt_class(self):

        # Verify Frostbolt class
        self.assert_spell_dictionary_entry(
            dl.SpellNames.FROSTBOLT.value,
            spell.Frostbolt,
        )

    # success
    def test_get_spell_returns_fireball(self):

        # Get Fireball
        self.assert_get_spell_returns(
            "Fireball",
            spell.Fireball,
        )

    # success
    def test_get_spell_returns_heal(self):

        # Get Heal
        self.assert_get_spell_returns(
            "Heal",
            spell.Heal,
        )

    # success
    def test_get_spell_returns_frostbolt(self):

        # Get Frostbolt
        self.assert_get_spell_returns(
            "Frostbolt",
            spell.Frostbolt,
        )

    # success
    def test_get_spell_name_is_case_insensitive(self):

        # Get Fireball with lowercase name
        self.assert_get_spell_returns(
            "fireball",
            spell.Fireball,
        )

        # Get Heal with uppercase name
        self.assert_get_spell_returns(
            "HEAL",
            spell.Heal,
        )

        # Get Frostbolt with mixed case
        self.assert_get_spell_returns(
            "fRoStBoLt",
            spell.Frostbolt,
        )

    # failure
    def test_get_spell_with_invalid_spell(self):

        # Attempt to get invalid spell
        with self.assertRaises(ValueError):
            spell.get_spell("NotASpell")

    # failure
    def test_get_spell_with_empty_name(self):

        # Attempt to get spell with empty name
        with self.assertRaises(ValueError):
            spell.get_spell("")

    # success
    def test_heal_dead_entity_does_not_revive(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Kill target
        target.health = 0
        target.handle_death()

        # Verify target is dead
        self.assertFalse(target.is_alive())

        # Create Heal
        heal = spell.Heal()

        # Cast Heal on dead target
        heal.cast_spell(caster, target)

        # Verify entity is still dead
        self.assertFalse(target.is_alive())

    # success
    def test_heal_dead_entity_does_not_restore_health(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Kill target
        target.health = 0
        target.handle_death()

        # Create Heal
        heal = spell.Heal()

        # Cast Heal on dead target
        heal.cast_spell(caster, target)

        # Verify health remains at zero
        self.assertEqual(target.health, 0)

    # success
    def test_heal_dead_entity_does_not_remove_dead_status(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Kill target
        target.health = 0
        target.handle_death()

        # Create Heal
        heal = spell.Heal()

        # Cast Heal on dead target
        heal.cast_spell(caster, target)

        # Verify Dead status remains
        self.assertFalse(target.is_alive())

        self.assertTrue(any(buff["Name"] == "Dead" for buff in target.temp_buffs))

    # success
    def test_heal_alive_entity_returns_healed_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Damage target
        target.health -= 20

        # Create Heal
        heal = spell.Heal()

        # Calculate expected healing
        expected_healing = max(
            1,
            caster.spell_power * heal.spell_power_modifier,
        )

        # Cast Heal
        effect = heal.cast_spell(caster, target)

        # Verify exact effect message
        self.assertEqual(
            effect,
            f"Healed {target.id} for {expected_healing} health!",
        )

    # success
    def test_heal_dead_entity_returns_dead_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target("Warrior")

        # Kill target
        target.health = 0
        target.handle_death()

        # Create Heal
        heal = spell.Heal()

        # Cast Heal
        effect = heal.cast_spell(caster, target)

        # Verify exact effect message
        self.assertEqual(
            effect,
            f"Healed {target.id} for 0 health! - Cannot heal a dead entity!",
        )

    # success
    def test_offensive_spell_returns_damage_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Fireball
        fireball = spell.Fireball()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            fireball,
        )

        # Cast Fireball
        effect = fireball.cast_spell(caster, target)

        # Verify exact effect message
        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.id}!",
        )

    # success
    def test_offensive_spell_returns_death_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Set target health low enough to die
        target.health = 1

        # Create Fireball
        fireball = spell.Fireball()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            fireball,
        )

        # Cast Fireball
        effect = fireball.cast_spell(caster, target)

        # Verify exact death message
        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.id}! " f"{target.id} has died!",
        )

        # Verify target is dead
        self.assertFalse(target.is_alive())

    # success
    def test_effect_spell_returns_damage_and_effect_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            frostbolt,
        )

        # Cast Frostbolt
        effect = frostbolt.cast_spell(caster, target)

        # Verify exact effect message
        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.id}! "
            f"Applied {frostbolt.name} effect to {target.id}!",
        )

    # success
    def test_effect_spell_returns_damage_effect_and_death_message(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Set target health low enough to die
        target.health = 1

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Calculate expected damage
        expected_damage = self.calculate_expected_damage(
            caster,
            target,
            frostbolt,
        )

        # Cast Frostbolt
        effect = frostbolt.cast_spell(caster, target)

        # Verify exact effect message
        self.assertEqual(
            effect,
            f"Dealt {expected_damage} damage to {target.id}! "
            f"Applied {frostbolt.name} effect to {target.id}! "
            f"{target.id} has died!",
        )

        # Verify target is dead
        self.assertFalse(target.is_alive())

    # success
    def test_effect_spell_applies_temporary_effect(self):

        # Create caster and target
        caster, target = self.create_caster_and_target()

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Cast Frostbolt
        frostbolt.cast_spell(caster, target)

        # Verify effect was added
        self.assertEqual(len(target.temp_buffs), 1)

        # Verify effect contents
        self.assertEqual(
            target.temp_buffs[0]["Name"],
            frostbolt.name,
        )
        self.assertEqual(
            target.temp_buffs[0]["Effects"],
            frostbolt.over_time_effects,
        )
        self.assertEqual(
            target.temp_buffs[0]["Turns"],
            frostbolt.duration,
        )
