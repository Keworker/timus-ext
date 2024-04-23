import random

from bs4 import BeautifulSoup
from requests import get


def userExist(id_: int) -> bool:  # {
    response = get(
        "https://acm.timus.ru/author.aspx",
        params={"id": id_, "locale": "en"}
    )
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    return not soup.find("div", style=lambda value: value and "color:Red" in value)
# }


def getUsername(id_: int) -> str:  # {
    response = get(
        "https://acm.timus.ru/author.aspx",
        params={"id": id_, "locale": "en"}
    )
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    try:  # {
        return soup.find("h2", attrs={"class": "author_name"}).text
    # }
    except AttributeError:  # {
        return str(id_)
    # }
# }


def getUsersProblemsDict(id_: int) -> dict:  # {
    response = get(
        "https://acm.timus.ru/author.aspx",
        params={"id": id_, "locale": "en", "sort": "difficulty"}
    )
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    result: dict = dict()
    for task in soup.find("table", attrs={"class": "attempt_list"}) \
                    .find_all("td"):  # {
        number: int = int(task.text)
        solutionStatus: str = task["class"][0]
        name: str = task.find("a")["title"]
        url: str = task.find("a")["href"]
        result[number] = {
            "name": name,
            "url": "https://acm.timus.ru/" + url,
            "solution_status": solutionStatus
        }
    # }
    return result
# }
