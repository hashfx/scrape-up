from bs4 import BeautifulSoup
import requests


class ICC:
    """
    Create an instance of `ICC` class.
    ```python
    scraper = ICC()
    ```
    | Method                       | Details                                                             |
    | ---------------------------- | ------------------------------------------------------------------- |
    | `.team_rankings(format)`     | Returns the list of rankings of teams of desired format             |
    |`.player_ranking(type,format)`| Returns the list of player ranking of desired type and format       |
    """

    def __init__(self):
        self.url = "https://www.icc-cricket.com/rankings/mens/"

    def team_rankings(self, format):
        """
        Create an instance of `ICC` class.\n
        Required Params - `format` - "ODI","T20" or "TEST"
        ```python
        icc = ICC()
        icc.team_rankings(format="odi")
        ```
        ```js
        [
            {
                "rank":1,
                "team":"Australia"
            }
        ]
        ```
        """
        try:
            format = format.lower()
            obj_keys = ["rank", "team"]
            resposne_list = []
            url = self.url + "team-rankings/" + format
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            teams = soup.find_all("span", class_="u-hide-phablet")
            for rank, team in enumerate(teams, 1):
                obj_values = [rank, team.get_text()]
                resposne_list.append(dict(zip(obj_keys, obj_values)))

            return resposne_list
        except:
            return None

    def player_ranking(self, type, format):
        """
        Create an instance of `ICC` class.\n
        Required Params
        - `format` - "ODI","T20" or "TEST"
        - `type` - "batting","bowling" or "all-rounder"\n
        ```python
        icc = ICC()
        icc.team_player(format="test",type="batting")
        ```
        Returns \n
        ```js
        [
            {
                "rank":1,
                "team":"Kane Williamson"
            }
            ...
        ]
        ```
        """
        try:
            format = format.lower()
            type = type.lower()
            response_list = []
            obj_keys = ["rank", "name"]
            url = self.url + f"/player-rankings/{format}/{type}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            top_player = soup.find(
                "div", class_="rankings-block__banner--name-large"
            ).get_text()
            rest_players = soup.find_all(
                "td", class_="table-body__cell rankings-table__name name"
            )
            response_list.append(dict(zip(obj_keys,[1,top_player])))
            for rank, player in enumerate(rest_players, 2):
                obj_values = [rank, player.get_text().replace("\n", "")]
                response_list.append(dict(zip(obj_keys, obj_values)))

            return response_list
        except:
            return None
