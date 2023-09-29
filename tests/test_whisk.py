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

from itertools import product as iterprod
from ROOT import RDataFrame
from ROOT.Numba import Declare
from typing import List, Union

import whisk


# To-do:
# - Fix instability in generated sample


def generate_rdataframe(colours: Union[str, List[str]],
                        shapes: Union[str, List[str]],
                        size: int = 1000):

    rdf = RDataFrame(size)
    
    rdf = rdf.Define("colour_idx", f"std::floor(gRandom->Rndm() * {len(colours)})")
    rdf = rdf.Define("colour",
                     f"""
                         std::vector<std::string> colours = {{"{'","'.join(colours)}"}};
                         return colours[colour_idx];
                     """)

    rdf = rdf.Define("shape_idx", f"std::floor(gRandom->Rndm() * {len(shapes)})")
    rdf = rdf.Define("shape",
                     f"""
                         std::vector<std::string> shapes = {{"{'","'.join(shapes)}"}};
                         return shapes[shape_idx];
                     """)

    return rdf


def test_whisk():
    ref_categories = {
        "colour" : ["red", "red", "red", "yellow", "yellow", "green", "blue"],
        "shape" : ["triangle", "triangle", "rectangle", "square"],
    }
    ref_rdf = generate_rdataframe(ref_categories["colour"], ref_categories["shape"], size = 1000)

    raw_categories = {
        "colour" : ["red", "yellow", "green", "blue"],
        "shape" : ["triangle", "rectangle", "square"],
    }
    
    raw_rdfs = {}
    for (colour, shape) in iterprod(*raw_categories.values()):
        raw_rdfs[(colour,shape)] = generate_rdataframe(colour, shape, size=10000)
    print(raw_rdfs["red", "triangle"])
    print(raw_rdfs["red", "triangle"].Count().GetValue())
    whisked_rdf = whisk.whisk(ref_rdf, raw_rdfs, raw_categories)
    print(whisked_rdf.Count().GetValue())
    print(whisked_rdf["red", "triangle"].Count().GetValue())
