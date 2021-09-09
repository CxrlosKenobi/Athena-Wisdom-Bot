def create_clock(hour=None, minute=None, m=None, user=None):
    # ↑ ↓
    keyboard = []
    now = datetime.datetime.now()
    if user:
        utc = json_utc(str(user))
    if not hour:
        hour = now.hour
        if hour > 12:
            m = "pm"
        else:
            m = "am"
        if hour > 12:
            hour -= 12
        if hour + utc > 12:
            hour += utc - 12
        elif hour + utc < 0:
            hour += utc + 12
        else:
            hour += utc

        minute = int(str(now.minute)[:-1] + "0")

    data_ignore = create_callback_clock("IGNORE", hour, minute, m)

    row = []
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-HOUR", hour, minute, m)))
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-MINUTE", hour, minute, m)))
    row.append(InlineKeyboardButton("↑", callback_data=create_callback_clock("PLUS-M", hour, minute, m)))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton(str(hour), callback_data=data_ignore))
    row.append(InlineKeyboardButton(str(minute), callback_data=data_ignore))
    row.append(InlineKeyboardButton(m, callback_data=data_ignore))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-HOUR", hour, minute, m)))
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-MINUTE", hour, minute, m)))
    row.append(InlineKeyboardButton("↓", callback_data=create_callback_clock("MINUS-M", hour, minute, m)))
    keyboard.append(row)

    row = []
    row.append(InlineKeyboardButton("OK", callback_data=create_callback_clock("OKAY", hour, minute, m)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)

def inline_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(context.bot, update)
    if selected:
        json_editor(str(update.callback_query.from_user.id), "date", date.strftime("%d/%m/%Y"))
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                        text="You selected %s" % (date.strftime("%d/%m/%Y")),
                        reply_markup=ReplyKeyboardRemove())
        context.bot.send_message(chat_id=update.callback_query.from_user.id, text="\U0001F553* Reminder Setup *\U0001F553\n\nWhich *time* do you want\nto be reminded?", parse_mode="markdown", reply_markup=telegramcalendar.create_clock(user=update.callback_query.from_user.id))
        return TIME_Q