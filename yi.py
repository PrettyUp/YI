import random
import datetime
from yi_book import book


class YiProgram():
    def __init__(self):
        pass

    # 设置随机数种子，确保用户输入一样时，得到的随机数是一样的
    def _set_random_seed(self, time_seed_str):
        def _transfer_str_to_time_seed():
            user_input_str_bytes = time_seed_str.encode()
            inner_random_seed = 0
            for tmp_byte in user_input_str_bytes:
                inner_random_seed += tmp_byte
            return inner_random_seed
        random_seed = _transfer_str_to_time_seed()
        random.seed(random_seed)

    # 执行一轮变化
    def _exec_one_transfer(self, cosmos_count):
        # 第一步，将四十九颗棋子随机分为左右两组，象征混沌初开，天地一分为二，一边为天，一边为地。
        cosmos_list = [1] * cosmos_count
        divide_index = random.randint(int(cosmos_count/3), int(cosmos_count/3)*2)
        sky_list = cosmos_list[:divide_index]
        land_list = cosmos_list[divide_index:]
        # 第二步，有天有地就该有人，所以任意拿掉一组中的一个棋子，这颗棋子便为人。然后形成三才。
        person_point = random.randint(0,cosmos_count)
        if person_point < divide_index:
            sky_list.pop()
        else:
            land_list.pop()
        # 第三步，以象征天的那组棋子数除以四，获得余数，如果整除则余数改为4（这里的四象征着一年四季）。
        sky_remainder = len(sky_list) % 4
        if sky_remainder == 0:
            sky_remainder = 4
        # sky_list = sky_list[:-sky_remainder]
        # 第四步，对象征地的那组进行同样的操作。
        land_remainder = len(land_list) % 4
        if land_remainder == 0:
            land_remainder = 4
        # land_list = land_list[:-land_remainder]
        # 第五步，减去象征人的棋子及两组的余数，获取剩余的棋子数
        remove_count = 1 + sky_remainder + land_remainder
        cosmos_count = cosmos_count - remove_count
        return cosmos_count

    # 递规执行三轮变化获取剩余的棋子数，即一爻
    def _gen_one_symbol(self, cosmos_count=49, transfer_index=0):
        cosmos_count = self._exec_one_transfer(cosmos_count)
        transfer_index += 1
        if transfer_index >= 3:
            return cosmos_count
        else:
            return self._gen_one_symbol(cosmos_count=cosmos_count, transfer_index=transfer_index)

    # 获取六爻，组成本卦
    def _gen_origin_hexagram(self):
        six_symbol_list = []
        for symbol_index in range(6):
            tmp_symbol = int(self._gen_one_symbol() / 4)
            six_symbol_list.append(tmp_symbol)
        return six_symbol_list

    # 根据本卦获取变卦
    def _gen_support_hexagram(self, origin_hexagram):
        support_hexagram = []
        for tmp_value in origin_hexagram:
            if tmp_value == 6:
                tmp_value = 9
            elif tmp_value == 9:
                tmp_value = 6
            support_hexagram.append(tmp_value)
        return support_hexagram

    # 分析变爻数及变爻下标列表
    def _get_turn_symbol_count_and_index_list(self, origin_hexagram, support_hexagram):
        turn_symbol_count = 0
        turn_symbol_index_list = []
        not_turn_symbol_index_list = []
        for index in range(len(origin_hexagram)):
            if origin_hexagram[index] != support_hexagram[index]:
                turn_symbol_count += 1
                turn_symbol_index_list.append(index)
            else:
                not_turn_symbol_index_list.append(index)
        return turn_symbol_count,turn_symbol_index_list,not_turn_symbol_index_list

    # 偶数为阴，奇数为阳
    def _get_hexagram_dict_key(self, hexagram):
        hexagram_dict_key = ""
        for tmp_value in hexagram:
            hexagram_dict_key += str(tmp_value % 2)
        return hexagram_dict_key

    # 解卦
    def _parser_hexagram(self, origin_hexagram, support_hexagram):
        main_indicate = ""
        support_indicate = ""
        turn_symbol_desc = ""
        origin_hexagram_dict_key = self._get_hexagram_dict_key(origin_hexagram)
        support_hexagram_dict_key = self._get_hexagram_dict_key(support_hexagram)
        turn_symbol_count,turn_symbol_index_list,not_turn_symbol_index_list = self._get_turn_symbol_count_and_index_list(origin_hexagram, support_hexagram)
        # 六爻皆不变者，占本卦卦辞
        if turn_symbol_count == 0:
            turn_symbol_desc = "六爻皆不变者，占本卦卦辞。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][0]
        # 一爻变者，以本卦变爻之辞占
        elif turn_symbol_count == 1:
            turn_symbol_desc = "一爻变者，以本卦变爻之辞占。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[0]+1]
        # 二爻变者，则以本卦二变爻之辞占，而以上爻之辞为主
        elif turn_symbol_count == 2:
            turn_symbol_desc = "二爻变者，则以本卦二变爻之辞占，而以上爻之辞为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[1]+1]
            support_indicate = book[origin_hexagram_dict_key]["indicate"][turn_symbol_index_list[0]+1]
        # 三爻变者，占本卦及之卦的卦辞，而以本卦为主
        elif turn_symbol_count == 3:
            turn_symbol_desc = "三爻变者，占本卦及之卦的卦辞，而以本卦为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][0]
            support_indicate = book[support_hexagram_dict_key]["indicate"][0]
        # 四爻变者，以之卦中二不变之爻辞占，以下爻为主
        elif turn_symbol_count == 4:
            turn_symbol_desc = "四爻变者，以之卦中二不变之爻辞占，以下爻为主。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[0]+1]
            support_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[1]+1]
        # 五爻变者，以之卦中不变爻的爻辞占
        elif turn_symbol_count == 5:
            turn_symbol_desc = "五爻变者，以之卦中不变爻的爻辞占。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][not_turn_symbol_index_list[0]+1]
        # 六爻皆变者，以乾坤二用之辞占，并参考其之卦卦辞
        elif turn_symbol_count == 6:
            turn_symbol_desc = "六爻皆变者，以乾坤二用之辞占，并参考其之卦卦辞。"
            main_indicate = book[origin_hexagram_dict_key]["indicate"][7]
            support_indicate = book[support_hexagram_dict_key]["indicate"][0]
        return turn_symbol_desc,main_indicate,support_indicate

    def main_logic_new(self):
        user_wish = input("请输入你所求之事:")
        user_pray = input(f"请输入你的祈祷：")
        today = datetime.datetime.now().__format__("%Y%m%d")
        time_seed_str = user_wish + user_pray + today
        # 设置随机数种子，确保当天同样的输出得到的结果是一样的
        self._set_random_seed(time_seed_str)
        print("\n稍等，正在计算卦象...")
        # 生成本卦
        origin_hexagram = self._gen_origin_hexagram()
        # 计算变卦
        support_hexagram = self._gen_support_hexagram(origin_hexagram)
        # 本卦对应的内容的key
        origin_hexagram_dict_key = self._get_hexagram_dict_key(origin_hexagram)
        # 变卦对应的内容的key
        support_hexagram_dict_key = self._get_hexagram_dict_key(support_hexagram)
        print(f"本卦：{origin_hexagram}--{book[origin_hexagram_dict_key]['name']}--{book[origin_hexagram_dict_key]['come_from']}\n"
              f"变卦：{support_hexagram}--{book[support_hexagram_dict_key]['name']}--{book[support_hexagram_dict_key]['come_from']}")
        print("\n稍等，正在解卦...")
        # 解卦
        turn_symbol_desc, main_indicate, support_indicate = self._parser_hexagram(origin_hexagram, support_hexagram)
        print(f"说明：{turn_symbol_desc}\n"
              f"主预言：{main_indicate}\n"
              f"辅预言：{support_indicate}")

if __name__ == "__main__":
    obj = YiProgram()
    obj.main_logic_new()
