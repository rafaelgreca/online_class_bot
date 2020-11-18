from bot import Bot
from decouple import config

try:
    class_bot = Bot(email=config('EMAIL'), password=config('PASSWORD'))
    class_bot.UpdateClasses()
    class_bot.CheckClasses()
    
except KeyboardInterrupt:
    print("Bot is offline right now.")