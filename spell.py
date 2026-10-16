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
from dataclasses import dataclass


# Spell Data Class
@dataclass
class SpellInfo:
    name: str
    spell_type: str
    mana_cost: int
    spell_range: int
    target_type: str
    spell_power_modifier: float


@dataclass
class EffectSpellInfo(SpellInfo):
    over_time_effects: tuple
    duration: int


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
        self.__name = name
        self.__spell_type = spell_type
        self.__mana_cost = mana_cost
        self.__spell_range = spell_range
        self.__target_type = target_type
        self.__spell_power_modifier = spell_power_modifier

    """
        # Get Range
        # Gets the range of spell this is called on
        # Params:   spell
        # Returns: range - int - Spell range
        def get_range(self):
            return self.__spell_range"""

    # Get Info
    # Gets the info of spell this is called on
    # Params: None
    # Returns: info - dict - Spell info
    def get_info(self):
        return SpellInfo(
            name=self.__name,
            spell_type=self.__spell_type,
            mana_cost=self.__mana_cost,
            spell_range=self.__spell_range,
            target_type=self.__target_type,
            spell_power_modifier=self.__spell_power_modifier,
        )

    # Cast Spell - REFACTOR ASAP - Sleep deprives when this was written so it is probably messy
    # Casts the spell on the target entity with the caster spell power
    # Params:   caster - entity - one that casts the spell
    #           target - entity - Target entity of the spell
    #           game_state - Game State - current game state
    # Return:   effect - string - Effect of the spell (damage, effetcs, heals etc.)
    def cast_spell(self, caster, target, game_state):
        # Get entity info
        caster_info = caster.get_info()
        target_info = target.get_info()
        # Calc damage/heals dealt by spell
        if self.__name.lower() == "heal":
            # only healing spell so it has special case
            damage = max(1, ((caster_info.spell_power * self.__spell_power_modifier)))
            # checks fors targets death
            if target_info.health > 0:
                if target_info.max_health > (target_info.health + damage):
                    expected_healing = damage
                else:  # overflow on healing
                    expected_healing = damage - (
                        (target_info.health + damage) - target_info.max_health
                    )
                # apply heal to target
                target.update_single_stat(
                    "health", min(target_info.max_health, target_info.health + damage)
                )
                effect = f"Healed {target_info.id} for {int(expected_healing)} health!"
            # If target is dead
            else:
                effect = f"Healed {target_info.id} for 0 health! - Cannot heal a dead entity!"
            # CHECK FOR EFFECTS FROM SUPPORT MAGIC HERE
            return effect
        # all other magic harms target with same calculations
        else:
            damage = max(
                1,
                (
                    (caster_info.spell_power * self.__spell_power_modifier)
                    - target_info.defence
                ),
            )
            # Subtract health from defender with max at 0 - prevents underflow
            target.update_single_stat("health", max(0, (target_info.health - damage)))
            # Need to refresh target info after damage is dealt
            target_info = target.get_info()
            # Handle target death
            if target_info.health == 0:
                target.handle_death()

        # Target is alive for debuffs to be added and debuffs exist
        # If spell has an effect
        if getattr(self, "has_over_time_effects", lambda: False)():
            buff = {
                "Name": self.__name,
                "Effects": self.over_time_effects,
                "Turns": self.duration,
            }
            # Store temp buff
            game_state.add_temp_buff_to_entity(target_info.id, buff)
            # Check for target death message
            if target_info.health == 0:
                effect = f"Dealt {damage} damage to {target_info.id}! Applied {self.__name} effect to {target_info.id}! {target_info.id} has died!"
            else:
                # Create effect message
                effect = f"Dealt {damage} damage to {target_info.id}! Applied {self.__name} effect to {target_info.id}!"
        # No spell effect
        else:
            # Check for is target is dead or not
            if target_info.health == 0:
                effect = f"Dealt {damage} damage to {target_info.id}! {target_info.id} has died!"
            else:
                effect = f"Dealt {damage} damage to {target_info.id}!"
        # return effect for success message
        return effect


# Spell Inits
# Fireball spell class - inherits from Spell class
class Fireball(Spell):
    # Init with base stats
    def __init__(self):
        super().__init__(
            "Fireball",
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
            "Heal",
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
        self.__over_time_effects = over_time_effects
        self.__duration = duration

    # Get Info
    # Gets the info of effect spell this is called on
    # Params: None
    # Returns: info - dict - Spell info
    def get_info(self):
        # Get parent spell info
        spell_info = super().get_info()
        # Return effect spell info
        return EffectSpellInfo(
            name=spell_info.name,
            spell_type=spell_info.spell_type,
            mana_cost=spell_info.mana_cost,
            spell_range=spell_info.spell_range,
            target_type=spell_info.target_type,
            spell_power_modifier=spell_info.spell_power_modifier,
            over_time_effects=(
                (
                    "Flat_modifiers",
                    tuple(self.__over_time_effects["Flat_modifiers"].items()),
                ),
                (
                    "Percent_modifiers",
                    tuple(self.__over_time_effects["Percent_modifiers"].items()),
                ),
            ),
            duration=self.__duration,
        )

    # Over Time Effects
    # Gets the over-time effects for the spell
    # Params: None
    # Returns: dict - Over-time effects applied by the spell
    @property
    def over_time_effects(self):
        return self.__over_time_effects

    # Duration
    # Gets the duration for the spell
    # Params: None
    # Returns: duration - int - spell duration
    @property
    def duration(self):
        return self.__duration

    # Has Over Time Effects
    # Checks if effect spell has over time effects
    # Params: None
    # Returns: bool - Whether spell has effects
    def has_over_time_effects(self):
        return any(
            self.__over_time_effects.get(category, {})
            for category in ("Flat_modifiers", "Percent_modifiers")
        )


# Frostbolt EffectSpell class - Inherits from EffectSpell
class Frostbolt(EffectSpell):
    def __init__(self):
        super().__init__(
            "Frostbolt",
            dl.SpellTypes.CONTROL.value,
            20,
            3,
            "Enemy",
            0.8,
            {"Flat_modifiers": {"Speed": -2}, "Percent_modifiers": {}},
            1,
        )


"""# Spells Dictionary
SPELLS = {
    dl.SpellNames.FIREBALL.value: Fireball,
    dl.SpellNames.HEAL.value: Heal,
    dl.SpellNames.FROSTBOLT.value: Frostbolt,
}"""

"""
# Spells Factory
# Creates a spell object based on the given spell name
# Params:   spell_name - str - Name of spell to create
# Returns:  Spell instance if valid, otherwise None
def create_spell(spell_name):
    # Normalize spell name
    spell_name = str(spell_name).lower()

    # Create spell based on name
    match spell_name:
        case "fireball":
            return Fireball()
        case "heal":
            return Heal()
        case "frostbolt":
            return Frostbolt()
        case _:
            # Invalid spell name
            return None
"""


# Get Spell - Spell Factory
# Finds and creates a spell based on the provided spell name
# Params:   spell_name - str - Name of spell
# Returns:  Spell instance if found
# Raises:   ValueError if spell is not found
def get_spell(spell_name):
    # Normalize spell name
    spell_name = str(spell_name).lower()

    # Create spell based on name
    match spell_name:
        case "fireball":
            return Fireball()
        case "heal":
            return Heal()
        case "frostbolt":
            return Frostbolt()
        case _:
            raise ValueError(f"Spell not found: {spell_name}")
