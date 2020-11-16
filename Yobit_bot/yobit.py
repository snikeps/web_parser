import requests

def get_btc():
    url = 'https://yobit.net/api/2/btc_usd/ticker'
    response = requests.get(url).json()
    last_price = response['ticker']['last']
    return str(last_price) + ' usd'

