from flask import Flask, render_template, send_file
import requests
import logging
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import matplotlib.dates as mdates

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Konfiguracja logowania
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Zdefiniowanie URL API
API_URL = "https://jsonplaceholder.typicode.com/posts"  # Zastąp tym, co chcesz używać

# Funkcja do pobierania danych z API
def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Sprawdzenie poprawności odpowiedzi
        data = response.json()
        logging.info("Data fetched successfully.")
        return data
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None

# Funkcja do generowania wykresu
def generate_line_chart(data):
    post_dates = []
    post_counts = {}

    for item in data:
        # Zakładając, że w danych jest pole 'createdAt' lub podobne, które zawiera datę
        # W tym przypadku JSONPlaceholder nie zawiera daty w postach, ale dodamy datę przykładową, np. '2025-04-01'
        # Zastąp to odpowiednim polem, które zawiera datę, np. 'createdAt', 'timestamp' lub 'date'
        
        try:
            post_date = datetime.strptime(item['createdAt'], '%Y-%m-%d')  # Zmień na właściwe pole
        except KeyError:
            # Obsługuje przypadek, gdy pole 'createdAt' nie istnieje
            post_date = datetime(2025, 4, 1)  # Przykładowa data, jeśli brak w danych
        
        post_dates.append(post_date)
        post_counts[post_date] = post_counts.get(post_date, 0) + 1
    
    # Przygotowanie danych do wykresu
    sorted_dates = sorted(post_counts.keys())
    sorted_counts = [post_counts[date] for date in sorted_dates]

    # Tworzenie wykresu liniowego
    fig, ax = plt.subplots()
    ax.plot(sorted_dates, sorted_counts, marker='o')

    ax.set_xlabel('Date')
    ax.set_ylabel('Post Count')
    ax.set_title('Posts per Date')

    # Formatowanie osi X na daty
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45)

    # Zapisanie wykresu do obrazu w pamięci
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    # Zwrócenie wykresu jako dane w formacie base64, aby wyświetlić go w HTML
    return base64.b64encode(img.getvalue()).decode('utf8')

# Strona główna, która wyświetla dane z API
@app.route('/')
def index():
    data = fetch_data()
    if data:
        chart = generate_line_chart(data)  # Generowanie wykresu na podstawie danych
        return render_template('index.html', chart=chart)  # Przesyłanie wykresu do szablonu
    else:
        return "Failed to fetch data from API."

# Uruchomienie aplikacji Flask
if __name__ == "__main__":
    app.run(debug=True)
