## chitchat
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat

## deny ask_whatspossible
* ask_whatspossible
    - action_chitchat
* deny
    - utter_nohelp

## more chitchat
* greet
    - action_greet_user
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat

## ask_whatspossible
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat

## ask_whatspossible more
* greet
    - action_greet_user
* ask_whatspossible
    - action_chitchat
* ask_whatspossible
    - action_chitchat

## just book
* greet
    - action_greet_user
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt
    - action_chitchat
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
    - form{"name": null}
    - utter_ask_feedback

## just book, continue, + confirm
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat
    - utter_ask_continue_booking
* affirm
    - utter_great
    - booking_form
    - form{"name": null}
    - utter_ask_feedback

## just book, don't continue, + confirm
* greet
    - action_greet_user
* want_to_book
    - utter_moreinformation
    - booking_form
    - form{"name": "booking_form"}
* ask_weather OR ask_builder OR ask_howdoing OR ask_whoisit OR ask_whatismovinga OR ask_isbot OR ask_howold OR ask_languagesbot OR ask_restaurant OR ask_time OR ask_wherefrom OR ask_whoami OR handleinsult OR nicetomeeyou OR telljoke OR ask_whatismyname OR ask_howbuilt OR ask_whatspossible
    - action_chitchat
    - utter_ask_continue_booking
* deny
    - utter_thumbsup
    - form{"name": null}
    - utter_ask_feedback
