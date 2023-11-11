import requests

apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6InF0ZXQ0cjNva2UiLCJ0b2tlbiI6eyJpdiI6IjE5MDUwNWJlZDI4OWViMjlkYmUxZWE3ZjIwM2QyMDYyIiwiY29udGVudCI6Ijg4YjMyNjYwZmYwNjQxN2IzOGRkMmIzMzZlM2JiZWZkMDJmZDliMTE2YjNmNGNlNjI0N2VmNzAwYTU1NDM3OTJjZTY0ODQ0ZmM1OTQ0Y2JhZWI3MmNkN2NlYTMwYjMyZDliZjYyZTY4Yzg2Yzc3MWJjN2QyNGUxY2ZkNzI2NmM1ZWM4ZTNmOWRjMmIyNjIyZWI4YTBhNTA1N2FlMmQ0ZTIxMDNiMTc3MDlmOTc1ZTA5ZmYwYWI5MTRmODgwMjk1ODEyNjA5NzZkMDQzMWMzNDc0ZDdjY2UxZWE1YjM4YjZjODUxZjA2Mjc5NDJkMDIyYjllNmFjY2YwN2E5YWNhYmQ0Y2UwZDkxMzZhZTE2NTFmMzU0MmQzNGQ3MGJhMTJlNzAzYmZkODdiNWE3N2UzOThlOTU3YmFjMDk5ZDM0YzI4NTJkN2M3MDcxZDhhYWE2ODQzZDJmNmMxZDdkMmUyMmZmYmM2ODRmNjFlZDZiNmFlMzBjODI4YTZiOTBlZmY3ZDNkZTNkYzZmMjUxYmQzMTEyMWQ0MDljMTNlYTdkOGRiZTUxM2I1ODVkZDc0OGQzOWNlMzJlMzQzMzdhYzg1MGE4NTZjNDNmNmZmMzY4YzBjZTliYzViZGJhYmNmNDNmYjhhYTM0NjM1OWFhMTBkNDRiNzYzZTUyNzM1NzJmMTg2MmIxYzg3ZTc0ZmM2Y2FkY2EzZWQwNWUwZjZhZDMyYWQzZmU5NjkwN2UwNzhiNDQzNzkzYWNiMGU5OTI0OGUzMzQ0MGRmMDRjMmMwMmNiNWU4MDA4NGIxOTcyMmY0OWMyYzUyZmU5ZTgzZDljNzY0NzVjOWM3MThlZjY4NzE3M2ViZjk4YjJjNzMyZTA2MDNlNmU2MmQ5In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiIxOTA1MDViZWQyODllYjI5ZGJlMWVhN2YyMDNkMjA2MiIsImNvbnRlbnQiOiJhYzhiMzQ1MWFmNmI1YjM4MjRjYzI1MTI2YjcwYmVmNTFjZmM4NDExNzEzZjZhOGEzZjZkZjk0NTljNzk3NDhiY2U3NWEzNGZhMWE5NzdjNWY2NWViNTQyIn0sImp0aSI6ImM0ZWNjNGI3LWZlODYtNDAyMi04YmExLWE2MzhkZTk2ZjI5ZSIsImlhdCI6MTY5OTc0MDIxMywiZXhwIjoxNjk5NzQzODEzfQ.Q6Rvz6vWQ7S0U7JrLvrJ01pAeXUDiDzscxvSr0cF1DM"

def getIncident(radius=10, center_x="37.7749", center_y="-122.4194", incidenttype="Flow", locale="en"):
    url = f"https://api.iq.inrix.com/v1/incidents?point={center_x}%7C{center_y}&radius={radius}&incidentoutputfields=All&incidenttype={incidenttype}&locale={locale}"
    payload = {}
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {apiToken}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    incidents = []
    for incident in response.json()['result']['incidents']:
        incidents.append({
            'severity': incident['severity'],
            'coordinates': incident['geometry']['coordinates'],
        })

    return incidents
print(getIncident())