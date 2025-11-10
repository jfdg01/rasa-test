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

from game_engine import cast_spell, get_game_status, list_spells, reset_game, rest


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
            dispatcher.utter_message(text="❓ Which spell do you want to cast? (fireball, lightning, ice_shard, heal, shield)")
            return []

        # For healing and shield spells, target is optional
        if spell_type.lower() in ["heal", "shield"]:
            target = target or "self"
        elif not target:
            dispatcher.utter_message(text="❓ Which enemy do you want to target? (golem, dragon, zombie, skeleton, goblin)")
            return []

        # Call the game engine's cast_spell function
        result = cast_spell(spell_type, target)
        
        # Send the result back to the user
        dispatcher.utter_message(text=result)

        # Clear the slots for the next spell
        return [SlotSet("spell_type", None), SlotSet("target", None)]


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

        return []


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
        
        # Send confirmation to the user
        dispatcher.utter_message(text=result)
        
        # Also show the initial status
        status = get_game_status()
        dispatcher.utter_message(text=status)

        return []


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

        return []
