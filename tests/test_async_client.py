from datetime import datetime, timedelta
from decimal import Decimal

from cbr_dws_client import AsyncCbrDwsClient
from cbr_dws_client.constants import CodeMetalEnum


class TestAsyncCbrDwsClient:
    @classmethod
    def setup_class(cls) -> None:
        cls.cbr_dws_client = AsyncCbrDwsClient(verify=False)

    async def test_get_currencies_on_date(self):
        res = await self.cbr_dws_client.get_currencies_on_date(datetime.now())
        assert isinstance(res, list)

    async def test_get_currencies_on_date_with_char_code(self):
        res = await self.cbr_dws_client.get_currencies_on_date(datetime.now(), "USD")
        assert isinstance(res.Vcurs, Decimal)

    async def test_get_enum_currency_codes_list(self):
        res = await self.cbr_dws_client.get_enum_currency_codes(False)
        assert isinstance(res, list)

    async def test_get_enum_currency_codes_list_with_char_code(self):
        res = await self.cbr_dws_client.get_enum_currency_codes(False, "USD")
        assert isinstance(res.Vcode, str)

    async def test_get_currencies_dynamic_past_15_days(self):
        res = await self.cbr_dws_client.get_currencies_dynamic(
            datetime.now() - timedelta(days=15), datetime.now(), "USD"
        )
        assert isinstance(res, list)

    async def test_get_key_rate(self):
        res = await self.cbr_dws_client.get_key_rate(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    async def test_get_drag_met_dynamic(self):
        res = await self.cbr_dws_client.get_drag_met_dynamic(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    async def test_get_drag_met_dynamic_with_drg_met_code(self):
        res = await self.cbr_dws_client.get_drag_met_dynamic(
            datetime.now() - timedelta(days=15), datetime.now(), CodeMetalEnum.GOLD.value
        )
        assert isinstance(res, list)
        assert res[0]["CodMet"] == 1

    async def test_get_bi_cur_base(self):
        res = await self.cbr_dws_client.get_bi_cur_base(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, value in res:
            assert isinstance(_date, datetime)
            assert isinstance(value, Decimal)
