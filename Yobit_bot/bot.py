import requests
import misc
from yobit import get_btc
from time import sleep
# import json

# https://api.telegram.org/bot1309623923:AAFy9XuGKNoxCPTfghPJPk3d-Tyzzp_nGMI/sendmessage?chat_id=123941343&text=trololo


token = misc.token
url_base = 'https://api.telegram.org/bot' + token + '/'

global last_update_id
last_update_id = 0

def get_updates():
    url = url_base + 'getupdates'
    # print(url)
    resp = requests.get(url)
    # print(resp)
    # print(resp.json())

    return resp.json()


def get_message():
    data = get_updates()

    last_object = data['result'][-1]
    current_update_id = last_object['update_id']

    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id': chat_id,
                   'text': message_text}

        return message
    return None

def send_message(chat_id, text='please wait'):
    url = url_base + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    # print(url)
    requests.get(url)



def main():
    # d = get_updates()

    # with open('updates.json', 'w') as file:
    #     json.dump(d, file, indent=2 , ensure_ascii=False)
    while True:
        response = get_message()

        if response != None:
            chat_id = response['chat_id']
            text = response['text']

            if text == '/btc':
                send_message(chat_id, get_btc())
        else:
            continue

        sleep(3)




if __name__ == '__main__':
    main()