"""
Author: Tony Pescatore
Major:  Computer Science
Creation Date: September 30, 2026
Due Date: Multiple Due Dates
Course: CPSC 520
Professor: Dr. Schwesinger
Assignment: Text Based RPG
Filename: spell.py
Purpose: Houses all functions necessary for proper spell logic in the game
"""

# Imports
import domain_library as dl


# Spell class
# Generic spell class so it incompasses any normal operaint spells
# Encompasses offensive magic and currently support spells
#   > May be broken up at later date with addition of new offensive/support spells
class Spell:

    # Init spell class with the following:
    def __init__(
        self,
        name,
        spell_type,
        mana_cost,
        spell_range,
        target_type,
        spell_power_modifier,
    ):
        self.name = name
        self.spell_type = spell_type
        self.mana_cost = mana_cost
        self.spell_range = spell_range
        self.target_type = target_type
        self.spell_power_modifier = spell_power_modifier

    # Get Range
    # Gets the range of spell this is called on
    # Params:
    # Returns: range - int - Spell range
    def get_range(self):
        return self.spell_range

    # Cast Spell - REFACTOR ASAP - Sleep deprives when this was written so it is probably messy
    # Casts the spell on the target entity with the caster spell power
    # Params:   caster - entity - one that casts the spell
    #           target - entity - Target entity of the spell
    # Return:   effect - string - Effect of the spell (damage, effetcs, heals etc.)
    def cast_spell(self, caster, target):
        # Calc damage/heals dealt by spell
        if self.name == dl.SpellNames.HEAL.value:
            # only healing spell so it has special case
            damage = max(1, ((caster.spell_power * self.spell_power_modifier)))
            # checks fors targets death
            if target.health > 0:
                # Apply heals
                target.health = min(target.max_health, target.health + damage)
                effect = f"Healed {target.id} for {damage} health!"
            # If target is dead
            else:
                effect = (
                    f"Healed {target.id} for 0 health! - Cannot heal a dead entity!"
                )
            # CHECK FOR EFFECTS FROM SUPPORT MAGIC HERE
            return effect
        # all other magic harms target with same calculations
        else:
            damage = max(
                1, ((caster.spell_power * self.spell_power_modifier) - target.defence)
            )
            # Subtract health from defender with max at 0 - prevents underflow
            target.health = max(0, (target.health - damage))
            # Handle target death
            if target.health == 0:
                target.handle_death()

        # Target is alive for debuffs to be added and debuffs exist
        # If spell has an effect
        if getattr(self, "over_time_effects", {}):
            # Store temp buff
            target.temp_buffs.append(
                {
                    "Name": self.name,
                    "Effects": self.over_time_effects,
                    "Turns": self.duration,
                }
            )
            # Check for target death message
            if target.health == 0:
                effect = f"Dealt {damage} damage to {target.id}! Applied {self.name} effect to {target.id}! {target.id} has died!"
            else:
                # Create effect message
                effect = f"Dealt {damage} damage to {target.id}! Applied {self.name} effect to {target.id}!"
        # No spell effect
        else:
            # Check for is target is dead or not
            if target.health == 0:
                effect = f"Dealt {damage} damage to {target.id}! {target.id} has died!"
            else:
                effect = f"Dealt {damage} damage to {target.id}!"
        # return effect for success message
        return effect


# Spell Inits
# Fireball spell class - inherits from Spell class
class Fireball(Spell):
    # Init with base stats
    def __init__(self):
        super().__init__(
            dl.SpellNames.FIREBALL.value,
            dl.SpellTypes.OFFENSIVE.value,
            25,
            4,
            "Enemy",  # Target types need full implmentation
            1.5,
        )


# Heal spell class - inherits from spell class
class Heal(Spell):
    # Init with base stats
    def __init__(self):
        super().__init__(
            dl.SpellNames.HEAL.value,
            dl.SpellTypes.SUPPORT.value,
            30,
            2,
            "All",  # Target types need full implmentation
            1.2,  # Heals target so "damage" is negative - May implement
        )


# Effect Spell Class - similar setup to Equipment and Consumable relationship
# Has additional effects in addition to damage/heal
#   > Buffs and Debuffs
class EffectSpell(Spell):
    def __init__(
        self,
        name,
        spell_type,
        mana_cost,
        spell_range,
        target_type,
        spell_power_modifier,
        over_time_effects,
        duration,
    ):
        super().__init__(
            name,
            spell_type,
            mana_cost,
            spell_range,
            target_type,
            spell_power_modifier,
        )
        self.over_time_effects = over_time_effects
        self.duration = duration


# Frostbolt EffectSpell class - Inherits from EffectSpell
class Frostbolt(EffectSpell):
    def __init__(self):
        super().__init__(
            dl.SpellNames.FROSTBOLT.value,
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
            {"Flat_modifiers": {"Speed": -2}, "Percent_modifiers": {}},
            1,
        )


# Spells Dictionary
SPELLS = {
    dl.SpellNames.FIREBALL.value: Fireball,
    dl.SpellNames.HEAL.value: Heal,
    dl.SpellNames.FROSTBOLT.value: Frostbolt,
}


# Get Spell
# Finds corresponding spell from spell name provided
# Provided name is validated prior to this being called
# Params: spell_name - string - Validated name of spell
# Returns spell - Spell/EffectSpell Instance - found spell
def get_spell(spell_name):
    spell_class = SPELLS.get(spell_name.capitalize())
    if spell_class:
        return spell_class()
    else:
        raise ValueError(f"Spell not found: {spell_name}")
