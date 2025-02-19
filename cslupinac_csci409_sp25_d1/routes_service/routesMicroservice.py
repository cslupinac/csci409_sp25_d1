import requests
from fastapi import FastAPI, HTTPException

API_KEY = "3872a6b16cd94e67a76e441665ab745f"  
ENDPOINT_URL = "https://api-v3.mbta.com/"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Routes Microservice"}

@app.get("/routes")
def get_routes():
    try:
        response = requests.get(f"{ENDPOINT_URL}/routes?api_key={API_KEY}")
        response.raise_for_status()  # Check for bad responses
        data = response.json().get("data", [])
        
        if not data:
            raise HTTPException(status_code=404, detail="No routes found")

        routes_list = [
            {
                "id": route["id"],
                "type": route["attributes"].get("type"),
                "color": route["attributes"].get("color"),
                "text_color": route["attributes"].get("text_color"),
                "description": route["attributes"].get("description"),
                "long_name": route["attributes"].get("long_name"),
            }
            for route in data
        ]
        return {"routes": routes_list}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching routes: {str(e)}")
