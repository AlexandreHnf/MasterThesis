#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import matplotlib.pyplot as plt
from IO import *
import numpy as np


def show(legend, title, ylabel, xlabel, save_filename):
    if legend is not None:
        plt.legend()
        plt.legend(loc=legend)

    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    if xlabel == "|V|":
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        plt.gca().ticklabel_format(useMathText=True)
    if ylabel == "|V|":
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.gca().ticklabel_format(useMathText=True)

    plt.tight_layout(pad=0.3)
    plt.savefig(save_filename, dpi=100)
    plt.show()


def plotBenchmarkResult(filename, title, categories, ylabel, xlabel, ymetric, kept_graphs, save_filename):
    """
    ymetrics = computation time (QT) or
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
        for g in kept_graphs:
            graph = GRAPHS[g]
            x.append(stats[graph]["nb_nodes"])
            y.append(stats[graph]["stats"][p][ymetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotImprovementsResult(filename, title, categories, ylabel, xlabel, ymetric, kept_graphs, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for p in categories:
        x, y = [], []
        for g in kept_graphs:
            graph = GRAPHS[g]
            x.append(stats[graph]["nb_nodes"])
            avg_metric_dijkstra = stats[graph]["stats"]["Dijkstra"][ymetric]
            improv = avg_metric_dijkstra / stats[graph]["stats"][p][ymetric]
            y.append(improv)

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=p)
        plt.plot(x, y)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotPreprocessingResult(filename, title, ylabel, xlabel, kept_graphs, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for g in kept_graphs:
        graph = GRAPHS[g]
        x.append(stats[graph]["nb_nodes"])
        y.append(stats[graph]["stats"][2])

    plt.plot(x, y, marker="o")

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotAvgDegResult(filename, title, ylabel, xlabel, kept_graphs, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for g in kept_graphs:
        graph = GRAPHS[g]
        x.append(stats[graph]["nb_nodes"])
        y.append(stats[graph]["avg_deg"])

    plt.plot(x, y, marker="o")

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotExp7Result(filename, title, ylabel, xlabel, ymetric, algo, graph, save_filename):
    """
    For each speed, plot the ymetrics with regards to the number of added edges
    """
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in SPEEDS:
        x, y = ADDED_EDGES, []
        for ae in ADDED_EDGES:
            y.append(stats[graph][str(s)][str(ae)][algo][ymetric])

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper right", title, ylabel, xlabel, save_filename)


def plotImprovementsExp7(filename, title, ylabel, xlabel, ymetric, graph, save_filename):
    """
    Exp7 : Query time or search space or relaxed space improvement
    over the nb of added edges
    """
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in SPEEDS:
        x, y = ADDED_EDGES, []
        for ae in ADDED_EDGES:
            avg_metric_dijkstra = stats[graph][str(s)][str(ae)]["Dijkstra"][ymetric]
            avg_metric_alt = stats[graph][str(s)][str(ae)]["ALT"][ymetric]
            if avg_metric_alt == 0.0:
                # print(avg_metric_dijkstra, avg_metric_alt)
                avg_metric_alt = avg_metric_dijkstra / 10
            improv = round(avg_metric_dijkstra / avg_metric_alt, 6)
            y.append(improv)

        # scatter points
        ax1.scatter(x, y, s=10, marker="s", label=str(s) + "km/h")
        plt.plot(x, y)
        plt.xticks(x, x)

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotExp7AvgDegResult(filename, title, ylabel, xlabel, graph, save_filename):
    """
    Exp 7 : plot the avg node degree per nb of added edges
    """
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    x, y = ADDED_EDGES, []
    for ae in ADDED_EDGES:
        y.append(stats[graph][str(SPEEDS[0])][str(ae)]["avg_degree_after"])

    plt.plot(x, y, marker="o")

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotMaxAvgLbExp7(filename, title, ylabel, xlabel, graph, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for s in SPEEDS:
        x, y = ADDED_EDGES, []
        for ae in ADDED_EDGES:
            y.append(stats[graph][str(s)][str(ae)]["ALT"]["max_avg_lb"])

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
# ====================================================
# ====================================================

def plotExp1(metrics, kept_graphs):
    """
    priority queues : bin, fib, list
    avg QT - |V|
    avg rel - |V|
    avg SS - |V|
    """
    categories = ["bin", "fib", "list"]

    graphs = ",".join([str(g + 1) for g in kept_graphs])
    for metric in metrics:
        save_filename = getFileExpPath(1, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(1, "exp1_all_stats.json"),
                            "Exp 1 - Dijkstra - {0} - graphs : {1}".format(metric, graphs),
                            categories, metrics[metric], "|V|", metric,
                            kept_graphs, save_filename)


# ====================================================


def plotExp2(metrics, kept_graphs):
    """
    heuristics : euclidean, manhattan, octile
    avg QT - |V|
    avg rel - |V|
    avg SS - |V|
    """
    categories = ["euclidean", "manhattan", "octile"]

    graphs = ",".join([str(g + 1) for g in kept_graphs])
    for metric in metrics:
        save_filename = getFileExpPath(2, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(2, "exp2_all_stats.json"),
                            "Exp 2 - A* - {0} - graphs : {1}".format(metric, graphs),
                            categories, metrics[metric], "|V|", metric,
                            kept_graphs, save_filename)


# ====================================================


def plotExp3(metrics, kept_graphs):
    """
    landmark selections : random, farthest, planar
    avg QT - |V|
    avg rel - |V|
    avg SS - |V|
    """
    categories = ["random", "farthest", "planar"]

    graphs = ",".join([str(g + 1) for g in kept_graphs])
    for metric in metrics:
        save_filename = getFileExpPath(3, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(3, "exp3_all_stats.json"),
                            "Exp 3 - ALT - {0} - graphs : {1}".format(metric, graphs),
                            categories, metrics[metric], "|V|", metric,
                            kept_graphs, save_filename)


# ====================================================


def plotExp4(metrics, kept_graphs):
    """
    landmarks number : 1, 2, 4, 8, 16, 32
    avg QT - |V|
    avg rel - |V|
    avg SS - |V|
    """
    categories = ["1", "2", "4", "8", "16", "32"]

    graphs = ",".join([str(g + 1) for g in kept_graphs])
    for metric in metrics:
        save_filename = getFileExpPath(4, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(4, "exp4_all_stats.json"),
                            "Exp 4 - ALT - {0} - graphs : {1}".format(metric, graphs),
                            categories, metrics[metric], "|V|", metric,
                            kept_graphs, save_filename)


# ====================================================


def plotExp5(kept_graphs):
    """
    Single modal
    preprocessing time - |V|
    """
    graphs = ",".join([str(g + 1) for g in kept_graphs])
    # preprocessing time - |V| with k=16, planar
    save_filename = getFileExpPath(5, "plot_prepro_QT_{0}.png".format(graphs))
    plotPreprocessingResult(getFileExpPath(5, "exp5_all_stats.json"),
                            "Exp 5 - Preprocessing - k={0}, {1}".format(NB_LANDMARKS, LANDMARK_SELECTION),
                            "computation time (sec.)", "|V|",
                            kept_graphs, save_filename)

    # preprocessing time - |V| with [random, farthest, planar]
    categories = ["random", "farthest", "planar"]
    save_filename = getFileExpPath(5, "plot_prepro_QT_selections_{0}.png".format(graphs))
    plotBenchmarkResult(getFileExpPath(3, "exp3_all_stats.json"),
                        "Exp 5 - Preprocessing - random, farthest, planar",
                        categories, "preprocessing time (sec.)",
                        "|V|", "lm_dists_CT", kept_graphs, save_filename)

    # preprocessing time - |V| with k=[1,2,4,8,16,32]
    categories = ["1", "2", "4", "8", "16", "32"]
    save_filename = getFileExpPath(5, "plot_prepro_QT_k_{0}.png".format(graphs))
    plotBenchmarkResult(getFileExpPath(4, "exp4_all_stats.json"),
                        "Exp 5 - Preprocessing - k=[1,2,4,8,16,32]",
                        categories, "preprocessing time (sec.)",
                        "|V|", "lm_dists_CT", kept_graphs, save_filename)


# ====================================================


def plotExp6(metrics, improvements, kept_graphs):
    """
    Single modal algos : Dijkstra, A*, ALT, BidiDijkstra, BidiA*, BidiALT
    """
    # plot standard metrics
    categories = ["Dijkstra", "A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    graphs = ",".join([str(g + 1) for g in KEPT_GRAPHS])
    for metric in metrics:
        save_filename = getFileExpPath(6, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(6, "exp6_all_stats.json"),
                            "Exp 6 - Single-modal car networks - " + metric,
                            categories, metrics[metric], "|V|", metric,
                            kept_graphs, save_filename)

    # plot : |V| - improv (1 for speedup, 1 for rel, 1 for SS
    categories = ["A*", "ALT", "BidiDijkstra", "BidiAstar", "BidiALT"]

    for metric in improvements:
        save_filename = getFileExpPath(6, "plot_improv_{0}_{1}.png".format(metric, graphs))
        plotImprovementsResult(getFileExpPath(6, "exp6_all_stats.json"),
                               "Exp 6 - Improvement - " + metric,
                               categories, improvements[metric], "|V|",
                               metric, kept_graphs, save_filename)

    # plot : |V| - avg deg
    save_filename = getFileExpPath(6, "plot_avg_deg_{0}.png".format(graphs))
    plotAvgDegResult(getFileExpPath(6, "exp6_all_stats.json"),
                     "Exp 6 - avg degree",
                     "avg deg", "|V|", kept_graphs, save_filename)


# ====================================================


def plotExp7(metrics, improvements, graphs):
    """
    Multi-modal public transport network : Dijkstra and ALT
    """

    for graph in graphs:
        for metric in metrics:
            save_filename = getFileExpPath(7, "plot_" + metric + "_" + graph + ".png")
            plotExp7Result(getFileExpPath(7, "exp7_all_stats.json"),
                           "Exp 7 - Nb added edges - " + metric + " - " + graph,
                           metrics[metric], "|added edges|", metric,
                           "ALT", graph, save_filename)

        for metric in improvements:
            save_filename = getFileExpPath(7, "plot_improv_" + metric + "_" + graph + ".png")
            plotImprovementsExp7(getFileExpPath(7, "exp7_all_stats.json"),
                                 "Exp 7 - improvement - " + metric + " - " + graph,
                                 improvements[metric], "|added edges|", metric,
                                 graph, save_filename)

        save_filename = getFileExpPath(7, "plot_prepro_" + graph + ".png")
        plotExp7Result(getFileExpPath(7, "exp7_all_stats.json"),
                       "Exp 7 - preprocessing time - " + graph,
                       "preprocessing time (sec.)", "|added edges|", "lm_dists_CT",
                       "ALT", graph, save_filename)

        save_filename = getFileExpPath(7, "plot_avgDeg_" + graph + ".png")
        plotExp7AvgDegResult(getFileExpPath(7, "exp7_all_stats.json"),
                             "Exp 7 - avg deg - " + graph,
                             "avg deg after", "|added edges|",
                             graph, save_filename)

        # plot : mac avg lower bound - ALT
        save_filename = getFileExpPath(7, "plot_max_avg_lb_" + graph + ".png")
        plotMaxAvgLbExp7(getFileExpPath(7, "exp7_all_stats.json"),
                         "Exp 7 - Max average distance lower bound - " + graph,
                         "max avg lower bound", "|added edges|",
                         graph, save_filename)


# ====================================================


def plotExp8(metrics, kept_graphs):
    """

    """
    categories = ["Dijkstra", "ALT"]

    # plot standard metrics
    for metric in metrics:
        save_filename = getFileExpPath(8, "plot_" + metric + ".png")
        plotBenchmarkResult(getFileExpPath(8, "exp8_all_stats.json"),
                            "Exp 8 - Multi-modal station-based - " + metric,
                            categories, metrics[metric], "|V|",
                            metric, kept_graphs, save_filename)

    # plot : modality1 - modality2 for Dijkstra & ALT
    save_filename = getFileExpPath(8, "plot_piechart_Dijkstra.png")
    plotModalitiesPieChart(getFileExpPath(8, "exp8_all_stats.json"),
                           "Exp 8 - Pie chart modalities",
                           "1_ULB", "Dijkstra", save_filename)


# ====================================================


def plotExp9(metrics, graphs):
    """

    """
    for graph in graphs:
        for metric in metrics:
            save_filename = getFileExpPath(9, "plot_" + metric + "" + graph + ".png")
            plotPrefExpResult(getFileExpPath(9, "exp9_all_stats.json"),
                              "Exp 9 - prefs - " + metric + " - " + graph,
                              metrics[metric], "c2", "c2", metric,
                              graph, save_filename)

        save_filename = getFileExpPath(9, "plot_travelTypes_" + graph + ".png")
        plotModalitiesLines(getFileExpPath(9, "exp9_all_stats.json"),
                            "Exp 9 - Travel types - " + graph,
                            "Travel types frequency", "c2", graph,
                            ["Villo", "fromStation", "toStation", "car"],
                            "Dijkstra", "c2", save_filename)

        # plot max avg lb
        save_filename = getFileExpPath(9, "plot_max_avg_lb_" + graph + ".png")
        plotPrefAvgMaxLb(getFileExpPath(9, "exp9_all_stats.json"),
                         "Exp 9 - Max avg lower bound - " + graph,
                         "Max avg dist lb", "c2", "c2",
                         graph, save_filename)


# ====================================================


def plotExp10(metrics, graphs):
    """

    """
    for graph in graphs:
        for metric in metrics:
            save_filename = getFileExpPath(10, "plot_" + metric + "" + graph + ".png")
            plotPrefExpResult(getFileExpPath(10, "exp10_all_stats.json"),
                              "Exp 10 - prefs - " + metric + " - " + graph,
                              metrics[metric], "c2", "c2", metric,
                              graph, save_filename)

        save_filename = getFileExpPath(10, "plot_travelTypes_" + graph + ".png")
        plotModalitiesLines(getFileExpPath(10, "exp10_all_stats.json"),
                            "Exp 10 - Travel types - " + graph,
                            "Travel types frequency", "c2", graph,
                            ["Villo", "fromStation", "toStation", "car"],
                            "Dijkstra", "c2", save_filename)

        # plot max avg lb
        save_filename = getFileExpPath(10, "plot_max_avg_lb_" + graph + ".png")
        plotPrefAvgMaxLb(getFileExpPath(10, "exp10_all_stats.json"),
                         "Exp 10 - Max avg lower bound - " + graph,
                         "Max avg dist lb", "c2", "c2",
                         graph, save_filename)


# ===============================================================


def launchPlotExp(metrics, improvements, exp):
    """
    exp = -1 = run all plots
    """
    if exp == 1 or exp == -1:
        plotExp1(metrics, KEPT_GRAPHS)
    if exp == 2 or exp == -1:
        plotExp2(metrics, KEPT_GRAPHS)
    if exp == 3 or exp == -1:
        plotExp3(metrics, KEPT_GRAPHS)
    if exp == 4 or exp == -1:
        plotExp4(metrics, KEPT_GRAPHS)
    if exp == 5 or exp == -1:
        plotExp5(KEPT_GRAPHS)
    if exp == 6 or exp == -1:
        plotExp6(metrics, improvements, KEPT_GRAPHS)
    if exp == 7 or exp == -1:
        plotExp7(metrics, improvements, [GRAPH_BXL_CAP])
    if exp == 8 or exp == -1:
        plotExp8(metrics, [GRAPH_ULB, GRAPH_BXL])
    if exp == 9 or exp == -1:
        plotExp9(metrics, [GRAPH_ULB])
    if exp == 10 or exp == -1:
        plotExp10(metrics, [GRAPH_ULB])


# ===============================================================


def multipleXticks():
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twiny()

    a = np.cos(2 * np.pi * np.linspace(0, 1, 6))

    ax1.plot(range(6), a)
    ax2.plot(range(3), np.ones(3))  # Create a dummy plot
    ax2.cla()
    ax2.set_xticklabels(['zero', 'two', 'four'])
    plt.show()


def main():
    metrics = {"avg_QT": "avg QT (sec.)",
               "avg_RS": "avg relaxed space size",
               "avg_SS": "avg search space size"}

    improvements = {"avg_QT": "Speedup (QT)",
                    "avg_RS": "avg relaxed space size improvement",
                    "avg_SS": "avg search space size improvement"}

    launchPlotExp(metrics, improvements, EXPERIMENT_PLOT)
    # multipleXticks()


if __name__ == "__main__":
    main()
