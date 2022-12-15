import numpy as np


class Indicator():

    def convert_number(self, value):
        return (float(str(float(np.format_float_scientific(value, unique=False, precision=8))).split('e-')[0]))

    def check_nhan_chim_tang(self, nen_truoc, nen_sau):
        if (nen_sau['open_price'] < nen_sau['close_price']) and (nen_truoc['open_price'] > nen_truoc['close_price']):
            change_vol_sau = (nen_sau['close_price'] - nen_sau['open_price']) / (nen_sau['open_price'] / 100)
            change_vol_truoc = (nen_truoc['close_price'] - nen_truoc['open_price']) / (nen_truoc['open_price'] / 100)
            if change_vol_sau > 1.3 and abs(change_vol_truoc) < change_vol_sau:
                return change_vol_sau

        return 0

    def check_rau(self, open_price, close_price, low_price, high_price):
        if close_price > open_price:
            rau = (high_price - close_price) / (open_price / 100)
        else:
            rau = (low_price - close_price) / (open_price / 100)
        if abs(rau) > 1.2:
            return round(abs(rau), 2)
        return 0

    def check_fox_wave(self, group_9_candle):
        group_3_candle_1 = [
            group_9_candle[0],
            group_9_candle[1],
            group_9_candle[2],
        ]
        group_3_candle_2 = [
            group_9_candle[3],
            group_9_candle[4],
            group_9_candle[5],
        ]
        group_3_candle_3 = [
            group_9_candle[6],
            group_9_candle[7],
            group_9_candle[8],
        ]
        up_count = self.up_count(group_3_candle_1, group_3_candle_2, group_3_candle_3)
        entry_check = self.check_entry(group_3_candle_3)
        check_count = self.check_up_down(group_9_candle)
        if up_count == 2 and entry_check == "up" and \
                check_count == "up":
            return "up"
        if up_count == 1 and entry_check == "down" and \
                check_count == "down":
            return "down"
        return "Khong có điểm vào"

    def check_entry(self, group_3_candle):

        if group_3_candle[0]["open_price"] < group_3_candle[0]["close_price"] and \
                group_3_candle[1]["open_price"] < group_3_candle[1]["close_price"] and \
                group_3_candle[2]["open_price"] > group_3_candle[2]["close_price"]:
            return "down"
        if group_3_candle[0]["open_price"] > group_3_candle[0]["close_price"] and \
                group_3_candle[1]["open_price"] > group_3_candle[1]["close_price"] and \
                group_3_candle[2]["open_price"] < group_3_candle[2]["close_price"]:
            return "up"

        return ""

    def up_count(self, group_3_candle_1, group_3_candle_2, group_3_candle_3):

        trend_group_1 = self.check_sub_wave(group_3_candle_1)
        trend_group_2 = self.check_sub_wave(group_3_candle_2)
        trend_group_3 = self.check_sub_wave(group_3_candle_3)
        up_count = 0
        if trend_group_1 == "up":
            up_count += 1
        if trend_group_2 == "up":
            up_count += 1
        if trend_group_3 == "up":
            up_count += 1

        return up_count

    def check_sub_wave(self, group_3_candle):
        trend = "down"
        candle_1 = group_3_candle[0]
        candle_2 = group_3_candle[1]
        candle_3 = group_3_candle[2]
        if candle_1['open_price'] < candle_3['close_price']:
            trend = 'up'
        return trend

    def check_up_down(self, group_9_candle):
        up_count = 0
        for candle in group_9_candle:
            if candle['open_price'] < candle['close_price']:
                up_count += 1
        if up_count >= 5:
            return "up"
        return "down"

    def check_volumn_candle(self, candle):
        volumn = (candle['high_price'] - candle['open_price']) / (candle['open_price'] / 100)
        if abs(volumn) > 4:
            return True
        return False
