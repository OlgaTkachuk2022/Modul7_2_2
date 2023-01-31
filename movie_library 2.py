import random
import datetime
from typing import List


class BasePlayable:

    def __init__(self, title: str, release_year: int, genre: str):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.watch_count = 0

    def play(self):
        self.watch_count += 1
        print(str(self))


class Movie(BasePlayable):

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Series(BasePlayable):
    def __init__(
            self, title: str, release_year: int,
            genre: str, season_number: int, series_number: int
    ):
        super(Series, self).__init__(title, release_year, genre)
        self.season_number = season_number
        self.series_number = series_number

    @staticmethod
    def get_series_episodes_amount(library, series_title):
        search = library.search(series_title)
        return len(search)

    def __str__(self):
        return f"{self.title} S{self.series_number:02}E{self.series_number:02}"


class MovieLibrary:

    def __init__(self):
        self.library: List[BasePlayable] = []

    def add_serial(self, title: str, release_year: int, genre: str, season_number: int, series_number: int):
        serial = Series(title, release_year, genre, season_number, series_number)
        self.library.append(serial)

    def add_serial_season(self, title: str, release_year: int, genre: str, season_number: int, series_amount: int):
        for series_number in range(1, series_amount + 1):
            self.add_serial(title, release_year, genre, season_number, series_number)

    def add_movie(self, title: str, release_year: int, genre: str):
        movie = Movie(title, release_year, genre)
        self.library.append(movie)

    def get_movies(self):
        return list(
            sorted(
                filter(
                    lambda item: isinstance(item, Movie), self.library
                ),
                key=lambda item: item.title
            )
        )

    def get_series(self):
        return list(
            sorted(
                filter(
                    lambda item: isinstance(item, Series), self.library
                ),
                key=lambda item: item.title
            )
        )

    def search(self, query):
        return list(filter(lambda item: item.title == query, self.library))

    def generate_views(self):
        rand_movie = random.choice(self.library)
        for _ in range(random.randint(1, 100)):
            rand_movie.play()

    def get_top_titles(self, limit, content_type = None):
        if limit == 0:
            return []
        try:
            if content_type is not None:
                if content_type == Movie:
                    return list(sorted(self.get_movies(), key=lambda item: item.watch_count))[:limit]
                elif content_type == Series:
                    return list(sorted(self.get_series(), key=lambda item: item.watch_count))[:limit]
                else:
                    raise ValueError(f"Wrong content_type, expected Movies or Series, got {content_type}")
            else:
                return list(sorted(self.library, key=lambda item: item.watch_count))[:limit]
        except IndexError:
            return self.get_top_titles(limit - 1, content_type)


def main():
    print("Фільмотека")

    library = MovieLibrary()

    library.add_movie("Star Wars 1", 1999, 'Sci-Fi')
    library.add_movie("Star Wars 2", 2002, 'Sci-Fi')
    library.add_movie("Star Wars 3", 2005, 'Sci-Fi')

    library.add_serial_season("Friends", 1994, 'Comedy', 1, 3)
    library.add_serial_season("House M.D.", 2004, 'Medical drama', 1, 5)

    for _ in range(1000):
        library.generate_views()

    today_str = datetime.datetime.today().strftime("%d.%m.%Y")
    print(f"Найпопулярніші фільми та серіали дня {today_str}")

    for movie in library.get_top_titles(3):
        print(movie)


if __name__ == '__main__':
    main()
