from collections import defaultdict
from dataclasses import dataclass, field

from bs4 import BeautifulSoup


@dataclass
class Parser:
    html: str
    soup: BeautifulSoup = field(init=False)
    counters: defaultdict[str, int] = field(init=False)

    def __post_init__(self) -> None:
        self.soup = BeautifulSoup(self.html, "html.parser")
        self.counters = defaultdict(int)

    def criar_ids(self) -> None:
        for tag in self.soup.find_all(True):
            tag_name = tag.name
            self.counters[tag_name] += 1
            novo_id = f"{tag_name}-{self.counters[tag_name]:03d}"
            tag["upa11y-id"] = novo_id

    def obter_elementos(self):
        return self.soup.find_all(True)

    def obter_soup(self):
        return self.soup

    def para_html(self):
        return str(self.soup)
