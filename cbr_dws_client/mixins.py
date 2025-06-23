class ParseResponseCbrMixin:
    """Миксин для методов парсинга ответа от сервиса ЦБ."""

    def parse_result_to_list(self, data: dict) -> list:
        return data["_value_1"]["_value_1"]

    def parse_currency_on_date_dict(self, data: dict, detail_currency_char_code: str | None = None):
        """Метод обработки ответа от сервиса ЦБ.

        :param data: Изначальный ответ.
        :param detail_currency_char_code: Код валюты.
        :return: Список значений или значение в зависимости от detail_currency_char_code.
        """
        parsed_data = self.parse_result_to_list(data=data)
        result = parsed_data
        if detail_currency_char_code:
            for elem in parsed_data:
                break_elements = False
                for _, v in elem.items():
                    if (getattr(v, "VchCode", None) == detail_currency_char_code) | (
                        getattr(v, "VcharCode", None) == detail_currency_char_code
                    ):
                        result = v
                        break_elements = True
                        break
                if break_elements:
                    break
        return result
