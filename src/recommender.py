from enum import Enum
import urllib3
import random
import re
from bs4 import BeautifulSoup


class Tier(Enum):
    BRONZE = "1,2,3,4,5"
    SILVER = "6,7,8,9,10"
    GOLD = "11,12,13,14,15"
    PLATINUM = "16,17,18,19,20"
    DIAMOND = "21,22,23,24,25"


class Problem:
    def __init__(self, soup):
        td_list = soup.find_all('td')
        self.base_url = "https://www.acmicpc.net"
        self.id = td_list[0].get_text()
        self.name = soup.find('a').get_text()
        self.href = soup.find('a')['href']
        self.correct_rate = td_list[-1].get_text()

    def get_problem_link(self):
        return self.base_url + self.href


class DataMiner:

    def __init__(self):
        self.base_url = "https://www.acmicpc.net"

    def _get_url(self, path):
        return self.base_url + path

    @staticmethod
    def parse_into_problem(soup):
        soup = soup.find("table", attrs={"id": "problemset"}).find("tbody").find_all("tr")
        return list(map(lambda x: Problem(x), soup))

    @staticmethod
    def get_max_page(http, url, tier):
        query_param = {"tier": tier.value}
        res = http.request('GET', url, query_param)
        soup = BeautifulSoup(res.data, 'lxml')
        return int(soup.find("ul", attrs={"class": "pagination"}).find_all('li')[-1].find('a').get_text())

    @staticmethod
    def is_korean_problem(problem_name):
        return len(re.compile('[가-힣]+').findall(problem_name)) > 0

    def get_problem_soup(self, tier):
        url = self._get_url("problemset")
        http = urllib3.PoolManager()
        pagination_num = self.get_max_page(http, url, tier)
        random_page = random.randrange(1, pagination_num + 1)
        query_param = {"tier": tier.value, "page": random_page}
        res = http.request('GET', url, query_param)
        soup = BeautifulSoup(res.data, "lxml")
        problem_list = self.parse_into_problem(soup)

        for _ in range(len(problem_list)):
            random_problem = random.choice(problem_list)
            if self.is_korean_problem(random_problem.name):
                return random_problem
        return None


if __name__ == '__main__':
    tier_list = [Tier.BRONZE, Tier.SILVER, Tier.GOLD]
    miner = DataMiner()

    for tier in tier_list:
        problem = miner.get_problem_soup(tier)
        print(problem.name, end=" ")
        print(problem.get_problem_link())
