import os
import config
from dotenv import load_dotenv
from app.main import Application

if __name__ == "__main__":
    application = Application()
    application.start()
