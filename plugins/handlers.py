from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pydub import AudioSegment
import datetime, logging

import openai

logging.basicConfig(filename='rvis.log', level=logging.INFO)
status = "uxlayabman"
bot_run = True
def convert_ogg_to_mp3(ogg_path, mp3_path):
    ogg_audio = AudioSegment.from_ogg(ogg_path)
    ogg_audio.export(mp3_path, format="mp3")


@Client.on_message(filters.text & filters.private, group=1)
async def chatgpt(client, message):
    print(message.text)
    global bot_run
    if message.text == "/stop":
        bot_run = False
        await message.reply("Bot to'xtatildi!")
        current_time = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        logging.info(f'{current_time} : Bot to\'xtatildi!')

    if message.text == "/start":
        bot_run = True
        await message.reply("Bot ishga tushdi!")
        current_time = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        logging.info(f'{current_time} : Bot ishga tushdi!')
        
    if bot_run:
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": "O'zbek tilida javob ber.\nMen: Assalomu alaykum men "+status+" biron so'zingiz bo'lsa yozib qoldiring!\nDo'stim: "+message.text+".\nMen: "}
        ]
        )
        is_unread = await client.read_chat_history(message.chat.id, message.id)
        print(completion.choices[0].message['content'])
        await message.reply_text(completion.choices[0].message['content'], quote=True, parse_mode=ParseMode.MARKDOWN)
        current_time = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        logging.info(f'{current_time} :' + message.text + ' \n: ' +  completion.choices[0].message['content'])



@Client.on_message(filters.voice & filters.private, group=1)
async def voice_func(client, message):
    if message.voice:
        voice_path = await client.download_media(message.voice)
        mp3_path = voice_path.replace(".ogg", ".mp3")
        convert_ogg_to_mp3(voice_path, mp3_path)
        print("Converted to MP3:", mp3_path)
        audio_file= open(mp3_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        await message.reply(transcript['text'])
