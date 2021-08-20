import telegram
import json

# Detect the token key on the json and import it
with open('token.json') as token_file:
    token = json.load(token_file)['token']
    
bot = telegram.Bot(token=token)

bot.send_message(
    text=f'[ ! ] TESTING MESSAGE [ ! ]',
    chat_id=1908752457
    )


