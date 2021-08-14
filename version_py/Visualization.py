#!/usr/bin/env python
# -*- coding: utf-8 -*-


import csv
import math

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
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

    m = 0
    for p in categories:
        x, y = [], []
        for g in kept_graphs:
            graph = GRAPHS[g]
            x.append(stats[graph]["nb_nodes"])
            y.append(stats[graph]["stats"][p][ymetric])

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=p)
        plt.plot(x, y)
        m += 1

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotImprovementsResult(filename, title, categories, ylabel, xlabel, ymetric, kept_graphs, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for p in categories:
        x, y = [], []
        for g in kept_graphs:
            graph = GRAPHS[g]
            x.append(stats[graph]["nb_nodes"])
            avg_metric_dijkstra = stats[graph]["stats"]["Dijkstra"][ymetric]
            improv = avg_metric_dijkstra / stats[graph]["stats"][p][ymetric]
            y.append(improv)

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=p)
        plt.plot(x, y)
        m += 1

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

    plt.plot(x, y, marker="p")

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotExp7Result(filename, title, ylabel, xlabel, ymetric, algo, graph, save_filename):
    """
    For each speed, plot the ymetrics with regards to the number of added edges
    """
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for s in SPEEDS:
        x, y = ADDED_EDGES, []
        for ae in ADDED_EDGES:
            y.append(stats[graph][str(s)][str(ae)][algo][ymetric])

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=SPEEDS_LABELS[s])
        plt.plot(x, y)
        plt.xticks(x, x)
        m += 1

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
    m = 0
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
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=SPEEDS_LABELS[s])
        plt.plot(x, y)
        plt.xticks(x, x)
        m += 1

    # show
    show("upper right", title, ylabel, xlabel, save_filename)


def plotExp7ModalitiesBars(filename, title, ylabel, xlabel, graph, categories, algo, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for mod in categories:
        x = [str(s) for s in SPEEDS]
        y = []
        for s in SPEEDS:
            avg_percentage = 0
            for ae in ADDED_EDGES:
                travel_types = stats[graph][str(s)][str(ae)][algo]["avg_travel_types"]
                tot = sum(travel_types.values())
                if mod in travel_types:
                    percentage = (travel_types[mod] * 100) / tot
                    avg_percentage += percentage / len(ADDED_EDGES)

            y.append(avg_percentage)

        # scatter points
        plt.bar(x, y, width=0.2)
        m += 1

    # show
    # plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=4)
    plt.legend(categories, loc="center right")
    show(None, title, ylabel, xlabel, save_filename)


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

    plt.plot(x, y, marker="p")

    # show
    show("upper left", title, ylabel, xlabel, save_filename)


def plotMaxAvgLbExp7(filename, title, ylabel, xlabel, graph, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for s in SPEEDS:
        x, y = ADDED_EDGES, []
        for ae in ADDED_EDGES:
            y.append(stats[graph][str(s)][str(ae)]["ALT"]["max_avg_lb"])

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=SPEEDS_LABELS[s])
        plt.plot(x, y)
        plt.xticks(x, x)
        m += 1

    # show
    show("upper right", title, ylabel, xlabel, save_filename)


def plotModalitiesLines(filename, title, ylabel, xlabel, graph, categories, algo, xmetric, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for t in categories:
        x, y = [], []
        for k in stats[graph]["stats"]:
            x.append(stats[graph]["stats"][k][xmetric])
            if t not in stats[graph]["stats"][k][algo]["avg_travel_types"]:
                y.append(0)
            else:
                y.append(stats[graph]["stats"][k][algo]["avg_travel_types"][t])

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=t)
        plt.plot(x, y)
        plt.xticks(x, x)
        m += 1

    # show
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=4)
    show(None, "", ylabel, xlabel, save_filename)


def plotModalitiesLines3D(filename, title, ylabel, xlabel, categories, modalities, algo, save_filename):
    stats = getJsonData(filename)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = {"Villo": "blue", "toStation": "orange", "fromStation": "brown", "car": "red"}
    markers = {"Villo": "s", "toStation": "*", "fromStation": "v", "car": "d"}
    v = 0
    for c in categories:
        xmetric = stats[c]["fixed"]
        for m in modalities:
            x, y = [], []
            for k in stats[c]["stats"]:
                x.append(stats[c]["stats"][k][xmetric])
                if m not in stats[c]["stats"][k][algo]["avg_travel_types"]:
                    y.append(0)
                else:
                    y.append(stats[c]["stats"][k][algo]["avg_travel_types"][m])
            z = [v for _ in range(len(x))]

            ax.scatter(xs=x, ys=y, zs=z, marker=markers[m], c=colors[m])

        v += 1

    ax.set_zlabel("Graphs")
    ax.legend(["Villo", "toStation", "fromStation", "car"], loc="best")
    show(None, title, ylabel, xlabel, save_filename)


def plotModalitiesPieChart(filename, title, graph, algo, categories, save_filename):
    """
    code from : https://www.pythonprogramming.in/how-to-pie-chart-with-different-color-themes-in-matplotlib.html
    # 10 = yellow,
    # 5 = lightblue,
    # 13 = red,
    # 7 = lightgreen
    # 4 = blue
    """
    stats = getJsonData(filename)

    # pie chart
    # categories = list(stats[graph]["stats"][algo]["avg_travel_types"].keys())
    sizes = []
    for cat in categories:
        sizes.append(stats[graph]["stats"][algo]["avg_travel_types"][cat])

    # sizes = [11, 3, 5, 6]
    labels = ["{0} %s".format(cat) % i for cat, i in zip(sizes, categories)]

    fig1, ax1 = plt.subplots(figsize=(5, 5))
    fig1.subplots_adjust(0.3, 0, 1, 1)

    theme = plt.get_cmap('jet')

    c = [theme(1. * i / 15) for i in range(15)]
    ax1.set_prop_cycle("color", [c[7], c[13], c[10], c[4]])

    _, _ = ax1.pie(sizes, startangle=90, radius=1800)

    ax1.axis('equal')

    total = sum(sizes)
    plt.legend(
        loc='upper left',
        labels=['%s, %1.1f%%' % (l, (float(s) / total) * 100)
                for l, s in zip(labels, sizes)],
        prop={'size': 11},
        bbox_to_anchor=(0.0, 1),
        bbox_transform=fig1.transFigure
    )

    plt.title(title)
    plt.tight_layout(pad=0.3)
    plt.savefig(save_filename, dpi=100)
    plt.show()


def plotPrefExpResult(filename, title, ylabel, xlabel, ymetric, categories, save_filename):
    stats = getJsonData(filename)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    m = 0
    for c in categories:
        xmetric = stats[c]["fixed"]
        x, y = [], []
        for k in stats[c]["stats"]:
            x.append(stats[c]["stats"][k][xmetric])
            y.append(stats[c]["stats"][k]["ALT"][ymetric])

        # scatter points
        ax1.scatter(x, y, s=MARKER_SIZE, marker=MARKERS[m], label=c)
        plt.plot(x, y)
        plt.xticks(x, x)
        m += 1

    show("upper left", title, ylabel, xlabel, save_filename)


def plotPrefAvgMaxLb(filename, title, ylabel, xlabel, xmetric, graph, save_filename):
    stats = getJsonData(filename)

    x, y = [], []
    for k in stats[graph]["stats"]:
        x.append(stats[graph]["stats"][k][xmetric])
        y.append(stats[graph]["stats"][k]["ALT"]["max_avg_lb"])

    plt.plot(x, y, marker="d")
    plt.xticks(x, x)

    # show
    show(None, title, ylabel, xlabel, save_filename)


def plotPrefModalitiesBars(filename, title, ylabel, xlabel, category, modalities, algo, save_filename):
    stats = getJsonData(filename)

    cols = ["cyan", "g", "r", "b"]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    data = []
    for m in modalities:
        subdata = []
        for k in stats[category]["stats"]:
            percentage = 0
            travel_types = stats[category]["stats"][k][algo]["avg_travel_types"]
            tot = sum(travel_types.values())
            if m in travel_types:
                percentage = (travel_types[m] * 100) / tot
            subdata.append(percentage)
        data.append(subdata)

    # show multiple bars
    c = 0
    shift = 0.00
    for d in data:
        x = np.arange(len(d))
        ax.bar(x + shift, d, color=cols[c], width=0.25)
        shift += 0.25
        c += 1

    # show
    ax.legend(labels=modalities)
    # plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", mode="expand", ncol=4)
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
    save_filename = getFileExpPath(5, "plot_prepro_CT_{0}.png".format(graphs))
    plotPreprocessingResult(getFileExpPath(5, "exp5_all_stats.json"),
                            "Exp 5 - Preprocessing - k={0}, {1}".format(NB_LANDMARKS, LANDMARK_SELECTION),
                            "computation time (sec.)", "|V|",
                            kept_graphs, save_filename)

    # preprocessing time - |V| with [random, farthest, planar]
    categories = ["random", "farthest", "planar"]
    save_filename = getFileExpPath(5, "plot_prepro_CT_selections_{0}.png".format(graphs))
    plotBenchmarkResult(getFileExpPath(3, "exp3_all_stats.json"),
                        "Exp 5 - Preprocessing - random, farthest, planar",
                        categories, "preprocessing time (sec.)",
                        "|V|", "lm_dists_CT", kept_graphs, save_filename)

    # preprocessing time - |V| with k=[1,2,4,8,16,32]
    categories = ["1", "2", "4", "8", "16", "32"]
    save_filename = getFileExpPath(5, "plot_prepro_CT_k_{0}.png".format(graphs))
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

        # plot modalities lines :
        save_filename = getFileExpPath(7, "plot_modalities_" + graph + ".png")
        plotExp7ModalitiesBars(getFileExpPath(7, "exp7_all_stats.json"),
                               "Exp 7 -Modalities repartition - " + graph,
                               "Percentage", "Speeds",
                               graph, FOOT_PUBLIC_TRANSPORT,
                               "ALT", save_filename)


# ====================================================


def plotExp8(metrics, improvements, kept_graphs):
    """
    Multi-modal station-based - Dijkstra & ALT
    """
    categories = ["Dijkstra", "ALT"]

    # plot standard metrics
    graphs = ",".join([str(g + 1) for g in KEPT_GRAPHS])
    for metric in metrics:
        save_filename = getFileExpPath(8, "plot_{0}_{1}.png".format(metric, graphs))
        plotBenchmarkResult(getFileExpPath(8, "exp8_all_stats.json"),
                            "Exp 8 - {0} - graphs : {1}".format(metric, graphs),
                            categories, metrics[metric], "|V|",
                            metric, kept_graphs, save_filename)

    save_filename = getFileExpPath(8, "plot_prepro_{0}.png".format(graphs))
    plotBenchmarkResult(getFileExpPath(8, "exp8_all_stats.json"),
                        "Exp 8 - Preprocessing - graphs : {0}".format(graphs),
                        ["ALT"], "Preprocessing time (sec.)", "|V|",
                        "lm_dists_CT", kept_graphs, save_filename)

    for metric in improvements:
        save_filename = getFileExpPath(8, "plot_improv_{0}_{1}.png".format(metric, graphs))
        plotImprovementsResult(getFileExpPath(8, "exp8_all_stats.json"),
                               "Exp 8 - Improvement - " + metric,
                               ["ALT"], improvements[metric], "|V|",
                               metric, kept_graphs, save_filename)

    # plot : modality1 - modality2 for Dijkstra & ALT
    for g in kept_graphs:
        save_filename = getFileExpPath(8, "plot_piechart_{0}.png".format(str(g + 1)))
        plotModalitiesPieChart(getFileExpPath(8, "exp8_all_stats.json"),
                               "Exp 8 - Graph " + str(g + 1),
                               GRAPHS[g], "ALT", FOOT_VILLO, save_filename)


# ====================================================


def plotExp9(metrics, kept_graphs):
    """
    station-based multimodal network
    User pref - preprocessing c1=c2=1, then vary c1/c2 during query
    """
    graphs = ",".join([str(g + 1) for g in KEPT_GRAPHS])
    kept_graphs = [GRAPHS[g] for g in kept_graphs]
    for metric in metrics:
        save_filename = getFileExpPath(9, "plot_{0}_{1}.png".format(metric, graphs))
        plotPrefExpResult(getFileExpPath(9, "exp9_all_stats.json"),
                          "Exp 9 - prefs - " + metric + " - Graphs : " + graphs,
                          metrics[metric], "c2", metric,
                          kept_graphs, save_filename)

    save_filename = getFileExpPath(9, "plot_prepro_{0}.png".format(graphs))
    plotPrefExpResult(getFileExpPath(9, "exp9_all_stats.json"),
                      "Exp 9 - Preprocessing - Graphs: " + graphs,
                      "Preprocessing time (sec.)", "c2", "lm_dists_CT",
                      kept_graphs, save_filename)

    save_filename = getFileExpPath(9, "plot_max_avg_lb_{0}.png".format(graphs))
    plotPrefExpResult(getFileExpPath(9, "exp9_all_stats.json"),
                      "Exp 9 - Max avg lower bound - Graphs: " + graphs,
                      "Max avg dist lb", "c2", "max_avg_lb",
                      kept_graphs, save_filename)

    # for graph in kept_graphs:
    #     save_filename = getFileExpPath(9, "plot_modalities_{0}.png".format(graphs))
    #     plotModalitiesLines(getFileExpPath(9, "exp9_all_stats.json"),
    #                         "Exp 9 - Travel types - " + str(graph + 1),
    #                         "Travel types frequency", "c2", GRAPHS[graph],
    #                         CAR_VILLO, "ALT", "c2", save_filename)

    save_filename = getFileExpPath(9, "plot_modalities_{0}.png".format(graphs))
    plotModalitiesLines3D(getFileExpPath(9, "exp9_all_stats.json"),
                          "Exp 9 - Travel types - Graphs: " + graphs,
                          "Travel types frequency", "c2", kept_graphs,
                          CAR_VILLO, "ALT", save_filename)

    for graph in kept_graphs:
        save_filename = getFileExpPath(9, "plot_modalitiesBars_{0}.png".format(graph))
        plotPrefModalitiesBars(getFileExpPath(9, "exp9_all_stats.json"),
                               "Exp 9 - Modalities repartition - bars - Graph " + graph,
                               "Percentage", "c2", graph,
                               CAR_VILLO, "ALT", save_filename)


# ====================================================


def plotExp10(metrics, graph):
    """
    station-based multimodal network
    User pref - vary c1 and c2 and using worst case users
    """
    for metric in metrics:
        save_filename = getFileExpPath(10, "plot_{0}_{1}.png".format(metric, str(graph+1)))
        plotPrefExpResult(getFileExpPath(10, "exp10_all_stats.json"),
                          "Exp 10 - prefs - " + metric + " - Graph : " + str(graph+1),
                          metrics[metric], "c", metric,
                          PREF_COMBI, save_filename)

    save_filename = getFileExpPath(10, "plot_prepro_{0}.png".format(str(graph+1)))
    plotPrefExpResult(getFileExpPath(10, "exp10_all_stats.json"),
                      "Exp 10 - Preprocessing - Graph: " + str(graph+1),
                      "Preprocessing time (sec.)", "c", "lm_dists_CT",
                      PREF_COMBI, save_filename)

    save_filename = getFileExpPath(10, "plot_max_avg_lb_{0}.png".format(str(graph+1)))
    plotPrefExpResult(getFileExpPath(10, "exp10_all_stats.json"),
                      "Exp 10 - Max avg lower bound - Graph: " + str(graph+1),
                      "Max avg dist lb", "c", "max_avg_lb",
                      PREF_COMBI, save_filename)

    save_filename = getFileExpPath(10, "plot_modalities_{0}.png".format(str(graph+1)))
    plotModalitiesLines3D(getFileExpPath(10, "exp10_all_stats.json"),
                          "Exp 10 - Travel types - Graph: " + str(graph+1),
                          "Travel types frequency", "c2", PREF_COMBI,
                          CAR_VILLO, "ALT", save_filename)

    for pref_combi in PREF_COMBI:
        save_filename = getFileExpPath(10, "plot_modalitiesBars_{0}_{1}.png".format(str(graph+1), pref_combi))
        plotPrefModalitiesBars(getFileExpPath(10, "exp10_all_stats.json"),
                               "Exp 10 - Modalities repartition - bars - Graph " + str(graph+1),
                               "Percentage", "c", pref_combi,
                               CAR_VILLO, "ALT", save_filename)


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
        plotExp8(metrics, improvements, KEPT_GRAPHS)
    if exp == 9 or exp == -1:
        plotExp9(metrics, KEPT_GRAPHS)
    if exp == 10 or exp == -1:
        plotExp10(metrics, EXP10_GRAPH)


# ==============================================================


def testPlot3D():
    np.random.seed(42)

    ages = np.random.randint(low=8, high=30, size=35)
    heights = np.random.randint(130, 195, 35)
    weights = np.random.randint(30, 160, 35)
    gender_labels = np.random.choice([0, 1], 35)  # 0 for male, 1 for female

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(xs=heights, ys=weights, zs=ages, c=gender_labels)

    ax.set_title("Age-wise body weight-height distribution")
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Weight (kg)")
    ax.set_zlabel("Age (years)")

    plt.show()


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


def testMultipleBars():
    data = [[30, 25, 50, 20, 2, 8],
            [40, 23, 51, 17, 5, 9],
            [35, 22, 45, 19, 7, 7]]
    X = np.arange(6)
    print(X)
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar(X + 0.00, data[0], color='b', width=0.25)
    ax.bar(X + 0.25, data[1], color='g', width=0.25)
    ax.bar(X + 0.50, data[2], color='r', width=0.25)

    ax.set_xticks(X, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'))
    plt.show()

def testSingleBar():
    fig = plt.figure()
    ax=fig.add_subplot(111)
    langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    students = [23, 17, 35, 29, 12]
    ax.bar(langs, students)
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
    # testPlot3D()
    # testMultipleBars()
    # testSingleBar()

if __name__ == "__main__":
    main()
