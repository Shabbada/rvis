from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
import datetime, logging

block_chat = ['-1001652859680']

logger = logging.basicConfig(filename='rvis_secret_chat.log', level=logging.WARNING)


@Client.on_message(filters.text & filters.group, group=0)
async def printer(client, message):
    chatid = message.chat.id
    if chatid in block_chat:
        await client.leave_chat(chatid)
    
@Client.on_message(filters.private)
async def secret_chat_logger(client, message):
    user_id = message.from_user.id
    message_text = message.text 
   
    current_time = message.date.strftime('%H:%M:%S %d-%m-%Y')
    if message_text is None:
        message_text = message
    log_message = f'{current_time} - User {user_id} {message.from_user.first_name} {message.from_user.last_name}: """{message_text}""" - phone number { message.from_user.phone_number} - username {message.from_user.username}'
    logging.warn(log_message)  