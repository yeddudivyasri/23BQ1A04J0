import requests
from flask import Flask, jsonify

app = Flask(__name__)

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyM2JxMWEwNGowQHZ2aXQubmV0IiwiZXhwIjoxNzgwNjM5NTUzLCJpYXQiOjE3ODA2Mzg2NTMsImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiIxZDY1YTVmNC0xMzkyLTRkNzktODkxMi04Njc3MzRiM2E0YjYiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJ5ZWRkdSBkaXZ5YSBzcmkiLCJzdWIiOiIwYjU5ZDVhNy0zYzEwLTRiMWMtOTczNi04YTZlMzM4YzhkN2UifSwiZW1haWwiOiIyM2JxMWEwNGowQHZ2aXQubmV0IiwibmFtZSI6InllZGR1IGRpdnlhIHNyaSIsInJvbGxObyI6IjIzYnExYTA0ajAiLCJhY2Nlc3NDb2RlIjoiUVFkRVl5IiwiY2xpZW50SUQiOiIwYjU5ZDVhNy0zYzEwLTRiMWMtOTczNi04YTZlMzM4YzhkN2UiLCJjbGllbnRTZWNyZXQiOiJqcU5KekdzY3BQRHVHc3VXIn0.7KMNy7J3Z0-yG67bc5VQeQ5Xc1GD6mXwVk6XlksBRnY"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
BASE = "http://4.224.186.213/evaluation-service"

def knapsack(tasks, capacity):
    n = len(tasks)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d = tasks[i-1]["Duration"]
        imp = tasks[i-1]["Impact"]
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]
            if d <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-d] + imp)
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(tasks[i-1]["TaskID"])
            w -= tasks[i-1]["Duration"]
    return dp[n][capacity], selected

@app.route("/schedule", methods=["GET"])
def schedule():
    depots = requests.get(f"{BASE}/depots", headers=HEADERS).json()["depots"]
    vehicles = requests.get(f"{BASE}/vehicles", headers=HEADERS).json()["vehicles"]
    result = []
    for depot in depots:
        capacity = depot["MechanicHours"]
        total_impact, selected = knapsack(vehicles, capacity)
        result.append({
            "depotID": depot["ID"],
            "mechanicHours": capacity,
            "totalImpact": total_impact,
            "selectedTasks": selected
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)