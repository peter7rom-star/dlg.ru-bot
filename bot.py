import asyncio
from telebot.async_telebot import logger, AsyncTeleBot
from telebot.apihelper import get_me, get_webhook_info
from config.config import *
import logging


logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot = AsyncTeleBot(BOT_TOKEN)
