import requests
import click
import schedule
import time


def check_stock_by_url(url):
    response = requests.get(url)
    return response.json()


def telegram_send(token, chat_id, message):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    param = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, json=param)
    return response.json()

def job(token, chat_id):
    pid = '691115870819'
    url = 'https://www.fila.com/on/demandware.store/Sites-FILA-Site/en_US/Product-GetAvailability?pid={}&Quantity=1'.format(
        pid)
    web_url = 'https://www.fila.com/womens-electrove-2/{}.html'.format(pid)
    message = check_stock_by_url(url)
    response = telegram_send(token, chat_id, web_url)
    response = telegram_send(token, chat_id, message['status'])

@click.command()
@click.option('--token', required=True)
@click.option('--chat_id', required=True)
def run(token, chat_id):
    schedule.every(10).minutes.do(job, token=token, chat_id=chat_id)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    run()
