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

    async def test_get_bliquidity(self):
        res = await self.cbr_dws_client.get_bliquidity(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    async def test_get_saldo(self):
        res = await self.cbr_dws_client.get_saldo(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, value in res:
            assert isinstance(_date, datetime)
            assert isinstance(value, Decimal)

    async def test_get_ruonia(self):
        res = await self.cbr_dws_client.get_ruonia(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, proc, value, date_pub in res:
            assert isinstance(_date, datetime)
            assert isinstance(proc, Decimal)
            assert isinstance(value, Decimal)
            assert isinstance(date_pub, datetime)

    async def test_get_ruonia_sv(self):
        res = await self.cbr_dws_client.get_ruonia_sv(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, index, ruonia_1m, ruonia_3m, ruonia_6m in res:
            assert isinstance(_date, datetime)
            assert isinstance(index, Decimal)
            assert isinstance(ruonia_1m, Decimal)
            assert isinstance(ruonia_3m, Decimal)
            assert isinstance(ruonia_6m, Decimal)

    async def test_get_mkr(self):
        res = await self.cbr_dws_client.get_mkr(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, p1, d1, d7, d30, d90, d180, d360 in res:
            assert isinstance(_date, datetime)
            assert isinstance(p1, Decimal)
            assert isinstance(d1, Decimal | None)
            assert isinstance(d7, Decimal | None)
            assert isinstance(d30, Decimal | None)
            assert isinstance(d90, Decimal | None)
            assert isinstance(d180, Decimal | None)
            assert isinstance(d360, Decimal | None)

    async def test_get_dv(self):
        res = await self.cbr_dws_client.get_dv(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, vovern, vlomb, viday, vother, vol_gold, vidate, vol_pm, vol_sm in res:
            assert isinstance(_date, datetime)
            assert isinstance(vovern, Decimal)
            assert isinstance(vlomb, Decimal)
            assert isinstance(viday, Decimal)
            assert isinstance(vother, Decimal)
            assert isinstance(vol_gold, Decimal)
            assert isinstance(vidate, datetime)
            assert isinstance(vol_pm, Decimal)
            assert isinstance(vol_sm, Decimal)
