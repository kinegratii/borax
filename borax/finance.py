# coding=utf8

from decimal import Decimal

from typing import Union

import warnings

from borax.numbers import FinanceNumbers

__all__ = ['financial_amount_capital']


def financial_amount_capital(num: Union[int, float, Decimal, str]) -> str:
    warnings.warn(
        'This method is deprecated and will be removed in V3.5.Use borax.numbers.FinanceNumbers instead.',
        category=PendingDeprecationWarning
    )

    return FinanceNumbers.to_capital_str(num)
