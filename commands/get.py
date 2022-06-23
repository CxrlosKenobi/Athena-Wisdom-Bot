from mongo.API import get_random_quote
from components.history import hist_handler

async def get(update, context) -> None:
  request = get_random_quote()

  while not hist_handler(request['id']):
    request = get_random_quote()

  desc = ""
  if ((request['source'] == None) or (request['source'] == 'None')):
    desc += f"~ Unknown source"

  elif (
    (request['source']['author'] != 'undefined') and
    (request['source']['book'] == 'undefined')
  ):
    desc += f"~ {request['source']['author']}"

  elif (
    (request['source']['author'] == 'undefined') and
    (request['source']['book'] != 'undefined')
  ):
    desc += f"~ [book] {request['source']['book']}"

  else:
    desc += f"~ Unknown source"


  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=f"_{request['quote']}_\n_{desc}_",
    parse_mode='Markdown'
  )
