import os
from flask_sqlalchemy import SQLAlchemy
from app import app, db, LandRecord  # Replace 'app' with the actual name of your Flask app file

db_name = "land_records.db"

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = os.path.join(project_dir, db_name)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(database_file)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Remove the line 'db = SQLAlchemy(app)' from this script since you're importing the existing db instance from 'app.py'.

def is_database_empty():
    num_records = LandRecord.query.count()
    return num_records == 0

def print_records():
    records = LandRecord.query.all()
    for record in records:
        print(f"ID: {record.id}")
        print(f"District: {record.district}")
        print(f"Tehsil: {record.tehsil}")
        print(f"Village: {record.village}")
        print(f"Village Code: {record.village_code}")
        print(f"Land Type: {record.land_type}")
        print(f"Khata Number: {record.khata_number}")
        print(f"Fasli Year: {record.fasli_year}")
        print(f"Khasra Number: {record.khasra_no}")
        print(f"Area: {record.area}")
        print(f"Name: {record.name}")
        print("----------------------")


if __name__ == "__main__":
    with app.app_context():
       
        if is_database_empty():
            print("The database is empty.")
        else:
            print("The database has records.")
            print_records()
