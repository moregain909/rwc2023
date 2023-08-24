
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
from dataclasses import dataclass, field, asdict

driver = webdriver.Firefox()

pool_names = ["a", "b", "c", "d"]

