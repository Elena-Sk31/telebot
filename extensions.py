from json import loads

from requests import get

from config import CRYPTOCOMPARE_HEADER

__all__ = ('APIException', 'Converter')


class APIException(Exception):
    pass


class Converter:
    CRYPTOCOMPARE_BASE_URL = 'https://min-api.cryptocompare.com/data/price?fsym=%s&tsyms=%s'

    currency_type = {
        'EUR': 'Евро',
        'RUR': 'Рубли',
        'USD': 'Доллары'
    }

    def get_price(self, base: str, quote: str, amount: str) -> float:
        """
        Конвертация

        :param base: имя валюты, цену на которую надо узнать
        :param quote: имя валюты, цену в которой надо узнать
        :param amount: количество переводимой валюты

        :return: сумму в валюте
        """
        base = base.upper()
        quote = quote.upper()

        if base not in self.currency_type:
            raise APIException(f'Валюта "{base}" не поддерживается')

        if quote not in self.currency_type:
            raise APIException(f'Валюта "{quote}" не поддерживается')

        if not amount.isnumeric():
            raise APIException(f'Сумма "{amount}" введена не верно')

        resp = get(
            self.CRYPTOCOMPARE_BASE_URL % (base, quote),
            headers=CRYPTOCOMPARE_HEADER
        )

        if resp.status_code != 200:
            raise APIException(f'Ошибка получения курса валют: {resp.reason}')

        resp = loads(resp.text)

        try:
            current_price = float(resp[quote])
        except KeyError:
            raise APIException('Ошибка получения курса валют')

        value = float(amount)

        return current_price * value
