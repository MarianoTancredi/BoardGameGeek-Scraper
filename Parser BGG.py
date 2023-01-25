import requests
import csv
from bs4 import BeautifulSoup

#Given any ranking of BGG Website url, returns a Dict list with every game Rating
def bgg_scraper(URL):
    try:
        page = requests.get(URL).content
        soup = BeautifulSoup(page, 'html.parser')
        games = []
        for rank,row in enumerate(soup.findAll("tr", {"id": 'row_'}),start=1):
            try:
                game = {}
                div_id = "results_objectname" + str(rank)
                div_text = row.find("div", {"id": div_id}).text
                game_name = (div_text.split('\n'))[1]
                game['name'] = game_name

                ratings = row.findAll("td",{"class": 'collection_bggrating'})

                game['Geek Rating'] = ratings[0].get_text(strip=True)
                game['Avg Rating'] = ratings[1].get_text(strip=True)
                game['Num Voters'] = ratings[2].get_text(strip=True)
                games.append(game)
            
            except AttributeError:
                print('Encountered Atrribute Error, parsing continues')
                continue
    except requests.exceptions.HTTPError:
        print('Encountered HTTP Error, most likely page does not exist')
        return None

    
    return games

def games_to_csv(games,name):
    if not name:
        name = 'Overall'

    with open(f'{name}.csv','w',encoding='UTF8') as file:
        writer = csv.DictWriter(file, fieldnames=games[0].keys())
        writer.writeheader()
        writer.writerows(games)

    file.close()

#Given any category of Boardgames, return an url for the ranking of that type of boardgames and number of page selected for parsing.
#In case no category is specified, will return overall ranking.
#In case no number of page is specifided, will return number 1
def format_url(category,number):
    if category:
        url = f"https://boardgamegeek.com/{category}/browse/boardgame/page/{number}"
    else:
        url = "https://boardgamegeek.com/browse/boardgame/page/{number}"
    return url


def main(category = None, pages = 1):
    games = []
    for i in range(pages):
        url = format_url(category,pages)
        rank_list = bgg_scraper(url)
        if rank_list:
            games = rank_list + games
    
    if len(games) > 0:
        games_to_csv(games,category)
    
    else:
        print('Could not fetch any games')

main('abstracts',2)