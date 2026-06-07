import os
import json
import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# --- LOAD CONFIGURATION FROM JSON FILE ---
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError(f"❌ Error: {CONFIG_FILE} not found! Please create it first.")

with open(CONFIG_FILE, "r") as file:
    config = json.load(file)

TELEGRAM_TOKEN = config.get("TELEGRAM_BOT_TOKEN")
GITLAB_PROJECT_ID = config.get("GITLAB_PROJECT_ID")
GITLAB_TRIGGER_TOKEN = config.get("GITLAB_TRIGGER_TOKEN")
# ----------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a greeting message when /start is issued."""
    await update.message.reply_text(
        "👋 Hello! Use the /run command followed by 3 arguments to trigger the binary.\n"
        "Example: `/run 11 22 33`"
    )

async def run_binary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /run xx yy zz command."""
    args = context.args

    if len(args) != 3:
        await update.message.reply_text("❌ Error: You must provide exactly 3 arguments.\nExample: `/run 11 22 33`")
        return

    xx, yy, zz = args
    await update.message.reply_text(f"⏳ Initiating pipeline with values:\n• xx: {xx}\n• yy: {yy}\n• zz: {zz}")

    gitlab_url = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/trigger/pipeline"
    
    payload = {
        "token": GITLAB_TRIGGER_TOKEN,
        "ref": "main",  
        "variables[ARG_XX]": xx,
        "variables[ARG_YY]": yy,
        "variables[ARG_ZZ]": zz
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(gitlab_url, data=payload)
            
            if response.status_code == 201:
                pipeline_data = response.json()
                web_url = pipeline_data.get("web_url")
                await update.message.reply_text(
                    f"🚀 **Pipeline successfully triggered!**\n\n🔗 [Track Progress in GitLab]({web_url})",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(f"❌ GitLab API rejected the request.\nStatus: {response.status_code}")
                logging.error(f"GitLab API Error: {response.text}")

        except Exception as e:
            await update.message.reply_text("❌ An error occurred while trying to connect to GitLab.")
            logging.error(f"Connection error: {e}")

def main():
    if not all([TELEGRAM_TOKEN, GITLAB_PROJECT_ID, GITLAB_TRIGGER_TOKEN]):
        print("❌ Error: One or more tokens are missing in config.json.")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("run", run_binary))

    print("Bot is online and listening using config.json...")
    application.run_polling()

if __name__ == "__main__":
    main()