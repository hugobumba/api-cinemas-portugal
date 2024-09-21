from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
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
    
def try_find_elements(browser, by, value, attr=None, default='Indisponível'):
    try:
        elements = browser.find_elements(by, value)
        if attr:
            return [element.get_attribute(attr) for element in elements]
        else:
            return [element.text for element in elements]
    except:
        return [default]

def castellolopes_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # URL do site
    url = 'https://castellolopescinemas.pt/'
    browser.get(url)
    browser.implicitly_wait(5)

    # Função para obter links de filmes
    def get_movie_links(selector):
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        movies = browser.find_elements(By.CSS_SELECTOR, selector)
        return [movie.get_attribute('href') for movie in movies]

    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.entry-title'))
            )
            movie_info = {
                'title': try_find_element(browser, By.CSS_SELECTOR, 'h1.entry-title'),
                'sinopsys': try_find_element(browser, By.CSS_SELECTOR, 'div.et_pb_post_content p'),
                'poster': try_find_element(browser, By.CSS_SELECTOR, 'span.et_pb_image_wrap img', 'src'),
                'trailer': try_find_element(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner a', 'href'),
                'original_title': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[5].replace(" (título original)", ""),
                'duration': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[7].replace(" |", "m"),
                'genre': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[8],
                'classification': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[6].replace("M/", "").replace(" |", ""),
                'director': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[11].replace("Realização: ", ""),
                'cast': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[12].replace("Atores: ", ""),
                'release_date': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[9].replace("Data de Estreia: ", ""),
                'year': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[9].split('/')[-1],
                'country': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[13].replace("País: ", ""),
                'language': try_find_elements(browser, By.CSS_SELECTOR, 'div.et_pb_text_inner')[14].replace("Idioma: ", ""),
                'cinema': 'Castello Lopes',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list
    
    # Obtenção de links de filmes lançados e futuros
    released_links = list(set(get_movie_links('li.filter-em-exibicao a')))
    upcoming_links = list(set(get_movie_links('li.filter-proximas-estreias a')))

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
with open('filmes_castellolopes.json', 'w', encoding='utf-8') as f:
    json.dump(castellolopes_scraper(), f, ensure_ascii=False, indent=4)
"""