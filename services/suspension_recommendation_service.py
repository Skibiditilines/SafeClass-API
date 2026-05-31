from datetime import date


def evaluar_riesgo(clima: dict) -> dict:
    motivos = []
    puntos = 0

    sensacion = clima.get("sensacion_termica", 0)
    lluvia = clima.get("lluvia_mm", 0)
    viento = clima.get("viento_kmh", 0)
    descripcion = clima.get("descripcion", "").lower()

    if sensacion >= 40:
        puntos += 2
        motivos.append("Sensación térmica igual o superior a 40°C")

    if lluvia >= 10:
        puntos += 2
        motivos.append("Lluvia intensa")

    if viento >= 40:
        puntos += 2
        motivos.append("Viento fuerte")

    if "tormenta" in descripcion:
        puntos += 3
        motivos.append("Condición de tormenta reportada")

    if puntos >= 4:
        riesgo = "ALTO"
        recomendacion = "SUSPENDER"
    elif puntos >= 2:
        riesgo = "MEDIO"
        recomendacion = "PRECAUCION"
    else:
        riesgo = "BAJO"
        recomendacion = "NINGUNA"

    return {
        "riesgo": riesgo,
        "recomendacion": recomendacion,
        "motivos": motivos
    }