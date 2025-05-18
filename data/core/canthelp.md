## chitchat
* canthelp
    - utter_canthelp
    
## out of scope
* out_of_scope
    - utter_out_of_scope

## greet + canthelp
* greet
    - action_greet_user
* canthelp
    - utter_canthelp

## greet + book + canthelp + continue
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
    - form{"name": null}

## greet + book + canthelp + don't continue
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue_booking
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
 
## book + change intent
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* change_booking OR change_booking_time OR change_booking_volume OR change_booking_requirement OR cancel_booking OR order_status
    - utter_ask_continue_booking
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
    - utter_what_help
 
## greet + change booking + canthelp + continue
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* affirm
    - utter_great
    - change_booking_form
    - form{"name": null}
    - utter_request_changes

## greet + change booking + canthelp + don't continue
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}

## greet + change booking time + canthelp + continue
* change_booking_time
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* affirm
    - utter_great
    - change_booking_form
    - form{"name": null}
    - utter_ask_time_changes

## greet + change booking time + canthelp + don't continue
* change_booking_time
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
    
## greet + change booking volume + canthelp + continue
* change_booking_volume
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* affirm
    - utter_great
    - change_booking_form
    - form{"name": null}
    - utter_ask_volume_changes

## greet + change booking volume + canthelp + don't continue
* change_booking_volume
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}

## greet + change booking requirement + canthelp + continue
* change_booking_requirement
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* affirm
    - utter_great
    - change_booking_form
    - form{"name": null}
    - utter_ask_requirement_changes

## greet + change booking requirement + canthelp + don't continue
* change_booking_requirement
    - change_booking_form
    - form{"name": "change_booking_form"}
* canthelp
    - utter_canthelp
    - utter_ask_continue
* deny
    - utter_thumbsup
    - action_deactivate_form
    - form{"name": null}
