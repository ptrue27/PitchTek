import matplotlib.pyplot as plt
import requests

def fetch_pitcher_era_stats(pitcher_name):
    # This URL should be the endpoint in your PitchTek backend that returns ERA stats by year for a given pitcher
    url = f"http://localhost:5000/api/pitcher_era_stats?pitcher_name={pitcher_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return {}

def plot_era_stats(pitcher_name, era_stats):
    years = list(era_stats.keys())
    era_values = list(era_stats.values())

    plt.plot(years, era_values, marker='o')
    plt.title(f'ERA Stats Over the Last 5 Years for {pitcher_name}')
    plt.xlabel('Year')
    plt.ylabel('ERA')
    plt.grid(True)
    plt.savefig(f'{pitcher_name}_ERA_Stats.png')
    plt.show()

if __name__ == "__main__":
    pitcher_name = input("Enter the pitcher's name: ")
    era_stats = fetch_pitcher_era_stats(pitcher_name)

    if era_stats:
        plot_era_stats(pitcher_name, era_stats)
