# Movinga Chatbot

A conversational AI assistant for Movinga, a moving services company. This chatbot helps users book moving services, manage their bookings, and get answers to frequently asked questions.

## Features

- **Booking Management**: Book a moving service, change booking details, cancel bookings, and check order status
- **FAQ Handling**: Answer common questions about Movinga's services
- **Multilingual Support**: Available in English, German, and French
- **Small Talk**: Engage in casual conversation with users

## Project Structure

- `actions/`: Custom action code
- `data/`: Training data for the chatbot
  - `core/`: Conversation flow training data
  - `nlu/`: Natural language understanding training data
  - `images/`: Images used by the chatbot
- `models/`: Trained model files
- `output/`: Output data files (bookings, feedback, etc.)

## Setup

### Prerequisites

- Python 3.7+
- MySQL database

### Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up the database:
   - Create a MySQL database named "movingabot"
   - Update database credentials in `actions/database.py` if needed

### Running the Chatbot

1. Start the action server:
   ```
   python -m rasa_sdk --actions actions
   ```

2. Train the model:
   ```
   rasa train
   ```

3. Start the Rasa server:
   ```
   rasa run --endpoints endpoints.yml --cors="*"
   ```

4. To interact with the chatbot in the command line:
   ```
   rasa shell
   ```

## Development

### Adding Training Data

- Add NLU examples in `data/nlu/nlu.md`
- Add conversation flows in `data/core/stories.md`
- Update responses in `domain.yml`

### Custom Actions

Custom actions are defined in `actions/actions.py`. To add a new action:

1. Create a new class that inherits from `Action`
2. Implement the required methods
3. Add the action to the `actions` list in `domain.yml`

## License

This project is proprietary and confidential.

## Credits

Developed as part of a master's thesis project.
