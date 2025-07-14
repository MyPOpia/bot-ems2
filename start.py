for filename in os.listdir("./events"):
    if filename.endswith(".py"):
        bot.load_extension(f"events.{filename[:-3]}")
        
from keep_alive import keep_alive

keep_alive()  
