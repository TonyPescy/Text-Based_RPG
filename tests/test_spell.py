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
    # Spell initialization
    # Tests that a generic Spell correctly assigns all provided attributes
    def test_spell_initialization(self):
        # Create test spell
        test_spell = spell.Spell(
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

        # Verify spell attributes
        self.assertEqual(test_spell.name, "Test Spell")
        self.assertEqual(test_spell.spell_type, dl.SpellTypes.OFFENSIVE.value)
        self.assertEqual(test_spell.mana_cost, 10)
        self.assertEqual(test_spell.spell_range, 5)
        self.assertEqual(test_spell.target_type, "Enemy")
        self.assertEqual(test_spell.spell_power_modifier, 1.5)

    # success
    def test_spell_get_range(self):
        # Create test spell
        test_spell = spell.Spell(
            "Test Spell",
            dl.SpellTypes.OFFENSIVE.value,
            10,
            5,
            "Enemy",
            1.5,
        )

        # Get spell range
        spell_range = test_spell.get_range()

        # Verify spell range
        self.assertEqual(spell_range, 5)

    # success
    def test_fireball_initialization(self):
        # Create Fireball
        fireball = spell.Fireball()

        # Verify Fireball attributes
        self.assertEqual(fireball.name, dl.SpellNames.FIREBALL.value)
        self.assertEqual(
            fireball.spell_type,
            dl.SpellTypes.OFFENSIVE.value,
        )
        self.assertEqual(fireball.mana_cost, 25)
        self.assertEqual(fireball.spell_range, 4)
        self.assertEqual(fireball.target_type, "Enemy")
        self.assertEqual(fireball.spell_power_modifier, 1.5)

    # success
    def test_heal_initialization(self):
        # Create Heal
        heal = spell.Heal()

        # Verify Heal attributes
        self.assertEqual(heal.name, dl.SpellNames.HEAL.value)
        self.assertEqual(
            heal.spell_type,
            dl.SpellTypes.SUPPORT.value,
        )
        self.assertEqual(heal.mana_cost, 30)
        self.assertEqual(heal.spell_range, 2)
        self.assertEqual(heal.target_type, "All")
        self.assertEqual(heal.spell_power_modifier, 1.2)

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
        self.assertEqual(test_spell.name, "Test Effect")
        self.assertEqual(
            test_spell.spell_type,
            dl.SpellTypes.CONTROL.value,
        )
        self.assertEqual(test_spell.mana_cost, 20)
        self.assertEqual(test_spell.spell_range, 3)
        self.assertEqual(test_spell.target_type, "Enemy")
        self.assertEqual(test_spell.spell_power_modifier, 0.8)

        # Verify EffectSpell attributes
        self.assertEqual(test_spell.over_time_effects, test_effects)
        self.assertEqual(test_spell.duration, 2)

    # success
    def test_frostbolt_initialization(self):
        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Verify Frostbolt attributes
        self.assertEqual(
            frostbolt.name,
            dl.SpellNames.FROSTBOLT.value,
        )
        self.assertEqual(
            frostbolt.spell_type,
            dl.SpellTypes.CONTROL.value,
        )
        self.assertEqual(frostbolt.mana_cost, 20)
        self.assertEqual(frostbolt.spell_range, 3)
        self.assertEqual(frostbolt.target_type, "Enemy")
        self.assertEqual(frostbolt.spell_power_modifier, 0.8)

        # Verify Frostbolt effects
        self.assertEqual(
            frostbolt.over_time_effects,
            {
                "Flat_modifiers": {"Speed": -2},
                "Percent_modifiers": {},
            },
        )
        self.assertEqual(frostbolt.duration, 1)

    # success
    def test_cast_offensive_spell(self):
        # Create caster and target
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

        # Create Fireball
        fireball = spell.Fireball()

        # Calculate expected damage
        expected_damage = max(
            1,
            ((caster.spell_power * fireball.spell_power_modifier) - target.defence),
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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

        # Give target extremely high defence
        target.defence = 1000

        # Create Fireball
        fireball = spell.Fireball()

        # Store target's starting health
        starting_health = target.health

        # Cast Fireball
        fireball.cast_spell(caster, target)

        # Verify minimum damage of 1
        self.assertEqual(target.health, starting_health - 1)

    # success
    def test_cast_offensive_spell_health_cannot_go_below_zero(self):
        # Create caster and target
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Warrior", 1, 0, 1)

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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Warrior", 1, 0, 1)

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
        self.assertEqual(target.health, expected_health)

    # success
    def test_cast_heal_spell_cannot_exceed_max_health(self):
        # Create caster and target
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Warrior", 1, 0, 1)

        # Set target below maximum health
        target.health = target.max_health - 1

        # Create Heal
        heal = spell.Heal()

        # Cast Heal
        heal.cast_spell(caster, target)

        # Verify health does not exceed maximum
        self.assertEqual(target.health, target.max_health)

    # success
    def test_cast_heal_spell_minimum_healing(self):
        # Create caster and target
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Warrior", 1, 0, 1)

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
        self.assertEqual(target.health, starting_health + 1)

    # success
    def test_cast_spell_without_over_time_effect(self):
        # Create caster and target
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

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
        caster = entity.create_entity("Mage", 0, 0, 0)
        target = entity.create_entity("Goblin", 1, 0, 1)

        # Store target's starting health
        starting_health = target.health

        # Create Frostbolt
        frostbolt = spell.Frostbolt()

        # Calculate expected damage
        expected_damage = max(
            1,
            ((caster.spell_power * frostbolt.spell_power_modifier) - target.defence),
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
        self.assertIn(dl.SpellNames.FIREBALL.value, spell.SPELLS)

        # Verify Heal exists
        self.assertIn(dl.SpellNames.HEAL.value, spell.SPELLS)

        # Verify Frostbolt exists
        self.assertIn(dl.SpellNames.FROSTBOLT.value, spell.SPELLS)

    # success
    def test_spell_dictionary_returns_correct_fireball_class(self):
        # Get Fireball class
        spell_class = spell.SPELLS[dl.SpellNames.FIREBALL.value]

        # Verify class
        self.assertEqual(spell_class, spell.Fireball)

    # success
    def test_spell_dictionary_returns_correct_heal_class(self):
        # Get Heal class
        spell_class = spell.SPELLS[dl.SpellNames.HEAL.value]

        # Verify class
        self.assertEqual(spell_class, spell.Heal)

    # success
    def test_spell_dictionary_returns_correct_frostbolt_class(self):
        # Get Frostbolt class
        spell_class = spell.SPELLS[dl.SpellNames.FROSTBOLT.value]

        # Verify class
        self.assertEqual(spell_class, spell.Frostbolt)

    # success
    def test_get_spell_returns_fireball(self):
        # Get Fireball
        test_spell = spell.get_spell("Fireball")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Fireball)

    # success
    def test_get_spell_returns_heal(self):
        # Get Heal
        test_spell = spell.get_spell("Heal")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Heal)

    # success
    def test_get_spell_returns_frostbolt(self):
        # Get Frostbolt
        test_spell = spell.get_spell("Frostbolt")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Frostbolt)

    # success
    def test_get_spell_name_is_case_insensitive(self):
        # Get Fireball with lowercase name
        test_spell = spell.get_spell("fireball")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Fireball)

        # Get Heal with uppercase name
        test_spell = spell.get_spell("HEAL")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Heal)

        # Get Frostbolt with mixed case
        test_spell = spell.get_spell("fRoStBoLt")

        # Verify correct class
        self.assertIsInstance(test_spell, spell.Frostbolt)

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
