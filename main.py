# -*- coding: utf-8 -*-
from typing import Dict, List
import random
import requests

class Launch():
    robot_hd_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=*****'

    def __init__(self, restaurants: Dict[str, int], users: List[str]):
        self.restaurants = restaurants
        self.msg = {
            'msgtype': 'text',
            'text': {
                    'content': '{restaurants_table}\n{star}\n'.format(
                        restaurants_table=self.restaurants_list_format(),
                        star=self.today_star_restaurant()),
                    # 'mentioned_list':['@all'],
                    'mentioned_mobile_list': users
                }
        }

    @staticmethod
    def md_table_item(key: str, val: str):
        return '| {key} | {val} |\n'.format(key=key, val=val)

    def restaurants_list_format(self) -> str:
        # md_table = '| 餐厅列表 | 评分(权重) |\n| --- | --- |\n'
        restaurant_list = '{r}评分(权重)\n'.format(r='餐厅列表'.ljust(6, chr(12288)))
        i = 1
        for k, v in self.restaurants.items():
            restaurant_list += '{index}. {key}{val}\n'.format(index=i, key=k.ljust(7, chr(12288)), val=str(v))
            i += 1
        return restaurant_list

    def today_star_restaurant(self) -> str:
        restaurant_list = []
        for k, v in self.restaurants.items():
            for _ in range(v):
                restaurant_list.append(k)
        random.shuffle(restaurant_list)
        star_restaurants = random.sample(restaurant_list, 2)
        star = '✧今日星选餐厅✧\n'
        for i in range(len(star_restaurants)):
            star += '✓ %s\n' % star_restaurants[i]
        return star

    def go(self):
        requests.post(Launch.robot_hd_url, json = self.msg)

def main():
    restaurants = {
        '剪花娘子': 7,
        '胡椒厨房': 7,
        '东北风': 5,
        '椒锅锅': 5,
        '外婆家': 7,
        '小菜园': 8,
    }
    users = ['1880027****', '1861681****', '1719991****', '1565141****']
    Launch(restaurants, users).go()

def handler(event, context):
    return main()

if __name__ == '__main__':
    main()
