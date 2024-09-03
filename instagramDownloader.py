import json
import requests
from haralyzer import HarPage
import os


def scarica_immagini_da_har(file_har, output_dir='downloaded_images'):
    # Crea la cartella di output se non esiste
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(file_har, 'r') as f:
        har_data = json.load(f)

        # Usa l'ID della pagina presente nel file HAR
        page_id = har_data['log']['pages'][0]['id'] if 'id' in har_data['log']['pages'][0] else None

        if not page_id:
            print("Nessun ID pagina trovato nel file HAR.")
            return

        print(f"Utilizzando la pagina con ID: {page_id}")
        har_page = HarPage(page_id, har_data=har_data)

    for i, entry in enumerate(har_page.entries):
        request = entry['request']
        url = request['url']

        # Gestione della mancanza del campo 'mimeType'
        if 'response' in entry and 'content' in entry['response'] and 'mimeType' in entry['response']['content']:
            mime_type = entry['response']['content']['mimeType']
            
            # Filtra solo le richieste che puntano a immagini
            if 'image' in mime_type:
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()  # Controlla se la richiesta ha avuto successo

                    pic_string = os.path.join(output_dir, "picture_{}.png".format(i))

                    # Salva l'immagine in un file
                    with open(pic_string, "wb") as file:
                        file.write(response.content)

                    print(f"Picture Nr {i} saved!")

                except requests.exceptions.RequestException as e:
                    print(f"Errore nel download dell'immagine {i}: {e}")
        else:
            print(f"Richiesta Nr {i} saltata: MIME type non presente o richiesta non riuscita.")

# Esecuzione
file_har = 'pictures.har'  # Nome file HAR
scarica_immagini_da_har(file_har)
