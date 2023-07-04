import requests
import json
import time
import datetime as dt
import quiz_movies

TOKEN = "6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q"
chat_id = "813012401"
URL = 'https://api.telegram.org/bot'
url_euro = 'https://api.audioaddict.com/v1/di/track_history/channel/69.json'

message = "Что вам сказать?"
img_url = 'https://severnykavkaz.ru/wp-content/uploads/2019/02/priroda-ingushetii-1200x540.jpg'
img = 'nu.png'
video = '1.mp4'

text = 'Проснись!'

def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")

def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']


def send_message(chat_id, message):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={message}')


def send_photo_url(chat_id, img_url):
    print(img_url)
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}')


def send_photo_file(chat_id, img):
    files = {'photo': open(img, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', files=files)


def send_video_file(chat_id, video):
    files = {'video': open(video, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendVideo?chat_id={chat_id}', files=files)


def inline_keyboard(chat_id, text):
    reply_markup = {'inline_keyboard': [[{'text': 'Наш сайт', 'url': 'https://google.com'}]]}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)


def reply_keyboard(chat_id, text):
    reply_markup = {"keyboard": [["Загадай фильм"], ["Что по радио Eurodance?"]], "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)




# send_massage(chat_id, message)
# send_photo_url(chat_id, img_url)
# send_photo_file(chat_id, img)
# send_video_file(chat_id, video)
# reply_keyboard(chat_id, text)

# print(requests.get(f'{URL}{TOKEN}/getUpdates').json())

def check_message(chat_id, message, date):
    if message.lower() in ['что по радио eurodance?', 'eurodance', 'евроденс']:
        track = requests.get(f'{url_euro}').json()[0]['track']
        art_url = requests.get(f'{url_euro}').json()[0]['art_url']
        print(track)
        send_message(chat_id, track)
        send_photo_url(chat_id, 'https:' + art_url)
    elif message.lower() in 'сайт':
        inline_keyboard(chat_id, 'Ссылка на какой-то сайт')
    elif message.lower() in 'фото по url':
        # Отправить URL-адрес картинки (телеграм скачает его и отправит)
        send_photo_url(chat_id, 'https://')
    elif message.lower() in 'фото с компьютера':
        # Отправить файл с компьютера
        send_photo_file(chat_id, 'nu.png')
    elif message.lower() in 'фото с сервера телеграм':
        # Отправить id файла (файл уже хранится где-то на серверах Telegram)
        send_photo_file_id(chat_id, 'AgACAgIAAxkBAAMqYVGBbdbivL53IzKLfUKUClBnB0cAApy0MRtfMZBKHL0tNw9aITwBAAMCAAN4AAMhBA')
    elif message.lower() in 'загадай фильм':
        send_message(chat_id, 'Минуточку, сейчас мы выберем произвольный советский фильм и случайный кадр из него...')
        file, title = quiz_movies.get_film(date)
        print(file, title)
        try:
            send_photo_file(chat_id, f'out/{file}')
            send_message(chat_id, 'Угадайте из какого фильма этот кадр? Ответ через несколько секунд.')
            time.sleep(15)
            send_message(chat_id, title)
        except BaseException:
            send_message(chat_id, 'Приносим извинение, какая-то ошибка. Попробуйте чуть позднее...')
    else:
        reply_keyboard(chat_id, 'Вот что я умею')


def run():
    update_id = get_updates()[-1]['update_id']  # Присваиваем ID последнего отправленного сообщения боту
    while True:
        time.sleep(4)
        messages = get_updates(update_id)  # Получаем обновления
        for message in messages:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']  # Присваиваем ID последнего отправленного сообщения боту
                # Отвечаем тому кто прислал сообщение боту
                check_message(message['message']['chat']['id'], message['message']['text'], message['message']['date'])


if __name__ == '__main__':
    run()



# https://api.telegram.org/bot6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q/getUpdates