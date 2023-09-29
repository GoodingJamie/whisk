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

import os

from ROOT import RDataFrame
from tempfile import TemporaryDirectory
from typing import Dict, List, Union

from ._recipe import recipe

def whisk(
    reference_data: RDataFrame,
    combining_data: Dict[Union[str, List[str]], RDataFrame],
    categories: Union[List[str], Dict[str, str]],
):

    reference_recipe = recipe(reference_data, categories)
    cdfs = []
    with TemporaryDirectory() as tmpdir:
        for n, (key, cdf) in enumerate(combining_data.items()):
            cdf_path = os.path.join(
                tmpdir,
                f"combining_dataframe{n}.root"
            )
            cdf.Snapshot("temp_tree", cdf_path)
            cdfs += [cdf_path]
        whisked_data = RDataFrame("temp_tree", cdfs)

    return whisked_data

def _calculate_proportions(
    data: RDataFrame,
    categories: Union[List[str], Dict[str, str]]
):
    proportions = {}
    if type(categories) == list:
        return

    for category, values in categories:
        for value in values:
            proportions.extend({
                category:  {
                    "total" : data.Filter(f"{category} == {value}").Count().getValue()
                }
            })

    return

    {
        "red" : {
            "total" : 1,
            "square" : {"total": 1}
        }
    }