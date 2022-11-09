import os

BOT_TOKEN = "" #bot token
PROCESS = "web"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))


APP_URL = "" #url of server containing the bot
WEBHOOK_PATH = f'/{BOT_TOKEN}'
WEBHOOK_PORT = 443
WEBHOOK_URL = f'{APP_URL}:{WEBHOOK_PORT}{WEBHOOK_PATH}'

