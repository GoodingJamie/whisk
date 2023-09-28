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

from ROOT import RDataFrame
from ROOT.Numba import Declare
import whisk



# To-do:
# - Fix instability in generated sample


def generate_rdataframe(categories):

    rdf = RDataFrame(1000)
    
    colours = ["red", "yellow", "green", "blue"]
    rdf = rdf.Define("colour_idx", f"std::floor(gRandom->Rndm() * {len(colours)})")
    rdf = rdf.Define("colour",
                     f"""
                         std::vector<std::string> colours = {{"{'","'.join(colours)}"}};
                         return colours[colour_idx];
                     """)
    
    shapes = ["triangle", "rectangle", "square"]
    rdf = rdf.Define("shape_idx", f"std::floor(gRandom->Rndm() * {len(shapes)})")
    rdf = rdf.Define("shape",
                     f"""
                         std::vector<std::string> shapes = {{"{'","'.join(shapes)}"}};
                         return shapes[shape_idx];
                     """)

    return rdf




def test_recipe():
    categories = {
        "colour" : ["red", "yellow", "green", "blue"],
        "shape" : ["triangle", "rectangle", "square"],
    }
    rdf = generate_rdataframe(categories)
    rec = whisk.recipe(rdf, categories)
    
    total = rdf.Count().GetValue()

    print(rec["red"])
    print(rec["triangle"])
    print(rec["red", "triangle"])
    #assert rec["red"] == rdf.Filter('colour == "red"').Count().GetValue() / total
    #assert rec["triangle"] == rdf.Filter('shape == "triangle"').Count().GetValue() / total
    #assert rec["red", "triangle"] == rdf.Filter('colour == "red" && shape == "triangle"').Count().GetValue() / total
    #assert rec["triangle", "red"] == rdf.Filter('colour == "red" && shape == "triangle"').Count().GetValue() / total
    #assert rec["blue", "triangle"] == rdf.Filter('colour == "blue" && shape == "triangle"').Count().GetValue() / total
    #assert rec["square", "red"] == rdf.Filter('colour == "red" && shape == "shape"').Count().GetValue() / total
    
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