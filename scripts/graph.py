import requests
import json
import matplotlib.pyplot as plt
import numpy as np

memory_settings = [512, 1024, 2048, 3072, 4096, 5120, 6144, 7168, 8192, 9216, 10240]

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
def generate_graph_fluctuation(memory, data):
    # Create lists for upload and download bandwidth
    upload_bandwidth = []
    download_bandwidth = []
    for result in data:
        upload_bandwidth.append(result["upload"]["total"]["bandwidth"])
        download_bandwidth.append(result["download"]["total"]["bandwidth"])

    call = list(range(1,11))

    plt.plot(call, upload_bandwidth, color='#D11149', label='Upload')
    plt.plot(call, download_bandwidth, color='#1A8FE3', label='Download')
    plt.xlabel("Invocations")
    plt.ylabel("Bandwidth [Mbps]")
    plt.title("Bandwidth fluctuation: " + str(memory) + " MB")
    plt.legend(["Upload", "Download"])

    # Save to file
    plt.savefig("../graphs/fluctuation_" + str(memory) + ".png")
    plt.close()

# Generate graph for bandwidth fluctuation
def generate_graph_spikes(memory, data):
    upload_bandwidth = data["upload"]["bandwidth"]
    download_bandwidth = data["download"]["bandwidth"]

    call = list(range(1,101))

    plt.plot(call, upload_bandwidth, color='#D11149', label='Upload')
    plt.plot(call, download_bandwidth, color='#1A8FE3', label='Download')
    plt.xlabel("Invocations")
    plt.ylabel("Bandwidth [Mbps]")
    plt.title("Bandwidth spikes: " + str(memory) + " MB")
    plt.legend(["Upload", "Download"])

    # Save to file
    plt.savefig("../graphs/spike_" + str(memory) + ".png")
    plt.close()


def avg_bandwidth(results):
    upload_bandwidth = []
    download_bandwidth = []
    for result in results:
        upload_bandwidth.append(result["upload"]["total"]["bandwidth"])
        download_bandwidth.append(result["download"]["total"]["bandwidth"])
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

    ax.bar(x, data[:,0], width, color='#D11149', label='Upload')
    ax.bar(x + width, data[:,1], width, color='#1A8FE3', label='Download')

    ax.set_ylabel('Bandwidth [Mbps]')
    ax.set_xticks(x + width + width/2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel('Memory [MB]')
    ax.set_title('Bandwidth at 10:00')
    ax.legend()

    fig.tight_layout()

    # Save to file
    plt.savefig("../graphs/bandwidth.png")
    plt.close()

def main():
    results = {}
    for memory in memory_settings:
        print("Testing for memory: " + str(memory))
        results[memory] = test_api(memory)
        generate_graph_fluctuation(memory, results[memory])
        if memory >= 2048:
            generate_graph_spikes(memory, results[memory][0])

    print("Generating bandwidth graph")
    generate_graph_bandwidth(results)
    print("Done")
    

if __name__ == "__main__":
    main()