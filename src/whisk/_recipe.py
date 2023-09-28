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

from collections import defaultdict
from itertools import product as iterprod
from itertools import permutations
from numpy import prod
from ROOT import RDataFrame
from typing import Dict, List, Union

from ._whisk import _calculate_proportions

# Categories should look like
#   []
#   

class recipe:
    def __init__(
        self,
        data: RDataFrame,
        categories: Union[List[str], Dict[str, str]],
        totals: bool = False
    ):
        self.data = data
        self.categories = categories
        self.default_to_fractions = not(totals)
        self.total_events = data.Count().GetValue()

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

    def _parse_filter(
        self,
        key : List[str]
    ):
        assert len(self.categories.keys()) == len(key), "Category list and possible keys are different length"

        filters = [f'{category[0]} == "{sub_key}"' for category, sub_key in zip(self.categories.items(), key)]

        assert len(filters) > 0, "Filter not parsed correctly."
        return " && ".join(filters)

    def _recipe(self):

        self.proportions = defaultdict(dict)
        keys = iterprod(*self.categories.values())
        for key in keys:
            filt = self._parse_filter(key)
            count = self.data.Filter(filt).Count().GetValue()
            value = count / self.data.Count().GetValue() if self.default_to_fractions else count
            self.proportions[key] = value


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