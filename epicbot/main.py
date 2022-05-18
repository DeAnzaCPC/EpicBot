import os
from app import App

App(os.getenv("BOT_TOKEN")).run()

