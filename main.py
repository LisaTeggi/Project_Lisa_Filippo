# cloud function

def save_data(request):
    from google.cloud import bigquery
    from datetime import datetime, timedelta
    client = bigquery.Client()
    project_id = 'degori-test2'
    dataset_id = 'test1'
    table_id = 'prova'
    table_full_id = f'{project_id}.{dataset_id}.{table_id}'
    request_json = request.get_json(silent=True)
    if request_json:
        username = request_json['username']
        # lat = request_json['lat']
        # lon = request_json['lon']
        position = request_json['position']
        date = request_json['date']
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        # rows = [{'username': username, 'lat': lat, 'lon': lon, 'datetime': date.strftime('%Y-%m-%d %H:%M:%S')}]
        rows = [{'username': username, 'position': position, 'datetime': date.strftime('%Y-%m-%d %H:%M:%S')}]
        errors = client.insert_rows_json(table_full_id, rows)  # Make an API request.
        if not errors:
            return "New rows have been added."
        else:
            return "Encountered errors while inserting rows: {}".format(errors)
    # return f'{username}, {lat}, {lon}, {date}'
