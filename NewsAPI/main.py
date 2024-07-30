import requests
import datetime as dt
api_key = open("api_key", "r").read().strip()

def get_news(city, api_key):
    # Incluye el parámetro language=es para obtener noticias en español
    url = f"https://newsapi.org/v2/everything?q={city}&language=es&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print(f"Error al obtener noticias para {city}: {data.get('message')}")
            return None

        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Error de tiempo de espera: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Ocurrió un error: {req_err}")

    return None

def format_date(date_str):
    # Convierte la fecha en formato ISO 8601 a un objeto datetime
    date_obj = dt.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    # Formatea la fecha como desees (ej. 'dd-mm-yyyy hh:mm:ss')
    return date_obj.strftime('%d-%m-%Y %H:%M:%S')
def display_news_info(city, data):
    if data:
        articles = data["articles"]
        print(f"Noticias en {city}:")
        for article in articles[:5]:
            title = article['title']
            source = article['source']['name']
            published_at = format_date(article['publishedAt'])
            description = article['description']
            url = article['url']

            print(f"- Título: {title}")
            print(f"  Fuente: {source}")
            print(f"  Publicado: {published_at}")
            print(f"  Descripción: {description}")
            print(f"  URL: {url}\n")
    else:
        print(f"No se pudo obtener noticias para {city}")


def compare_news(city_a, city_b, api_key):
    news_data_a = get_news(city_a, api_key)
    news_data_b = get_news(city_b, api_key)

    print(f"Noticias en {city_a}:")
    display_news_info(city_a, news_data_a)

    print(f"\nNoticias en {city_b}:")
    display_news_info(city_b, news_data_b)


# Define las ciudades
city_a = "Puerto de Panamá"
city_b = "Puerto de Colón"


compare_news(city_a, city_b, api_key)