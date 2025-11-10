"""
Wizard Game - Dummy Interface
This is a simple game engine for testing the Rasa spell-casting bot.
"""

from enum import Enum
from typing import Dict, Optional
import random


class SpellType(Enum):
    """Available spells in the game"""
    FIREBALL = "bola_fuego"
    LIGHTNING = "rayo"
    ICE_SHARD = "fragmento_hielo"
    HEAL = "curar"
    SHIELD = "escudo"


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
            return f"¡{self.name} ha sido derrotado! 💀"
        return f"¡{self.name} recibe {damage} de daño! Vida: {self.hp}/{self.max_hp}"


class WizardGame:
    """Main game engine"""
    
    def __init__(self):
        self.player_hp = 100
        self.player_max_hp = 100
        self.mana = 50
        self.max_mana = 50
        self.enemies: Dict[str, Enemy] = {}
        self.shield_active = False
        self.game_over = False
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
            "golem": Enemy("Golem de Piedra", 80, "rayo"),
            "dragon": Enemy("Dragón de Fuego", 120, "fragmento_hielo"),
            "zombie": Enemy("Zombi", 50, "bola_fuego"),
            "esqueleto": Enemy("Guerrero Esqueleto", 60),
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
        # Check if game is over
        if self.game_over:
            return "💀 El juego ha terminado. Usa 'reiniciar juego' para volver a jugar."
        
        spell_name = spell_name.lower().replace(" ", "_")
        target_name = target_name.lower().strip()
        
        # Map English and Spanish spell names to internal names
        spell_mappings = {
            "fireball": "bola_fuego",
            "lightning": "rayo",
            "ice_shard": "fragmento_hielo",
            "ice": "fragmento_hielo",
            "heal": "curar",
            "shield": "escudo",
            "fragmento_de_hielo": "fragmento_hielo",
            "bola_de_fuego": "bola_fuego",
            "hielo": "fragmento_hielo",
            "fuego": "bola_fuego",
            "fragmento": "fragmento_hielo",
            "cúrame": "curar",
            "curame": "curar",
            "protégeme": "escudo",
            "protegeme": "escudo",
            "congelar": "fragmento_hielo",
            "quemar": "bola_fuego",
            "electrocutar": "rayo",
            "bola": "bola_fuego",  # Partial match
        }
        
        # Map target names
        target_mappings = {
            "dragon": "dragon",
            "dragón": "dragon",
            "skeleton": "esqueleto",
            "zombi": "zombie",
            "guerrero": "esqueleto",  # Partial match for "Guerrero Esqueleto"
            "guerrero_esqueleto": "esqueleto",
        }
        
        # Try direct mapping first
        spell_name = spell_mappings.get(spell_name, spell_name)
        target_name = target_mappings.get(target_name, target_name)
        
        # If still not found, try partial matching for targets
        if target_name not in self.enemies:
            for enemy_key, enemy in self.enemies.items():
                enemy_name_lower = enemy.name.lower()
                # Check if target_name is a substring of enemy name
                if target_name in enemy_name_lower or enemy_key in target_name:
                    target_name = enemy_key
                    break
        
        # Check if spell exists
        try:
            spell = SpellType(spell_name)
        except ValueError:
            return f"❌ Hechizo desconocido: {spell_name}. Hechizos disponibles: bola_fuego, rayo, fragmento_hielo, curar, escudo"
        
        # Check mana
        cost = self.spell_costs.get(spell, 10)
        if self.mana < cost:
            return f"❌ ¡No tienes suficiente maná! Necesitas {cost} de maná, pero solo tienes {self.mana}."
        
        # Deduct mana
        self.mana -= cost
        
        # Handle healing spell
        if spell == SpellType.HEAL:
            heal_amount = 30
            old_hp = self.player_hp
            self.player_hp = min(self.player_hp + heal_amount, self.player_max_hp)
            healed = self.player_hp - old_hp
            message = f"✨ ¡Lanzas Curar! Restaurado {healed} de vida. Vida: {self.player_hp}/{self.player_max_hp}<br>Maná: {self.mana}/{self.max_mana}"
            
            # Enemy counterattack
            enemy_attack = self.enemy_turn()
            if enemy_attack:
                message += "<br><br>" + enemy_attack
            
            return message
        
        # Handle shield spell
        if spell == SpellType.SHIELD:
            self.shield_active = True
            return f"🛡️ ¡Lanzas Escudo! Estás protegido para el próximo ataque.<br>Maná: {self.mana}/{self.max_mana}"
        
        # Handle attack spells
        enemy = self.get_enemy(target_name)
        if not enemy:
            available = ", ".join([e for e in self.enemies.keys() if self.enemies[e].is_alive])
            return f"❌ Objetivo '{target_name}' no encontrado. Enemigos disponibles: {available}"
        
        if not enemy.is_alive:
            return f"❌ ¡{enemy.name} ya fue derrotado!"
        
        # Calculate damage
        base_damage = self.spell_damage.get(spell, 15)
        
        # Apply weakness bonus
        if enemy.element_weakness == spell.value:
            base_damage = int(base_damage * 1.5)
            weakness_msg = " 💥 ¡GOLPE CRÍTICO! ¡Explotaste su debilidad!"
        else:
            weakness_msg = ""
        
        # Apply some randomness
        damage = random.randint(int(base_damage * 0.9), int(base_damage * 1.1))
        
        # Deal damage
        result = enemy.take_damage(damage)
        
        spell_emoji = {"bola_fuego": "🔥", "rayo": "⚡", "fragmento_hielo": "❄️"}.get(spell.value, "✨")
        spell_display = {"bola_fuego": "Bola de Fuego", "rayo": "Rayo", "fragmento_hielo": "Fragmento de Hielo"}.get(spell.value, spell.value.replace('_', ' ').title())
        
        message = f"{spell_emoji} ¡Lanzas {spell_display} a {enemy.name}!{weakness_msg}<br>{result}<br>Maná: {self.mana}/{self.max_mana}"
        
        # Enemy counterattack if still alive
        if enemy.is_alive:
            enemy_attack = self.enemy_turn()
            message += "<br><br>" + enemy_attack
        
        return message
    
    def enemy_turn(self) -> str:
        """Enemy attacks the player"""
        alive_enemies = [e for e in self.enemies.values() if e.is_alive]
        
        if not alive_enemies:
            return ""
        
        # Random enemy attacks
        attacker = random.choice(alive_enemies)
        damage = random.randint(10, 20)
        
        # Check shield
        if self.shield_active:
            self.shield_active = False
            return f"🛡️ ¡{attacker.name} ataca pero tu escudo lo bloquea! (0 daño)"
        
        # Apply damage
        self.player_hp -= damage
        
        if self.player_hp <= 0:
            self.player_hp = 0
            self.game_over = True
            return f"⚔️ ¡{attacker.name} te ataca! Recibes {damage} de daño.<br>💀 <strong>¡HAS SIDO DERROTADO! Usa 'reiniciar juego' para volver a jugar.</strong>"
        
        return f"⚔️ ¡{attacker.name} te ataca! Recibes {damage} de daño. Tu Vida: {self.player_hp}/{self.player_max_hp}"
    
    def get_status(self) -> str:
        """Get current game status"""
        alive_enemies = [e for e in self.enemies.values() if e.is_alive]
        dead_enemies = [e for e in self.enemies.values() if not e.is_alive]
        
        status = f"🧙 <strong>Tu Estado:</strong><br>"
        status += f"&nbsp;&nbsp;Vida: {self.player_hp}/{self.player_max_hp} | Maná: {self.mana}/{self.max_mana}<br>"
        if self.shield_active:
            status += f"&nbsp;&nbsp;🛡️ Escudo activo<br>"
        status += "<br>"
        
        if alive_enemies:
            status += "⚔️ <strong>Enemigos:</strong><br>"
            for enemy in alive_enemies:
                weakness = f" (Débil a {enemy.element_weakness})" if enemy.element_weakness else ""
                status += f"&nbsp;&nbsp;• {enemy.name}: {enemy.hp}/{enemy.max_hp} Vida{weakness}<br>"
        
        if dead_enemies:
            status += f"<br>💀 <strong>Derrotados:</strong> {', '.join([e.name for e in dead_enemies])}<br>"
        
        if not alive_enemies:
            status += "<br>🎉 <strong>¡Victoria! ¡Todos los enemigos derrotados!</strong>"
        
        if self.game_over:
            status += "<br><br>💀 <strong>JUEGO TERMINADO</strong> - Usa 'reiniciar juego' para volver a jugar."
        
        return status
    
    def list_spells(self) -> str:
        """List available spells"""
        spells = "📜 <strong>Hechizos Disponibles:</strong><br>"
        spells += "&nbsp;&nbsp;• Bola de Fuego (15 maná) - 30 de daño 🔥<br>"
        spells += "&nbsp;&nbsp;• Rayo (12 maná) - 25 de daño ⚡<br>"
        spells += "&nbsp;&nbsp;• Fragmento de Hielo (10 maná) - 20 de daño ❄️<br>"
        spells += "&nbsp;&nbsp;• Curar (20 maná) - Restaura 30 de vida ✨<br>"
        spells += "&nbsp;&nbsp;• Escudo (15 maná) - Bloquea el próximo ataque 🛡️<br>"
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
    return "🎮 ¡Juego reiniciado! ¡Una nueva aventura comienza!"


def rest() -> str:
    """
    Rest to restore mana
    """
    # Check if game is over
    if game.game_over:
        return "💀 El juego ha terminado. Usa 'reiniciar juego' para volver a jugar."
    
    mana_restored = min(25, game.max_mana - game.mana)
    game.mana = min(game.mana + 25, game.max_mana)
    
    message = f"🧘 Te tomas un momento para descansar y meditar...<br>✨ ¡Restaurado {mana_restored} de maná! Maná: {game.mana}/{game.max_mana}"
    
    # Enemy attacks while resting
    enemy_attack = game.enemy_turn()
    if enemy_attack:
        message += "<br><br>⚠️ ¡Los enemigos aprovechan tu descanso!<br>" + enemy_attack
    
    return message


# Example usage
if __name__ == "__main__":
    import sys
    import io
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=== Demo del Juego del Mago ===")
    print(get_game_status())
    print("\n" + list_spells())
    print("\n--- Lanzando Hechizos ---")
    print(cast_spell("bola_fuego", "golem"))
    print(cast_spell("rayo", "golem"))
    print("\n" + get_game_status())

