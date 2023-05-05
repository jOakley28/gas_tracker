import sqlite3
import pandas as pd
from datetime import datetime
from datetime import timedelta 

class Gas:
    def __init__(self, db_location: str):
        self.db = sqlite3.connect(db_location, check_same_thread=False)

    def db_size(self) -> int:
        return len(
            pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table'", self.db
            )
        )

    def convert_df_to_dict(self, df: pd.DataFrame) -> list:
        try:
            df_list = df.to_dict(orient="records")
        except:
            return None
        return df_list

    """
    add to database
    """
    def add_car(self, owner, make, model, year, tank_size) -> bool:
        try:
            self.db.execute(
                "INSERT INTO cars (owner, make, model, year, mpg, tank_size) VALUES (?, ?, ?, ?, ?, ?)",
                (owner, make, model, year, None, tank_size),
            )
            self.db.commit()
            return True
        except:
            return False

    def add_gas(self, car_id: str, cost, amount, distance, phase) -> bool:
        cost = float(cost)
        distance = float(distance)
        amount = float(amount)

        # gets current date for database
        current_date = datetime.now().strftime("%d-%m-%y")

        # calculates $/gal and mpg 
        cost_per_gallon = round(cost / amount, 2)
        trip_mpg = round(distance / amount, 2)

        # calculates the approx miles left 
        car = self.get_car(car_id)
        tank_size = car['tank_size'][0]
        distance_remaining = round((tank_size - amount)*trip_mpg, 2)

        # determines phase: if phase is left blank use previous phase, otherwise use listed phase 
        if phase == None:
            prev_gas = self.get_gas_by_car(car_id)
            last_gas = prev_gas.tail(n=1)
            last_phase = last_gas.loc[:, 'phase'].iloc[-1]
            phase = last_phase

        try:
            self.db.execute(
                "INSERT INTO gas (car_id, date, cost, amount, distance, cost_per_gallon, trip_mpg, distance_remaining, phase) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (car_id, current_date, cost, amount, distance, cost_per_gallon, trip_mpg, distance_remaining, phase),
            )
            self.db.commit()
            return True
        except:
            return False

    """
    get from database
    """
    def get_gas_by_car(self, car_id) -> pd.DataFrame:
        gas_df = pd.read_sql_query("SELECT * FROM gas WHERE car_id = ?", self.db, params=(car_id,))
        return gas_df
    
    def get_last_gas(self):
        gas_df = pd.read_sql_query("SELECT * FROM gas", self.db)
        last_gas_df = (gas_df.tail(n=1))
        return last_gas_df

    def get_car(self, car_id) -> pd.DataFrame:
        cars_df = pd.read_sql_query(
            "SELECT * FROM cars WHERE car_id = ?", self.db, params=(car_id,)
        )
        return cars_df

    def get_all_cars(self):
        cars_df = pd.read_sql_query("SELECT * FROM cars", self.db)
        return cars_df.to_dict(orient="records")
    
    def get_phases_by_car(self, car_id):
        prev_gas = self.get_gas_by_car(car_id)
        phases = prev_gas['phase']        
        return phases.tolist()
    
    """
    edit in database
    """
    def edit_car(self, car_id, owner, make, model, year, mpg, tank_size) -> bool:
        try:
            self.db.execute(
                "UPDATE cars SET owner = ?, make = ?, model = ?, year = ?, mpg = ?, tank_size = ? WHERE car_id = ?",
                (owner, make, model, year, mpg, tank_size, car_id),
            )
            self.db.commit()
            return True
        except Exception as e:
            print(f"Failed to edit car: {e}")
            return False

    def edit_gas(self, gas_id, cost, amount, distance, phase) -> bool:
        try:
            self.db.execute(
                "UPDATE gas SET cost = ?, amount = ?, distance = ?, phase = ? WHERE gas_id = ?",
                (cost, amount, distance, phase, gas_id),
            )
            self.db.commit()
            return True
        except Exception as e:
            print(f"Failed to edit gas: {e}")
            return False

    """
    calculate based on database
    """
    def trip_cost(self, car_id, trip_length):
        # calculated based off of 5 most recent trips, 
        gas = self.get_gas_by_car(car_id)
        last_five_gas = gas.tail(n=5)

        # more conservative estamate mpg (will take the higher of the 5 trip average or the most recent mpg)
        average_mpg = float(last_five_gas['trip_mpg'].mean())
        most_recent_mpg = float(last_five_gas['trip_mpg'].tail(n=1).to_list()[0])
        if average_mpg >= most_recent_mpg:
            approx_mpg = average_mpg
        else:
            approx_mpg = most_recent_mpg

        # conservative $/gal
        average_cost_per_gallon = float(last_five_gas['cost_per_gallon'].mean())
        most_recent_cost_per_gallon = float(last_five_gas['cost_per_gallon'].tail(n=1).to_list()[0])
        if average_cost_per_gallon >= most_recent_cost_per_gallon:
            approx_cost_per_gallon = average_cost_per_gallon
        else:
            approx_cost_per_gallon = most_recent_cost_per_gallon

        # cost = cost/gal * (miles/gal)^-1 * miles
        trip_cost = approx_cost_per_gallon / approx_mpg * float(trip_length)

        return round(trip_cost, 2)

    """
    dashboard plots
    """        
    def dashboard_plots(self, car_id):
        gas_table = self.dashboard_gas_table(car_id)

        cost_per_gal_plot = self.dashboard_cost_per_gal_plot(car_id)

        cost_per_mile_plot = self.dashboard_cost_per_mile_plot(car_id)

        trip_distance_plot = self.dashboard_trip_distance_plot(car_id)
    
        efficacy_plot = self.dashboard_efficacy_plot(car_id)
        
        return gas_table, cost_per_gal_plot, cost_per_mile_plot, trip_distance_plot, efficacy_plot

    def dashboard_gas_table(self, car_id):
        gas_table = self.get_gas_by_car(car_id)[['date','cost','amount','distance','cost_per_gallon','trip_mpg','distance_remaining','phase']]
        return gas_table


    def dashboard_cost_per_gal_plot(car_id):
        pass

    def dashboard_cost_per_mile_plot(car_id):
        pass

    def dashboard_trip_distance_plot(car_id):
        pass

    def dashboard_efficacy_plot(car_id):
        pass
