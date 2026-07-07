from telethon import TelegramClient

api_id = 33325581
api_hash = "30e11108023b17d4e6fd7d91ae505c32"

client = TelegramClient("session.session", api_id, api_hash)

print("Starting session creation...")
client.start()
print("Session created successfully!")
client.disconnect()
