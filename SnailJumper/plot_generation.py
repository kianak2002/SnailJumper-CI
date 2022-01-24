import matplotlib.pyplot as plt
import json


class Plot_generation:

    def plot(self):
        fig, ax = plt.subplots()
        with open('data_avg.json') as f:
            data1 = json.load(f)
            ax.plot(data1, label='avg')
        with open('data_max.json') as f:
            data2 = json.load(f)
            ax.plot(data2, label='max')
        with open('data_min.json') as f:
            data3 = json.load(f)
            ax.plot(data3, label='min')
        ax.legend()
        plt.show()

