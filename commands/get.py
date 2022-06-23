from mongo.API import get_random_quote
from components.history import hist_handler

async def get(update, context) -> None:
  request = get_random_quote()

  while not hist_handler(request['id']):
    print('[get] Retrying...')
    request = get_random_quote()

  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=(
      f"""
      __{request['quote']}__
      """
    ), parse_mode='Markdown'
  )

