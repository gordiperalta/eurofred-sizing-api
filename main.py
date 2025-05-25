from utils.io_utils import load_user_input
from services.climate_api import get_climate_data
from services.supabase_queries import get_u_ach, get_orientation_factor
from models.calculations import compute_humidity_ratio_and_load
from services.unit_selection import select_indoor_units, select_outdoor_units
import os



def main():
    user_input = load_user_input("inputs/sample_user_input.json")
    temp, rh = get_climate_data(user_input["address"])
    U, ACH = get_u_ach(user_input["construction_year"])
    orientation_factor = get_orientation_factor(user_input["orientation"])

    humidity_ratio, cooling_load = compute_humidity_ratio_and_load(
        U, ACH, temp, rh,
        user_input["square_meters"],
        user_input["people_count"],
        user_input["floor_count"],
        orientation_factor
    )
    indoor_units = select_indoor_units(user_input["bedroom_info"], cooling_load, user_input["square_meters"])
    outdoor_units = select_outdoor_units(indoor_units, user_input["floor_count"])

    result = {
        "humidity_ratio": humidity_ratio,
        "cooling_load_kW": cooling_load,
        "indoor_units": indoor_units,
        "outdoor_units": outdoor_units
    }

    print(result)

if __name__ == "__main__":
    main()

def compute_project(user_input):
    temp, rh = get_climate_data(user_input["address"])
    U, ACH = get_u_ach(user_input["construction_year"])
    orientation_factor = get_orientation_factor(user_input["orientation"])

    humidity_ratio, cooling_load = compute_humidity_ratio_and_load(
        U, ACH, temp, rh,
        user_input["square_meters"],
        user_input["people_count"],
        user_input["floor_count"],
        orientation_factor
    )

    indoor_units = select_indoor_units(user_input["bedroom_info"], cooling_load, user_input["square_meters"])
    outdoor_units = select_outdoor_units(indoor_units, user_input["floor_count"])

    return {
        "humidity_ratio": humidity_ratio,
        "cooling_load_kW": cooling_load,
        "indoor_units": indoor_units,
        "outdoor_units": outdoor_units
    }
