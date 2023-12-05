import os
import pandas as pd


def count_calories_per_minute(body_weight, speed, height):
    return 0.035 * body_weight + ((speed**2)/height) * 0.029 * body_weight


def get_speed(age, gender):
    file_path = os.path.join(os.path.dirname(__file__), "user_speed_constraints.json")
    df = pd.read_json(file_path)
    for constraint in df['data']:
        min_age, max_age = map(int, constraint['age_range'].split(";"))
        if min_age <= age <= max_age:
            return round(constraint[_get_gender(gender)], 2)
    return None


def _get_gender(gender):
    return "male" if gender == "M" else "female"