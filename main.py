from pyrogram import Client
from dotenv import load_dotenv
import os, openai
load_dotenv()

openai.api_key = os.getenv('API_KEY')
api_id = os.getenv('API_ID')
api_hash =  os.getenv('API_HASH')

plugins = dict(root="plugins")

Client("my_account", api_id=api_id, api_hash=api_hash, plugins=plugins ).run()