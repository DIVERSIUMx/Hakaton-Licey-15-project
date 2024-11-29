import asyncio
import logging
import sys
import sqlite3

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

dp = Dispatcher()
CON = sqlite3.connect("main_db.sqlite")
CUR = CON.cursor()