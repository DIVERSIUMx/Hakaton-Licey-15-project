import asyncio
import logging
import sys
import sqlite3
import shutil

from os import getenv

from pyexpat.errors import messages

from config import TOKEN
import random
from aiogram import Bot, Dispatcher, html, F
from aiogram.utils.keyboard import *
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

Moderator_name_redact = {}
Moderator_body_redact = {}
User_publish_redact = {}
User_publish_name_redact = []
User_publish_body_redact = []
User_publish_img_redact = []

dp = Dispatcher()
CON = sqlite3.connect("main_db.sqlite")
CUR = CON.cursor()