import telebot
from telebot import types

bot = telebot.TeleBot('6035462811:AAGO-t1tirrcXdliwFEbgS7E8vizZC0lp3Y') # Введите свой токен
task_id = 1
task_name = ''
time = 0
worker_id = 0
manager_id = 0

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_manager = types.InlineKeyboardButton(text='Менеджер', callback_data='manager');  # кнопка «Да»
    keyboard.add(key_manager);  # добавляем кнопку в клавиатуру
    key_worker = types.InlineKeyboardButton(text='Работник', callback_data='worker');
    keyboard.add(key_worker);
    bot.send_message(message.chat.id, 'Привет, ' + str(message.from_user.first_name) + '!' + '\n' + 'Это бот напоминалка.')
    bot.send_message(message.from_user.id, text='Выбери один из двух вариантов', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global worker_id, manager_id
    if call.data == "manager":
        manager_id = call.message.chat.id
        bot.send_message(call.message.chat.id, 'Введите задание: ');
        bot.register_next_step_handler(call.message, get_task_name)
    elif call.data == "worker":
        worker_id = call.message.chat.id
        bot.send_message(call.message.chat.id, 'Ожидайте задания ' + str(call.message.user_name));

def get_task_name(message):
    global task_name
    task_name = message.text
    bot.send_message(message.from_user.id, "Введите временной лимит: ")
    bot.register_next_step_handler(message, get_task_time)

def get_task_time(message):
    global time
    time = message.text
    bot.send_message(message.chat.id, "Задание было отправлено")
    bot.send_message(worker_id, "Новое задание: ")
    bot.register_next_step_handler(message, set_task)

def set_task(message):
    keyboard1 = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Выполнено', callback_data='yes')
    keyboard1.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Не сделано', callback_data='no')
    keyboard1.add(key_no)
    task = f"Задача: {task_name}. \n" \
           f"Время работы: {time}"
    bot.send_message(worker_id, text=task, reply_markup=keyboard1)

@bot.callback_query_handler(func=lambda call: True)
def callback_ans(call):
    if call.data == "yes":
        bot.send_message(worker_id, 'Хорошая Работа');
        bot.send_message(manager_id, 'Работник выполнил работу')
    elif call.data == "no":
        bot.send_message(worker_id, 'Результат сохранен');
        bot.send_message(manager_id, 'Работник невыполнил работу')


bot.polling(none_stop=True, interval=0)