# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sys
import os

# Add the parent directory to the path so we can import game_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import cast_spell, get_game_status, list_spells, rest, reset_game


class ActionCastSpell(Action):
    """Custom action to cast a spell on a target"""

    def name(self) -> Text:
        return "action_cast_spell"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the spell_type and target entities from the user's message
        spell_type = tracker.get_slot("spell_type")
        target = tracker.get_slot("target")

        # If spell type is not provided, ask for it
        if not spell_type:
            dispatcher.utter_message(text="❓ ¿Qué hechizo quieres lanzar? (bola_fuego, rayo, fragmento_hielo, curar, escudo)")
            return []

        # For healing and shield spells, target is optional
        if spell_type.lower() in ["curar", "escudo", "heal", "shield"]:
            target = target or "self"
        elif not target:
            dispatcher.utter_message(text="❓ ¿A qué enemigo quieres atacar? (golem, dragon, zombie, esqueleto, goblin)")
            return []

        # Call the game engine's cast_spell function
        result = cast_spell(spell_type, target)
        
        # Send the result back to the user
        dispatcher.utter_message(text=result)

        # Save this action for repeat functionality
        return [
            SlotSet("spell_type", None), 
            SlotSet("target", None),
            SlotSet("last_action", "cast_spell"),
            SlotSet("last_spell_type", spell_type),
            SlotSet("last_target", target)
        ]


class ActionCheckStatus(Action):
    """Custom action to check game status"""

    def name(self) -> Text:
        return "action_check_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the game status from the game engine
        status = get_game_status()
        
        # Send the status to the user
        dispatcher.utter_message(text=status)

        # Save this action for repeat functionality
        return [
            SlotSet("last_action", "check_status"),
            SlotSet("last_spell_type", None),
            SlotSet("last_target", None)
        ]


class ActionListSpells(Action):
    """Custom action to list available spells"""

    def name(self) -> Text:
        return "action_list_spells"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the spell list from the game engine
        spells = list_spells()
        
        # Send the spell list to the user
        dispatcher.utter_message(text=spells)

        # Save this action for repeat functionality
        return [
            SlotSet("last_action", "list_spells"),
            SlotSet("last_spell_type", None),
            SlotSet("last_target", None)
        ]


class ActionRest(Action):
    """Custom action to rest and restore mana"""

    def name(self) -> Text:
        return "action_rest"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Rest to restore mana
        result = rest()
        
        # Send the result to the user
        dispatcher.utter_message(text=result)

        # Save this action for repeat functionality
        return [
            SlotSet("last_action", "rest"),
            SlotSet("last_spell_type", None),
            SlotSet("last_target", None)
        ]


class ActionRepeatLast(Action):
    """Custom action to repeat the last action"""

    def name(self) -> Text:
        return "action_repeat_last"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the last action from slots
        last_action = tracker.get_slot("last_action")
        
        if not last_action:
            dispatcher.utter_message(text="❓ No hay acción previa para repetir. ¡Intenta lanzar un hechizo primero!")
            return []
        
        # Repeat based on the last action type
        if last_action == "cast_spell":
            last_spell = tracker.get_slot("last_spell_type")
            last_target = tracker.get_slot("last_target")
            
            if last_spell:
                result = cast_spell(last_spell, last_target)
                dispatcher.utter_message(text=f"🔁 Repitiendo: lanzando {last_spell} a {last_target}<br><br>{result}")
                
                # Keep the same last_action slots
                return [
                    SlotSet("last_action", "cast_spell"),
                    SlotSet("last_spell_type", last_spell),
                    SlotSet("last_target", last_target)
                ]
        
        elif last_action == "rest":
            result = rest()
            dispatcher.utter_message(text=f"🔁 Repitiendo: descansando<br><br>{result}")
            return [SlotSet("last_action", "rest")]
        
        elif last_action == "check_status":
            status = get_game_status()
            dispatcher.utter_message(text=f"🔁 Repitiendo: revisando estado<br><br>{status}")
            return [SlotSet("last_action", "check_status")]
        
        elif last_action == "list_spells":
            spells = list_spells()
            dispatcher.utter_message(text=f"🔁 Repitiendo: listando hechizos<br><br>{spells}")
            return [SlotSet("last_action", "list_spells")]
        
        else:
            dispatcher.utter_message(text="❓ No se puede repetir esa acción.")
            return []


class ActionResetGame(Action):
    """Custom action to reset the game"""

    def name(self) -> Text:
        return "action_reset_game"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Reset the game
        result = reset_game()
        
        # Send confirmation to the user with a special metadata for UI reset
        dispatcher.utter_message(
            text=result + "<br><br>🔄 La conversación se ha reiniciado."
        )
        
        # Also show the initial status
        status = get_game_status()
        dispatcher.utter_message(text=status)

        return []
