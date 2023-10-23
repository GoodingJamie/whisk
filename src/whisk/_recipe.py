###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import awkward as ak
import itertools as it
import numba as nb
import numpy as np
import os

from typing import Dict, List, Union

# Categories should look like
#   []
#   

class recipe:
    def __init__(
        self,
        data,
        categories: Union[List[str], Dict[str, str]],
        totals: bool = False
    ):
        self.data = data
        self.categories = categories
        self.default_to_fractions = not(totals)
        self.total_events = len(data)
        self.maximum = 0

        self._recipe()

    def __getitem__(
        self,
        key: Union[str, List[str]]
    ):

        values = []
        if type(key) == str:
            values = [self.proportions[proportions_key] for proportions_key in self.proportions.keys() if key in proportions_key]
        else:
            for proportions_key in self.proportions.keys():
                if all([each_key in proportions_key for each_key in key]):
                    values += [self.proportions[proportions_key]]

        return sum(values)

    #def max(
    #    self
    #):
    #    return self.maximum

    def _filter(
        self,
        key : List[str]
    ):
        assert len(self.categories.keys()) == len(key), "Category list and possible keys are different length"
        return np.logical_and.reduce([self.data[category[0]] == sub_key for category, sub_key in zip(self.categories.items(), key)])

    def _recipe(self):

        self.proportions = {}
        keys = it.product(*self.categories.values())
        for key in keys:
            filt = self._filter(key)
            count = len(self.data[filt])
            value = count / self.total_events if self.default_to_fractions else count
            self.proportions[key] = value
            if value > self.maximum: self.maximum = value


    def _convert_to_fractions(self):

        for key in self.proportions.keys():
            self.proportions[key] /= self.total_events

    def default_to_fractions(
        self,
        value: bool = True
    ):

        self.default_to_fractions = value
        _convert_to_fractions()


    def _convert_to_totals(self):

        for key in self.proportions.keys():
            self.proportions[key] *= self.total_events

    def default_to_totals(
        self,
        value: bool = True
    ):

        self.default_to_fractions = not(value)
        _convert_to_totals()