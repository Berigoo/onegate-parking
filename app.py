import os
from dotenv import load_dotenv
from app.main import Application

load_dotenv() 

if __name__ == "__main__":
    application = Application()
    application.start()
