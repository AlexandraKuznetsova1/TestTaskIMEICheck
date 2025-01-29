import requests
import time

TELEGRAM_TOKEN = '7872738868:AAFG6skg9WXfyZmLpgg0nCgu1QkuWkE-QiM'
# Белый список пользователей (идентификаторы чатов)
WHITE_LIST = [1071873769]


# Функция проверки IMEI через API
def check_imei(imei):
    url = "https://imeicheck.net/api/check-imei"
    headers = {'Authorization': 'Bearer e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b'}

    response = requests.post(url, json={'imei': imei}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Не удалось получить информацию о IMEI."}


# Функция для отправки сообщения пользователю
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    requests.post(url, json=payload)


# Основная функция для работы бота
def main():
    offset = 0
    while True:
        # Получение обновлений от Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}"
        response = requests.get(url)

        if response.status_code == 200:
            updates = response.json().get('result', [])

            for update in updates:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']
                offset = update['update_id'] + 1  # Обновляем offset для получения новых сообщений

                # Проверка, есть ли пользователь в белом списке
                if chat_id in WHITE_LIST:
                    imei = message_text.strip()

                    if len(imei) == 15 and imei.isdigit():  # Проверка на валидность IMEI
                        info = check_imei(imei)
                        send_message(chat_id, f"Информация о IMEI: {info}")
                    else:
                        send_message(chat_id, "Некорректный IMEI. Пожалуйста, введите 15-значный номер.")
                else:
                    send_message(chat_id, "У вас нет доступа к этому боту.")

        time.sleep(1)  # Задержка перед следующим запросом


if __name__ == '__main__':
    main()