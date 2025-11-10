# 🧙 Wizard Game - Rasa Chatbot

A conversational AI wizard game built with Rasa Open Source! Battle enemies using natural language spell-casting commands.

## 🎮 Game Overview

You're a wizard battling various enemies using spells. Tell the bot what spell to cast and which enemy to target, and watch the battle unfold!

### Available Spells
- **Fireball** (15 mana) - 30 damage 🔥
- **Lightning** (12 mana) - 25 damage ⚡
- **Ice Shard** (10 mana) - 20 damage ❄️
- **Heal** (20 mana) - Restore 30 HP ✨
- **Shield** (15 mana) - Block next attack 🛡️

### Enemies
- **Stone Golem** - 80 HP (Weak to lightning)
- **Fire Dragon** - 120 HP (Weak to ice shard)
- **Zombie** - 50 HP (Weak to fireball)
- **Skeleton Warrior** - 60 HP
- **Goblin** - 40 HP

## 🚀 Getting Started

### Prerequisites
- Python 3.10.11 (managed by pyenv-win)
- Rasa 3.6.21

### Installation

1. **Activate the virtual environment:**
```powershell
.\venv\Scripts\Activate.ps1
```

2. **Train the model** (if not already trained):
```powershell
rasa train
```

### Running the Game

You need to run TWO terminals:

#### Terminal 1: Action Server
This runs the game engine and custom actions.

```powershell
.\venv\Scripts\Activate.ps1
rasa run actions
```

Keep this running in the background.

#### Terminal 2: Rasa Shell
This is where you interact with the bot.

```powershell
.\venv\Scripts\Activate.ps1
rasa shell
```

## 🎯 How to Play

### Example Commands

**Greet the wizard:**
```
You: hello
Bot: 🧙 Welcome, Wizard! Ready to battle some enemies?
```

**Check game status:**
```
You: check status
Bot: 🧙 Your Status:
     HP: 100/100 | Mana: 50/50
     
     ⚔️ Enemies:
     • Stone Golem: 80/80 HP (Weak to lightning)
     • Fire Dragon: 120/120 HP (Weak to ice_shard)
     ...
```

**List available spells:**
```
You: list spells
Bot: 📜 Available Spells:
     • Fireball (15 mana) - 30 damage 🔥
     • Lightning (12 mana) - 25 damage ⚡
     ...
```

**Cast spells:**
```
You: cast fireball on golem
Bot: 🔥 You cast Fireball on Stone Golem!
     Stone Golem takes 28 damage! HP: 52/80
     Mana: 35/50

You: throw lightning at dragon
Bot: ⚡ You cast Lightning on Fire Dragon!
     Fire Dragon takes 24 damage! HP: 96/120
     Mana: 23/50

You: use ice shard against zombie
Bot: ❄️ You cast Ice Shard on Zombie!
     Zombie takes 19 damage! HP: 31/50
     Mana: 13/50
```

**Healing and defense:**
```
You: cast heal
Bot: ✨ You cast Heal! Restored 30 HP. HP: 100/100

You: cast shield
Bot: 🛡️ You cast Shield! You are protected for the next attack.
```

**Rest to restore mana:**
```
You: rest
Bot: 🧘 You take a moment to rest and meditate...
     ✨ Restored 25 mana! Mana: 48/50
     ⚠️ Warning: Enemies may attack while you rest!

You: meditate
Bot: 🧘 You take a moment to rest and meditate...
     ✨ Restored 25 mana! Mana: 50/50
```

**Reset the game:**
```
You: reset game
Bot: 🎮 Game reset! A new adventure begins!
```

## 📁 Project Structure

```
rasa-test/
├── game_engine.py          # Game logic and spell-casting mechanics
├── actions/
│   └── actions.py          # Custom Rasa actions that interface with game_engine
├── data/
│   ├── nlu.yml            # Training data for intent recognition
│   ├── stories.yml        # Conversation flow examples
│   └── rules.yml          # Simple rule-based responses
├── domain.yml             # Bot's domain (intents, entities, responses, actions)
├── config.yml             # NLU pipeline and policy configuration
├── endpoints.yml          # Action server endpoint configuration
└── models/                # Trained models
```

## 🔧 Technical Details

### How It Works

1. **User Input:** "cast fireball on golem"
2. **NLU Processing:** Rasa identifies:
   - Intent: `cast_spell`
   - Entities: `spell_type=fireball`, `target=golem`
3. **Dialogue Management:** Rasa decides to execute `action_cast_spell`
4. **Custom Action:** `ActionCastSpell` in `actions/actions.py` calls `game_engine.cast_spell()`
5. **Game Logic:** `game_engine.py` processes the spell, calculates damage, updates game state
6. **Response:** Bot sends result back to user

### Key Files to Modify

**To add new spells:**
1. Add to `game_engine.py` (spell damage, mana cost, logic)
2. Add training examples to `data/nlu.yml`
3. Retrain: `rasa train`

**To add new enemies:**
1. Add to `game_engine.py` in `initialize_enemies()`
2. Add training examples to `data/nlu.yml`
3. Retrain: `rasa train`

**To add new game mechanics:**
1. Implement in `game_engine.py`
2. Create custom action in `actions/actions.py`
3. Add to `domain.yml` (new intents, actions, responses)
4. Add training data to `data/nlu.yml` and `data/stories.yml`
5. Retrain: `rasa train`

## 🎲 Game Mechanics

- **Elemental Weakness:** Exploit enemy weaknesses for 1.5x damage!
- **Mana Management:** Each spell costs mana. Plan your attacks wisely!
- **Rest to Recover:** Run out of mana? Use `rest` or `meditate` to restore 25 mana!
- **Critical Hits:** Damage has slight randomness (90%-110% of base)
- **Victory Condition:** Defeat all enemies!

## 🐛 Troubleshooting

**Action server not responding:**
- Make sure `rasa run actions` is running in a separate terminal
- Check that `endpoints.yml` has `action_endpoint` uncommented

**Bot doesn't recognize commands:**
- Train the model: `rasa train`
- Add more training examples to `data/nlu.yml`

**Import errors:**
- Make sure you're in the project directory
- Verify `game_engine.py` is in the root directory

## 📝 Example Full Game Session

```
You: hello
Bot: 🧙 Welcome, Wizard! Ready to battle some enemies?

You: check status
Bot: 🧙 Your Status:
     HP: 100/100 | Mana: 50/50
     ⚔️ Enemies: (5 alive)

You: list spells
Bot: 📜 Available Spells: (shows all spells)

You: cast lightning on golem
Bot: ⚡ You cast Lightning on Stone Golem!
     💥 CRITICAL HIT! Exploited weakness!
     Stone Golem takes 38 damage! HP: 42/80

You: cast lightning on golem
Bot: ⚡ You cast Lightning on Stone Golem!
     💥 CRITICAL HIT! Exploited weakness!
     Stone Golem has been defeated! 💀

You: check status
Bot: 🧙 Your Status:
     HP: 100/100 | Mana: 26/50
     ⚔️ Enemies: (4 alive)
     💀 Defeated: Stone Golem

You: goodbye
Bot: 🧙 May your spells be ever powerful! Farewell, wizard!
```

## 🧰 Development

### Training
```powershell
rasa train
```

### Testing
```powershell
rasa test
```

### Interactive Learning
```powershell
rasa interactive
```

### Data Validation
```powershell
rasa data validate
```

## 📚 Resources

- [Rasa Documentation](https://rasa.com/docs/rasa/)
- [Rasa Forum](https://forum.rasa.com/)
- [Custom Actions Guide](https://rasa.com/docs/rasa/custom-actions)

## 🎉 Have Fun!

Now go forth and vanquish your enemies with the power of conversational AI! 🧙‍♂️⚔️🐉

