# -*- coding: utf-8 -*-

#  Copyright (c) ©2019, Cardinal Operations and/or its affiliates. All rights reserved.
#  CARDINAL OPERATIONS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

# @author: songjie@shanshu.ai
# @date: 2019/10/03
import decimal
import math

from marshmallow.fields import Integer, Float, Decimal
import numbers

class UdfInt(Integer):
    def _validated(self, value):
        if value == '':
            return None
        if self.strict:
            if isinstance(value, numbers.Number) and isinstance(
                    value, numbers.Integral
            ):
                return super()._validated(value)
            raise self.make_error("invalid", input=value)
        return super()._validated(value)

class UdfFloat(Float):
    def _validated(self, value):
        if value == '':
            return None
        num = super()._validated(value)
        if self.allow_nan is False:
            if math.isnan(num) or num == float("inf") or num == float("-inf"):
                raise self.make_error("special")
        return num

class UdfDecimal(Decimal):
    def _validated(self, value):
        if value == '':
            return None
        try:
            num = super()._validated(value)
        except decimal.InvalidOperation as error:
            raise self.make_error("invalid") from error
        if not self.allow_nan and (num.is_nan() or num.is_infinite()):
            raise self.make_error("special")
        return num
