from src.dataminer import DataMiner
from src.problem import Tier

if __name__ == '__main__':
    tier_list = [Tier.BRONZE, Tier.SILVER, Tier.GOLD]
    miner = DataMiner()

    for tier in tier_list:
        problem = miner.get_problem_soup(tier)
        print(problem.name, end=" ")
        print(problem.get_problem_link())