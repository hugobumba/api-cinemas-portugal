from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json

def cinematrindade_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # URL do site
    url = 'https://cinematrindade.pt/'
    browser.get(url)
    browser.implicitly_wait(5)

    # Função para obter links de filmes
    def get_movie_links(element_status):
        movies = browser.find_elements(By.CSS_SELECTOR, element_status)
        return [movie.get_attribute('href') for movie in movies]

    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            try:
                movie_title = browser.find_element(By.CSS_SELECTOR, 'div.col-12.mt-5.mb-3 h1').text
            except:
                movie_title = 'Indisponível'

            try:
                movie_sinopsys = browser.find_elements(By.CSS_SELECTOR, 'div#sinopse p')[0].text
            except:
                movie_sinopsys = 'Indisponível'

            try:
                movie_poster = browser.find_element(By.CSS_SELECTOR, 'section.capaFilmes img').get_attribute('src')
            except:
                movie_poster = 'Indisponível'

            try:
                movie_trailer = browser.find_element(By.CSS_SELECTOR, 'iframe').get_attribute('src')
            except:
                movie_trailer = 'Indisponível'

            try:
                movie_duration = browser.find_element(By.CSS_SELECTOR, 'div.col-12.mt-3.mb-3 h6').text.split('/')[2].replace(']', '').replace(' ', '')
            except:
                movie_duration = 'Indisponível'

            try:
                movie_director = browser.find_element(By.CSS_SELECTOR, 'div.col-12.mt-3.mb-3 h4').text
            except:
                movie_director = 'Indisponível'

            try:
                movie_year = browser.find_element(By.CSS_SELECTOR, 'div.col-12.mt-3.mb-3 h6').text.split('/')[1].replace(' ', '')
            except:
                movie_year = 'Indisponível'

            try:
                movie_country = browser.find_element(By.CSS_SELECTOR, 'div.col-12.mt-3.mb-3 h6').text.split('/')[0].replace('[', '')
            except:
                movie_country = 'Indisponível'

            # Organizar os dados em um dicionário
            movie_info = {
                'title': movie_title,
                'sinopsys': movie_sinopsys,
                'poster': movie_poster,
                'trailer': movie_trailer,
                'duration': movie_duration,
                'director': movie_director,
                'year': movie_year,
                'country': movie_country,
                'cinema': 'Cinema Trindade',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list

    # Obtenção de links de filmes lançados
    released_links = list(set(get_movie_links('a.jet-listing-dynamic-link__link')))

    # Obtenção das informações dos filmes lançados
    released_info = get_movie_info(released_links, "Em Exibição")

    # Fechamento do navegador
    browser.quit()

    return {
        'Filmes lançados': released_info
    }

"""# Grava os dados em um arquivo JSON
with open('filmes_cinematrindade.json', 'w', encoding='utf-8') as f:
    json.dump(cinematrindade_scraper(), f, ensure_ascii=False, indent=4)
"""