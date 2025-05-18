## thanks
* thank
    - utter_noworries
    - utter_anything_else

## bye
* bye
    - utter_bye

## greet
* greet OR enter_data{"name": "sou"}
    - action_greet_user

## book
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
    - form{"name": null}
    - utter_ask_feedback
    
## book + dep + arr
* want_to_book{"location": "Munich", "location": "Passau"}
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
    - form{"name": null}
    - utter_ask_feedback
    
## greet + book
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
    - form{"name": null}
    - utter_ask_feedback
    
## book + explain
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* explain
    - action_explain_booking_form
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
    - form{"name": null}
    - utter_ask_feedback
    
## book + 2 explains
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* explain
    - action_explain_booking_form
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
* explain
    - action_explain_booking_form
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
    - form{"name": null}
    - utter_ask_feedback

## change booking + customer not found
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities
    
## change booking time + customer not found
* change_booking_time
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities
    
## change booking volume + customer not found
* change_booking_volume
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities
    
## change booking requirement + customer not found
* change_booking_requirement
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities

## change booking time
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_request_changes
* change_booking_time
    - utter_ask_time_changes
* enter_data
    - action_change_time
    
## change booking time direct
* change_booking_time
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_ask_time_changes
* enter_data
    - action_change_time

## change booking + explain
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
* explain
    - action_explain_booking_form
    - utter_ask_continue
* affirm
    - utter_great
    - change_booking_form
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_request_changes

## change booking volume
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_request_changes
* change_booking_volume
    - utter_ask_volume_changes
* enter_data{"furniture": "Sofa"}
    - action_change_volume
    
## change booking volume direct
* change_booking_volume
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_ask_volume_changes
* enter_data
    - action_change_volume

## change booking requirement
* change_booking
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_request_changes
* change_booking_requirement
    - utter_ask_requirement_changes
* enter_data
    - action_change_requirement
    
## change booking requirement direct
* change_booking_requirement
    - change_booking_form
    - form{"name": "change_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - utter_ask_requirement_changes
* enter_data
    - action_change_requirement
    
## cancel booking + affirm
* cancel_booking
    - cancel_booking_form
    - form{"name": "cancel_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
* affirm
    - action_cancel_booking
    
## cancel booking + deny
* cancel_booking
    - cancel_booking_form
    - form{"name": "cancel_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
* deny
    - utter_thumbsup

## cancel booking + explain
* cancel_booking
    - cancel_booking_form
    - form{"name": "cancel_booking_form"}
* explain
    - action_explain_booking_form
    - utter_ask_continue
* affirm
    - utter_great
    - cancel_booking_form
    - form{"name": null}
    
# cancel booking + customer not found
* cancel_booking
    - cancel_booking_form
    - form{"name": "cancel_booking_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities

## order status
*order_status
    - order_status_form
    - form{"name": "order_status_form"}
    - form{"name": null}
    - slot{"exists_in_database": "true"}
    - action_get_order_status
    
## order status + customer not found
*order_status
    - order_status_form
    - form{"name": "order_status_form"}
    - form{"name": null}
    - slot{"exists_in_database": "false"}
    - utter_customer_not_found
    - utter_possibilities
    
## anything else? - yes
#* affirm
#    - utter_what_help

## anything else? - no
* deny
    - utter_thumbsup

## anything else?
* enter_data
    - utter_not_sure
    - utter_possibilities

## positive reaction
* react_positive
    - utter_react_positive

## negative reaction
* react_negative
    - utter_react_negative