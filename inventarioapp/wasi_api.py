import requests

WASI_TOKEN = "aMun_s6tV_gYrq_TDNG"
ID_COMPANY = "2046349"           

def obtener_paises():
    url = "https://api.wasi.co/v1/location/all-countries"
    payload = {
        "id_company": ID_COMPANY,
        "wasi_token": WASI_TOKEN
    }
    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        return [(c["id_country"], c["name"]) for c in resp.json().values() if isinstance(c, dict)]
    return []

def obtener_regiones(id_country):
    if id_country.isdigit():
        url = "https://api.wasi.co/v1/location/regions-from-country/" + id_country
        payload = {
            "id_company": ID_COMPANY,
            "wasi_token": WASI_TOKEN
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return [(c["id_region"], c["name"]) for c in resp.json().values() if isinstance(c, dict)]
        return []
    else:
        return []
    
def obtener_ciudades(id_region):
    if id_region.isdigit():
        url = "https://api.wasi.co/v1/location/cities-from-region/" + id_region
        payload = {
            "id_company": ID_COMPANY,
            "wasi_token": WASI_TOKEN
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return [(c["id_city"], c["name"]) for c in resp.json().values() if isinstance(c, dict)]
        return []
    else:
        return []
    
def obtener_localidades(id_city):
    if id_city.isdigit():
        url = "https://api.wasi.co/v1/location/locations-from-city/" + id_city
        payload = {
            "id_company": ID_COMPANY,
            "wasi_token": WASI_TOKEN
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return [(c["id_location"], c["name"]) for c in resp.json().values() if isinstance(c, dict)]
        return []
    else:
        return []
    
def obtener_zonas(id_city):
    if id_city.isdigit():
        url = "https://api.wasi.co/v1/location/zones-from-city/" + id_city
        payload = {
            "id_company": ID_COMPANY,
            "wasi_token": WASI_TOKEN
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            return [(c["id_zone"], c["name"]) for c in resp.json().values() if isinstance(c, dict)]
        return []
    else:
        return []
