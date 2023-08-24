#import httpx
#from selenium import webdriver
from bs4 import BeautifulSoup
#import re
import time
from dataclasses import dataclass, field, asdict
import config

driver = config.driver

pools_url = "https://www.rugbyworldcup.com/2023/pools"

driver.get(pools_url)
time.sleep(2)
pools_html = driver.page_source

pools_soup = BeautifulSoup(pools_html, "html.parser")

@dataclass
class Row:
    name: str = field(repr=True, default=None)
    name_short: str = field(repr=True, default=None)
    played: str = field(repr=True, default=None)
    won: str = field(repr=True, default=None)
    drawn: str = field(repr=True, default=None)
    lost: str = field(repr=True, default=None)
    points: str = field(repr=True, default=None)
    points_against: str = field(repr=True, default=None)
    diff: str = field(repr=True, default=None)
    tries: str = field(repr=True, default=None)
    bonus: str = field(repr=True, default=None)
    points: str = field(repr=True, default=None)

@dataclass
class Pool:
    name: str = field(repr=True, default=None)
    teams: list[Row] = field(repr=True, default_factory=list)
    
pools_block = pools_soup.find("div", class_="pools__items-wrapper")

pool_names = config.pool_names

pools = []

for p in pool_names:
    pool = Pool()
    pool.name = p.upper()

    if p == "a":
        p = "a active"

    
    pool_block = pools_block.find("div", class_=f"pools__item-wrapper js-tab pools__item-wrapper--pool-{p}")
    
    rows_block = pool_block.find_all("tr", class_="pools__row")

    for r in rows_block:
        row = Row()
        row.name_short = r.find("div", class_="pools__team-name pools__team-name--short").text
        row.name = r.find("div", class_="pools__team-name pools__team-name--long").text
        row.played = r.find("td", class_="pools__cell pools__cell--played").text.strip()
        row.won = r.find("td", class_="pools__cell pools__cell--won").text.strip()
        row.drawn = r.find("td", class_="pools__cell pools__cell--drawn").text.strip()
        row.lost = r.find("td", class_="pools__cell pools__cell--lost").text.strip()
        row.points = r.find("td", class_="pools__cell pools__cell--points-for").text.strip()        
        row.points_against = r.find("td", class_="pools__cell pools__cell--points-against").text.strip()        
        row.diff = r.find("td", class_="pools__cell pools__cell--diff").text.strip()
        row.tries = r.find("td", class_="pools__cell pools__cell--tries-for").text.strip()
        row.bonus = r.find("td", class_="pools__cell pools__cell--bp").text.strip()
        row.points = r.find("td", class_="pools__cell pools__cell--points").text.strip()
        print(row)
        pool.teams.append(row)
    print()
    
    pools.append(pool)


