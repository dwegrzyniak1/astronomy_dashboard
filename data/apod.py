import requests

#function to retrieve the nasa photo of the dat
def get_apod(api_key):
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    print(response.status_code)
    print(response.json())

    
    return 3;