from bs4 import BeautifulSoup
from collections import defaultdict

class Parser:
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")
        self.counters = defaultdict(int)

    def criar_ids(self):
        for tag in self.soup.find_all(True):
            tag_name = tag.name
            self.counters[tag_name] += 1
            novo_id = f"{tag_name}-{self.counters[tag_name]:03d}"
            tag["upa11y-id"] = novo_id

    def obter_elementos(self):
        return self.soup.find_all(True)

    def para_html(self):
        return str(self.soup)