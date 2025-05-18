## chitchat
* human_handoff OR contact_sales
    - utter_reaching_human_agent

## greet + handoff
* greet
    - action_greet_user
* human_handoff OR contact_sales
    - utter_reaching_human_agent

## just book + handoff, continue
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* contact_sales
    - utter_contact_email
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
    - form{"name": null}
    - utter_ask_feedback

## just book + handoff, don't continue
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* contact_sales
    - utter_contact_email
    - utter_ask_continue_booking
* deny
    - utter_thumbsup
    - form{"name": null}
