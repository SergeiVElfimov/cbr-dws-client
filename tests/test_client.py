from datetime import datetime, timedelta
from decimal import Decimal

from cbr_dws_client import CbrDwsClient
from cbr_dws_client.constants import CodeMetalEnum


class TestCbrDwsClient:
    @classmethod
    def setup_class(cls) -> None:
        cls.cbr_dws_client = CbrDwsClient(verify=False)

    def test_get_currencies_on_date(self):
        res = self.cbr_dws_client.get_currencies_on_date(datetime.now())
        assert isinstance(res, list)

    def test_get_currencies_on_date_with_char_code(self):
        res = self.cbr_dws_client.get_currencies_on_date(datetime.now(), "USD")
        assert isinstance(res.Vcurs, Decimal)

    def test_get_enum_currency_codes_list(self):
        res = self.cbr_dws_client.get_enum_currency_codes(False)
        assert isinstance(res, list)

    def test_get_enum_currency_codes_list_with_char_code(self):
        res = self.cbr_dws_client.get_enum_currency_codes(False, "USD")
        assert isinstance(res.Vcode, str)

    def test_get_currencies_dynamic_past_15_days(self):
        res = self.cbr_dws_client.get_currencies_dynamic(datetime.now() - timedelta(days=15), datetime.now(), "USD")
        assert isinstance(res, list)

    def test_get_key_rate(self):
        res = self.cbr_dws_client.get_key_rate(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    def test_get_drag_met_dynamic(self):
        res = self.cbr_dws_client.get_drag_met_dynamic(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    def test_get_drag_met_dynamic_with_drg_met_code(self):
        res = self.cbr_dws_client.get_drag_met_dynamic(
            datetime.now() - timedelta(days=15), datetime.now(), CodeMetalEnum.GOLD.value
        )
        assert isinstance(res, list)
        assert res[0]["CodMet"] == 1

    def test_get_bi_cur_base(self):
        res = self.cbr_dws_client.get_bi_cur_base(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, value in res:
            assert isinstance(_date, datetime)
            assert isinstance(value, Decimal)

    def test_get_bliquidity(self):
        res = self.cbr_dws_client.get_bliquidity(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)

    def test_get_saldo(self):
        res = self.cbr_dws_client.get_saldo(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, value in res:
            assert isinstance(_date, datetime)
            assert isinstance(value, Decimal)

    def test_get_ruonia(self):
        res = self.cbr_dws_client.get_ruonia(datetime.now() - timedelta(days=15), datetime.now())
        assert isinstance(res, list)
        for _date, proc, value, date_pub in res:
            assert isinstance(_date, datetime)
            assert isinstance(proc, Decimal)
            assert isinstance(value, Decimal)
            assert isinstance(date_pub, datetime)
