from telethon import TelegramClient, events
import re
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

api_id = 33325581
api_hash = "30e11108023b17d4e6fd7d91ae505c32"

# Source groups (যেখান থেকে message আসবে)
source_groups = [
    -1002649910215,
    -1003820641755,
    -1002422112887,
    -1002099067496,
    -1001533645229,
    -1003510677902,
    -1002238813566,
]

# Target Channel (তোমার channel)
target_channel = -1002809088110

# তোমার referral link
my_link = "https://broker-qx.pro/sign-up/?lid=2034027"

# তোমার telegram username
my_username = "@TraderSanzuBD"

# Store processed message IDs to prevent duplicates
processed_messages = set()

client = TelegramClient("session.session", api_id, api_hash)

url_pattern = re.compile(r'https?://\S+|www\.\S+')
mention_pattern = re.compile(r'@\w+')

@client.on(events.NewMessage(chats=source_groups))
async def handler(event):
    try:
        logger.info(f"📩 Received message {event.message.id} from chat {event.chat_id}")
        
        # Prevent duplicate processing
        if event.message.id in processed_messages:
            logger.info(f"⚠️ Duplicate message skipped: {event.message.id}")
            return
        
        processed_messages.add(event.message.id)
        
        # Limit cache size
        if len(processed_messages) > 1000:
            processed_messages.clear()
        
        message_text = event.message.text or ""
        logger.info(f"📝 Original text: {message_text[:100] if message_text else 'No text'}")

        # Replace links
        message_text = re.sub(url_pattern, my_link, message_text)

        # Replace mentions
        message_text = re.sub(mention_pattern, my_username, message_text)
        
        logger.info(f"📝 Modified text: {message_text[:100] if message_text else 'No text'}")

        # Text message
        if event.message.text and not event.message.media:
            await client.send_message(target_channel, message_text)
            logger.info(f"✅ Text message {event.message.id} forwarded to {target_channel}")

        # Media message
        if event.message.media:
            await client.send_file(
                target_channel,
                event.message.media,
                caption=message_text
            )
            logger.info(f"✅ Media message {event.message.id} forwarded to {target_channel}")
            
    except Exception as e:
        logger.error(f"❌ Error processing message {event.message.id}: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

async def start_bot():
    """Start the bot with proper error handling"""
    try:
        await client.start()
        logger.info("✅ Bot started successfully!")
        logger.info(f"📡 Monitoring {len(source_groups)} source groups")
        logger.info(f"🎯 Target channel: {target_channel}")
        await client.run_until_disconnected()
    except Exception as e:
        logger.error(f"❌ Bot startup error: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")