import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from . import tasks

COMMANDS = {
    'help': {
        'help': 'Display help message.',
    },
    'meeting': {
        'args': 2,
        'help': 'Calculate sum of two integer arguments. Example: `sum 12 32`.',
        'task': 'add'
    },
    'booking': {
        'args': 1,
        'help': 'Check website status. Example: `status twitter.com`.',
        'task': 'url_status'
    },
}

# Sentences we'll respond with if the user greeted us
MEETING_KEYWORDS = ("meeting", "booking", "presentation", )

CANCEL_MEETING_KEYWORDS = ("can't", "cancel", "won't", "busy", )

BOOKING_DETAILS = ("hdmi", "vga", "time", "projector", "am", "pm" "hour", "hours", )

CONFIRM_BOOKING = ("yes",)

CONFIRM_CANCEL = ("okay",)

bot = False

class ChatConsumer(WebsocketConsumer):
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        response_message = message
        message_parts = message.split()
        if message_parts:
            #command = message_parts[0].lower()
            # if command == 'meeting':
            
            for word in message_parts:
                if word.lower() in CONFIRM_BOOKING:
                    bot = True
                    response_message = '[BOT]: Specify date, time, number of people and equipments needed'
                
                if word.lower() in BOOKING_DETAILS:
                    bot = True
                    response_message = '[BOT]: The meeting room is booked successfully'

                if word.lower() in CONFIRM_CANCEL:
                    bot = True
                    response_message = '[BOT]: The meeting room booking has been cancelled'

                if word.lower() in MEETING_KEYWORDS:
                    bot = True
                    response_message = '[BOT]: Hello would like to book for a meeting room?'

                elif word.lower() in CANCEL_MEETING_KEYWORDS:
                    bot = True
                    response_message = '[BOT]: Hello would you like to cancel the booking for the meeting room?'
                    
                    #getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
                    #response_message = f'Command `{command}` received.'
        
        async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    'type': 'chat_message',
                    'message': response_message
                }
            )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        if bot:
            self.send(text_data=json.dumps({
                'message': f'[bot]: {message}'
            }))
        else:
            self.send(text_data=json.dumps({
                'message': f'{message}'
            }))

