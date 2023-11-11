import requests

def getIncident():
    url = "https://api.iq.inrix.com/v1/incidents?point=37.7749%7C-122.4194&radius=1&incidentoutputfields=All&incidenttype=Flow&locale=en"

    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjcxMDU4ZjQ2YjhhZDNiZGJhM2U0NDAxYTU4NjY5MTFjIiwiY29udGVudCI6IjQ1N2Y5YzE4ZWI0NDIyMjdlZjU3ZTE1NmJkYTAxZDE0NjU4ZTc0ZTUxNDIzNjNlYjNlZmI5YjFkZmUzZmFkZDA4YzM3YzgxNWE3YTc3NTJmM2VmMWFmOGU4Mjk1MWVhNDc2ODcwM2NkODBiOTdjYzRkMGI1ZjljZDllOTJhMmI4YmQxYTVmYjAwYjkyMjBlZTExODdiMzU1ZTU3YzIyZjJkNjk5Zjg4NDdmZDI2YmQzYTYzYzM1NjcxNTk4YTM5OGFiOTQ4YmMxMTBjZDg4OTRmYTYxZjlmYjIzYjE2NmE3MDYyNmNlY2IzZTI0OTMxNzU3ZTJlN2RlNWY2ZTEyMjIwODQ5YmI1MTRmZmZiNTc2MDA4MmExZTE2ZWQ2N2Y5Yjc5Yzk1NTdlMGFiNjc3ZGNiYjc0MTU1MWFmZWVhYzBiZTc1OGRlNThmODk3ODU5MzcwZWJhMjFhN2M4NTljMjBhY2U5Yjc3ZmRkNWMwMzRlYzVmYjg0NjM2MTE0YjdkYTYxNjVjYTJhOGQ0NGU5ZDZhODUyYTNmOTU3YWUyMTAwM2RlNzYwNDYwNDU3YmExZjkyYzg5NDhjOTQwZjAzY2E3ZDNmNDZlZGQwMGEyOWVjYWU4Nzk4MTAzOTE2NmUyYmIyNWZlODE2YjRmZGNiMGYyZTJiMjhjZjg5NjQwZjk1OTM2MzRjYmQ0MDdmYjlmZWMzNzc3YzdhNTQwMzQ5MDlmZWM3ZmM1ZDExM2EyZWIzZTZiYWZlYzA5ZjBlYTE2NjUwYTA5NWZiMTAyNzUwMjQ3Yzg4YzY5ZjBhMDBmNTI4MmI5OWIxNTVhNjk1YTQ0YmEwNmYxZGNlNmUxZWFmZTg3ZGRmY2JiZGNmNTM3NTZhMTRlNjI1In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiI3MTA1OGY0NmI4YWQzYmRiYTNlNDQwMWE1ODY2OTExYyIsImNvbnRlbnQiOiI0OTRjZTUzOWZiNWEwMzFiZjk0NmNlNWNhYzhkMzI0YjEzYTU0ZmZiMDgwNjFjODk2YmU5OWY3MWRhM2I5OWYyZWYxNmQ1NjJiOGFjN2UwNjNiZGU4NGIwIn0sImp0aSI6IjkwMmJmOGJiLThkZmItNDc1Zi05ZDUwLWRlMjI3Yzc2OTMyOCIsImlhdCI6MTY5OTczNTc0MywiZXhwIjoxNjk5NzM5MzQzfQ.mqu75CirpNuk2GhtueMhE3naR3swdNfKMXgiGOnU4-Y'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    incidents = []
    for incident in response.json()['result']['incidents']:
        incidents.append({
            'severity': incident['severity'],
            'coordinates': incident['geometry']['coordinates'],
        })

    return incidents
