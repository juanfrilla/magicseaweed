import warnings, time, asyncio
from halo import Halo

warnings.filterwarnings("ignore")

import utils

def main():
    urls = [
        {
            "beach": "Matagorda",
            "url": "https://es.magicseaweed.com/Matagorda-Beach-Surf-Report/6850/",
        },
        {
            "beach": "Las Cucharas",
            "url": "https://es.magicseaweed.com/Playa-de-las-Cucharas-Surf-Report/6852/",
        },
        {
            "beach": "Famara",
            "url": "https://es.magicseaweed.com/Playa-de-Famara-Surf-Report/209/",
        },
        {
            "beach": "Las Conchas",
            "url": "https://es.magicseaweed.com/Playa-de-las-Conchas-Surf-Report/5891/",
        },
        {
            "beach": "El Castillo",
            "url": "https://es.magicseaweed.com/Castillo-Surf-Report/8255/",
        },
        {
            "beach": "Arrieta",
            "url": "https://es.magicseaweed.com/Arrieta-Beach-Surf-Report/6851/",
        },
        {
            "beach": "Jameos",
            "url": "https://es.magicseaweed.com/Jameos-del-Agua-Surf-Report/206/",
        },
        {
            "beach": "El Espino",
            "url": "https://es.magicseaweed.com/El-Espino-Surf-Report/6854/",
        },
        {
            "beach": "La Santa",
            "url": "https://es.magicseaweed.com/La-Santa-Surf-Report/207/",
        },
        {
            "beach": "Caleta Caballo",
            "url": "https://es.magicseaweed.com/Ghost-Town-Surf-Report/208/",
        },
        {
            "beach": "San Juan",
            "url": "https://es.magicseaweed.com/San-Juan-Surf-Report/6853/",
        },
    ]

    #front.plot_data(urls)
    
    start_time = time.time()
    spinner = Halo(
        text="Scrapping data from MagicSeaWeed\n",
        text_color="blue",
        color="magenta",
        spinner="dots",
    )
    spinner.start()
    
    
    df = utils.scrape_multiple_sites(urls)
    
    df = utils.format_dataframe(df)
    utils.df_to_csv("magicseaweed.csv", df)

    spinner.stop_and_persist(
        text="You can check the url (👨‍💻) or if you prefer, the csv file (👀📈), happy surfing (🏄) and respect the sea(🌊)"
    )
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()

