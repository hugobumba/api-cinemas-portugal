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

def medeiafilmes_scraper():
    # Configuração do ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    # Função para obter links de filmes
    def get_movie_links(element_status):
        url = f'https://medeiafilmes.com/{element_status}'
        browser.get(url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'article.card--vertical a'))
        )
        movies = browser.find_elements(By.CSS_SELECTOR, 'article.card--vertical a')
        return [movie.get_attribute('href') for movie in movies]

    # Função para obter informações dos filmes
    def get_movie_info(links, status):
        movie_info_list = []
        for link in links:
            browser.get(link)
            movie_info = {
                'title': try_find_element(browser, By.CSS_SELECTOR, 'h1.t-headline--main-smaller'),
                'synopsis': try_find_element(browser, By.CSS_SELECTOR, 'div.t-text.t-text-body--smaller.l-margin-top-small p').replace("sinopse\n", ""),
                'poster': try_find_element(browser, By.CSS_SELECTOR, 'a.h-modal-create', 'href'),
                'trailer': try_find_element(browser, By.CSS_SELECTOR, 'div.h-video', 'data-plyr-embed-id'),
                'original_title': try_find_element(browser, By.CSS_SELECTOR, 'ul.u-line.u-line--inline.u-line--center li:nth-child(1)').replace(' | ', ''),
                'duration': try_find_element(browser, By.CSS_SELECTOR, 'ul.u-line.u-line--inline.u-line--center li:nth-child(2)').replace('|', '').replace(' ', ''),
                'classification': try_find_element(browser, By.CSS_SELECTOR, 'ul.u-line.u-line--inline.u-line--center li:nth-child(3)').replace('M/', '').replace(' | ', ''),
                'director': try_find_element(browser, By.CSS_SELECTOR, 'h2.t-headline--small').replace('de ', ''),
                'cast': try_find_element(browser, By.CSS_SELECTOR, 'div.t-text.l-margin-bottom-xxxsmall p.t-semi').replace('com ', ''),
                'release_date': try_find_element(browser, By.CSS_SELECTOR, 'ul.u-line.u-line--inline.u-line--center li:nth-child(5)').replace('estreia ', ''),
                'year': try_find_element(browser, By.CSS_SELECTOR, 'ul.u-line.u-line--inline.u-line--center li:nth-child(4)').replace(' | ', ''),
                'cinema': 'Medeia Filmes',
                'status': status,                
                'link': link
            }
            movie_info_list.append(movie_info)
        return movie_info_list

    # Obtenção de links de filmes lançados e futuros
    released_links = list(set(get_movie_links('filmes-em-exibicao')))
    upcoming_links = list(set(get_movie_links('proximas-estreias')))

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
with open('filmes_medeiafilmes.json', 'w', encoding='utf-8') as f:
    json.dump(medeiafilmes_scraper(), f, ensure_ascii=False, indent=4)
"""