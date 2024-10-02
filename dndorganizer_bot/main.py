from email import message
import telebot;
from telebot import types;
import json;

bot = telebot.TeleBot('7087728399:AAGs6eukMBsP6pr8WsmZVKumYKCCkQZpR24');

@bot.message_handler(commands=['start'])
def start(message):
    if 'user_data' not in globals():
        global user_data
        user_data = {}
    if message.from_user.id not in user_data:
        bot.send_message(message.from_user.id, "Привітик! Я твій особистий днд помічник) Щоб переглянути всі доступні команди пришли '/help', а для створення нового персонажу - '/new_character'")
    else:
        bot.send_message(message.from_user.id, "Привітик! Я твій особистий днд помічник) Щоб переглянути всі доступні команди пришли '/help', а для створення нового персонажу - '/new_character' або введи '/character' щоб переглянути інформацію про свого персонажа")

@bot.message_handler(commands=['help'])
def help(message):
    if message.from_user.id not in user_data:
        bot.send_message(message.from_user.id, ' /start - запуск бота \n /new_character - створити нового персонажа ')
    else:
        bot.send_message(message.from_user.id, ' /start - запуск бота \n /new_character - створити нового персонажа \n /character - переглянути інформацію про персонажа \n /add_characteristics - додати значення характеристик \n /update_characteristics - оновити значення харакura;теристик \n /show_characteristics - показати значення характеристик \n /backpack - переглянути що є в рюкзаку \n /reputation - переглянути свою репутацію \n /myexp - переглянути кількість одиниць досвіду \n /new_item - додати новий предмет в інвентар \n /short_break - сходити на короткий відпочинок(рандомна подія) \n /long_break - запустити довгий відпочинок \n /off_campaign - піти на відпочинок між пригодами')

@bot.message_handler(commands=['new_character'])
def new_character(message):
    if message.from_user.id not in user_data:
        bot.send_message(message.from_user.id, 'Як тебе звати?')
        bot.register_next_step_handler(message, get_playername)
    else:
        bot.send_message(message.from_user.id, 'Ти вже створив персонажа. Введи команду /character щоб переглянути інформацію про свого персонажа')


def repeat_questions(message):
    bot.send_message(message.from_user.id, "Як тебе звати?")
    bot.register_next_step_handler(message, get_playername)

def get_playername(message):
    global playername_;
    playername_ = message.text; 
    bot.send_message(message.from_user.id, "Який звати твого персонажа?");
    bot.register_next_step_handler(message, get_charactername);

def get_charactername(message):
    global charactername_;
    charactername_ = message.text; 
    bot.send_message(message.from_user.id, "Які у твого персонажа займенники?(він/вона/вони)");
    bot.register_next_step_handler(message, get_definition);

def get_definition(message):
    global definition_;
    definition_ = message.text.lower();
    bot.send_message(message.from_user.id, "Який у твого персонажа клас?");
    bot.register_next_step_handler(message, get_class);

def get_class(message):
    global class_;
    class_ = message.text.lower();
    bot.send_message(message.from_user.id, "Яка у твого персонажа раса?");
    bot.register_next_step_handler(message, get_race);

def get_race(message):
    global race_;
    race_ = message.text.lower();
    bot.send_message(message.from_user.id, "Який у твого персонажа світогляд?");
    bot.register_next_step_handler(message, get_worldview);

def get_worldview(message):
    global worldview_;
    worldview_ = message.text.lower();
    keyboard = types.InlineKeyboardMarkup();
    key_yes = types.InlineKeyboardButton(text='Так', callback_data='yes');
    keyboard.add(key_yes);
    key_no= types.InlineKeyboardButton(text='Ні', callback_data='no');
    keyboard.add(key_no);
    if definition_ == 'він':
        question = 'Тебе звати '+playername_+', твого персонажа звати '+charactername_+', він '+race_+'-'+class_+' і має '+worldview_+' світогляд?';
    elif definition_ == 'вона':
        question = 'Тебе звати '+playername_+', твого персонажа звати '+charactername_+', вона '+race_+'-'+class_+' і має '+worldview_+' світогляд?';
    elif definition_ == 'вони':
        question = 'Тебе звати '+playername_+', твого персонажа звати '+charactername_+', вони '+race_+'-'+class_+' і мають '+worldview_+' світогляд?';
    else: 
        bot.send_message(message.from_user.id, "Щось пішло не так, ти ввів/ввела неправильні займенники")
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

def save_user_data():
    global user_data
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        user_id = call.message.chat.id
        user_data[user_id] = {
            'playername': playername_,
            'charactername': charactername_,
            'definition': definition_,
            'race': race_,
            'class': class_,
            'worldview': worldview_,
            'reputation': 0,
            'exp': 0,
            'level': 1,
            'proficiency_bonus': 2,
            'backpack' : [
                {
                "name": "item name",
                "type": "item type",
                "damage": "item damage",
                "effect": "item effect",
                "description": "item description",
                "quantity" : 1,
                },
            ],
        }
        save_user_data()
        bot.send_message(call.message.chat.id, 'Дякую, твого персонажа збережено.')
    elif call.data == "no":
        repeat_questions(message);

@bot.message_handler(commands=['character'])
def display_user_data(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        playername = user_data_record['playername']
        charactername = user_data_record['charactername']
        definition = user_data_record['definition']
        race = user_data_record['race']
        class_ = user_data_record['class']
        worldview = user_data_record['worldview']
        bot.send_message(message.from_user.id, 'Вибач за затримку, '+ playername +'! Ось інформація про твого персонажа:\n🔹Ім*я персонажа: '+ charactername +'\n🔹 Раса персонажа: '+ race +'\n🔹 Займенники: '+ definition +'\n🔹 Клас персонажа: '+ class_ +'\n🔹 Світогляд: '+ worldview +'');
    else:
        bot.send_message(message.from_user.id, 'Я звірився зі списками і, на жаль, не зміг знайти тебе чи твого персонажа(. Введи команду /new_character щоб його створити.')

@bot.message_handler(commands=['add_characteristics'])
def add_characteristics(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        bot.send_message(message.from_user.id, 'Введи значення для таких характеристик: сила, спритність, статура, інтелект, мудрість, харизма.')
        bot.register_next_step_handler(message, save_characteristics)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def save_characteristics(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    characteristics = message.text.split(', ')
    if len(characteristics) == 6:
        user_data_record['characteristics'] = {
            'strength': characteristics[0],
            'dexterity': characteristics[1],
            'constitution': characteristics[2],
            'intelligence': characteristics[3],
            'wisdom': characteristics[4],
            'charisma': characteristics[5]
        }
        save_user_data()
        bot.send_message(message.from_user.id, 'Дякую, характеристики персонажа збережено.')
    else:
        bot.send_message(message.from_user.id, 'Введено неправильну кількість характеристик. Введи команду /add_characteristics щоб спробувати знову.')

@bot.message_handler(commands=['show_characteristics'])
def show_characteristics(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        characteristics = user_data_record['characteristics']
        modifiers = {
            'strength': calculate_modifier(int(characteristics['strength'])),
            'dexterity': calculate_modifier(int(characteristics['dexterity'])),
            'constitution': calculate_modifier(int(characteristics['constitution'])),
            'intelligence': calculate_modifier(int(characteristics['intelligence'])),
            'wisdom': calculate_modifier(int(characteristics['wisdom'])),
            'charisma': calculate_modifier(int(characteristics['charisma']))
        }
        bot.send_message(message.from_user.id, 'Звісно, ось характеристики персонажа ' +charactername_+'\n🔹 Сила: ' + characteristics['strength'] + ' (' + str(modifiers['strength']) + ')\n🔹 Спритність: ' + characteristics['dexterity'] + ' (' + str(modifiers['dexterity']) + ')\n🔹 Статура: ' + characteristics['constitution'] + ' (' + str(modifiers['constitution']) + ')\n🔹 Інтелект: ' + characteristics['intelligence'] + ' (' + str(modifiers['intelligence']) + ')\n🔹 Мудрість: ' + characteristics['wisdom'] + ' (' + str(modifiers['wisdom']) + ')\n🔹 Харизма: ' + characteristics['charisma'] + ' (' + str(modifiers['charisma']) + ')')
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def calculate_modifier(value):
    if value < 1:
        return -5
    elif value < 3:
        return -4
    elif value < 5:
        return -3
    elif value < 7:
        return -2
    elif value < 9:
        return -1
    elif value < 11:
        return 0
    elif value < 13:
        return 1
    elif value < 15:
        return 2
    elif value < 17:
        return 3
    elif value < 19:
        return 4
    elif value < 21:
        return 5
    elif value < 23:
        return 6
    elif value < 25:
        return 7
    elif value < 27:
        return 8
    elif value < 29:
        return 9
    else:
        return 10
    
@bot.message_handler(commands=['update_characteristics'])
def update_characteristics(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        bot.send_message(message.from_user.id, 'Введи нові значення для таких характеристик: сила, спритність, статура, інтелект, мудрість, харизма.')
        bot.register_next_step_handler(message, save_updated_characteristics)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def save_updated_characteristics(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    characteristics = message.text.split(', ')
    if len(characteristics) == 6:
        user_data_record['characteristics'] = {
            'strength': characteristics[0],
            'dexterity': characteristics[1],
            'constitution': characteristics[2],
            'intelligence': characteristics[3],
            'wisdom': characteristics[4],
            'charisma': characteristics[5]
        }
        save_user_data()
        bot.send_message(message.from_user.id, 'Дякую, характеристики персонажа оновлено.')
    else:
        bot.send_message(message.from_user.id, 'Введено неправильну кількість характеристик. Введи команду /update_characteristics щоб спробувати знову.')

@bot.message_handler(commands=['reputation'])
def display_reputation(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        reputation = user_data_record['reputation']
        if reputation <= -100:
            reputation_status = 'Справжній злодій з історій'
        elif reputation <= -50:
            reputation_status = 'Ворог народу'
        elif reputation == 0:
            reputation_status = 'Нейтрально'
        elif reputation >= 50:
            reputation_status = 'Дружній мандрівник'
        elif reputation >= 100:
            reputation_status = 'Справжній герой з історій'
        else:
            reputation_status = 'Невідомо'
        bot.send_message(message.from_user.id, 'Ваша репутація: ' + str(reputation) + '\nСтатус: ' + reputation_status)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

@bot.message_handler(commands=['add_reputation_points'])
def add_reputation_points(message):
    user_id = message.from_user.id
    if user_id in user_data:
        bot.send_message(message.from_user.id, 'Введи кількість балів репутації, яку хочеш додати.')
        bot.register_next_step_handler(message, save_reputation_points)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def save_reputation_points(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    reputation_points = int(message.text)
    user_data_record['reputation'] += reputation_points
    save_user_data()
    bot.send_message(message.from_user.id, 'Дякую, бали репутації додано. Ваша нова репутація: ' + str(user_data_record['reputation']))

@bot.message_handler(commands=['my_exp'])
def display_exp(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        exp = user_data_record['exp']
        level = calculate_level(exp)
        proficiency_bonus = calculate_proficiency_bonus(level)
        bot.send_message(message.from_user.id, 'Ваш досвід: ' + str(exp) + '\nРівень: ' + str(level) + '\nБонус майстерності: ' + str(proficiency_bonus))
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

@bot.message_handler(commands=['add_exp'])
def add_exp(message):
    user_id = message.from_user.id
    if user_id in user_data:
        bot.send_message(message.from_user.id, 'Введи кількість досвіду, яку хочеш додати.')
        bot.register_next_step_handler(message, save_exp)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def save_exp(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    exp_points = int(message.text)
    user_data_record['exp'] += exp_points
    save_user_data()
    new_level = calculate_level(user_data_record['exp'])
    bot.send_message(message.from_user.id, 'Дякую, досвід додано. Ваш новий досвід: ' + str(user_data_record['exp']))
    if new_level > user_data_record['level']:
        bot.send_message(message.from_user.id, 'Вітаю! Ти піднявся на новий рівень! Твій новий рівень: ' + str(new_level))
    user_data_record['level'] = new_level

def calculate_level(exp):
    if exp < 300:
        return 1
    elif exp < 900:
        return 2
    elif exp < 2700:
        return 3
    elif exp < 6500:
        return 4
    elif exp < 14000:
        return 5
    elif exp < 23000:
        return 6
    elif exp < 34000:
        return 7
    elif exp < 48000:
        return 8
    elif exp < 64000:
        return 9
    elif exp < 85000:
        return 10
    elif exp < 100000:
        return 11
    elif exp < 120000:
        return 12
    elif exp < 140000:
        return 13
    elif exp < 165000:
        return 14
    elif exp < 195000:
        return 15
    elif exp < 225000:
        return 16
    elif exp < 265000:
        return 17
    elif exp < 305000:
        return 18
    elif exp < 355000:
        return 19
    else:
        return 20

def calculate_proficiency_bonus(level):
    if level <= 4:
        return 2
    elif level <= 8:
        return 3
    elif level <= 12:
        return 4
    elif level <= 16:
        return 5
    elif level <= 20:
        return 6
    else:
        return 2

@bot.message_handler(commands=['backpack'])
def display_backpack(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        backpack = user_data_record['backpack']
        if len(backpack) > 0:
            items = []
            for i, item in enumerate(backpack):
                if item['type'] == 'зброя':
                    if 'damage' in item:
                        items.append(str(i+1) + '. ' + item['name'] + ' (' + item['type'] + ') x' + str(item['quantity']) + ' - урон: ' + item['damage'])
                    else:
                        items.append(str(i+1) + '. ' + item['name'] + ' (' + item['type'] + ') x' + str(item['quantity']) + ' - урон: N/A')
                elif item['type'] == 'зілля':
                    if 'effect' in item:
                        items.append(str(i+1) + '. ' + item['name'] + ' (' + item['type'] + ') x' + str(item['quantity']) + ' - ефект: ' + item['effect'])
                    else:
                        items.append(str(i+1) + '. ' + item['name'] + ' (' + item['type'] + ') x' + str(item['quantity']) + ' - ефект: N/A')
                else:
                    items.append(str(i+1) + '. ' + item['name'] + ' (' + item['type'] + ') x' + str(item['quantity']))
            bot.send_message(message.from_user.id, 'Рюкзак персонажа ' + charactername_ + ':\n' + '\n'.join(items))
        else:
            bot.send_message(message.from_user.id, 'Ваш рюкзак порожній.')
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

@bot.message_handler(commands=['new_item'])
def new_item(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        bot.send_message(message.from_user.id, 'Введи назву предмету:')
        bot.register_next_step_handler(message, get_item_name)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def get_item_name(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_name = message.text
    bot.send_message(message.from_user.id, 'Введи тип предмету(зброя, зілля, сюжет, інше):')
    bot.register_next_step_handler(message, get_item_type, item_name)

def get_item_type(message, item_name):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_type = message.text.lower()
    if item_type not in ['зброя', 'зілля', 'сюжет', 'інше']:
        bot.send_message(message.from_user.id, 'Неправильний тип предмету. Введи команду /new_item щоб спробувати знову.')
    else:
        if item_type == 'зілля':
            bot.send_message(message.from_user.id, 'Введи ефект предмету:')
            bot.register_next_step_handler(message, get_item_effect, item_name, item_type)
        elif item_type == 'зброя':
            bot.send_message(message.from_user.id, 'Введи урон зброї:')
            bot.register_next_step_handler(message, get_item_damage, item_name, item_type)
        else: 
            bot.send_message(message.from_user.id, 'Введи кількість предмету:')
            bot.register_next_step_handler(message, get_item_quantity, item_name, item_type)

def get_item_effect(message, item_name, item_type):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_effect = message.text
    bot.send_message(message.from_user.id, 'Введи кількість предмету:')
    bot.register_next_step_handler(message, get_item_quantity, item_name, item_type, item_effect)

def get_item_damage(message, item_name, item_type,):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_damage = message.text
    bot.send_message(message.from_user.id, 'Введи кількість предмету:')
    bot.register_next_step_handler(message, get_item_quantity, item_name, item_type, item_damage)


def get_item_quantity(message, item_name, item_type, item_damage, item_effect=None):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_quantity = int(message.text)
    if item_quantity < 1:
        bot.send_message(message.from_user.id, 'Неправильна кількість предмету. Введи команду /new_item щоб спробувати знову.')
    else:
        if 'backpack' not in user_data_record:
            user_data_record['backpack'] = []
        user_data_record['backpack'].append({
            'name': item_name,
            'type': item_type,
            'quantity': item_quantity,
            'effect': item_effect,
            'damage' : item_damage
        })
        save_user_data()
        bot.send_message(message.from_user.id, 'Дякую, предмет додано в рюкзак.')


@bot.message_handler(commands=['delete_item'])
def delete_item(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data_record = user_data[user_id]
        bot.send_message(message.from_user.id, 'Введи номер предмету, який хочеш видалити:')
        bot.register_next_step_handler(message, get_item_number_to_delete)
    else:
        bot.send_message(message.from_user.id, 'Ти ще не створив персонажа. Введи команду /new_character щоб створити нового персонажа.')

def get_item_number_to_delete(message):
    user_id = message.from_user.id
    user_data_record = user_data[user_id]
    item_number = int(message.text) - 1
    if item_number < 0 or item_number >= len(user_data_record['backpack']):
        bot.send_message(message.from_user.id, 'Неправильний номер предмету. Введи команду /delete_item щоб спробувати знову.')
    else:
        del user_data_record['backpack'][item_number]
        save_user_data()
        bot.send_message(message.from_user.id, 'Предмет видалено.')





















bot.polling(none_stop=True, interval=0)