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
#import numba as nb
import numpy as np

from typing import List, Union

import whisk

#@nb.njit
def generate_data(colours: Union[str, List[str]],
                  shapes: Union[str, List[str]],
                  size: int = 1000):

    if type(colours) == str: colours = [colours]
    if type(shapes) == str: shapes = [shapes]

    data = {}

    data["colour"] = np.random.choice(colours, size=size)
    data["shape"] = np.random.choice(shapes, size=size)

    return ak.Array(data)

def test_recipe():
    categories = {
        "colour" : ["red", "yellow", "green", "blue"],
        "shape" : ["triangle", "rectangle", "square"],
    }
    data = generate_data(*categories.values())
    recipe = whisk.recipe(data, categories)
    
    total = len(data)#, axis=None)
    print(total)

    print(f"{recipe['red']:.4f} +/- {np.sqrt(recipe['red'] / total):.4f}")
    print(f"{recipe['triangle']:.4f} +/- {np.sqrt(recipe['triangle'] / total):.4f}")
    print(f"{recipe['red', 'triangle']:.4f} +/- {np.sqrt(recipe['red', 'triangle'] / total):.4f}")
    #assert rec["red"] == rdf.Filter('colour == "red"').Count().GetValue() / total
    #assert rec["triangle"] == rdf.Filter('shape == "triangle"').Count().GetValue() / total
    #assert rec["red", "triangle"] == rdf.Filter('colour == "red" && shape == "triangle"').Count().GetValue() / total
    #assert rec["triangle", "red"] == rdf.Filter('colour == "red" && shape == "triangle"').Count().GetValue() / total
    #assert rec["blue", "triangle"] == rdf.Filter('colour == "blue" && shape == "triangle"').Count().GetValue() / total
    #assert rec["square", "red"] == rdf.Filter('colour == "red" && shape == "shape"').Count().GetValue() / total


"""
def dummy(rec):
    test_indices = (["red", "triangle"],
                    ["triangle", "red"],
                    ["blue", "triangle"],
                    ["square", "red"])
    print()
    for test_index in test_indices:
        # [[lst[i] for i in pattern] for lst in a]
        count = [[rec[i] for i in test_indices]]
        print(f"{test_index}: {count}")
"""