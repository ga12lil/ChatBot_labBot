
import telebot
import requests
import jsons
from Class_ModelResponse import ModelResponse

# Замените 'YOUR_BOT_TOKEN' на ваш токен от BotFather
API_TOKEN = '7268978720:AAEH9Nr0uCkHZc_c8Bm8PCCmRgRFGYM8UbI'
bot = telebot.TeleBot(API_TOKEN)

# Хранилище для контекста диалогов пользователей
user_contexts = {}

# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я ваш Telegram бот.\n"
        "Доступные команды:\n"
        "/start - вывод всех доступных команд\n"
        "/model - выводит название используемой модели\n"
        "/clear - очистка контекста диалога\n"
        "Отправьте любое сообщение, и я отвечу с помощью LLM модели."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['clear'])
def clear_context(message):
    # Очистка контекста для пользователя
    user_id = message.chat.id
    if user_id in user_contexts:
        del user_contexts[user_id]
    bot.reply_to(message, "Контекст диалога очищен.")

@bot.message_handler(commands=['model'])
def send_model_name(message):
    # Отправляем запрос к LM Studio для получения информации о модели
    response = requests.get('http://localhost:1234/v1/models')

    if response.status_code == 200:
        model_info = response.json()
        model_name = model_info['data'][0]['id']
        bot.reply_to(message, f"Используемая модель: {model_name}")
    else:
        bot.reply_to(message, 'Не удалось получить информацию о модели.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_query = message.text

    # Инициализация контекста для пользователя, если его нет
    if user_id not in user_contexts:
        user_contexts[user_id] = []

    # Добавление нового сообщения пользователя в контекст
    user_contexts[user_id].append({"role": "user", "content": user_query})

    # Создание запроса к модели с использованием сохраненного контекста
    request = {
        "messages": user_contexts[user_id]
    }

    response = requests.post(
        'http://localhost:1234/v1/chat/completions',
        json=request
    )

    if response.status_code == 200:
        model_response: ModelResponse = jsons.loads(response.text, ModelResponse)
        response_content = model_response.choices[0].message.content

        # Добавление ответа модели в контекст
        user_contexts[user_id].append({"role": "assistant", "content": response_content})

        bot.reply_to(message, response_content)
    else:
        bot.reply_to(message, 'Произошла ошибка при обращении к модели.')

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
