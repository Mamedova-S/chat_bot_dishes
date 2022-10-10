from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters import Command 
from aiogram.contrib.fsm_storage.memory import MemoryStorage 
from aiogram.dispatcher.filters.state import StatesGroup, State 
import config
from keyboards import for_questions
import logging
from aiogram.types import Message
import json
import re

data = [
  {
  "dish": "сырники",
  "type": "завтрак",
  "ingredients": [
    "творог",
    "яйцо",
    "соль",
    "мука",
    "сахар",
    "ванильный сахар" ]
  },
  
  {
  "dish": "блины",
  "type": "завтрак",
  "ingredients": [
    "мука",
    "яйцо",
    "соль",
    "сода",
    "сахар",
    "масло растительное", 
    "молоко" ]
  },
   
  {
  "dish": "курица терияки",
  "type": "обед",
  "ingredients": [
    "куриное филе",
    "соус терияки",
    "сок лимона",
    "кунжутные семечки" ]
  },

  {
  "dish": "грибной суп",
  "type": "обед",
  "ingredients": [
    "шампиньоны",
    "картофель",
    "лапша пшеничная",
    "лук репчатый",
    "оливковое масло",
    "соль" ]
  },

  {
  "dish": "драники с сыром",
  "type": "ужин",
  "ingredients": [
    "картофель",
    "сыр",
    "мука пшеничная",
    "яйцо",
    "соль",
    "перец черный молотый",
    "масло растительное" ]
  },

  {
  "dish": "макароны по-флотски",
  "type": "ужин",
  "ingredients": [
    "макароны",
    "мясо",
    "лук репчатый",
    "соль",
    "масло растительное" ]
  },

  {
  "dish": "рогалики",
  "type": "перекус",
  "ingredients": [
    "масло сливочное",
    "мука пшеничная",
    "дрожжи",
    "молоко",
    "сахар",
    "яйцо",
    "повидло вишневое",
    "соль"
   ]
  },

  {
  "dish": "бутерброды со шпротами",
  "type": "перекус",
  "ingredients": [
    "шпроты",
    "шпроты",
    "огурцы",
    "чеснок",
    "майонез",
    "зелень" ]
  }
]

class dishes(StatesGroup):
  choice = State()

storage = MemoryStorage() # FOR FSM
bot = Bot(token=config.bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )

@dp.message_handler(commands=['start'])
async def welcome(message):
    joinedFile = open("user.txt","r")
    joinedUsers = set ()
    for line in joinedFile:
        joinedUsers.add(line.strip())

    if not str(message.chat.id) in joinedUsers:
        joinedFile = open("user.txt","a")
        joinedFile.write(str(message.chat.id)+ "\n")
        joinedUsers.add(message.chat.id)

    await bot.send_message(message.chat.id, f"Привет, *{message.from_user.first_name}!* Выберите тип блюда", reply_markup=for_questions.start, parse_mode='Markdown')



    
@dp.message_handler(commands=['завтрак'])
async def breakfast_message(message: types.Message, state: FSMContext):
  type1="завтрак"
  await dishes.choice.set()
  async with state.proxy() as type_dish:
    type_dish['text']=type1
  await bot.send_message(message.chat.id, text = "Отлично! Вы выбрали категорию 'завтрак'! Введите список продуктов, которые имеются у вас в наличии,через запятую.", parse_mode='Markdown')

@dp.message_handler(commands=['обед'])
async def lunch_message(message: types.Message,state: FSMContext):
  type1="обед"
  await dishes.choice.set()
  async with state.proxy() as type_dish:
    type_dish['text']=type1
  await bot.send_message(message.chat.id, text = "Отлично! Вы выбрали категорию 'обед'! Введите список продуктов, которые имеются у вас в наличии,через запятую.", parse_mode='Markdown')
    
@dp.message_handler(commands=['ужин'])
async def dinner_message(message: types.Message, state: FSMContext):
  type1="ужин" 
  await dishes.choice.set()
  async with state.proxy() as type_dish:
    type_dish['text']=type1
  await bot.send_message(message.chat.id, text = "Отлично! Вы выбрали категорию 'ужин'! Введите список продуктов, которые имеются у вас в наличии,через запятую.", parse_mode='Markdown')

@dp.message_handler(commands=['перекус'])
async def snack_message(message: types.Message, state: FSMContext):
  type1="перекус"
  await dishes.choice.set()
  async with state.proxy() as type_dish:
    type_dish['text']=type1
  await bot.send_message(message.chat.id, text = "Отлично! Вы выбрали категорию 'перекус'! Введите список продуктов, которые имеются у вас в наличии,через запятую.", parse_mode='Markdown')



@dp.message_handler(state=dishes.choice)
async def get_message(message: Message, state: FSMContext):
  
  #data = json.load(open('dishes.json', 'r'))
  pattern = re.compile("^\s+|\s*,\s*|\s+$")
  dict=message.text
  dict2=dict.lower()
  dictionary= re.split(pattern, dict2)
 

  async with state.proxy() as type_dish:
    type1=type_dish['text']

  print(type1)
  for i in range(len(data)):
    if  data[i]['type']==type1:
      for k in range(len(dictionary)):
        if dictionary[k] in data[i]['ingredients'] :
          
          await bot.send_message(message.chat.id, text = data[i]["dish"], parse_mode='Markdown')

  
  await state.finish() # Завершаем FSM, очищаем переменные




##############################################################
if __name__ == '__main__':
    print('Запущен!')                                
executor.start_polling(dp)
##############################################################















