import warnings

warnings.filterwarnings("ignore")

import front


def main():
    spots_data = [
        {
            "island": "Lanzarote",
            "beach": "Matagorda",
            "url": "https://es.magicseaweed.com/Matagorda-Beach-Surf-Report/6850/",
        },
        {
            "island": "Lanzarote",
            "beach": "Las Cucharas",
            "url": "https://es.magicseaweed.com/Playa-de-las-Cucharas-Surf-Report/6852/",
        },
        {
            "island": "Lanzarote",
            "beach": "Famara",
            "url": "https://es.magicseaweed.com/Playa-de-Famara-Surf-Report/209/",
        },
        {
            "island": "Lanzarote",
            "beach": "Las Conchas",
            "url": "https://es.magicseaweed.com/Playa-de-las-Conchas-Surf-Report/5891/",
        },
        {
            "island": "Lanzarote",
            "beach": "El Castillo",
            "url": "https://es.magicseaweed.com/Castillo-Surf-Report/8255/",
        },
        {
            "island": "Lanzarote",
            "beach": "Arrieta",
            "url": "https://es.magicseaweed.com/Arrieta-Beach-Surf-Report/6851/",
        },
        {
            "island": "Lanzarote",
            "beach": "Jameos",
            "url": "https://es.magicseaweed.com/Jameos-del-Agua-Surf-Report/206/",
        },
        {
            "island": "Lanzarote",
            "beach": "El Espino",
            "url": "https://es.magicseaweed.com/El-Espino-Surf-Report/6854/",
        },
        {
            "island": "Lanzarote",
            "beach": "La Santa",
            "url": "https://es.magicseaweed.com/La-Santa-Surf-Report/207/",
        },
        {
            "island": "Lanzarote",
            "beach": "Caleta Caballo",
            "url": "https://es.magicseaweed.com/Ghost-Town-Surf-Report/208/",
        },
        {
            "island": "Lanzarote",
            "beach": "San Juan",
            "url": "https://es.magicseaweed.com/San-Juan-Surf-Report/6853/",
        },
        {
            "island": "Gran Canaria",
            "beach": "La Cícer",
            "url": "https://es.magicseaweed.com/La-Cicer-Surf-Report/218/",
        },
        {
            "island": "Gran Canaria",
            "beach": "La Barra",
            "url": "https://es.magicseaweed.com/La-Barra-Las-Canteras-Surf-Report/1874/",
        },
        {
            "island": "Gran Canaria",
            "beach": "El Confital",
            "url": "https://es.magicseaweed.com/El-Confital-Surf-Report/219/",
        },
    ]

    front.plot_data(spots_data)


if __name__ == "__main__":
    main()
