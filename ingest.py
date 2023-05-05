import pandas as pd
import sqlite3
from classes.gas import Gas 
from argparse import ArgumentParser

def ingest_main(datafile, database):
    db = sqlite3.connect(database)

    gas_ingest = pd.read_csv(datafile, header=0)
    gas_ingest['car_id'] = 1
    gas_ingest.to_sql('gas', db, if_exists='append', index=False) 
    
gas = Gas("database.db")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--datafile",
        dest="datafile",
        help="datafile location",
        required=True
    )

    parser.add_argument(
        "-db",
        "--database",
        dest="database",
        help="database location",
        required=True
    )

    args = parser.parse_args()
    datafile = args.datafile
    database = args.database

    ingest_main(datafile, database)
