from enum import Enum


class Tier(Enum):
    BRONZE = "1,2,3,4,5"
    SILVER = "6,7,8,9,10"
    GOLD = "11,12,13,14,15"
    PLATINUM = "16,17,18,19,20"
    DIAMOND = "21,22,23,24,25"
    # RUBY 는 없습니다. 제가 절대 풀 수가 없기 때문이죠.


class Problem:
    def __init__(self, soup):
        td_list = soup.find_all('td')
        self.base_url = "https://www.acmicpc.net"
        self.id = td_list[0].get_text()
        self.name = soup.find('a').get_text()
        self.href = soup.find('a')['href']
        self.correct_rate = td_list[-1].get_text()

    def get_problem_link(self):
        return f"{self.base_url}{self.href}"