import requests
from fastapi import FastAPI, HTTPException

API_KEY = "3872a6b16cd94e67a76e441665ab745f"  
ENDPOINT_URL = "https://api-v3.mbta.com/"

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Lines Microservice"}

@app.get("/lines")
def get_lines():
    try:
        response = requests.get(f"{ENDPOINT_URL}/routes?api_key={API_KEY}")
        response.raise_for_status()
        data = response.json().get("data", [])

        if not data:
            raise HTTPException(status_code=404, detail="No lines found")

        lines_list = [
            {
                "id": route["id"],
                "text_color": route["attributes"].get("text_color"),
                "short_name": route["attributes"].get("short_name"),
                "long_name": route["attributes"].get("long_name"),
                "color": route["attributes"].get("color"),
            }
            for route in data
        ]
        return {"lines": lines_list}

    except requests.exceptions.RequestException as e: # Check for bad responses. 
        raise HTTPException(status_code=500, detail=f"Error fetching lines: {str(e)}")
