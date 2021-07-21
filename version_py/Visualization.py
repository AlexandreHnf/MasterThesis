import csv
import matplotlib.pyplot as plt
from IO import *


def show(legend, title, ylabel, xlabel, save_filename):
    if legend is not None:
        plt.legend()
        plt.legend(loc='upper left')

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.savefig(save_filename, dpi=100)
    plt.show()


def plotBenchmarkResult(filename, title, categories, ylabel, xlabel, yMetric, save_filename):
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
    for p in categories:
        x, y = [], []
        for graph in stats:
            x.append(stats[graph]["nb_nodes"])
            y.append(stats[graph]["stats"][p][yMetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotImprovementsResult(filename, title, categories, ylabel, xlabel, yMetric, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for p in categories:
        x, y = [], []
        for graph in stats:
            x.append(stats[graph]["nb_nodes"])
            avg_metric_dijkstra = stats[graph]["stats"]["Dijkstra"][yMetric]
            improv = avg_metric_dijkstra / stats[graph]["stats"][p][yMetric]
            y.append(improv)

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)

def plotPreprocessingResult(filename, title, ylabel, xlabel, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for graph in stats:
        x.append(stats[graph]["nb_nodes"])
        y.append(stats[graph]["stats"][2])

    plt.plot(x, y, marker="o")

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotExp7Result(filename, title, ylabel, xlabel, yMetric, speeds, algo, graph, save_filename):
    # TODO : "zoomer" sur l'axe y pour mieux voir les différences
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in speeds:
        x, y = [], []
        for k in stats[graph]:
            if k not in ["nb_nodes", "nb_edges", "avg_deg"]:
                if stats[graph][k]["speed_limit"] == s:
                    x.append(stats[graph][k]["nb_added_edges"])
                    y.append(stats[graph][k]["ALT"][yMetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotModalitiesLines(filename, title, ylabel, xlabel, graph, categories, algo, xMetric, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for t in categories:
        x, y = [], []
        for k in stats[graph]["stats"]:
            x.append(stats[graph]["stats"][k][xMetric])
            if t not in stats[graph]["stats"][k][algo]["avg_travel_types"]:
                y.append(0)
            else:
                y.append(stats[graph]["stats"][k][algo]["avg_travel_types"][t])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=t)
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left",  mode="expand", ncol=4)
    show(None, "", ylabel, xlabel, save_filename)


def plotModalitiesPieChart(filename, title, graph, algo, save_filename):
    stats = getJsonData(filename)

    # pie chart
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')

    values = list(stats[graph]["stats"][algo]["avg_travel_types"].values())
    categories = list(stats[graph]["stats"][algo]["avg_travel_types"].keys())

    ax.pie(values, labels=categories, autopct='%1.2f%%')

    plt.title(title)
    plt.savefig(save_filename, dpi=100)
    plt.show()


def plotExp9Result(filename, title, ylabel, xlabel, xMetric, yMetric, graph, save_filename):
    # TODO : "zoomer" sur l'axe y pour mieux voir les différences
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for algo in ["Dijkstra", "ALT"]:
        x, y = [], []
        for k in stats[graph]["stats"]:
            x.append(stats[graph]["stats"][k][xMetric])
            y.append(stats[graph]["stats"][k][algo][yMetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=algo)
        plt.plot(x, y)
        plt.xticks(x, x)


