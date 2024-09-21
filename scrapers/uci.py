from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json

def try_find_element(browser, by, value, attr=None, default='Indisponível'):
    try:
        element = browser.find_element(by, value)
        if attr:
            return element.get_attribute(attr)
        else:
            return element.text
    except:
        return default

def uci_scraper():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    url = 'https://www.ucicinemas.pt/filmes/'
    browser.get(url)
    browser.implicitly_wait(5)

    def get_movie_links(element_status):
        buttons = browser.find_elements(By.CSS_SELECTOR, 'button.v-tab__button')
        button = buttons[element_status]
        browser.execute_script("arguments[0].click();", button)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.v-film-list-film__link'))
        )
        movies = browser.find_elements(By.CSS_SELECTOR, 'a.v-film-list-film__link')
        return [movie.get_attribute('href') for movie in movies]

    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            movie_info = {
                'title': try_find_element(browser, By.CSS_SELECTOR, 'h1.v-film-title__text'),
                'synopsis': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-synopsis span.v-display-text-part'),
                'poster': try_find_element(browser, By.CSS_SELECTOR, 'img.v-image__img', attr='src'),
                'duration': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-runtime span').replace(" ", ""),
                'genre': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-genres'),
                'classification': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-classification-description dd'),
                'director': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-director span.v-display-text-part'),
                'cast': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-actors span.v-display-text-part'),
                'release_date': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-release-date span.v-display-text-part'),
                'year': try_find_element(browser, By.CSS_SELECTOR, 'div.v-film-release-date span.v-display-text-part').split(' ')[-1],
                'cinema': 'UCI Cinemas',
                'status': status,
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list
    
    released_links = list(set(get_movie_links(1)))
    upcoming_links = list(set(get_movie_links(2)))

    released_info = get_movie_info(released_links, "Em Exibição")
    upcoming_info = get_movie_info(upcoming_links, "Em Breve")

    browser.quit()

    return {
        'Filmes lançados': released_info,
        'Filmes futuros': upcoming_info
    }

"""# Grava os dados em um arquivo JSON
with open('filmes_uci.json', 'w', encoding='utf-8') as f:
    json.dump(uci_scraper(), f, ensure_ascii=False, indent=4)"""