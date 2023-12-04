def analyse(results):
    walking_time = 0
    running_time = 0
    last_timestamp = None
    for result in results:
        activity_type = result[1]
        timestamp = result[8]
        if last_timestamp is not None:
            time_difference = timestamp - last_timestamp
            if activity_type == 0:
                walking_time += time_difference.total_seconds()
            elif activity_type == 1:
                running_time += time_difference.total_seconds()
        last_timestamp = timestamp
    return {
        'walking_time_minutes': walking_time,
        'running_time_minutes': running_time
    }


