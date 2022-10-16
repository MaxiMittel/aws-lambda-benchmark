# Call api 10 times generate graph of results

import requests
import json
import matplotlib.pyplot as plt

# Define function to call api
def call_api():
    response = requests.get("https://awm7phlz3j.execute-api.eu-central-1.amazonaws.com/test")
    response_json = response.json()
    return response_json

# Define function to generate graph
def generate_graph():
    # Define empty lists
    x = []
    y = []

    # Call api 10 times
    for i in range(5):
        response_json = call_api()
        x.append(i)
        y.append(response_json["download100"]["bandwidth"])
        print("Call", i, ":", response_json["download100"]["bandwidth"])

    # Generate graph
    plt.plot(x, y)
    plt.xlabel("Call")
    plt.ylabel("Bandwidth [mbit/s]")
    plt.title("Bandwidth of 100 MB download")

    # Save graph
    plt.savefig("graph.png")

# Call function
generate_graph()