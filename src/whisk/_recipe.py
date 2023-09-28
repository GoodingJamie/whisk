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

def recipe(
    data: RDataFrame,
    categories: Union[List[str], Dict[str, str]],
    totals: bool = False,

):
    proportions = defaultdict(dict)
    keys = iterprod(*categories.values())
    for key in keys:
        filt = _parse_filter(categories, key)
        assert filt != "", "Filter not parsed correctly."
        count = data.Filter(filt).Count().GetValue()
        value = count if totals else count / data.Count().GetValue()
        for perm_key in permutations(key):
            proportions[perm_key] = value

    return proportions

def _parse_filter(
    categories: Dict[str, str],
    key : List[str]
):
    assert len(categories.keys()) == len(key), "Category list and possible keys are different length"
    
    #assert all([sub_key in category for category, sub_key in zip(categories.items(), key)]), "Category list and possible keys do not match"
    filters = []
    for n, (category, sub_key) in enumerate(zip(categories.items(), key)):
        filters += [f'{category[0]} == "{sub_key}"']

    return " && ".join(filters)


