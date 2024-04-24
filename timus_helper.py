from bs4 import BeautifulSoup
from requests import get


TIMUS_BASE_URL: str = "https://acm.timus.ru/"


def userExist(id_: int) -> bool:  # {
    """
    Check if Timus user exist.
    :param id_: id of Timus user
    :return: bool
    """
    response = get(
        f"{TIMUS_BASE_URL}author.aspx",
        params={"id": id_, "locale": "en"}
    )
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    return not soup.find("div", style=lambda value: value and "color:Red" in value)
# }


def getUsername(id_: int) -> str:  # {
    """
    Returns Timus user's name.
    :param id_: id of Timus user
    :return: str
    """
    response = get(
        f"{TIMUS_BASE_URL}author.aspx",
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
    """
    Return dict with all tasks for Timus user.
    :param id_: id of Timus user
    :return: dict
    """
    response = get(
        f"{TIMUS_BASE_URL}author.aspx",
        params={"id": id_, "locale": "en", "sort": "difficulty"}
    )
    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")
    result: dict = {}
    for task in soup.find("table", attrs={"class": "attempt_list"}) \
                    .find_all("td"):  # {
        number: int = int(task.text)
        solutionStatus: str = task["class"][0]
        name: str = task.find("a")["title"]
        url: str = task.find("a")["href"]
        result[number] = {
            "name": name,
            "url": TIMUS_BASE_URL + url.replace("status.aspx", "problem.aspx"),
            "solution_status": solutionStatus
        }
    # }
    return result
# }
