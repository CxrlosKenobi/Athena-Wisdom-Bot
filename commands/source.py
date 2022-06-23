#
async def info(update, context) -> None:
  source_code = "https://github.com/CxrlosKenobi/Athena-Wisdom-Bot"
  await context.bot.send_message(
    chat_id=update.effective_chat.id,
    text=(
      "*Athena's Wisdom v2.0*\n\n"
      f"Código fuente: [GitHub]({source_code})"
    ), parse_mode="Markdown"
  )
