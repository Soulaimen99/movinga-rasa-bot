## question
* question
    - utter_question
## faqs
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs

## more faqs
* greet
    - action_greet_user
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs

## just book
* greet
    - action_greet_user
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs
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
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs
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
* ask_faq_whatfitintruck OR ask_faq_transportinsured OR ask_faq_tutorialcore OR ask_faq_tutorialnlu OR ask_faq_transporttakelotoftime OR ask_faq_noconfirmationreceived OR ask_faq_paymentmethods OR ask_faq_helperstopmultiplelocations OR ask_faq_ordertimestart OR ask_faq_needtobeatlocation OR ask_faq_changeforgetpassword OR ask_faq_downloadapp OR ask_faq_differencehelperdriver
    - action_faqs
    - utter_ask_continue_booking
* deny
    - utter_thumbsup
    - form{"name": null}
    - utter_ask_feedback
    