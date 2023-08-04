from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from coffee_cabal.db import connection
from coffee_cabal import coffee

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/least-acidic-regions")
def least_acidic_regions():
    return coffee.least_acidic_coffee_by_elevation(connection)[0:10]


@app.get("/processing-method-balance")
def least_acidic_regions():
    return coffee.balance_by_processing_method(connection)[0:10]


@app.get("/largest-exporter")
def largest_exporter():
    return coffee.largest_exporter_by_processing_method(connection)[0:10]
