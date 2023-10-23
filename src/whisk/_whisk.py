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
import numba as nb
import numpy as np
import os
from typing import Dict, List, Union

from ._recipe import recipe

def whisk(
    reference_data,
    combining_data,#: Dict[Union[str, List[str]], ],
    categories: Union[List[str], Dict[str, str]],
):

    reference_recipe = recipe(reference_data, categories)
    combine_data = (data[np.random.rand(len(data)) < reference_recipe[categories] / reference_recipe.maximum] for categories, data in combining_data.items())

    return ak.concatenate(combine_data)