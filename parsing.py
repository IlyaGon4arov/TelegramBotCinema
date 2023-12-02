from bs4 import BeautifulSoup
import requests


def get_soup(city_href="/ua/kyivnewway/"):
    HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 OPR/77.0.4054.298"}
    URL = "https://wizoria.ua" + city_href

    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser') # get main data

    return soup


def get_cities():
    soup = get_soup()
    data = soup.find("header", class_="header").find("div", class_="location-wrapper")
    cities = {}
    cities[data.find("p", class_="choosen-location").get_text(strip=True)] = "/ua/kyivnewway/"

    for item in data.find("div", class_="locations").find_all("a", class_="location"):
        cities[item.get_text(strip=True)] = item.get("href")
    
    return cities


def get_movies(request_type="current", city_href="/ua/kyivnewway/"):
    soup = get_soup(city_href) # get data
    match request_type: # сhanging operating data depending on request
        case "current":
            all_items = soup.find("section", class_="current-movies-list movies-list").find("div", class_="grid-x").find_all("div", class_="movie")
        case "comming_soon":
            all_items = soup.find("section", class_="comming-soon-movies-list movies-list").find("div", class_="grid-x").find_all("div", class_="movie")

    movies = [] # final array that will contain data about all movies

    for i in range(len(all_items)):
        item = all_items[i].find("div", class_="movie__card").find("div", class_="movie__card-timetable")
        movie_info = {}
        movie_info["title"] = item.find("div", class_="title-wrapper").find("h3").get_text(strip=True) # get title
        movie_info["age"] = item.find("div", class_="movie__tags").find("span", class_="age").find("span", class_="age-description").find("span", class_="left").get_text(strip=True) # get age limit
        movie_info["genres"] = item.find("div", class_="movie__tags").find("span", class_="genre").get_text(strip=True) # get all genres
        if (request_type == "comming_soon"): # only if we need to search "comming soon" films
            movie_info["premiere_date"] = item.find("h5", class_="start-date-title").find("span", class_="day").get_text(strip=True) # get premiere date
            if item.find("div", class_="timetable-wrapper").find("div", class_="inner-content") is not None: # sometimes there is no description
                movie_info["description"] = item.find("div", class_="timetable-wrapper").find("div", class_="inner-content").find("p").get_text(strip=True) # get description
            else:
                movie_info["description"] = None
        movie_info["href"] = "https://wizoria.ua" + item.find("a").get("href") # get link
        movies.append(movie_info)

    return movies

