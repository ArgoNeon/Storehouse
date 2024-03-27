import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def save_fig(pheromone_file_0, pheromone_file_1, figure_file_0, figure_file_1):
    data_0 = pd.read_csv(pheromone_file_0, sep=';', header=None)
    data_1 = pd.read_csv(pheromone_file_1, sep=';', header=None)

    plt.figure(figsize=(8, 8))
    sns.heatmap(data_0, annot=False, cmap='Greens', vmin=0.0, vmax=40.0, cbar=False, xticklabels=False, yticklabels=False, linewidth=1.0, linecolor='grey')
    plt.savefig(figure_file_0 + '.eps', format='eps')
    plt.savefig(figure_file_0 + '.png', format='png')

    plt.figure(figsize=(8, 8))
    sns.heatmap(data_1, annot=False, cmap='Greens', vmin=0.0, vmax=40.0, cbar=False, xticklabels=False, yticklabels=False, linewidth=1.0, linecolor='grey')
    plt.savefig(figure_file_1 + '.eps', format='eps')
    plt.savefig(figure_file_1 + '.png', format='png')

if __name__ == "__main__":
    save_fig(   'pheromone_map/pheromone_map_0_50_tick.csv',
                'pheromone_map/pheromone_map_1_50_tick.csv',
                'pheromone_fig/pheromone_map_0_50_tick',
                'pheromone_fig/pheromone_map_1_50_tick')
    save_fig(   'pheromone_map/pheromone_map_0_100_tick.csv',
                'pheromone_map/pheromone_map_1_100_tick.csv',
                'pheromone_fig/pheromone_map_0_100_tick',
                'pheromone_fig/pheromone_map_1_100_tick')
    save_fig(   'pheromone_map/pheromone_map_0_200_tick.csv',
                'pheromone_map/pheromone_map_1_200_tick.csv',
                'pheromone_fig/pheromone_map_0_200_tick',
                'pheromone_fig/pheromone_map_1_200_tick')
    save_fig(   'pheromone_map/pheromone_map_0_400_tick.csv',
                'pheromone_map/pheromone_map_1_400_tick.csv',
                'pheromone_fig/pheromone_map_0_400_tick',
                'pheromone_fig/pheromone_map_1_400_tick')

