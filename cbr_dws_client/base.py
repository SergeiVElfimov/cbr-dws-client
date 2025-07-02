import logging
from datetime import date

import httpx
from zeep import AsyncClient, Client, Transport
from zeep.transports import AsyncTransport

from cbr_dws_client.mixins import ParseResponseCbrMixin

logger = logging.getLogger(__name__)


class CbrDwsClient(ParseResponseCbrMixin):
    """Клиент для работы с веб-сервис для получения ежедневных данных.

    Документация https://cbr.ru/development/dws/.

    Args:
        timeout: Время ожидания.
        verify: Признак проверки ssl сертификатов.
    Attributes:
       client: Объект Client.
    """

    cbr_dws_url = "https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"

    def __init__(self, timeout: int = 10, verify: bool = True):
        transport = Transport(timeout=timeout)
        transport.session.verify = verify
        self.client = Client(self.cbr_dws_url, transport=transport)

    def get_currencies_on_date(self, on_date: date, detail_currency_char_code: str | None = None):
        """Метод получения списка или конкретного значения курса валют на дату.

        :param on_date: Дата на которую нужен курс.
        :param detail_currency_char_code: Код валюты.
        :return: Курс валюты.
        """
        return self.parse_currency_on_date_dict(
            self.client.service.GetCursOnDate(On_date=on_date), detail_currency_char_code
        )

    def get_enum_currency_codes(self, seld: bool = False, detail_currency_char_code: str | None = None):
        """Метод извлечения данных из справочника по внутренним кодам валют.

        :param seld: Полный перечень валют котируемых Банком России:
                    True — перечень ежемесячных валют, False — перечень ежедневных валют.
        :param detail_currency_char_code: Код валюты.
        :return: Возвращает код валюты.
        """
        return self.parse_currency_on_date_dict(self.client.service.EnumValutes(Seld=seld), detail_currency_char_code)

    def get_currencies_dynamic(self, from_date: date, to_date: date, detail_currency_char_code: str) -> list:
        """Метод извлечения динамки курсов валют.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :param detail_currency_char_code: Код валюты.
        :return: Динамики курсов валют.
        """
        currency_code = self.get_enum_currency_codes(False, detail_currency_char_code)
        return self.parse_result_to_list(
            self.client.service.GetCursDynamic(
                FromDate=from_date, ToDate=to_date, ValutaCode=currency_code.Vcode.strip()
            )
        )

    def get_key_rate(self, from_date: date, to_date: date):
        """Метод извлечения динамки ключевой ставки.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамика ключевой ставки (список словарей).
        """
        return self.parse_result_to_list(self.client.service.KeyRate(fromDate=from_date, ToDate=to_date))

    def get_drag_met_dynamic(self, from_date: date, to_date: date, drg_met_code: int | None = None):
        """Метод извлечения динамки учетных цен на драгоценные металлы.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамика учетных цен на драгоценные металлы (список словарей).
        """
        return self.parse_currency_on_period_dict(
            self.client.service.DragMetDynamic(fromDate=from_date, ToDate=to_date), drg_met_code=drg_met_code
        )

    def get_bi_cur_base(self, from_date: date, to_date: date):
        """Метод извлечения динамки стоимости бивалютной корзины.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамка стоимости бивалютной корзины (список кортежей [(Дата1, Значение1), ...]).
        """
        return self.parse_bi_cur_base(
            data=self.parse_result_to_list(self.client.service.BiCurBase(fromDate=from_date, ToDate=to_date))
        )


class AsyncCbrDwsClient(ParseResponseCbrMixin):
    """Асинхронный клиент для работы с веб-сервис для получения ежедневных данных.

    Документация https://cbr.ru/development/dws/.

    Args:
        timeout: Время ожидания.
        verify: Признак проверки ssl сертификатов.
    Attributes:
       client: Объект Client.
    """

    cbr_dws_url = "https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL"

    def __init__(self, timeout: int = 10, verify: bool = True):
        httpx_client = httpx.AsyncClient(verify=verify)
        transport = AsyncTransport(client=httpx_client, timeout=timeout, verify_ssl=verify)
        self.client = AsyncClient(wsdl=self.cbr_dws_url, transport=transport)

    async def get_currencies_on_date(self, on_date: date, detail_currency_char_code: str | None = None):
        """Метод получения списка или конкретного значения курса валют на дату.

        :param on_date: Дата на которую нужен курс.
        :param detail_currency_char_code: Код валюты.
        :return: Курс валюты.
        """
        return self.parse_currency_on_date_dict(
            (await self.client.service.GetCursOnDate(On_date=on_date)), detail_currency_char_code
        )

    async def get_enum_currency_codes(self, seld: bool = False, detail_currency_char_code: str | None = None):
        """Метод извлечения данных из справочника по внутренним кодам валют.

        :param seld: Полный перечень валют котируемых Банком России:
                    True — перечень ежемесячных валют, False — перечень ежедневных валют.
        :param detail_currency_char_code: Код валюты.
        :return: Возвращает код валюты.
        """
        return self.parse_currency_on_date_dict(
            await self.client.service.EnumValutes(Seld=seld), detail_currency_char_code
        )

    async def get_currencies_dynamic(self, from_date: date, to_date: date, detail_currency_char_code: str) -> list:
        """Метод извлечения динамки курсов валют.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :param detail_currency_char_code: Код валюты.
        :return: Динамики курсов валют.
        """
        currency_code = await self.get_enum_currency_codes(False, detail_currency_char_code)
        return self.parse_result_to_list(
            await self.client.service.GetCursDynamic(
                FromDate=from_date, ToDate=to_date, ValutaCode=currency_code.Vcode.strip()
            )
        )

    async def get_key_rate(self, from_date: date, to_date: date):
        """Метод извлечения динамки ключевой ставки.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамику ключевой ставки (список словарей).
        """
        return self.parse_result_to_list(await self.client.service.KeyRate(fromDate=from_date, ToDate=to_date))

    async def get_drag_met_dynamic(self, from_date: date, to_date: date, drg_met_code: int | None = None):
        """Метод извлечения динамки учетных цен на драгоценные металлы.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамика учетных цен на драгоценные металлы (список словарей).
        """
        return self.parse_currency_on_period_dict(
            await self.client.service.DragMetDynamic(fromDate=from_date, ToDate=to_date), drg_met_code=drg_met_code
        )

    async def get_bi_cur_base(self, from_date: date, to_date: date):
        """Метод извлечения динамки стоимости бивалютной корзины.

        :param from_date: Дата начала.
        :param to_date: Дата окончания.
        :return: Динамка стоимости бивалютной корзины (список кортежей [(Дата1, Значение1), ...]).
        """
        return self.parse_bi_cur_base(
            data=self.parse_result_to_list(await self.client.service.BiCurBase(fromDate=from_date, ToDate=to_date))
        )
