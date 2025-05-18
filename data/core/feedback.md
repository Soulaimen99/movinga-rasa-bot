## feedback positive
* feedback{"feedback_value": "positive"}
    - slot{"feedback_value": "positive"}
    - action_save_feedback
    - utter_great
    - utter_anything_else

## feedback negative
* feedback{"feedback_value": "negative"}
    - slot{"feedback_value": "negative"}
    - action_save_feedback
    - utter_thumbsup
    - utter_anything_else
    
## feedback + message
* feedback {"feedback_message": "I like you"}
    - action_save_feedback
    - utter_anything_else
    
## feedback with no message
* feedback
    - utter_ask_feedback_message
    - action_save_feedback
    - utter_anything_else
