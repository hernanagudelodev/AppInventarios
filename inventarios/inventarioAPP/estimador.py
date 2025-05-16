import requests

# esta función se encarga de obtener lás propiedades de la API de wasi
# retorna un json con los datos de las propiedaes según los filtros
def obtener_propiedades(id_company, wasi_token, filtros_base):
    url = "https://api.wasi.co/v1/property/search"
    payload = {
        "id_company": id_company,
        "wasi_token": wasi_token,
        "for_sale": True,
        "short": True,
        "take": 100,
        **filtros_base
    }

    response = requests.post(url, json=payload)
    print("Status code:", response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None

# Esta función permite, según un listado de propiedades, calcular un valor de metro cuadrado promedio
# Devuelve, según ese valor de metro cuadrado promedio, y area objetivo de la nueva propiedad, dar un valor de venta
def calcular_valor_estimado_por_m2(propiedades, area_objetivo):
    precios_m2 = []

    for prop in propiedades.values():
        if isinstance(prop, dict):
            try:
                precio = float(prop.get("sale_price", 0))
                area = float(prop.get("area", 0))
                if precio > 0 and area > 0:
                    precios_m2.append(precio / area)
            except ValueError:
                continue

    if not precios_m2:
        print("Error calculando precios")
        return None

    promedio_m2 = sum(precios_m2) / len(precios_m2)
    valor_estimado = promedio_m2 * area_objetivo
    return round(valor_estimado, -4)

# Esta función ejecuta 3 filtros por jerarquía, la idea es obtener un valor para una propiedad con un área objetivo
# resultado de calcular un valor de metro cuadrado promedio
def asistente_estimador_dinamico(area_objetivo, id_company, wasi_token, id_city, id_location=None, id_zone=None):
    filtros = {"id_city": id_city}

    if id_location and id_location != 0:
        filtros["id_location"] = id_location
        data = obtener_propiedades(area_objetivo, id_company, wasi_token, filtros)
        if data and data.get("total", 0) > 3:
            return calcular_valor_estimado_por_m2(data, area_objetivo)
        else:
            print ("sin resultados por localidad")

    if id_zone and id_zone != 0:
        filtros.pop("id_location", None)
        filtros["id_zone"] = id_zone
        data = obtener_propiedades(area_objetivo, id_company, wasi_token, filtros)
        if data and data.get("total", 0) > 3:
            return calcular_valor_estimado_por_m2(data, area_objetivo)
        else:
            print ("sin resultados por Zona")

    filtros.pop("id_zone", None)
    data = obtener_propiedades(area_objetivo, id_company, wasi_token, filtros)
    if data and data.get("total", 0) > 0:
        return calcular_valor_estimado_por_m2(data, area_objetivo)
    else:
            print ("sin resultados por ciudad")
    return None