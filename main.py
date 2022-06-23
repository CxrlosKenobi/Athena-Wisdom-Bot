import logging
from telegram.ext import (
  ApplicationBuilder,
  CommandHandler,
  JobQueue
)
#
from components.fetch import fetch_config
from commands.source import info
from commands.get import get
from jobs.init import send_jobs


logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO
)

if __name__ == "__main__":
  bot = (
    ApplicationBuilder()
    .token(fetch_config({ 'key': 'token' }))
    .job_queue(JobQueue())
    .build()
  )
  
  job_queue = bot.job_queue
  send_jobs(job_queue)

  bot.add_handler(CommandHandler("info", info))
  bot.add_handler(CommandHandler("get", get))
  bot.run_polling()
