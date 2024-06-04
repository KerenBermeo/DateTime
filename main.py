from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from api import addsubtract, convert, current, dayofweek, difference, weeknumber

app = FastAPI(
    title="DATETIME",
    description='''DATETIME is a versatile API that offers multiple functionalities 
    related to date and time manipulation and conversion. 
    This API allows you to convert dates to different formats, 
    calculate differences between dates, obtain detailed time 
    zone information, and much more.''',
    version="1.0.0"
)

def docs_route():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API DateTime")

@app.get("/")
def main():
    """
    Página de Inicio de la API DateTime

    Esta página proporciona una visión general de la API DateTime,
    incluyendo una descripción de sus funcionalidades y una lista de
    los distintos endpoints disponibles.

    - **Endpoints**:
        - `/addsubtract`: Suma o resta un intervalo de tiempo a una fecha específica.
        - `/convert`: Convierte una fecha y hora a diferentes zonas horarias.
        - `/current`: Devuelve la fecha y hora actuales en varios formatos.
        - `/dayofweek`: Devuelve el día de la semana para una fecha específica.
        - `/difference`: Calcula la diferencia entre dos fechas y horas.
        - `/weeknumber`: Devuelve el número de semana ISO para una fecha específica.

    Al acceder a esta dirección se espera devolver la documentación de la API en formato HTML.
    """
    return  docs_route()

app.include_router(addsubtract.router, tags=["EndPoints"])
app.include_router(convert.router, tags=["EndPoints"])
app.include_router(current.router, tags=["EndPoints"])
app.include_router(dayofweek.router, tags=["EndPoints"])
app.include_router(difference.router, tags=["EndPoints"])
app.include_router(weeknumber.router, tags=["EndPoints"])