"""
=====================
Get manga related stuff.
=====================
"""

import requests
from bs4 import BeautifulSoup
from AniManga.helpers.helpers import check_if_exists
from AniManga.helpers.helpers import format_ as format_manga_name

class Manga:
    """
    Manga class.
    """

    def __init__(self, verbose=False):
        """
        __init__
        """
        self.base_manga_url = "https://www.anime-planet.com/manga/"
        self.base_manga_reviews = "https://www.anime-planet.com/manga/{}/reviews"
        self.base_manga_tags = "https://www.anime-planet.com/manga/"
        self.verbose = verbose

    def get_manga_json(self, manga: str) -> dict:
        """Get information on a manga.

        Args:
            manga (str): manga name you want to search for.

        Returns:
            dict: dict with information on the manga.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")
        soup = BeautifulSoup(r.content, "html5lib")
        tags = soup.find_all("div", {"class": "tags"})
        rr = requests.get(self.base_manga_reviews.format(manga))
        rsoup = BeautifulSoup(rr.content, "html5lib")

        if check_if_exists(manga):

            rank = soup.find_all("div", {"class": "pure-1 md-1-5"})
            for x in rank:
                if x.text.startswith("\nRank"):
                    rank = x.text.replace("\n", "")

            tags_list = []

            for x in tags:
                x = x.find_all("li")
                for z in x:
                    z = z.text.replace("\n", "")
                    tags_list.append(z)

            characters = []
            for x in soup.find_all(
                "strong", {"class": "CharacterCard__title rounded-card__title"}
            ):
                characters.append(x.text)

            characters = characters[:-1]

            warning_list = []

            content_warning = soup.find_all(
                "div", {"class": "tags tags--plain"})

            for x in content_warning:
                x = x.text.replace("\n", "").replace("Content Warning", "")
                warning_list.append(x)

            reviews = rsoup.find_all(
                "div", {"class": "pure-1 userContent readMore"})
            review_list = []

            for x in reviews:
                review_list.append(x)

            reviews = []

            for x in review_list:
                string = ""
                while True:
                    try:
                        x = x.find("p")
                        x = x.getText()
                        string += f"{x}\n"
                    except Exception:
                        break

                reviews.append(string)

            manga_dict = {}
            manga_dict["title"] = soup.find("meta", property="og:title")["content"]
            manga_dict["description"] = soup.find("meta", property="og:description")[
                "content"
            ]
            manga_dict["url"] = soup.find("meta", property="og:url")["content"]
            manga_dict["type"] = soup.find("meta", property="og:type")["content"]
            manga_dict["size"] = soup.find("div", {"class": "pure-1 md-1-5"}).text.replace(
                "\n", ""
            )
            manga_dict["year"] = soup.find("span", {"class": "iconYear"}).text.replace(
                "\n", ""
            )
            manga_dict["rating"] = soup.find("div", {"class": "avgRating"}).text.replace(
                "\n", ""
            )
            manga_dict["rank"] = rank
            manga_dict["author"] = soup.find(
                "meta", property="book:author")["content"]
            manga_dict["author"] = manga_dict["author"].replace(
                "https://www.anime-planet.com/people/", ""
            )
            manga_dict["cover"] = soup.find("meta", property="og:image")["content"]
            manga_dict["tags"] = tags_list
            manga_dict["content warning"] = warning_list
            manga_dict["characters"] = characters
            manga_dict["reviews"] = reviews
            try:
                return manga_dict
            except Exception:
                return "We could not find that. Manga is most likely not available."
        else:
            return "We could not find that."

    def get_manga_description(self, manga: str) -> str:
        """Gets description of a manga.

        Args:
            manga (str): manga for which description you need.

        Returns:
            str: description of the manga.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            description = soup.find("meta", property="og:description")["content"]
        else:
            description = "Manga could not be found, it most likely doesnt exist."
        return description

    def get_manga_url(self, manga: str) -> str:
        """Get Anime-Planet URL of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: Anime-Planet URL.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            url = soup.find("meta", property="og:url")["content"]
        else:
            url = "Manga could not be found, it most likely doesnt exist."
        return url

    def get_manga_size(self, manga: str) -> str:
        """Get the chapters/volume of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: chapters/volume numbers.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            size = soup.find("div", {"class": "pure-1 md-1-5"}).text.replace("\n", "")
        else:
            size = "Manga could not be found, it most likely doesnt exist."
        return size

    def get_manga_year(self, manga: str) -> str:
        """Get the years a manga ran.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: years the manga ran.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            year = soup.find("span", {"class": "iconYear"}).text.replace("\n", "")
        else:
            year = "Manga could not be found, it most likely doesnt exist."
        return year

    def get_manga_rating(self, manga: str) -> str:
        """Get the rating of a manga

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: the rating.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            rating = soup.find("div", {"class": "avgRating"}).text.replace("\n", "")
        else:
            rating = "Manga could not be found, it most likely doesnt exist."
        return rating

    def get_manga_rank(self, manga: str) -> str:
        """Get the rank of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: the rank.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            rank = soup.find_all("div", {"class": "pure-1 md-1-5"})
            for x in rank:
                if x.text.startswith("\nRank"):
                    rank = x.text.replace("\n", "")
        else:
            rank = "Manga could not be found, it most likely doesnt exist."
        return rank

    def get_manga_cover(self, manga: str) -> str:
        """Get the cover image url of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: cover image url. 
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            cover = soup.find("meta", property="og:image")["content"]
        else:
            cover = "Manga could not be found, it most likely doesnt exist."
        return cover
        

    def get_manga_author(self, manga: str) -> str:
        """Get the author of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            str: author.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            author = soup.find("meta", property="book:author")["content"]
            author = author.replace("https://www.anime-planet.com/people/","")
        else:
            author = "Manga could not be found, it most likely doesnt exist."
        return author

    def get_manga_tags(self, manga: str) -> list:
        """Get the tags of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            list: tags of the manga.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            tags = soup.find_all("div", {"class": "tags"})
            tags_list = []

            for x in tags:
                x = x.find_all("li")
                for z in x:
                    z = z.text.replace("\n", "")
                    tags_list.append(z)
        else:
            tags_list = "Manga could not be found, it most likely doesnt exist."
        return tags_list

    def get_manga_content_warning(self, manga: str) -> list:
        """Get the content warning of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            list: content warning.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            soup = BeautifulSoup(r.content, "html5lib")
            warning_list = []

            content_warning = soup.find_all(
                "div", {"class": "tags tags--plain"})

            for x in content_warning:
                x = x.text.replace("\n", "").replace("Content Warning", "")
                warning_list.append(x)

        else:
            warning_list = "Manga could not be found, it most likely doesnt exist."
        return warning_list

    def get_manga_reviews(self, manga: str) -> list:
        """Get the reviews of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            list: reviews of the manga.
        """
        manga = format_manga_name(manga)
        r = requests.get(self.base_manga_url + f"{manga}")

        if check_if_exists(manga):
            rr = requests.get(self.base_manga_reviews.format(manga))
            rsoup = BeautifulSoup(rr.content, "html5lib")
            reviews = rsoup.find_all(
                "div", {"class": "pure-1 userContent readMore"})
            
            review_list = []

            for x in reviews:
                review_list.append(x)

            reviews = []

            for x in review_list:
                string = ""
                while True:
                    try:
                        x = x.find("p")
                        x = x.getText()
                        string += f"{x}\n"
                    except Exception as ex:
                        break

                reviews.append(string)
        else:
            reviews = "Manga could not be found, it most likely doesnt exist."
        return reviews

    def get_manga_characters(self, manga: str) -> list:
        """Get the characters of a manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            list: characters.
        """
        manga = format_manga_name(manga)

        r = requests.get(
            "https://www.anime-planet.com/manga/{}/characters".format(manga)
        )
        soup = BeautifulSoup(r.content, "html5lib")
        
        try:
            character_list = []
            characters = soup.find_all("a", {"class": "name"})
            for i in characters:
                character_list.append(i.text)
            
        except Exception:
            character_list = "We could not find characters from that manga, manga most likely doesn't exist."
        return character_list

    def get_popular_manga(self) -> list:
        """Get currently popular manga.

        Args:
            manga (str): manga you want to search for.

        Returns:
            list: popular manga.
        """
        r = requests.get("https://www.anime-planet.com/manga/all")
        soup = BeautifulSoup(r.content, "html5lib")

        try:
            x = soup.find_all("ul", {"class": "cardDeck cardGrid"})

            popular_mangas = []

            for ultag in x:
                for y in ultag.find_all("li"):
                    y = y.text.replace("Add to list ", "").replace("\n", "")
                    popular_mangas.append(y)
            return popular_mangas
        except Exception as ex:
            return ex