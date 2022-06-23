import logging
from telegram import Update 
from telegram.ext import (
  ApplicationBuilder,
  CommandHandler
)
#
from components.fetch import fetch_token
from commands.source import info
from commands.get import get


logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO
)

if __name__ == "__main__":
  bot = (
    ApplicationBuilder()
    .token(fetch_token())
    .build()
  )

  bot.add_handler(CommandHandler("info", info))
  bot.add_handler(CommandHandler("get", get))
  bot.run_polling()
