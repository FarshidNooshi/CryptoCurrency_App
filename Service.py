from fastapi import FastAPI, HTTPException
import sqlite3
import requests

app = FastAPI()

# SQLite Database Connection
conn = sqlite3.connect('crypto_prices.db')
cursor = conn.cursor()

# Create Price table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS price (
        coin_name TEXT,
        timestamp DATETIME,
        price FLOAT
    )
""")

# Create Alert Subscription table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alert_subscription (
        email TEXT,
        coin_name TEXT,
        difference_percentage INTEGER
    )
""")


@app.on_event("startup")
def startup_event():
    # Perform any initialization or setup tasks here
    pass


@app.get("/coins")
def get_active_coins():
    # Fetch the list of active currencies from the 'coinnews' service
    response = requests.get("https://coinnews.example.com/coins")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch active coins")


@app.get("/coin_price/{coin_name}")
def get_coin_price(coin_name: str):
    # Fetch the price of a specific currency from the 'coinnews' service
    response = requests.get(f"https://coinnews.example.com/coin_price/{coin_name}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch coin price")


@app.get("/coin_price_history/{coin_name}")
def get_coin_price_history(coin_name: str):
    # Fetch the price history of a currency from the 'coinnews' service
    response = requests.get(f"https://coinnews.example.com/coin_price_history/{coin_name}")
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch coin price history")


@app.post("/subscribe_coin")
def subscribe_coin(email: str, coin_name: str, difference_percentage: int):
    # Add a new alert subscription to the database
    cursor.execute("INSERT INTO alert_subscription (email, coin_name, difference_percentage) VALUES (?, ?, ?)",
                   (email, coin_name, difference_percentage))
    conn.commit()
    return {"message": "Successfully subscribed to coin updates"}


@app.get("/price_history/{coin_name}")
def get_price_history(coin_name: str):
    # Fetch the price history of a currency from the database
    cursor.execute("SELECT timestamp, price FROM price WHERE coin_name = ? ORDER BY timestamp DESC", (coin_name,))
    result = cursor.fetchall()
    if result:
        return {"coin_name": coin_name, "price_history": result}
    else:
        raise HTTPException(status_code=404, detail="Price history not found for the coin")


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
