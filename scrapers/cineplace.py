from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def try_find_element(browser, by, value, attr=None, default='Indisponível'):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((by, value)))#
        element = browser.find_element(by, value)
        if attr:
            return element.get_attribute(attr)
        else:
            return element.text
    except:
        return default

def cineplace_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # URL do site
    url = 'https://cineplace.pt/filmes/'
    browser.get(url)
    #browser.implicitly_wait(5)

    # Função para obter links de filmes
    def get_movie_links(tab_selector):
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, tab_selector))
        )
        tab = browser.find_element(By.CSS_SELECTOR, tab_selector)
        movies = tab.find_elements(By.CSS_SELECTOR, 'a.movie-action-info')
        return [movie.get_attribute('href') for movie in movies]
    
    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            movie_info = {
                'title': try_find_element(browser, By.CSS_SELECTOR, 'h1.entry-title'),
                'sinopsys': try_find_element(browser, By.CSS_SELECTOR, 'div.storyline'),
                'original_title': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(2) fieldset:nth-child(2)').replace('TÍTULO ORIGINAL\n', ''),
                'duration': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-info-icon:nth-child(2)'),
                'genre': [genre.text for genre in browser.find_elements(By.CSS_SELECTOR, 'ul.movie-categories li')] or ['---'],
                'classification': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-info-icon:nth-child(1)').split('/')[-1].replace('-\n', ''),
                'director': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(1) fieldset:nth-child(1)').replace('REALIZADOR\n', ''),
                'cast': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(1) fieldset:nth-child(2)').replace('ELENCO\n', ''),
                'year': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(2) fieldset:nth-child(1)').replace('ANO\n', ''),
                'country': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(1) fieldset:nth-child(3)').replace('PAÍS\n', ''),
                'language': try_find_element(browser, By.CSS_SELECTOR, 'div.col.col-md-6:nth-child(2) fieldset:nth-child(3)').replace('IDIOMA\n', ''),
                'cinema': 'CinePlace',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list

    # Obtenção de links de filmes lançados e futuros
    released_links = list(set(get_movie_links('div.tab-pane#showing')))
    upcoming_links = list(set(get_movie_links('div.tab-pane#coming-soon')))

    # Obtenção das informações dos filmes lançados e futuros
    released_info = get_movie_info(released_links, "Em Exibição")
    upcoming_info = get_movie_info(upcoming_links, "Em Breve")

    # Fechamento do navegador
    browser.quit()

    return {
        'Filmes lançados': released_info,
        'Filmes futuros': upcoming_info
    }

"""# Grava os dados em um arquivo JSON
with open('filmes_cineplace.json', 'w', encoding='utf-8') as f:
    json.dump(cineplace_scraper(), f, ensure_ascii=False, indent=4)
"""