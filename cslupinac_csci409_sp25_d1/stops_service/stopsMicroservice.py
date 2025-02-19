import requests
from fastapi import FastAPI, HTTPException

API_KEY = "3872a6b16cd94e67a76e441665ab745f"  # Ensure this is a valid API key
ENDPOINT_URL = "https://api-v3.mbta.com/"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Stops Microservice"}

@app.get("/stops")
def get_stops():
    try:
        response = requests.get(f"{ENDPOINT_URL}/stops?api_key={API_KEY}")
        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            raise HTTPException(status_code=404, detail="No stops found")

        stops_list = [
            {
                "id": stop["id"],
                "name": stop["attributes"].get("name"),
                "latitude": stop["attributes"].get("latitude"),
                "longitude": stop["attributes"].get("longitude"),
            }
            for stop in data
        ]
        return {"stops": stops_list}

    except requests.exceptions.RequestException as e: # Check for bad responses
        raise HTTPException(status_code=500, detail=f"Error fetching stops: {str(e)}")
