import httpx
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from dataclasses import dataclass, field, asdict
import config

#client = httpx.Client()
#headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
#response = client.get(matches_url, headers=headers, follow_redirects=True)


driver = config.driver

matches_url = "https://rugbyworldcup.com/2023/matches"

driver.get(matches_url)
time.sleep(2)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

pool_names = config.pool_names

all_pool_matches = []
for pool in pool_names:
    matches_blocks = soup.find_all("div", class_=f"fixtures__match-wrapper fixtures__match-wrapper--upcoming fixtures__match-wrapper--pool-{pool} js-match")   
    all_pool_matches.extend(matches_blocks)


@dataclass
class Match:
    match_id: str = field(repr=None, default=None)
    time: str = field(repr=None, default=None)
    venue: str = field(repr=None, default=None)
    phase: str = field(repr=None, default=None)
    team_a: str = field(repr=True, default=None)
    score_a: str = field(repr=None, default=None)
    team_b: str = field(repr=True, default=None)
    score_b: str = field(repr=None, default=None)
    pool: str = field(repr=None, default=None)
    

#   GET MATCHES

matches = []
for match_block in all_pool_matches:
    match = Match()

    match.match_id = match_block.find_all("a", href=True)[0]["href"].split("/")[-1]
    day = match_block.find("span", class_="fixtures-date__day-number").text.strip(" ")
    month = match_block.find("span", class_="fixtures-date__month").text.strip(" ")
    match.time = match_block.find("span", class_="bolder js-your-time").text
    match.pool = match_block.find("span", class_="fixtures__event-phase").text.split(" ")[1]
    # trae el nombre del equipo A
    team_a = match_block.find_all("span", class_="fixtures__team-name")[0]
    extra_span_a = team_a.find("span", class_="fixtures__team-name-win")
    if extra_span_a:
        extra_span_a.extract()
    match.team_a = team_a.get_text(strip=True)
    match.score_a = match_block.find("span", class_="fixtures__team-score js-team-a-score").text

    # trae el nombre del equipo B
    team_b = match_block.find_all("span", class_="fixtures__team-name")[1]
    extra_span_b = team_b.find("span", class_="fixtures__team-name-win")
    if extra_span_b:
        extra_span_b.extract()
    match.team_b = team_b.get_text(strip=True)
    match.score_b = match_block.find("span", class_="fixtures__team-score js-team-b-score").text
    
    match.phase = match_block.find("span", class_="fixtures__event-phase").text
    match.venue = match_block.find("span", class_="fixtures__venue").text

    matches.append(match)

for m in matches:
    match = asdict(m)
    print(f"{match['team_a']} - {match['team_b']}")
    print(m)







