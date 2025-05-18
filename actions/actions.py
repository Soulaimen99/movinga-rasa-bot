# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
from typing import Text, Dict, Any, List, Optional, Union, Tuple

from dotenv import load_dotenv
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, UserUtteranceReverted, ConversationPaused, ConversationResumed, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.database import Database

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class Functions:
    """Utility functions for the chatbot actions"""

    @staticmethod
    def save_data(file_path: str, data: List[Any]) -> List:
        """
        Save data to a CSV file

        Args:
            file_path: Path to the CSV file
            data: List of data to save

        Returns:
            Empty list for compatibility with Rasa actions
        """
        import csv
        import os

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, mode='a', newline='') as data_file:
                data_writer = csv.writer(data_file, delimiter=',')
                data_writer.writerow(data)
                logger.info(f"Data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data to {file_path}: {e}")

        return []

    @staticmethod
    def get_slots(tracker: Tracker, requested_slots: List[str]) -> List[Any]:
        """
        Get values of requested slots from the tracker

        Args:
            tracker: Rasa conversation tracker
            requested_slots: List of slot names to retrieve

        Returns:
            List of slot values in the same order as requested_slots
        """
        slots = []
        for slot in requested_slots:
            slot_value = tracker.get_slot(slot)
            slots.append(slot_value)

        return slots


class BookingForm(FormValidationAction):
    """Form action for booking a moving service"""

    def name(self) -> Text:
        return "validate_booking_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Return the list of slots that the form has to fill"""

        # Check if we have locations from entities
        entities = tracker.latest_message.get("entities", [])
        locations = [
            e["value"] for e in entities 
            if e.get("entity") in ["location", "LOC"]
        ]

        if len(locations) >= 2:
            logger.info(f"Found locations in message: {locations}")
            # We already have departure and arrival, so we don't need to ask for them
            return ["date", "name", "volume", "phone_number", "email"]

        # Default required slots
        return ["departure", "arrival", "date", "name", "volume", "phone_number", "email"]

    async def extract_departure(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Extract the departure location from entities"""

        # Check for location entities
        entities = tracker.latest_message.get("entities", [])
        locations = [
            e["value"] for e in entities 
            if e.get("entity") in ["location", "LOC"]
        ]

        if len(locations) >= 1:
            return {"departure": locations[0]}

        # No location found
        return {}

    async def extract_arrival(
        self, 
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Extract the arrival location from entities"""

        # Check for location entities
        entities = tracker.latest_message.get("entities", [])
        locations = [
            e["value"] for e in entities 
            if e.get("entity") in ["location", "LOC"]
        ]

        if len(locations) >= 2:
            return {"arrival": locations[1]}

        # No second location found
        return {}

    async def validate_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate date value"""

        if not slot_value:
            dispatcher.utter_message("Please provide a valid date for your move.")
            return {"date": None}

        return {"date": slot_value}

    async def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email value"""

        if not slot_value or "@" not in slot_value:
            dispatcher.utter_message("Please provide a valid email address.")
            return {"email": None}

        return {"email": slot_value}


class SubmitBookingForm(Action):
    """Action to submit the booking form"""

    def name(self) -> Text:
        return "action_submit_booking_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit the booking form"""

        # Get the required slots
        required_slots = [
            "departure", "arrival", "date", "name", "volume", "phone_number", "email"
        ]
        slots = Functions.get_slots(tracker, required_slots)

        # Add current date and order status
        current_date = datetime.datetime.now()
        slots.append(current_date)
        order_status = "created"
        slots.append(order_status)

        # Save to CSV
        Functions.save_data("output/booking.csv", slots)

        # Check if customer already exists
        customer = Functions.get_slots(tracker, ["name", "phone_number"])
        db = Database()

        if not db.exist_in_db(customer):
            # Write to database
            db.write_to_db(slots)
            dispatcher.utter_message(response="utter_book")
        else:
            dispatcher.utter_message("Sorry, but you already have a booking!")

        return []


class ChangeBookingForm(FormValidationAction):
    """Form action for changing a booking"""

    def name(self) -> Text:
        return "validate_change_booking_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Return the list of slots that the form has to fill"""
        return ["name", "phone_number"]

    async def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value"""

        if not slot_value or len(slot_value) < 2:
            dispatcher.utter_message("Please provide a valid name.")
            return {"name": None}

        return {"name": slot_value}

    async def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone number value"""

        if not slot_value:
            dispatcher.utter_message("Please provide a valid phone number.")
            return {"phone_number": None}

        return {"phone_number": slot_value}


class SubmitChangeBookingForm(Action):
    """Action to submit the change booking form"""

    def name(self) -> Text:
        return "action_submit_change_booking_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit the change booking form"""

        # Get customer information
        required_slots = ["name", "phone_number"]
        customer = Functions.get_slots(tracker, required_slots)

        # Check if customer exists in database
        db = Database()
        exists_in_database = "false"

        if db.exist_in_db(customer):
            exists_in_database = "true"
            logger.info(f"Customer found in database: {customer[0]} ({customer[1]})")
        else:
            logger.info(f"Customer not found in database: {customer[0]} ({customer[1]})")

        return [SlotSet("exists_in_database", exists_in_database)]


class CancelBookingForm(FormValidationAction):
    """Form action for canceling a booking"""

    def name(self) -> Text:
        return "validate_cancel_booking_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Return the list of slots that the form has to fill"""
        return ["name", "phone_number"]

    async def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value"""

        if not slot_value or len(slot_value) < 2:
            dispatcher.utter_message("Please provide a valid name.")
            return {"name": None}

        return {"name": slot_value}

    async def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone number value"""

        if not slot_value:
            dispatcher.utter_message("Please provide a valid phone number.")
            return {"phone_number": None}

        return {"phone_number": slot_value}


class SubmitCancelBookingForm(Action):
    """Action to submit the cancel booking form"""

    def name(self) -> Text:
        return "action_submit_cancel_booking_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit the cancel booking form"""

        # Get customer information
        required_slots = ["name", "phone_number"]
        customer = Functions.get_slots(tracker, required_slots)

        # Check if customer exists in database
        db = Database()
        exists_in_database = "false"

        if db.exist_in_db(customer):
            exists_in_database = "true"
            logger.info(f"Customer found in database for cancellation: {customer[0]} ({customer[1]})")
        else:
            logger.info(f"Customer not found in database for cancellation: {customer[0]} ({customer[1]})")

        return [SlotSet("exists_in_database", exists_in_database)]


class OrderStatusForm(FormValidationAction):
    """Form action for checking order status"""

    def name(self) -> Text:
        return "validate_order_status_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Return the list of slots that the form has to fill"""
        return ["name", "phone_number"]

    async def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value"""

        if not slot_value or len(slot_value) < 2:
            dispatcher.utter_message("Please provide a valid name.")
            return {"name": None}

        return {"name": slot_value}

    async def validate_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone number value"""

        if not slot_value:
            dispatcher.utter_message("Please provide a valid phone number.")
            return {"phone_number": None}

        return {"phone_number": slot_value}


class SubmitOrderStatusForm(Action):
    """Action to submit the order status form"""

    def name(self) -> Text:
        return "action_submit_order_status_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit the order status form"""

        # Get customer information
        required_slots = ["name", "phone_number"]
        customer = Functions.get_slots(tracker, required_slots)

        # Check if customer exists in database
        db = Database()
        exists_in_database = "false"

        if db.exist_in_db(customer):
            exists_in_database = "true"
            logger.info(f"Customer found in database for order status: {customer[0]} ({customer[1]})")
        else:
            logger.info(f"Customer not found in database for order status: {customer[0]} ({customer[1]})")

        return [SlotSet("exists_in_database", exists_in_database)]


class SalesForm(FormValidationAction):
    """Form action for collecting sales information"""

    def name(self) -> Text:
        return "validate_sales_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Text]:
        """Return the list of slots that the form has to fill"""
        return [
            "job_function",
            "budget",
            "name",
            "company",
            "business_email",
        ]

    async def validate_job_function(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate job function value"""

        if not slot_value:
            dispatcher.utter_message("Please provide your job function.")
            return {"job_function": None}

        return {"job_function": slot_value}

    async def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate budget value"""

        if not slot_value:
            dispatcher.utter_message("Please provide your budget.")
            return {"budget": None}

        return {"budget": slot_value}

    async def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value"""

        if not slot_value or len(slot_value) < 2:
            dispatcher.utter_message("Please provide a valid name.")
            return {"name": None}

        return {"name": slot_value}

    async def validate_company(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate company value"""

        if not slot_value:
            dispatcher.utter_message("Please provide your company name.")
            return {"company": None}

        return {"company": slot_value}

    async def validate_business_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate business email value"""

        # Check if an email entity was picked up
        if not slot_value or "@" not in slot_value:
            dispatcher.utter_message(response="utter_no_email")
            return {"business_email": None}

        return {"business_email": slot_value}


class SubmitSalesForm(Action):
    """Action to submit the sales form"""

    def name(self) -> Text:
        return "action_submit_sales_form"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Submit the sales form"""

        # Get sales information from slots
        budget = tracker.get_slot("budget")
        company = tracker.get_slot("company")
        email = tracker.get_slot("business_email")
        job_function = tracker.get_slot("job_function")
        name = tracker.get_slot("name")
        date = datetime.datetime.now().strftime("%d/%m/%Y")

        # Prepare and save sales information
        sales_info = [company, budget, date, name, job_function, email]
        Functions.save_data("output/data.csv", sales_info)

        logger.info(f"Sales information saved for {name} ({email}) from {company}")

        # Confirm to the user
        dispatcher.utter_message(response="utter_confirm_salesrequest")

        return []


class ActionChangeVolume(Action):
    """Action to change the volume of a booking"""

    def name(self) -> Text:
        return "action_change_volume"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Change the volume of a booking"""

        # Get the volume from entities or text
        volume = next(
            tracker.get_latest_entity_values("furniture"), 
            tracker.latest_message.get("text")
        )

        # Get customer information
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone_number")
        current_date = datetime.datetime.now()

        # Update the database
        db = Database()
        data = [name, phone, volume, current_date]
        db.update_db(data, "volume")

        logger.info(f"Changed volume to '{volume}' for {name} ({phone})")

        # Confirm to the user
        dispatcher.utter_message("Your moving volume is changed successfully")

        return []


class ActionChangeTime(Action):
    """Action to change the time of a booking"""

    def name(self) -> Text:
        return "action_change_time"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Change the time of a booking"""

        # Get the time from entities or text
        time = next(
            tracker.get_latest_entity_values("time"), 
            tracker.latest_message.get("text")
        )

        # Get customer information
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone_number")
        current_date = datetime.datetime.now()

        # Update the database
        db = Database()
        data = [name, phone, time, current_date]
        db.update_db(data, "time")

        logger.info(f"Changed time to '{time}' for {name} ({phone})")

        # Confirm to the user
        dispatcher.utter_message("Your moving time is changed successfully")

        return []


class ActionCancelBooking(Action):
    """Action to cancel a booking"""

    def name(self) -> Text:
        return "action_cancel_booking"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Cancel a booking"""

        # Get customer information
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone_number")
        order_status = "cancelled"
        current_date = datetime.datetime.now()

        # Update the database
        db = Database()
        data = [name, phone, order_status, current_date]
        db.update_db(data, "cancel")

        logger.info(f"Cancelled booking for {name} ({phone})")

        # Confirm to the user
        dispatcher.utter_message("Your booking is canceled successfully")

        return []


class GetOrderStatus(Action):
    """Action to get the status of an order"""

    def name(self) -> Text:
        return "action_get_order_status"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Get the status of an order"""

        # Get customer information
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone_number")

        # Get order status from database
        db = Database()
        order_status = db.order_status(name, phone)

        if order_status:
            logger.info(f"Retrieved order status for {name} ({phone}): {order_status}")
            dispatcher.utter_message(f"Your order status is: {order_status}")
        else:
            logger.info(f"No order status found for {name} ({phone})")
            dispatcher.utter_message("Sorry, we couldn't find any order for you.")

        return []


class ActionChangeRequirement(Action):

    def name(self):
        return "action_change_requirement"

    def run(self, dispatcher, tracker, domain):
        requirement = tracker.latest_message.get("text")
        name = tracker.get_slot("name")
        phone = tracker.get_slot("phone_number")
        currentdate = datetime.datetime.now()
        db = Database()
        data = [name, phone, requirement, currentdate]
        db.update_db(data, "requirement")
        dispatcher.utter_message("Your moving requirements are changed successfully")
        return [SlotSet("requirement", requirement)]


class ActionSaveFeedback(Action):

    def name(self):
        return "action_save_feedback"

    def run(self, dispatcher, tracker, domain):
        feedback_message = tracker.get_slot("feedback_message")
        if not feedback_message:
            feedback_message = tracker.latest_message.get("text")
        feedback_value = tracker.get_slot("feedback_value")
        name = tracker.get_slot("name")
        currentdate = datetime.datetime.now()
        data = [name, feedback_value, feedback_message, currentdate]
        Functions.save_data("output/feedback.csv", data)
        dispatcher.utter_template("utter_thanks_for_feedback", tracker)
        return []


class ActionExplainSalesForm(Action):

    def name(self):
        return "action_explain_booking_form"

    def run(self, dispatcher, tracker, domain):
        requested_slot = tracker.get_slot("requested_slot")

        if requested_slot not in BookingForm.required_slots(tracker):
            dispatcher.utter_message(
                "Sorry, I didn't get that. Please rephrase or answer the question "
                "above."
            )
            return []

        dispatcher.utter_template("utter_explain_" + requested_slot, tracker)
        return []


class ActionChitchat(Action):

    def name(self):
        return "action_chitchat"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_builder",
            "ask_weather",
            "ask_howdoing",
            "ask_whatspossible",
            "ask_whatismovinga",
            "ask_isbot",
            "ask_howold",
            "ask_languagesbot",
            "ask_restaurant",
            "ask_time",
            "ask_wherefrom",
            "ask_whoami",
            "handleinsult",
            "nicetomeeyou",
            "telljoke",
            "ask_whatismyname",
            "ask_howbuilt",
            "ask_whoisit",
        ]:
            dispatcher.utter_template("utter_" + intent, tracker)
        return []


class ActionFaqs(Action):

    def name(self):
        return "action_faqs"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if intent in [
            "ask_faq_whatfitintruck",
            "ask_faq_transportinsured",
            "ask_faq_tutorialcore",
            "ask_faq_tutorialnlu",
            "ask_faq_transporttakelotoftime",
            "ask_faq_noconfirmationreceived",
            "ask_faq_paymentmethods",
            "ask_faq_helperstopmultiplelocations",
            "ask_faq_ordertimestart",
            "ask_faq_needtobeatlocation",
            "ask_faq_changeforgetpassword",
            "ask_faq_downloadapp",
            "ask_faq_differencehelperdriver",
        ]:
            dispatcher.utter_template("utter_" + intent, tracker)
        return []


class ActionPause(Action):
    """Pause the conversation"""

    def name(self):
        return "action_pause"

    def run(self, dispatcher, tracker, domain):
        return [ConversationPaused()]


class ActionStoreUnknownProduct(Action):
    """Stores unknown tools people are migrating from in a slot"""

    def name(self):
        return "action_store_unknown_product"

    def run(self, dispatcher, tracker, domain):
        # if we dont know the product the user is migrating from,
        # store his last message in a slot.
        return [SlotSet("unknown_product", tracker.latest_message.get("text"))]


class ActionStoreUnknownNluPart(Action):
    """Stores unknown parts of nlu which the user requests information on
       in slot.
    """

    def name(self):
        return "action_store_unknown_nlu_part"

    def run(self, dispatcher, tracker, domain):
        # if we dont know the part of nlu the user wants information on,
        # store his last message in a slot.
        return [SlotSet("unknown_nlu_part", tracker.latest_message.get("text"))]


class ActionStoreBotLanguage(Action):
    """Takes the bot language and checks what pipelines can be used"""

    def name(self):
        return "action_store_bot_language"

    def run(self, dispatcher, tracker, domain):
        spacy_languages = [
            "english",
            "french",
            "german",
            "spanish",
            "portuguese",
            "french",
            "italian",
            "dutch",
        ]
        language = tracker.get_slot("language")
        if not language:
            return [
                SlotSet("language", "that language"),
                SlotSet("can_use_spacy", False),
            ]

        if language in spacy_languages:
            return [SlotSet("can_use_spacy", True)]
        else:
            return [SlotSet("can_use_spacy", False)]


class ActionStoreEntityExtractor(Action):
    """Takes the entity which the user wants to extract and checks
        what pipelines can be used.
    """

    def name(self):
        return "action_store_entity_extractor"

    def run(self, dispatcher, tracker, domain):
        spacy_entities = ["place", "date", "name", "organisation"]
        duckling = [
            "money",
            "duration",
            "distance",
            "ordinals",
            "time",
            "amount-of-money",
            "numbers",
            "date",
        ]

        entity_to_extract = next(tracker.get_latest_entity_values("entity"), None)

        extractor = "CRFEntityExtractor"
        if entity_to_extract in spacy_entities:
            extractor = "SpacyEntityExtractor"
        elif entity_to_extract in duckling:
            extractor = "DucklingHTTPExtractor"

        return [SlotSet("entity_extractor", extractor)]


class SuggestionForm(FormAction):
    """Accept free text input from the user for suggestions"""

    def name(self):
        return "suggestion_form"

    @staticmethod
    def required_slots(tracker):
        return ["suggestion"]

    def slot_mappings(self):
        return {"suggestion": self.from_text()}

    def submit(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_thank_suggestion", tracker)
        return []


class ActionStoreProblemDescription(Action):
    """Stores the problem description in a slot."""

    def name(self):
        return "action_store_problem_description"

    def run(self, dispatcher, tracker, domain):
        problem = tracker.latest_message.get("text")

        return [SlotSet("problem_description", problem)]


class ActionGreetUser(Action):
    """Greets the user"""

    def name(self):
        return "action_greet_user"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message["intent"].get("name")
        name_entity = next(tracker.get_latest_entity_values("name"), None)
        if intent == "greet":
            if name_entity:
                dispatcher.utter_template("utter_greet_name", tracker, name=name_entity)
                return []
            else:
                dispatcher.utter_template("utter_greet", tracker)
                return []
        return []


import requests


class ActionTalkToHuman(Action):

    def name(self):
        return "action_talk_to_human"

    def run(self, dispatcher, tracker, domain):
        response = "Reaching out to a human agent [{}]...".format(tracker.sender_id)
        dispatcher.utter_message(response)
        #ConversationPaused()
        message = ""
        if message != "unpause":
            url = "http://127.0.0.1:5000/handoff/{}".format(tracker.sender_id)
            req = requests.get(url)
            resp = json.loads(req.text)
            if "error" in resp:
                raise Exception("Error fetching message: " + repr(resp["error"]))
            message = resp["message"]
            #if message != "unpause":
            dispatcher.utter_message("Human agent: {}".format(message))
            return(FollowupAction("action_talk_to_human"))
        else:
            return []


class ActionDefaultAskAffirmation(Action):
    """Asks for an affirmation of the intent if NLU threshold is not met."""

    def name(self) -> Text:
        return "action_default_ask_affirmation"

    def __init__(self) -> None:
        import pandas as pd

        self.intent_mappings = pd.read_csv("actions/intent_description_mapping.csv")
        self.intent_mappings.fillna("", inplace=True)
        self.intent_mappings.entities = self.intent_mappings.entities.map(
            lambda entities: {e.strip() for e in entities.split(",")}
        )

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List["Event"]:

        intent_ranking = tracker.latest_message.get("intent_ranking", [])
        if len(intent_ranking) > 1:
            diff_intent_confidence = intent_ranking[0].get(
                "confidence"
            ) - intent_ranking[1].get("confidence")
            if diff_intent_confidence < 0.2:
                intent_ranking = intent_ranking[:2]
            else:
                intent_ranking = intent_ranking[:1]
        first_intent_names = [
            intent.get("name", "")
            for intent in intent_ranking
            if intent.get("name", "") != "out_of_scope"
        ]

        message_title = (
            "Sorry, I'm not sure I've understood " "you correctly 🤔 Do you mean..."
        )

        entities = tracker.latest_message.get("entities", [])
        entities = {e["entity"]: e["value"] for e in entities}

        entities_json = json.dumps(entities)

        buttons = []
        for intent in first_intent_names:
            logger.debug(intent)
            logger.debug(entities)
            buttons.append(
                {
                    "title": self.get_button_title(intent, entities),
                    "payload": "/{}{}".format(intent, entities_json),
                }
            )

        buttons.append({"title": "Something else", "payload": "/out_of_scope"})

        dispatcher.utter_button_message(message_title, buttons=buttons)

        return []

    def get_button_title(self, intent: Text, entities: Dict[Text, Text]) -> Text:
        default_utterance_query = self.intent_mappings.intent == intent
        utterance_query = (
                self.intent_mappings.entities == entities.keys() & default_utterance_query
        )

        utterances = self.intent_mappings[utterance_query].button.tolist()

        if len(utterances) > 0:
            button_title = utterances[0]
        else:
            utterances = self.intent_mappings[default_utterance_query].button.tolist()
            button_title = utterances[0] if len(utterances) > 0 else intent

        return button_title.format(**entities)


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List["Event"]:

        # Fallback caused by TwoStageFallbackPolicy
        if (
                len(tracker.events) >= 4
                and tracker.events[-4].get("name") == "action_default_ask_affirmation"
        ):

            dispatcher.utter_template("utter_restart_with_button", tracker)

            return [SlotSet("feedback_value", "negative"), ConversationPaused()]

        # Fallback caused by Core
        else:
            dispatcher.utter_template("utter_default", tracker)
            return [UserUtteranceReverted()]
