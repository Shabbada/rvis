from pyrogram import Client, filters
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import openai


openai.api_key = os.getenv('API_KEY')


def convert_ogg_to_mp3(ogg_path, mp3_path):
    ogg_audio = AudioSegment.from_ogg(ogg_path)
    ogg_audio.export(mp3_path, format="mp3")


@Client.on_message(filters.text & filters.private, group=1)
async def echo_reversed(client, message):
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "user", "content": message.text}
    ]
    )
    await message.reply(completion.choices[0].message['content'])


@Client.on_message(filters.voice & filters.private, group=1)
async def echo_reversed(client, message):
    if message.voice:
        voice_path = await client.download_media(message.voice)
        mp3_path = voice_path.replace(".ogg", ".mp3")
        convert_ogg_to_mp3(voice_path, mp3_path)
        print("Converted to MP3:", mp3_path)
        audio_file= open(mp3_path, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        await message.reply(transcript['text'])