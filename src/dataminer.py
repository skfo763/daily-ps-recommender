import urllib3
import random
import re
from bs4 import BeautifulSoup
from src.problem import Problem


class DataMiner:

    def __init__(self):
        self.base_url = "https://www.acmicpc.net"

    def _get_url(self, path):
        return f"{self.base_url}/{path}"

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
