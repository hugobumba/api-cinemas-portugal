from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def cinemacity_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # URL do site
    url = 'https://www.cinemacity.pt/'
    browser.get(url)
    browser.implicitly_wait(5)

    # Função para obter links de filmes
    def get_movie_links(element_status):
        button = browser.find_element(By.CSS_SELECTOR, element_status)
        button.click()
        time.sleep(3)
        movies = browser.find_elements(By.CSS_SELECTOR, 'div.actions a')
        return [movie.get_attribute('href') for movie in movies]

    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            try:
                movie_title = browser.find_element(By.CSS_SELECTOR, 'h1.film-title').text
            except:
                movie_title = 'Indisponível'

            try:
                movie_sinopsys = browser.find_elements(By.CSS_SELECTOR, 'col-12 col-md-8')[1].find_elements(By.CSS_SELECTOR, 'p')[0].text
            except:
                movie_sinopsys = 'Indisponível'

            try:
                movie_poster = browser.find_element(By.CSS_SELECTOR, 'div.cover img').get_attribute('src')
            except:
                movie_poster = 'Indisponível'

            try:
                movie_trailer = browser.find_element(By.CSS_SELECTOR, 'a.ytp-title-link').get_attribute('href')
            except:
                movie_trailer = 'Indisponível'

            try:
                movie_duration = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[5].text.replace("Duração: ", "")
            except:
                movie_duration = 'Indisponível'

            try:
                movie_classification = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[4].text.replace("Rating: M/", "")
            except:
                movie_classification = 'Indisponível'

            try:
                movie_director = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[0].text.replace("Realização: ", "")
            except:
                movie_director = 'Indisponível'

            try:
                movie_cast = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[3].text.replace("Actores: ", "")
            except:
                movie_cast = 'Indisponível'

            try:
                movie_release_date = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[6].text.replace("Data de Lançamento: ", "")
            except:
                movie_release_date = 'Indisponível'

            try:
                movie_year = browser.find_elements(By.CSS_SELECTOR, 'p.m-0')[6].text.split('/')[-1]
            except:
                movie_year = 'Indisponível'

            # Organizar os dados em um dicionário
            movie_info = {
                'title': movie_title,
                'sinopsys': movie_sinopsys,
                'poster': movie_poster,
                'trailer': movie_trailer,
                'duration': movie_duration,
                'classification': movie_classification,
                'director': movie_director,
                'cast': movie_cast,
                'year': movie_year,
                'release_date': movie_release_date,
                'cinema': 'CinemaCity',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list

    # Obtenção de links de filmes lançados e futuros
    released_links = list(set(get_movie_links('a.nav-link[data-hash="#EMEXIBIÇÃO"]')))
    upcoming_links = list(set(get_movie_links('a.nav-link[data-hash="#BREVEMENTE"]')))

    # Obtenção dos títulos dos filmes lançados e futuros
    released_info = get_movie_info(released_links, "Em Exibição")
    upcoming_info = get_movie_info(upcoming_links, "Em Breve")

    # Fechamento do navegador
    browser.quit()

    return {
        'Filmes lançados': released_info,
        'Filmes futuros': upcoming_info
    }

"""# Grava os dados em um arquivo JSON
with open('filmes_cinemacity.json', 'w', encoding='utf-8') as f:
    json.dump(cinemacity_scraper(), f, ensure_ascii=False, indent=4)
"""