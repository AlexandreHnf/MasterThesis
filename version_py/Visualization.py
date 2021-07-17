import csv
import matplotlib.pyplot as plt
from IO import *



def plotBenchmarkResult(filename, title, ylabel, xlabel):
    """
    yMetrics = computation time (CT) or
                search space (SS) or
                nb relaxed edges (RE) or
                speed up or
                search space improvement or
                relaxed edges improvement
    """
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for p in ["bin", "fib", "list"]:
        x, y = [], []
        for graph in stats:
            x.append(stats[graph]["nb_nodes"])
            y.append(stats[graph]["stats"][p]["avg_CT"])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    plt.legend()
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.legend(loc='upper left')
    plt.show()