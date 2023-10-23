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

def table(
    data,
    categories: Union[List[str], Dict[str, str]],
    absolute,
    output: bool = False,
    totals: bool = False,

):
    if type(categories) == list:
        return
    spacing = 12
    combinations = prod([len(category) for category in categories.values()])
    header = ""
    previous_categories = 1
    column_width = combinations

    labels = list(categories.keys())
    values_sets = list(categories.values())
    print(labels)
    print(values_sets)



    if readable:


        for n, (label, values) in enumerate(zip(labels, values_sets)):
            previous_category_count = len(values_sets[n-1]) if n-1 > 0 and n < len(values_sets) else 1
            next_category_count = len(values_sets[n+1]) if n+1 < len(values_sets) else 1
            combinations = int(combinations / next_category_count)
            header += f"{label : <{spacing * combinations * next_category_count}} | "
            column_width = spacing * combinations

            for _ in range(previous_category_count):
                for value in values:
                    header += f"{value : <{column_width}} | "

            #"catA | valA1   | valA2  | valA3"
            #"catB | valB1 VALB2    | valB2  | valB3"
            header += "\n"
            print(label)
        print(header)


        print(combinations)
        print('a')

        return True