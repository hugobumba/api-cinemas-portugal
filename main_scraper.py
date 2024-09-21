import json
import threading
from pymongo import MongoClient
from scrapers.nos import nos_scraper
from scrapers.uci import uci_scraper
from scrapers.cinemacity import cinemacity_scraper
from scrapers.cineplace import cineplace_scraper
from scrapers.cinematrindade import cinematrindade_scraper
from scrapers.castellolopes import castellolopes_scraper
from scrapers.medeiafilmes import medeiafilmes_scraper

def main():
    result_dict = {}

    username = "hugobumba"
    password = "mhungodb"
    database_name = "movies_db"
    collection_name = "movies_info"

    # Conectar ao MongoDB Atlas
    client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.rkwdb.mongodb.net/{database_name}?retryWrites=true&w=majority')
    db = client[database_name]
    collection = db[collection_name]

    # Função para scraping e atualização do dicionário
    def scrape_and_update(scraper_func, key):
        result_dict[key] = scraper_func()

    # Criar threads para cada scraper
    threads = [
        threading.Thread(target=scrape_and_update, args=(nos_scraper, 'nos')),
        threading.Thread(target=scrape_and_update, args=(uci_scraper, 'uci')),
        threading.Thread(target=scrape_and_update, args=(cinemacity_scraper, 'cinemacity')),
        threading.Thread(target=scrape_and_update, args=(cineplace_scraper, 'cineplace')),
        threading.Thread(target=scrape_and_update, args=(cinematrindade_scraper, 'cinematrindade')),
        threading.Thread(target=scrape_and_update, args=(castellolopes_scraper, 'castellolopes')),
        threading.Thread(target=scrape_and_update, args=(medeiafilmes_scraper, 'medeiafilmes'))
    ]

    # Iniciar as threads
    for thread in threads:
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    # Salvar resultados em um arquivo JSON
    with open('movies.json', 'w', encoding='utf-8') as file:
        json.dump(result_dict, file, ensure_ascii=False, indent=4)

    # Verificar e depurar o conteúdo de result_dict
    print("Conteúdo de result_dict:", json.dumps(result_dict, indent=4))

        # Salvar resultados no MongoDB Atlas
    for key, data in result_dict.items():
        collection.update_one(
            {"source": key},
            {"$set": data},
            upsert=True
        )

    # Fechar a conexão com o MongoDB
    client.close()

if __name__ == "__main__":
    main()
