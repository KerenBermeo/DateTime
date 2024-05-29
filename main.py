from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from api import addsubtract, convert, current, dayofweek, difference, nextoccurrence, validate, weeknumber

app = FastAPI()

def docs_route():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Documentation")

@app.get("/")
def read_root():
    return  docs_route()

app.include_router(addsubtract.router)
app.include_router(convert.router)
app.include_router(current.router)
app.include_router(dayofweek.router)
app.include_router(difference.router)
app.include_router(nextoccurrence.router)
app.include_router(validate.router)
app.include_router(weeknumber.router)