# cbr-dws-client

[![build-status-image]][build-status]
[![codeql-image]][codeql]
[![pypi-version]][pypi]
[![pypi-downloads]][pypi]

Клиент для работы с [сервисом](http://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx) получения ежедневных данных ЦБ.

Подробную документацию по сервису см. [тут](https://cbr.ru/development/dws/)

## Пример

```python
from cbr_dws_client import CbrDwsClient, AsyncCbrDwsClient
from datetime import datetime
from cbr_dws_client.constants import CodeMetalEnum

cbr_dws_client = CbrDwsClient()
async_cbr_dws_client = AsyncCbrDwsClient()

# Получить список текущих курсов.
cbr_dws_client.get_currencies_on_date(datetime.now())
await async_cbr_dws_client.get_currencies_on_date(datetime.now())

# Получить список курс доллара.
cbr_dws_client.get_currencies_on_date(datetime.now(), "USD")
await async_cbr_dws_client.get_currencies_on_date(datetime.now(), "USD")

# Получить текущую динамику курса доллара за 15 дней.
cbr_dws_client.get_currencies_dynamic(datetime.now() - timedelta(days=15), datetime.now(), "USD")
await async_cbr_dws_client.get_currencies_dynamic(datetime.now() - timedelta(days=15), datetime.now(), "USD")

# Получить текущую динамику ключевой ставки за 15 дней.
cbr_dws_client.get_key_rate(datetime.now() - timedelta(days=15), datetime.now())
await async_cbr_dws_client.get_key_rate(datetime.now() - timedelta(days=15), datetime.now())

# Получить текущую динамику курса золота за 15 дней.
cbr_dws_client.get_drag_met_dynamic(datetime.now() - timedelta(days=15), datetime.now(), CodeMetalEnum.GOLD.value)
await async_cbr_dws_client.get_drag_met_dynamic(datetime.now() - timedelta(days=15), datetime.now(), CodeMetalEnum.GOLD.value)
```

## Требования

- python >=3.11, <4.0
- zeep >=4.2.1
- httpx <0.28

## Установка

```pip install cbr-dws-client```

## Сотрудничество

Перед тем как вносить вклад в проект, ознакомьтесь с нашими [правилами](CONTRIBUTING.md).

[build-status-image]: https://github.com/SergeiVElfimov/cbr-dws-client/actions/workflows/python-package.yml/badge.svg
[build-status]: https://github.com/SergeiVElfimov/cbr-dws-client/actions/workflows/python-package.yml
[pypi-version]: https://img.shields.io/pypi/v/cbr-dws-client.svg
[pypi-downloads]: https://img.shields.io/pypi/dm/cbr-dws-client?color=%232E73B2&logo=python&logoColor=%23F9D25F
[pypi]: https://pypi.org/project/cbr-dws-client/
[codeql-image]: https://github.com/SergeiVElfimov/cbr-dws-client/actions/workflows/codeql.yml/badge.svg
[codeql]: https://github.com/SergeiVElfimov/cbr-dws-client/actions/workflows/codeql.yml
