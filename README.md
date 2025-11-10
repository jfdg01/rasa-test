# 🧙‍♂️ Wizard Battle Game - Rasa Chatbot

An interactive turn-based wizard battle game powered by Rasa conversational AI. Cast spells, defeat enemies, and survive the arena using natural language commands!

![Game Type](https://img.shields.io/badge/Type-RPG%20Battle-purple)
![Platform](https://img.shields.io/badge/Platform-Rasa%203.x-blue)
![Language](https://img.shields.io/badge/Language-Spanish-yellow)

## 🎮 Features

- **Natural Language Combat**: Use conversational commands to cast spells and battle enemies
- **Visual Game Interface**: Real-time battle arena with HP/mana bars and enemy status
- **Strategic Gameplay**: Exploit enemy weaknesses for critical hits
- **Multiple Spells**: Fireball, Lightning, Ice Shard, Heal, and Shield
- **5 Unique Enemies**: Each with different stats and elemental weaknesses
- **Turn-Based Combat**: Enemies counterattack after your actions

## 🎯 Game Mechanics

### Your Wizard
- **HP**: 100/100
- **Mana**: 50/50
- **Shield**: Can block one enemy attack

### Enemies
- **🗿 Stone Golem** (80 HP) - Weak to Lightning
- **🐉 Fire Dragon** (120 HP) - Weak to Ice Shard
- **🧟 Zombie** (50 HP) - Weak to Fireball
- **💀 Skeleton Warrior** (60 HP) - No weakness
- **👺 Goblin** (40 HP) - No weakness

### Spells
| Spell | Mana Cost | Damage/Effect |
|-------|-----------|---------------|
| Fireball 🔥 | 15 | 30 damage |
| Lightning ⚡ | 12 | 25 damage |
| Ice Shard ❄️ | 10 | 20 damage |
| Heal ✨ | 20 | Restore 30 HP |
| Shield 🛡️ | 15 | Block next attack |

**Tip**: Hitting an enemy's weakness deals 50% more damage!

## 🚀 Quick Start

### Prerequisites
```bash
pip install rasa
pip install -r requirements.txt
```

### Launch Game

**Terminal 1 - Start Actions Server:**
```bash
rasa run actions
```

**Terminal 2 - Start Rasa Server:**
```bash
rasa run --enable-api --cors "*"
```

**Browser - Open Game UI:**
```
Open game_ui.html in your browser
```

## 💬 Example Commands

### Combat
- `lanza bola de fuego al golem`
- `ataca al dragón con rayo`
- `usa fragmento de hielo contra el zombie`
- `lanza curar` / `cúrame`
- `usa escudo`

### Information
- `revisar estado` / `estado`
- `listar hechizos` / `hechizos disponibles`
- `ayuda`

### Game Control
- `descansar` - Restore 25 mana (enemies attack!)
- `repetir` / `de nuevo` - Repeat last action
- `reiniciar juego` - Reset game

## 📁 Project Structure

```
rasa-test/
├── actions/
│   └── actions.py          # Custom Rasa actions
├── data/
│   ├── nlu.yml            # Training data for intent recognition
│   ├── rules.yml          # Conversation rules
│   └── stories.yml        # Conversation flows
├── models/                # Trained Rasa models
├── config.yml            # Rasa pipeline configuration
├── domain.yml            # Intents, entities, slots, responses
├── endpoints.yml         # Action server configuration
├── game_engine.py        # Game logic and mechanics
├── game_ui.html          # Visual game interface
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ Development

### Train New Model
```bash
rasa train
```

### Test Conversations
```bash
rasa shell
```

### Visualize Stories
```bash
rasa visualize
```

### Run Tests
```bash
rasa test
```

## 🎨 UI Features

- **Real-time Stats**: Live HP and mana bars
- **Enemy Cards**: Visual representation with weaknesses
- **Spell Effects**: Animated spell casting
- **Damage Indicators**: Visual feedback for hits
- **Chat Interface**: Clean message display with HTML formatting

## 🧩 Technical Details

### Rasa Pipeline
- Language: Spanish (`es`)
- Tokenizer: WhitespaceTokenizer
- Featurizer: CountVectorsFeaturizer
- Intent Classifier: DIETClassifier
- Entity Extractor: DIETClassifier
- Policy: RulePolicy + TEDPolicy

### Custom Components
- **Game Engine**: Manages game state, combat, and rules
- **Custom Actions**: Bridge between Rasa and game logic
- **Web UI**: Real-time visualization with JavaScript

## 🐛 Troubleshooting

**Issue**: Changes not reflected in game
- **Solution**: Restart both `rasa run actions` and `rasa run` servers

**Issue**: "No response from bot"
- **Solution**: Ensure both servers are running on ports 5005 and 5055

**Issue**: CORS errors
- **Solution**: Make sure Rasa is running with `--cors "*"` flag

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve! Some ideas:
- Add more spells and enemies
- Implement equipment system
- Add difficulty levels
- Create multiplayer mode
- Add sound effects

---

**Made with ❤️ using Rasa and Python**

🎮 Have fun battling! May your spells hit their mark! ⚔️

