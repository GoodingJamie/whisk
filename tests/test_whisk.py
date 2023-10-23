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
#import numba as nb
import numpy as np

from typing import List, Union

import whisk



# To-do:
# - Fix instability in generated sample

def generate_data(colours: Union[str, List[str]],
                  shapes: Union[str, List[str]],
                  size: int = 1000):

    if type(colours) == str: colours = [colours]
    if type(shapes) == str: shapes = [shapes]

    data = {}

    data["colour"] = np.random.choice(colours, size=size)
    data["shape"] = np.random.choice(shapes, size=size)

    return ak.Array(data)

def test_whisk():
    ref_categories = {
        "colour" : ["red", "red", "red", "yellow", "yellow", "green", "blue"],
        "shape" : ["triangle", "triangle", "rectangle", "square"],
    }
    ref_data = generate_data(ref_categories["colour"], ref_categories["shape"], size = 1000)

    raw_categories = {
        "colour" : ["red", "yellow", "green", "blue"],
        "shape" : ["triangle", "rectangle", "square"],
    }
    
    raw_data = {}
    for (colour, shape) in it.product(*raw_categories.values()):
        rd = generate_data(colour, shape, size=10000)
        raw_data[(colour,shape)] = rd

    print(len(raw_data["red", "triangle"]))
    whisked_data = whisk.whisk(ref_data, raw_data, raw_categories)
    print(len(whisked_data[whisked_data["colour"] == "red"]))
    print(len(whisked_data[whisked_data["shape"] == "rectangle"]))
    print(len(whisked_data[np.logical_and(whisked_data["colour"] == "red", whisked_data["shape"] == "rectangle")]))