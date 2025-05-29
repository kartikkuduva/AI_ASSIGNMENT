#!/usr/bin/env python
# coding: utf-8

# In[1]:


# agents/scraping_agent.py

import requests
from bs4 import BeautifulSoup

class ScrapingAgent:
    def __init__(self, base_url="https://finance.yahoo.com"):
        self.base_url = base_url

    def get_market_headlines(self, count=5):
        """
        Scrape top market news headlines from Yahoo Finance.

        Args:
            count (int): Number of headlines to return.

        Returns:
            list[dict]: A list of dictionaries with 'title' and 'link'.
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            headlines = []
            for tag in soup.select("h3 a")[:count]:
                title = tag.text.strip()
                link = tag["href"]
                if link.startswith("/"):
                    link = self.base_url + link
                headlines.append({"title": title, "link": link})

            return headlines

        except Exception as e:
            return [{"error": str(e)}]

