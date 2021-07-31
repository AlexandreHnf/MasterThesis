import csv
import matplotlib.pyplot as plt
from IO import *


def show(legend, title, ylabel, xlabel, save_filename):
    if legend is not None:
        plt.legend()
        plt.legend(loc=legend)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.savefig(save_filename, dpi=100)
    plt.show()


def plotBenchmarkResult(filename, title, categories, ylabel, xlabel, ymetric, save_filename):
    """
    ymetrics = computation time (CT) or
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
            y.append(stats[graph]["stats"][p][ymetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotImprovementsResult(filename, title, categories, ylabel, xlabel, ymetric, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for p in categories:
        x, y = [], []
        for graph in stats:
            x.append(stats[graph]["nb_nodes"])
            avg_metric_dijkstra = stats[graph]["stats"]["Dijkstra"][ymetric]
            improv = avg_metric_dijkstra / stats[graph]["stats"][p][ymetric]
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


def plotAvgDegResult(filename, title, ylabel, xlabel, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for graph in stats:
        x.append(stats[graph]["nb_nodes"])
        y.append(stats[graph]["avg_deg"])

    plt.plot(x, y, marker="o")

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotExp7Result(filename, title, ylabel, xlabel, ymetric, speeds, algo, graph, save_filename):
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
                    y.append(stats[graph][k][algo][ymetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotImprovementsExp7(filename, title, ylabel, xlabel, ymetric, speeds, graph, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in speeds:
        x, y = [], []
        for k in stats[graph]:
            if k not in ["nb_nodes", "nb_edges", "avg_deg"]:
                if stats[graph][k]["speed_limit"] == s:
                    x.append(stats[graph][k]["nb_added_edges"])
                    avg_metric_dijkstra = stats[graph][k]["Dijkstra"][ymetric]
                    avg_metric_ALT = stats[graph][k]["ALT"][ymetric]
                    if avg_metric_ALT == 0.0:
                        print(avg_metric_dijkstra, avg_metric_ALT)
                        avg_metric_ALT = (avg_metric_dijkstra) / 10
                    improv = round(avg_metric_dijkstra / avg_metric_ALT, 6)
                    y.append(improv)

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper right", title, ylabel, xlabel, save_filename)


def plotExp7AvgDegResult(filename, title, ylabel, xlabel, speeds, graph, save_filename):
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
                    y.append(stats[graph][k]["avg_degree_after"])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotMaxAvgLbExp7(filename, title, ylabel, xlabel, speeds, graph, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in speeds:
        x, y = [], []
        for k in stats[graph]:
            if k not in ["nb_nodes", "nb_edges", "avg_deg"]:
                if stats[graph][k]["speed_limit"] == s:
                    x.append(stats[graph][k]["nb_added_edges"])
                    y.append(stats[graph][k]["ALT"]["max_avg_lb"])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotModalitiesLines(filename, title, ylabel, xlabel, graph, categories, algo, xmetric, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for t in categories:
        x, y = [], []
        for k in stats[graph]["stats"]:
            x.append(stats[graph]["stats"][k][xmetric])
            if t not in stats[graph]["stats"][k][algo]["avg_travel_types"]:
                y.append(0)
            else:
                y.append(stats[graph]["stats"][k][algo]["avg_travel_types"][t])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=t)
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=4)
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


def plotPrefExpResult(filename, title, ylabel, xlabel, xmetric, ymetric, graph, save_filename):
    # TODO : "zoomer" sur l'axe y pour mieux voir les différences
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for algo in ["Dijkstra", "ALT"]:
        x, y = [], []
        for k in stats[graph]["stats"]:
            x.append(stats[graph]["stats"][k][xmetric])
            y.append(stats[graph]["stats"][k][algo][ymetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=algo)
        plt.plot(x, y)
        plt.xticks(x, x)

    show("upper left", title, ylabel, xlabel, save_filename)


def plotPrefAvgMaxLb(filename, title, ylabel, xlabel, xmetric, graph, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for k in stats[graph]["stats"]:
        x.append(stats[graph]["stats"][k][xmetric])
        y.append(stats[graph]["stats"][k]["ALT"]["max_avg_lb"])

    plt.plot(x, y, marker="o")

    # show
    show(None, title, ylabel, xlabel, save_filename)


# ====================================================

def plotExp1(metrics):
    """

    """
    categories = ["bin", "fib", "list"]

    for metric in metrics:
        save_filename = FILE_EXP1 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP1_ALL,
                            "Experience 1 - Dijkstra - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            save_filename)


def plotExp2(metrics):
    """

    """
    categories = ["euclidean", "manhattan", "octile"]

    for metric in metrics:
        save_filename = FILE_EXP2 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP2_ALL,
                            "Experience 2 - A* - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            save_filename)


def plotExp3(metrics):
    """

    """
    categories = ["random", "farthest", "planar"]

    for metric in metrics:
        save_filename = FILE_EXP3 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP3_ALL,
                            "Experience 3 - ALT - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            save_filename)


def plotExp4(metrics):
    """

    """
    categories = ["1", "2", "4", "8", "16", "32"]

    for metric in metrics:
        save_filename = FILE_EXP4 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP4_ALL,
                            "Experience 4 - ALT - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            save_filename)


def plotExp5(metrics, improvements):
    """

    """
    # plot standard metrics
    categories = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    for metric in metrics:
        save_filename = FILE_EXP5 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP5_ALL,
                            "Experience 5 - Single-modal car networks - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            save_filename)

    # plot : |V| - improv (1 for speedup, 1 for rel, 1 for SS
    categories = ["A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    for metric in improvements:
        save_filename = FILE_EXP5 + "plot_improv_" + metric + ".png"
        plotImprovementsResult(FILE_EXP5_ALL,
                               "Experience 5 - Improvement - " + metric,
                               categories, improvements[metric], "|V|",
                               metric, save_filename)

    # plot : |V| - avg deg
    save_filename = FILE_EXP5 + "plot_avg_deg.png"
    plotAvgDegResult(FILE_EXP5_ALL, "Experience 5 - avg degree",
                     "avg deg", "|V|", save_filename)


def plotExp6():
    """

    """
    save_filename = FILE_EXP6 + "plot_prepro_CT.png"
    plotPreprocessingResult(FILE_EXP6_ALL,
                            "Experience 6 - Preprocessing",
                            "computation time (sec.)", "|V|",
                            save_filename)


def plotExp7(metrics, improvements, graphs):
    """
    TODO : prendre tous les algos (Dijkstra et ALT) et tous les graphs
    1 -> 6
    """
    speeds = [0.1, 15, 30, 90, 120, 1e10]

    for graph in graphs:
        for metric in metrics:
            save_filename = FILE_EXP7 + "plot_" + metric + "_" + graph + ".png"
            plotExp7Result(FILE_EXP7_ALL,
                           "Experience 7 - Nb added edges - " + metric + " - " + graph,
                           metrics[metric], "|added edges|", metric,
                           speeds, "ALT", graph, save_filename)

        for metric in improvements:
            save_filename = FILE_EXP7 + "plot_improv_" + metric + "_" + graph + ".png"
            plotImprovementsExp7(FILE_EXP7_ALL,
                                 "Experience 7 - improvement - " + metric + " - " + graph,
                                 improvements[metric], "|added edges|", metric,
                                 speeds, graph, save_filename)

        save_filename = FILE_EXP7 + "plot_avgDeg_" + graph + ".png"
        plotExp7AvgDegResult(FILE_EXP7_ALL, "Experience 7 - avg deg - " + graph,
                             "avg deg after", "|added edges|", speeds,
                             graph, save_filename)

        # plot : mac avg lower bound - ALT
        save_filename = FILE_EXP7 + "plot_max_avg_lb_" + graph + ".png"
        plotMaxAvgLbExp7(FILE_EXP7_ALL,
                         "Experience 7 - Max average distance lower bound - " + graph,
                         "max avg lower bound", "|added edges|", speeds,
                         graph, save_filename)


def plotExp8(metrics):
    """

    """
    categories = ["Dijkstra", "ALT"]

    # plot standard metrics
    for metric in metrics:
        save_filename = FILE_EXP8 + "plot_" + metric + ".png"
        plotBenchmarkResult(FILE_EXP8_ALL,
                            "Experience 8 - Multi-modal station-based - " + metric,
                            categories, metrics[metric], "|V|",
                            metric, save_filename)

    # plot : modality1 - modality2 for Dijkstra & ALT
    save_filename = FILE_EXP8 + "plot_piechart_Dijkstra.png"
    plotModalitiesPieChart(FILE_EXP8_ALL,
                           "Experience 8 - Pie chart modalities",
                           "1_ULB", "Dijkstra", save_filename)


def plotExp9(metrics, graphs):
    """

    """
    for graph in graphs:
        for metric in metrics:
            save_filename = FILE_EXP9 + "plot_" + metric + "_" + graph + ".png"
            plotPrefExpResult(FILE_EXP9_ALL,
                              "Experience 9 - prefs - " + metric + " - " + graph,
                              metrics[metric], "c2", "c2", metric,
                              graph, save_filename)

        save_filename = FILE_EXP9 + "plot_travelTypes_" + graph + ".png"
        plotModalitiesLines(FILE_EXP9_ALL,
                            "Experience 9 - Travel types - " + graph,
                            "Travel types frequency", "c2", graph,
                            ["Villo", "fromStation", "toStation", "car"],
                            "Dijkstra", "c2", save_filename)

        # plot max avg lb
        save_filename = FILE_EXP9 + "plot_max_avg_lb_" + graph + ".png"
        plotPrefAvgMaxLb(FILE_EXP9_ALL,
                         "Experience 9 - Max avg lower bound - " + graph,
                         "Max avg dist lb", "c2", "c2",
                         graph, save_filename)


def plotExp10(metrics, graphs):
    """

    """
    for graph in graphs:
        for metric in metrics:
            save_filename = FILE_EXP10 + "plot_" + metric + "_" + graph + ".png"
            plotPrefExpResult(FILE_EXP10_ALL, "Experience 10 - prefs - " + metric + " - " + graph,
                              metrics[metric], "c2", "c2", metric,
                              graph, save_filename)

        save_filename = FILE_EXP10 + "plot_travelTypes_" + graph + ".png"
        plotModalitiesLines(FILE_EXP10_ALL, "Experience 10 - Travel types - " + graph,
                            "Travel types frequency", "c2", graph,
                            ["Villo", "fromStation", "toStation", "car"],
                            "Dijkstra", "c2", save_filename)

        # plot max avg lb
        save_filename = FILE_EXP10 + "plot_max_avg_lb_" + graph + ".png"
        plotPrefAvgMaxLb(FILE_EXP10_ALL,
                         "Experience 10 - Max avg lower bound - " + graph,
                         "Max avg dist lb", "c2", "c2",
                         graph, save_filename)


# ===============================================================

def main():
    metrics = {"avg_CT": "avg CT (sec.)",
               "avg_rel": "avg nb rel edges",
               "avg_SS": "avg search space size"}

    improvements = {"avg_CT": "Speedup (CT)",
                    "avg_rel": "avg relaxed edges improvement",
                    "avg_SS": "avg search space size improvement"}

    graphs = [GRAPH_1_NAME, GRAPH_2_NAME, GRAPH_3_NAME, GRAPH_4_NAME, GRAPH_5_NAME, GRAPH_6_NAME]

    plotExp1(metrics)
    plotExp2(metrics)
    plotExp3(metrics)
    plotExp4(metrics)
    plotExp5(metrics, improvements)
    plotExp6()
    plotExp7(metrics, improvements, [GRAPH_1_NAME])
    plotExp8(metrics)
    plotExp9(metrics, [GRAPH_1_NAME])
    plotExp10(metrics, [GRAPH_1_NAME])


if __name__ == "__main__":
    main()
