import requests

#function to retrieve the nasa photo of the dat
def get_apod(api_key):
#connect to nasa api
    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")

    #check if connection is succesfull
    if response.status_code != 200:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

    #parse json
    data = response.json()

    image_url = data['hdurl'] or data["url"]
    
    return {
        "date" : data["date"]
        ,"title" : data["title"]
        ,"explanation" : data["explanation"]
        ,"img_url" : image_url
    }