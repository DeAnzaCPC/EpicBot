import os
from app import App
from dotenv import load_dotenv

load_dotenv()

App(os.getenv("BOT_TOKEN")).run()

