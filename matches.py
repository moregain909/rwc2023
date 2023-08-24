import httpx
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from dataclasses import dataclass, field

#client = httpx.Client()
#headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
#response = client.get(matches_url, headers=headers, follow_redirects=True)

@dataclass
class Match:
    
    match_id: str = field(repr=True)
    #venue
    #phase
    #date: str
    #time: str
    #team_a: str
    #team_a_score: int
    #team_b: str
    #team_b_score: int
    
@dataclass
class Team:
    name: str = field(repr=True)
    pool: str
    profile_link: str = field(repr=True)



driver = webdriver.Chrome()


#   GET MATCHES

matches = []
matches_url = "https://rugbyworldcup.com/2023/matches"

driver.get(matches_url)
time.sleep(2)
html = driver.page_source

soup = BeautifulSoup(html, "html.parser")

matches_blocks = soup.find_all("div", class_="fixtures__match-wrapper fixtures__match-wrapper--upcoming fixtures__match-wrapper--pool-a js-match")

for match_block in matches_blocks:

    match_id = match_block.find_all("a", href=True)[0]["href"].split("/")[-1]
    day = match_block.find("span", class_="fixtures-date__day-number").text.strip(" ")
    month = match_block.find("span", class_="fixtures-date__month").text.strip(" ")
    my_time = match_block.find("span", class_="bolder js-your-time").text

    # trae el nombre del equipo A
    team_a = match_block.find_all("span", class_="fixtures__team-name")[0]
    extra_span_a = team_a.find("span", class_="fixtures__team-name-win")
    if extra_span_a:
        extra_span_a.extract()
    team_a = team_a.get_text(strip=True)
    score_a = match_block.find("span", class_="fixtures__team-score js-team-a-score").text

    # trae el nombre del equipo B
    team_b = match_block.find_all("span", class_="fixtures__team-name")[1]
    extra_span_b = team_b.find("span", class_="fixtures__team-name-win")
    if extra_span_b:
        extra_span_b.extract()
    team_b = team_b.get_text(strip=True)
    score_b = match_block.find("span", class_="fixtures__team-score js-team-b-score").text
    
    phase = match_block.find("span", class_="fixtures__event-phase").text
    venue = match_block.find("span", class_="fixtures__venue").text


#   GET TEAMS