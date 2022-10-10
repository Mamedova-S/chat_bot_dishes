from pickle import TRUE
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

######################################################
start = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # СОЗДАЕМ ВООБЩЕ ОСНОВУ ДЛЯ КНОПОК

breakfast = types.KeyboardButton("/завтрак")            
lunch = types.KeyboardButton("/обед")     
dinner = types.KeyboardButton("/ужин")   
snack  = types.KeyboardButton("/перекус")        

start.add(breakfast, lunch, dinner, snack) #ДОБАВЛЯЕМ ИХ В БОТА