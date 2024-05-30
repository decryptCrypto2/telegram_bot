import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gradio_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the Gradio client
client = Client("SakanaAI/EvoSDXL-JP")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me a text message to generate an image.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    
    # Call the Gradio API
    result = client.predict(
        user_text,  # str in 'parameter_4' Textbox component
        0,          # float (numeric value between 0 and 2147483647) in 'シード値' Slider component
        True,       # bool in 'ランダムにシード値を決定' Checkbox component
        api_name="/run"
    )
    
    # Extract the image path from the result tuple
    image_path = result[0]
    
    print(image_path)
    
    # Send the image back to the user
    with open(image_path, 'rb') as img_file:
        await update.message.reply_photo(photo=InputFile(img_file))

def main() -> None:
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
