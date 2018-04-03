# coding: utf-8

import requests
import pickle


class GetQQNum(object):
    def __init__(self, bkn, cookie):
        """
        初始化参数


        """

        self.bkn = bkn
        self.cookie = cookie
        self.mem_lst = self.__get_uin_lst()

    def __get_uin_lst(self):
        """
        获取qq好友qq号(uin)和对应备注(name), 保存在mem_lst中
        [{'name': 'aaa', 'uin': 123456},
        {'name': 'bbb', 'uin': 12030},
        {'name': 'ccc', 'uin': 303},
        {'name': 'ddd', 'uin': 341}]
        """

        # 请求的url
        url = "http://qun.qq.com/cgi-bin/qun_mgr/get_friend_list"
        # 请求携带的参数
        payload = {"bkn": self.bkn}
        headers = {
            "cookie":
            self.cookie,
            "user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        response = requests.post(url, data=payload, headers=headers).json()

        # 如果参数正确应该能够获取到相应的信息
        try:
            friends_json = response["result"]
        except Exception:
            raise TypeError("Please input correct params")

        # 获取每个分组，可能存在分组为空的情况

        for key in friends_json.keys():
            if not friends_json.get(key, 0):
                del friends_json[key]

        mem_lst = [
            friend for key, friend_value in friends_json.items()
            for friend in friend_value["mems"]
        ]

        return mem_lst

    def save_data(self, fname):
        """
        保存信息到本地
        """
        with open(fname, "wb+") as f:
            pickle.dump(self.mem_lst, f)
