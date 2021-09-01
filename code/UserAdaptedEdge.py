#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Utils import haversine, getCarGasPrice
from Edge import Edge
from Constants import *


class UserAdaptedEdge(Edge):
    def __init__(self, extremity_node, travel_type, weight, length_km, speed, prefs):
        Edge.__init__(self, extremity_node, travel_type, weight, length_km, speed)

        self.p = prefs

    def getWeightedSum(self):
        """
        weighted sum = c1.x1 + c2.x2
        c1, c2 = preferences
        x1, x2 = metrics : travel time and gas price
        """
        if self.travel_type == "car":
            ws = self.p[0] * self.weight + self.p[1] * getCarGasPrice(self.length_km)
            # print("car : {0} . {1} + {2} . {3} = {4}".
            #       format(prefs[0], edge.getWeight(), prefs[1], getCarGasPrice(edge.getLengthKm()), ws))
            return ws

        elif self.travel_type == "toStation":
            # get the non-null preference
            ws = (self.p[0]+self.p[1]) * self.weight
            return ws

        elif self.travel_type == "fromStation":
            ws = (self.p[0]+self.p[1]) * self.weight
            return ws

        else:  # bike or foot
            ws = self.p[0] * self.weight + self.p[1] * PRICE_VILLO
            # print("{0} : {1} . {2} + {3} . {4} = {5}".
            #       format(edge.getTravelType(), prefs[0], edge.getWeight(), prefs[1], 0, ws))
            return ws

    def getWeight(self):
        return self.getWeightedSum()
