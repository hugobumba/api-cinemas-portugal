from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def nos_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # URL do site
    url = 'https://cinemas.nos.pt/filmes'
    browser.get(url)
    browser.implicitly_wait(5)

    # Função para obter links de filmes
    def get_movie_links(element_status):
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_status))
        )
        button = browser.find_element(By.CSS_SELECTOR, element_status)
        button.click()
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.js-gtm-movie'))
        )
        movies = browser.find_elements(By.CSS_SELECTOR, 'a.js-gtm-movie')
        return [movie.get_attribute('href') for movie in movies]

    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            movie_info = {
                'title': try_find_element(browser, By.CSS_SELECTOR, 'h2.movie-detail__hero__content__title'),
                'synopsis': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__synopsis').replace("sinopse\n", ""),
                'poster': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__hero__content__poster-image-container img', attr='src'),
                'trailer': try_find_element(browser, By.CSS_SELECTOR, 'a.movie-detail__hero__trailer-link', attr='href'),
                'original_title': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__hero__content__original-title'),
                'duration': try_find_element(browser, By.CSS_SELECTOR, 'span.order__duration').replace(" | ", ""),
                'genre': try_find_element(browser, By.CSS_SELECTOR, 'span.order__genre').replace(" ・ ", ""),
                'classification': try_find_element(browser, By.CSS_SELECTOR, 'span.order__classification').replace("M", ""),
                'director': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__datasheet__director').replace("realizador ", ""),
                'cast': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__datasheet__cast').replace("actores ", ""),
                'release_date': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__datasheet__releasedate').replace("estreia ", ""),
                'year': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__datasheet__year').replace("ano ", ""),
                'country': try_find_element(browser, By.CSS_SELECTOR, 'div.movie-detail__content__datasheet__country').replace("país ", ""),
                'cinema': 'NOS Cinemas',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list

    
    # Obter links dos filmes e remover duplicados
    released_links = list(set(get_movie_links('button.movies-filter__tab[value="in-theaters"]')))
    upcoming_links = list(set(get_movie_links('button.movies-filter__tab[value="soon"]')))

    # Obter informações dos filmes
    released_info = get_movie_info(released_links, "Em Exibição")
    upcoming_info = get_movie_info(upcoming_links, "Em Breve")

    # Fechar navegador
    browser.quit()

    return {
        'Filmes lançados': released_info,
        'Filmes futuros': upcoming_info
    }

"""# Grava os dados em um arquivo JSON
with open('filmes_nos.json', 'w', encoding='utf-8') as f:
    json.dump(nos_scraper(), f, ensure_ascii=False, indent=4)"""