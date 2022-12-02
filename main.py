import utils
import warnings

warnings.filterwarnings('ignore')
from halo import Halo

if __name__ == "__main__":
    urls = [{
        "beach":
        "Famara",
        "url":
        "https://es.magicseaweed.com/Playa-de-Famara-Surf-Report/209/"
    }, {
        "beach":
        "Las Conchas",
        "url":
        "https://es.magicseaweed.com/Playa-de-las-Conchas-Surf-Report/5891/"
    }, {
        "beach": "El Castillo",
        "url": "https://es.magicseaweed.com/Castillo-Surf-Report/8255/"
    }, {
        "beach":
        "Matagorda",
        "url":
        "https://es.magicseaweed.com/Matagorda-Beach-Surf-Report/6850/"
    }, {
        "beach":
        "Las Cucharas",
        "url":
        "https://es.magicseaweed.com/Playa-de-las-Cucharas-Surf-Report/6852/"
    }, {
        "beach":
        "Arrieta",
        "url":
        "https://es.magicseaweed.com/Arrieta-Beach-Surf-Report/6851/"
    }, {
        "beach":
        "Jameos",
        "url":
        "https://es.magicseaweed.com/Jameos-del-Agua-Surf-Report/206/"
    }, {
        "beach": "El Espino",
        "url": "https://es.magicseaweed.com/El-Espino-Surf-Report/6854/"
    }, {
        "beach": "La Santa",
        "url": "https://es.magicseaweed.com/La-Santa-Surf-Report/207/"
    }, {
        "beach": "Caleta Caballo",
        "url": "https://es.magicseaweed.com/Ghost-Town-Surf-Report/208/"
    }, {
        "beach": "San Juan",
        "url": "https://es.magicseaweed.com/San-Juan-Surf-Report/6853/"
    }]
    
    
    spinner = Halo(text='Scrapping Surf Forecast Parameters from MagicSeaWeed ...', spinner='dots', color='magenta')
    spinner.start()
    df = utils.scrape_multiple_sites(urls)
    df= utils.format_dataframe(df)
    utils.df_to_csv("magicseaweed.csv", df)
    spinner.stop_and_persist(text=('Check the CSV file (👀📝) and have a good surfing 🏄‍!').encode('utf-8'))