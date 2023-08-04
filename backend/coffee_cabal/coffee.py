from psycopg2.extras import Json

from pydantic.dataclasses import dataclass
from dataclasses import asdict

from typing import Iterable, List, Dict
import csv

COFFEE_INDEX_NAME = "coffee"


@dataclass
class Coffee:
    id: int
    species: str
    owner: str
    country_of_origin: str
    farm_name: str
    lot_number: str
    mill: str
    ico_number: str
    company: str
    altitude: str
    region: str
    producer: str
    number_of_bags: str
    bag_weight: str
    in_country_partner: str
    harvest_year: str
    grading_date: str
    owner_1: str
    variety: str
    processing_method: str
    aroma: float
    flavor: float
    aftertaste: float
    acidity: float
    body: float
    balance: float
    uniformity: float
    clean_cup: float
    sweetness: float
    cupper_points: float
    total_cup_points: float
    moisture: float
    category_one_defects: int
    quakers: float
    color: str
    category_two_defects: str
    expiration: str
    certification_body: str
    certification_address: str
    certification_contact: str
    unit_of_measurement: str
    altitude_low_meters: float
    altitude_high_meters: float
    altitude_mean_meters: float


def load_coffee_csv(filepath: str) -> Iterable[Coffee]:
    coffees: Iterable = []
    with open(filepath) as csv_file:
        csv_reader = csv.reader(
            csv_file,
            delimiter=",",
        )
        next(csv_reader)
        for line in csv_reader:
            coffees.append(
                Coffee(
                    id=int(line[0]),
                    species=line[1],
                    owner=line[2],
                    country_of_origin=line[3],
                    farm_name=line[4],
                    lot_number=line[5],
                    mill=line[6],
                    ico_number=line[7],
                    company=line[8],
                    altitude=line[9],
                    region=line[10],
                    producer=line[11],
                    number_of_bags=line[12],
                    bag_weight=line[13],
                    in_country_partner=line[14],
                    harvest_year=line[15],
                    grading_date=line[16],
                    owner_1=line[17],
                    variety=line[18],
                    processing_method=line[19],
                    aroma=float(line[20]) if line[20] else 0.0,
                    flavor=float(line[21]) if line[21] else 0.0,
                    aftertaste=float(line[22]) if line[22] else 0.0,
                    acidity=float(line[23]) if line[23] else 0.0,
                    body=float(line[24]) if line[24] else 0.0,
                    balance=float(line[25]) if line[25] else 0.0,
                    uniformity=float(line[26]) if line[26] else 0.0,
                    clean_cup=float(line[27]) if line[27] else 0.0,
                    sweetness=float(line[28]) if line[28] else 0.0,
                    cupper_points=float(line[29]) if line[29] else 0.0,
                    total_cup_points=float(line[30]) if line[30] else 0.0,
                    moisture=float(line[31]) if line[31] else 0.0,
                    category_one_defects=int(line[32]) if line[32] else 0,
                    quakers=float(line[33]) if line[33] else 0.0,
                    color=line[34],
                    category_two_defects=line[35],
                    expiration=line[36],
                    certification_body=line[37],
                    certification_address=line[38],
                    certification_contact=line[39],
                    unit_of_measurement=line[40],
                    altitude_low_meters=float(line[41]) if line[41] else 0.0,
                    altitude_high_meters=float(line[42]) if line[42] else 0.0,
                    altitude_mean_meters=float(line[43]) if line[43] else 0.0,
                )
            )
        return coffees


def load_coffee_into_db(connection):
    coffees = load_coffee_csv("dataset/merged_data_cleaned.csv")
    with connection, connection.cursor() as tx:
        for coffee in coffees:
            tx.execute(
                "INSERT INTO coffee (id, data) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                [coffee.id, Json(asdict(coffee))],
            )


def least_acidic_coffee_by_elevation(connection) -> Iterable[Dict[str, any]]:
    result: List[Dict] = []
    with connection.cursor() as tx:
        tx.execute(
            """
        SELECT data->>'region'
             , ROUND(AVG((data->>'acidity')::numeric), 2) AS avg_acididty
        FROM coffee 
        GROUP BY 1
        ORDER BY avg_acididty ASC
        """
        )
        rs = tx.fetchall()
        for r in rs:
            result.append({"region": r[0], "average_acidity": r[1]})
    return result


def balance_by_processing_method(connection) -> Iterable[Dict[str, any]]:
    result: List[Dict] = []
    with connection.cursor() as tx:
        tx.execute(
            """
        SELECT data->>'processing_method'
             , ROUND(AVG((data->>'balance')::numeric), 2) AS avg_balance
        FROM coffee 
        WHERE data->>'processing_method' != ''
        GROUP BY 1
        ORDER BY avg_balance DESC
        """
        )
        rs = tx.fetchall()
        for r in rs:
            result.append({"processing_method": r[0], "average_balance": r[1]})
    return result


def largest_exporter_by_processing_method(connection) -> Iterable[Dict[str, any]]:
    result: List[Dict] = []
    with connection.cursor() as tx:
        tx.execute(
            """
            SELECT data->>'country_of_origin'
             , SUM((data->>'number_of_bags')::numeric) AS amount
            FROM coffee
            WHERE data->>'country_of_origin' != ''
            GROUP BY 1
            ORDER BY amount DESC;
        """
        )
        rs = tx.fetchall()
        for r in rs:
            result.append({"country_of_origin": r[0], "amount": r[1]})
    return result
