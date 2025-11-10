"""
Wizard Game - Dummy Interface
This is a simple game engine for testing the Rasa spell-casting bot.
"""

from enum import Enum
from typing import Dict, Optional
import random


class SpellType(Enum):
    """Available spells in the game"""
    FIREBALL = "fireball"
    LIGHTNING = "lightning"
    ICE_SHARD = "ice_shard"
    HEAL = "heal"
    SHIELD = "shield"


class Enemy:
    """Enemy class"""
    def __init__(self, name: str, hp: int, element_weakness: Optional[str] = None):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.element_weakness = element_weakness
        self.is_alive = True
    
    def take_damage(self, damage: int) -> str:
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
            return f"{self.name} has been defeated! 💀"
        return f"{self.name} takes {damage} damage! HP: {self.hp}/{self.max_hp}"


class WizardGame:
    """Main game engine"""
    
    def __init__(self):
        self.player_hp = 100
        self.player_max_hp = 100
        self.mana = 50
        self.max_mana = 50
        self.enemies: Dict[str, Enemy] = {}
        self.initialize_enemies()
        
        # Spell damage values
        self.spell_damage = {
            SpellType.FIREBALL: 30,
            SpellType.LIGHTNING: 25,
            SpellType.ICE_SHARD: 20,
        }
        
        # Spell mana costs
        self.spell_costs = {
            SpellType.FIREBALL: 15,
            SpellType.LIGHTNING: 12,
            SpellType.ICE_SHARD: 10,
            SpellType.HEAL: 20,
            SpellType.SHIELD: 15,
        }
    
    def initialize_enemies(self):
        """Create initial enemies"""
        self.enemies = {
            "golem": Enemy("Stone Golem", 80, "lightning"),
            "dragon": Enemy("Fire Dragon", 120, "ice_shard"),
            "zombie": Enemy("Zombie", 50, "fireball"),
            "skeleton": Enemy("Skeleton Warrior", 60),
            "goblin": Enemy("Goblin", 40),
        }
    
    def get_enemy(self, target_name: str) -> Optional[Enemy]:
        """Get enemy by name (case insensitive)"""
        target_name = target_name.lower().strip()
        return self.enemies.get(target_name)
    
    def cast_spell(self, spell_name: str, target_name: str) -> str:
        """
        Main spell casting function
        Returns a message describing what happened
        """
        spell_name = spell_name.lower().replace(" ", "_")
        target_name = target_name.lower().strip()
        
        # Check if spell exists
        try:
            spell = SpellType(spell_name)
        except ValueError:
            return f"❌ Unknown spell: {spell_name}. Available spells: fireball, lightning, ice_shard, heal, shield"
        
        # Check mana
        cost = self.spell_costs.get(spell, 10)
        if self.mana < cost:
            return f"❌ Not enough mana! You need {cost} mana, but only have {self.mana}."
        
        # Deduct mana
        self.mana -= cost
        
        # Handle healing spell
        if spell == SpellType.HEAL:
            heal_amount = 30
            old_hp = self.player_hp
            self.player_hp = min(self.player_hp + heal_amount, self.player_max_hp)
            healed = self.player_hp - old_hp
            return f"✨ You cast Heal! Restored {healed} HP. HP: {self.player_hp}/{self.player_max_hp}"
        
        # Handle shield spell
        if spell == SpellType.SHIELD:
            return f"🛡️ You cast Shield! You are protected for the next attack."
        
        # Handle attack spells
        enemy = self.get_enemy(target_name)
        if not enemy:
            available = ", ".join([e for e in self.enemies.keys() if self.enemies[e].is_alive])
            return f"❌ Target '{target_name}' not found. Available enemies: {available}"
        
        if not enemy.is_alive:
            return f"❌ {enemy.name} is already defeated!"
        
        # Calculate damage
        base_damage = self.spell_damage.get(spell, 15)
        
        # Apply weakness bonus
        if enemy.element_weakness == spell.value:
            base_damage = int(base_damage * 1.5)
            weakness_msg = " 💥 CRITICAL HIT! Exploited weakness!"
        else:
            weakness_msg = ""
        
        # Apply some randomness
        damage = random.randint(int(base_damage * 0.9), int(base_damage * 1.1))
        
        # Deal damage
        result = enemy.take_damage(damage)
        
        spell_emoji = {"fireball": "🔥", "lightning": "⚡", "ice_shard": "❄️"}.get(spell.value, "✨")
        
        return f"{spell_emoji} You cast {spell.value.replace('_', ' ').title()} on {enemy.name}!{weakness_msg}\n{result}\nMana: {self.mana}/{self.max_mana}"
    
    def get_status(self) -> str:
        """Get current game status"""
        alive_enemies = [e for e in self.enemies.values() if e.is_alive]
        dead_enemies = [e for e in self.enemies.values() if not e.is_alive]
        
        status = f"🧙 **Your Status:**\n"
        status += f"  HP: {self.player_hp}/{self.player_max_hp} | Mana: {self.mana}/{self.max_mana}\n\n"
        
        if alive_enemies:
            status += "⚔️ **Enemies:**\n"
            for enemy in alive_enemies:
                weakness = f" (Weak to {enemy.element_weakness})" if enemy.element_weakness else ""
                status += f"  • {enemy.name}: {enemy.hp}/{enemy.max_hp} HP{weakness}\n"
        
        if dead_enemies:
            status += f"\n💀 **Defeated:** {', '.join([e.name for e in dead_enemies])}\n"
        
        if not alive_enemies:
            status += "\n🎉 **Victory! All enemies defeated!**"
        
        return status
    
    def list_spells(self) -> str:
        """List available spells"""
        spells = "📜 **Available Spells:**\n"
        spells += "  • Fireball (15 mana) - 30 damage 🔥\n"
        spells += "  • Lightning (12 mana) - 25 damage ⚡\n"
        spells += "  • Ice Shard (10 mana) - 20 damage ❄️\n"
        spells += "  • Heal (20 mana) - Restore 30 HP ✨\n"
        spells += "  • Shield (15 mana) - Block next attack 🛡️\n"
        return spells


# Global game instance
game = WizardGame()


def cast_spell(spell_type: str, target: str) -> str:
    """
    Public interface for casting spells
    This is what Rasa will call
    """
    return game.cast_spell(spell_type, target)


def get_game_status() -> str:
    """Get current game status"""
    return game.get_status()


def list_spells() -> str:
    """List available spells"""
    return game.list_spells()


def reset_game() -> str:
    """Reset the game"""
    global game
    game = WizardGame()
    return "🎮 Game reset! A new adventure begins!"


def rest() -> str:
    """
    Rest to restore mana
    """
    mana_restored = min(25, game.max_mana - game.mana)
    game.mana = min(game.mana + 25, game.max_mana)
    
    if mana_restored > 0:
        return f"🧘 You take a moment to rest and meditate...\n✨ Restored {mana_restored} mana! Mana: {game.mana}/{game.max_mana}\n\n⚠️ Warning: Enemies may attack while you rest!"
    else:
        return f"🧘 You rest, but your mana is already full! Mana: {game.mana}/{game.max_mana}"


# Example usage
if __name__ == "__main__":
    import sys
    import io
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=== Wizard Game Demo ===")
    print(get_game_status())
    print("\n" + list_spells())
    print("\n--- Casting Spells ---")
    print(cast_spell("fireball", "golem"))
    print(cast_spell("lightning", "golem"))
    print("\n" + get_game_status())

