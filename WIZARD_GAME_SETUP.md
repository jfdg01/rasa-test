# 🧙 Wizard Game Setup Summary

## ✅ What Was Created

### Files Modified for the Wizard Game:

1. **`game_engine.py`** (NEW)
   - Complete game engine with spell casting, enemy management, and damage calculation
   - Functions: `cast_spell(spell_type, target)`, `get_game_status()`, `list_spells()`, `reset_game()`

2. **`domain.yml`** (MODIFIED)
   - Added game intents: `cast_spell`, `check_status`, `list_spells`, `reset_game`
   - Added entities: `spell_type`, `target`
   - Added slots for spell_type and target
   - Added custom actions: `action_cast_spell`, `action_check_status`, `action_list_spells`, `action_reset_game`
   - Updated responses with wizard-themed greetings

3. **`data/nlu.yml`** (MODIFIED)
   - Added 20+ training examples for `cast_spell` intent with entity annotations
   - Added examples for `check_status`, `list_spells`, `reset_game` intents

4. **`data/stories.yml`** (MODIFIED)
   - Added 6 new story flows for wizard game interactions
   - Covers: spell casting, status checking, spell listing, game reset

5. **`data/rules.yml`** (MODIFIED)
   - Added rules for direct responses to game commands

6. **`config.yml`** (MODIFIED)
   - Enabled NLU pipeline for entity extraction
   - Uncommented and configured policies for dialogue management

7. **`actions/actions.py`** (MODIFIED)
   - Created 4 custom actions that interface with game_engine:
     - `ActionCastSpell` - Calls `cast_spell()` with extracted entities
     - `ActionCheckStatus` - Shows game status
     - `ActionListSpells` - Lists available spells
     - `ActionResetGame` - Resets the game

8. **`endpoints.yml`** (MODIFIED)
   - Enabled action_endpoint to connect to action server

9. **`README.md`** (NEW)
   - Comprehensive guide on how to play the wizard game
   - Command examples and troubleshooting

## 🎮 How the System Works

### The Flow: From User Input to Game Action

```
USER: "cast fireball on golem"
    ↓
[Rasa NLU - data/nlu.yml]
    → Intent: cast_spell
    → Entities: {spell_type: "fireball", target: "golem"}
    ↓
[Dialogue Manager - stories.yml + rules.yml + policies]
    → Predicts: action_cast_spell
    ↓
[Custom Action - actions/actions.py]
    → ActionCastSpell.run()
    → Extracts: spell_type from slot
    → Extracts: target from slot
    ↓
[Game Engine - game_engine.py]
    → cast_spell("fireball", "golem")
    → Calculates damage
    → Updates enemy HP
    → Returns result message
    ↓
[Response to User]
    → "🔥 You cast Fireball on Stone Golem!"
    → "Stone Golem takes 29 damage! HP: 51/80"
```

## 🚀 Quick Start Commands

### Setup (First Time)
```powershell
# Already done - venv created, packages installed, model trained
.\venv\Scripts\Activate.ps1
```

### Running the Game (Every Time)

**Terminal 1 - Action Server:**
```powershell
cd C:\Users\gara\Documents\Projects\Python\rasa-test
.\venv\Scripts\Activate.ps1
rasa run actions
```
> Keep this running!

**Terminal 2 - Chat Interface:**
```powershell
cd C:\Users\gara\Documents\Projects\Python\rasa-test
.\venv\Scripts\Activate.ps1
rasa shell
```
> Play here!

## 📝 Example Commands

| What You Want | What to Say |
|---------------|-------------|
| Start | `hello` or `hi` |
| See enemies & your stats | `check status` or `show status` |
| See available spells | `list spells` or `what spells do I have` |
| Cast a spell | `cast fireball on golem` |
|  | `throw lightning at dragon` |
|  | `use ice shard against zombie` |
| Heal yourself | `cast heal` or `use heal` |
| Use shield | `cast shield` |
| **Restore mana** | **`rest`** or **`meditate`** or **`recharge`** |
| Start over | `reset game` |
| End conversation | `goodbye` or `bye` |

## 🎯 Key Concepts

### Intents
- What the user wants to do
- Examples: `cast_spell`, `check_status`, `list_spells`

### Entities
- Specific information extracted from user input
- Examples: `spell_type=fireball`, `target=golem`

### Slots
- Memory that stores extracted entities
- Used to pass information to custom actions

### Custom Actions
- Python code that runs when triggered
- Can call external APIs, databases, or in our case, the game engine

### Stories
- Example conversations that train the dialogue model
- Show the bot what action to take after specific intents

### Rules
- Simple, always-true responses
- "If user says goodbye, always respond with utter_goodbye"

## 🔧 Customization Guide

### Add a New Spell

1. **game_engine.py:**
```python
class SpellType(Enum):
    FIREBALL = "fireball"
    POISON = "poison"  # Add new spell

self.spell_damage = {
    SpellType.FIREBALL: 30,
    SpellType.POISON: 15,  # Add damage
}

self.spell_costs = {
    SpellType.FIREBALL: 15,
    SpellType.POISON: 8,  # Add cost
}
```

2. **data/nlu.yml:**
```yaml
- intent: cast_spell
  examples: |
    - cast [poison](spell_type) on [golem](target)
    - use [poison](spell_type) against [dragon](target)
```

3. **Retrain:**
```powershell
rasa train
```

### Add a New Enemy

1. **game_engine.py:**
```python
def initialize_enemies(self):
    self.enemies = {
        "golem": Enemy("Stone Golem", 80, "lightning"),
        "troll": Enemy("Mountain Troll", 100, "fireball"),  # New enemy
    }
```

2. **data/nlu.yml:**
```yaml
- intent: cast_spell
  examples: |
    - cast [fireball](spell_type) on [troll](target)
    - attack [troll](target) with [lightning](spell_type)
```

3. **Retrain:**
```powershell
rasa train
```

## 🐛 Common Issues

### "Action server not found"
- Solution: Make sure `rasa run actions` is running in another terminal

### "Bot doesn't understand my command"
- Solution: Add more training examples to `data/nlu.yml` and retrain

### "Entity not recognized"
- Solution: Check entity annotations in `data/nlu.yml` use `[text](entity)` format

### Encoding errors with emojis
- Solution: Already fixed in `game_engine.py` with UTF-8 encoding

## 📚 Files You Should Know

| File | Purpose | When to Edit |
|------|---------|-------------|
| `game_engine.py` | Game logic | Add spells, enemies, mechanics |
| `actions/actions.py` | Connect Rasa to game | Add new game commands |
| `domain.yml` | Bot's universe | Add intents, entities, responses |
| `data/nlu.yml` | Training examples | Improve understanding |
| `data/stories.yml` | Conversation flows | Add complex dialogues |
| `config.yml` | ML configuration | Fine-tune performance |

## 🎓 What You Learned

1. **NLU (Natural Language Understanding)**
   - Intent classification
   - Entity extraction
   - Training data annotation

2. **Dialogue Management**
   - Stories for multi-turn conversations
   - Rules for simple responses
   - Policies for decision making

3. **Custom Actions**
   - Connecting Rasa to external code
   - Slot management
   - Building interactive experiences

4. **Integration**
   - Combining ML (Rasa) with traditional code (game engine)
   - Action server architecture
   - Real-time state management

## 🎉 Next Steps

- Play the game and test different commands
- Add new spells with special effects (stun, poison, etc.)
- Add player leveling system
- Create boss enemies
- Add inventory system
- Implement multiplayer features
- Deploy to a web interface or messaging platform

Have fun! 🧙‍♂️⚔️

