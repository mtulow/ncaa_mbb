import time
import pandas as pd
import datetime as dt
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    
def get_current_season():
    game_date = dt.datetime.today()
    return '{}-{}'.format(game_date.year-1, game_date.year) if game_date.month in [*range(1,4+1)] else '{}-{}'.format(game_date.year, game_date.year+1)



def get_game_pbp(game_id: int, season: str = None):
    # default to current season
    season = season or get_current_season()

    # get game data
    if season == get_current_season():
        # Set up Selenium webdriver and navigate to game's play-by-play page
        driver = webdriver.Chrome()
        driver.get('http://www.espn.com/mens-college-basketball/playbyplay/_/gameId/{game_id}'.format(game_id=game_id))

        # Wait for the play-by-play table to load
        time.sleep(1)

        # Find the game period tab buttons
        tab_buttons = driver.find_elements(By.CLASS_NAME, 'tabs__list__item')

        # instantiate a dictionary to store the game period data
        pbp_data = defaultdict(list)
        headers = ['time','image','play','home_team','away_team']

        # iterate through game periods, 2 w/o overtime
        for tab_button in tab_buttons:
            # select the game period 
            button = tab_button.find_element(By.TAG_NAME, 'button')
            button.click()

            # Wait for the play-by-play table to load
            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Table__TBODY')))

            # # find the play-by-play headers
            # header_tags = driver.find_elements(By.TAG_NAME, 'thead')[1].find_elements(By.TAG_NAME, 'th')
            # table_headers = [header.text for header in header_tags]
            # print(table_headers)


            # iterate over table rows
            for row in driver.find_elements(By.CLASS_NAME, 'playByPlay__tableRow'):
                # iterate over table headers & cells
                for name,cell in zip(headers, row.find_elements(By.TAG_NAME, 'td')):
                    if name == 'image':
                        img = cell.get_attribute('src')
                        if img:
                            pbp_data['image'].append(img)
                            print(img)
                    else:
                        pbp_data[name].append(cell.text)
            
        # Close the webdriver
        driver.quit()

        return pd.DataFrame(pbp_data)
    
    # if fetching a specific season
    else:
        # TODO: use data from ncaahoopR_data repo
        # link: https://github.com/lbenz730/ncaahoopR_data
        return None


def main():
    df = get_game_pbp(401514239)
    print(df)


if __name__ == '__main__':
    print()
    main()
    print()