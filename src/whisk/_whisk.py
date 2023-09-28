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

from typing import Dict, List, Union
from ROOT import RDataFrame

def whisk(
    data: RDataFrame,
    categories: Union[List[str], Dict[str, str]],
):

    return

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