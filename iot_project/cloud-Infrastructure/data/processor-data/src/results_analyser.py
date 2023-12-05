import db_handler_service as dbHandler
import user_data_service as userDataHandler


db_handler = dbHandler.DatabaseHandlerService()


def convert_to_hours_minutes_seconds(total_seconds):
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return hours, minutes, seconds


def calc_calories(user_data, walking_minutes, running_minutes):
    speed = userDataHandler.get_speed(user_data[4], user_data[3])
    h_in_meters = user_data[5] / 100
    calories = userDataHandler.count_calories_per_minute(user_data[6], speed, h_in_meters)
    return round(walking_minutes * calories, 3), round(running_minutes * calories, 3)


def analyse(date_begin, date_end, results):
    result_list = []
    current_day = None
    walking_time = 0
    running_time = 0
    last_activity = None
    last_timestamp = None
    start_timestamp = None
    user_data = db_handler.get_user_data()

    for result in results:
        activity_type = result[1]
        timestamp = result[8].date()

        if current_day is None or current_day != timestamp:
            if current_day is not None:
                walking_hours, walking_minutes, walking_seconds = convert_to_hours_minutes_seconds(walking_time)
                running_hours, running_minutes, running_seconds = convert_to_hours_minutes_seconds(running_time)
                walking_calories, running_calories = calc_calories(user_data, walking_minutes, running_minutes)
                result_list.append({
                    'day': str(current_day),
                    'calories_walking': str(walking_calories),
                    'calories_running': str(running_calories),
                    'walking': f'{walking_hours} hours, {walking_minutes} minutes, and {walking_seconds} seconds',
                    'running': f'{running_hours} hours, {running_minutes} minutes, and {running_seconds} seconds',
                })

            # Reset variables for the new day
            current_day = timestamp
            walking_time = 0
            running_time = 0
            last_activity = None
            last_timestamp = None
            start_timestamp = None

        if last_activity is not None and activity_type != last_activity:
            time_difference = result[8] - start_timestamp
            if last_activity == 0:
                walking_time += time_difference.total_seconds()
            elif last_activity == 1:
                running_time += time_difference.total_seconds()

            start_timestamp = result[8]

        if start_timestamp is None:
            start_timestamp = result[8]

        last_activity = activity_type
        last_timestamp = result[8]

    if current_day is not None:
        walking_hours, walking_minutes, walking_seconds = convert_to_hours_minutes_seconds(walking_time)
        running_hours, running_minutes, running_seconds = convert_to_hours_minutes_seconds(running_time)
        walking_calories, running_calories = calc_calories(user_data, walking_minutes, running_minutes)
        result_list.append({
            'day': str(current_day),
            'calories_walking': str(walking_calories),
            'calories_running': str(running_calories),
            'walking': f'{walking_hours} hours, {walking_minutes} minutes, and {walking_seconds} seconds',
            'running': f'{running_hours} hours, {running_minutes} minutes, and {running_seconds} seconds',
        })

    return {'result': result_list}
