# Call api 10 times generate graph of results

import requests
import json
import matplotlib.pyplot as plt
import numpy as np

memory_settings = [512, 1024, 1536, 2048, 3072, 4096, 5120, 6144, 7168, 8192, 9216, 10240]

# Define function to call api
def call_api(memory):
    response = requests.get("https://awm7phlz3j.execute-api.eu-central-1.amazonaws.com/test" + str(memory))
    response_json = response.json()
    return response_json

def test_api(memory):
    # Call api 10 times and save results
    results = []
    for i in range(10):
        results.append(call_api(memory))
    return results

# Generate graph for bandwidth fluctuation
def generate_graph_fluctuation(memory, results):
    # Create lists for upload and download bandwidth
    upload_bandwidth = []
    download_bandwidth = []
    for result in results:
        upload_bandwidth.append(result["upload"]["bandwidth"])
        download_bandwidth.append(result["download"]["bandwidth"])

    call = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    plt.plot(call, upload_bandwidth, color='blue')
    plt.plot(call, download_bandwidth, color='red')
    plt.xlabel("Memory")
    plt.ylabel("Bandwidth")
    plt.title("Upload and download bandwidth")

    # Save to file
    plt.savefig("../graphs/fluctuation_" + str(memory) + ".png")


def avg_bandwidth(results):
    upload_bandwidth = []
    download_bandwidth = []
    for result in results:
        upload_bandwidth.append(result["upload"]["bandwidth"])
        download_bandwidth.append(result["download"]["bandwidth"])
    return sum(upload_bandwidth)/len(upload_bandwidth), sum(download_bandwidth)/len(download_bandwidth)

# Generate upload and download bandwidth bar chart
def generate_graph_bandwidth(api_results):
    # Iterate dictionary and generate graph
    x_labels = []
    data = []
    for memory, results in api_results.items():
        upload_bandwidth, download_bandwidth = avg_bandwidth(results)
        
        x_labels.append(str(memory))
        data.append([upload_bandwidth, download_bandwidth])
  
    length = len(data)

    data = np.array(data)

    # Set plot parameters
    fig, ax = plt.subplots()
    width = 0.2 # width of bar
    x = np.arange(length)

    ax.bar(x, data[:,0], width, color='#000080', label='Upload')
    ax.bar(x + width, data[:,1], width, color='#0F52BA', label='Download')

    ax.set_ylabel('Bandwidth [Mbps]')
    ax.set_xticks(x + width + width/2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Memory [MB]')
    ax.set_title('Bandwidth')
    ax.legend()
    #plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    fig.tight_layout()

    # Save to file
    plt.savefig("../graphs/bandwidth.png")

def main():
    results = {}
    for memory in memory_settings:
        print("Testing for memory: " + str(memory))
        results[memory] = test_api(memory)
        generate_graph_fluctuation(memory, results[memory])

    print("Generating bandwidth graph")
    generate_graph_bandwidth(results)
    print("Done")
    

if __name__ == "__main__":
    main()