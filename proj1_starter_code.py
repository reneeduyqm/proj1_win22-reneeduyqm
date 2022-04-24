# -*- coding: utf-8 -*-

"""
Created on Sat Jul 17 16:09:52 2021
"""

# Your name: Renee Du
# Your student id: 97626101
# Your email: reneedu@umich.edu
# List who you have worked with on this project:

import io
import sys
import csv
import unittest
import os
from more_itertools import difference

from pandas import read_csv


def load_csv(file):
    '''
    Reads in the csv, removes the header (first row) and
    stores the data in the following nested dictionary format:
    {'region': {'ethnicity': count...}...}

    Parameters
    ----------
    file: string
        the file to read

    Returns
    -------
    data_dict: dict
        a nested dictionary
    '''
    source_dir = os.path.dirname(__file__) 
    full_path = os.path.join(source_dir, file)
    with open(full_path) as f:
        csv_file = csv.reader(f, delimiter=',')

        data_dict = {}
        count = 0
        for line in csv_file:
            if count == 0:
                headers = line
                count += 1
            else:  
                region = line[0] 
                data_dict[region] = {}

                headers = list(headers)
                for i in range(1, len(headers)):
                    data_dict[region][headers[i]] = int(line[i])
    return data_dict
    
   

def get_perc(data_dict):
    '''
    Calculate the percentage of each demographic using this
    formula: (demographic / total people) * 100

    Parameters
    ----------
    data_dict: dict
        Either AP or Census data

    Returns
    -------
    pct_dict: dict
        the dictionary that represents the data in terms of percentage share
        for each demographic for each region in the data set
    '''
  
    
    pct_dict = {} 
    for region in data_dict:
        pct_dict[region] = {}
        
        for demo in data_dict[region].keys():
            if demo != "Region Totals":
                num = data_dict[region][demo]
                total = data_dict[region]["Region Totals"]
                pct_dict[region][demo] = round(((num / total) * 100), 2)
    
    return pct_dict
    


def get_diff(ap_data, census_data):
    '''
    Takes the absolute value, rounded to 2 deicmal places,
    of the difference between each demographic's percentage
    value in census_data from ap_data

    Parameters
    ----------
    ap_data: dict
        AP data
    census_data: dict
        Census data

    Returns
    -------
    pct_dif_dict: dict
        the dictionary of the percent differences
    '''
    pct_dif_dict = {}
    for i in ap_data:
        new_pct_dif_dict = {}
        pct_dif_dict[i] = new_pct_dif_dict

        for demon in ap_data[i]:
            if demon in census_data[i]:
                value = abs((ap_data[i][demon]) - (census_data[i][demon]))
                new_pct_dif_dict[demon] = round(value, 2)

    return pct_dif_dict

def write_csv(data_dict, file_name):
    '''
    Writes the data to csv, adding the header as
    the first row

    Parameters
    ----------
    data_dict: dict
        dictionary with percent differences (pct_dif_dict)

    file_name: str
        the name of the file to write

    Returns
    -------
    None. (Doesn't return anything)
    '''
    fields  = ["Region"]
    rows = [] 
    n = 0
    while(n < 1):
        for i in data_dict.keys():
            for j in data_dict[i].keys():
                fields.append(j)
            n += 1

    for i in data_dict.keys():
        temp_row = []
        temp_row.append(i)
        for j in data_dict[i].keys():
            temp_row.append(data_dict[i][j])
        rows.append(temp_row)    

    with open(file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def max_min_mutate(data_dict, col_list):
    # Do not change the code in this function
    # edit this code
    '''
    Mutates the data to simplify sorting

    Parameters
    ----------
    data_dict : dict
        dictionary of data passed in. In this case, it's the
    col_list : list
        list of columns to mutate to.

    Returns
    -------
    demo_vals: dict
    '''
    # Do not change the code in this function
    demo_vals = {}
    for demo in col_list:
        demo_vals.setdefault(demo, {})
        for region in data_dict:
            demo_vals[demo].setdefault(region, data_dict[region][demo])
    return demo_vals

def min_max(data_dict):
    '''
    Finds the max and min regions and vals for each demographic,
    filling a dictionary in the following format:
    {"max": {"demographic": {"region": value...}...} "min": {demographic: {"region": value}...}...}

    Parameters
    ----------
    data_dict: dict
        the data_dictionary you're passing in. In this case, the mutated dict

    Returns
    -------
    min_max: dict
        a triple nested dict with the this basic format
        {"max":{demographic:{"region":value}}}
    '''
    min_max = {"max": {}, "min": {}}
    for demo in data_dict:
        min_max["max"][demo] = {}
        min_max["min"][demo] = {}
        for region in data_dict[demo]:
            min_max["max"][demo] = dict(sorted(data_dict[demo].items(), key = lambda x:x[1],reverse=True))
            min_max["min"][demo] = dict(sorted(data_dict[demo].items(), key = lambda x:x[1],reverse=False))
    return min_max
    
def nat_perc(data_dict, col_list):
    '''
    EXTRA CREDIT
    Uses either AP or Census data dictionaries
    to sum demographic values, calculating
    national demographic percentages from regional
    demographic percentages

    Parameters
    ----------
    data_dict: dict
        Either AP or Census data
    col_list: list
        list of the columns to loop through. helps filter out region totals cols

    Returns
    -------
    data_dict_totals: dict
        dictionary of the national demographic percentages

    '''
    data_dict = {}

def nat_diff(data_dict1, data_dict2):
    '''
    EXTRA CREDIT
    Calculates the difference between AP and Census
    data on a national scale

    Parameters
    ----------
    data_dict1: dict
        Either national AP or national Census data
    data_dict2: dict
        Either national AP or national Census data

    Returns
    nat_diff: dict
        the dictionary consisting of the demographic difference on natl. level
    '''
    nat_diff = {}

def main():
    # read in the data
    data_dict1 = load_csv('region_ap_data.csv')
    data_dict2 = load_csv('region_census_data.csv')
    # compute demographic percentages
    
    demographic_perc1 = get_perc(data_dict1)
    demographic_perc2 = get_perc(data_dict2)
    
    # computing the difference between test taker and state demographics
    pct_dif_dict = get_diff(demographic_perc1, demographic_perc2)
    

    # outputing the csv
    write_csv(pct_dif_dict, "HW5V1.csv")

    # creating a list from the keys of inner dict
    col_list = list(pct_dif_dict["west"].keys())

    # mutating the data
    mutated = max_min_mutate(pct_dif_dict, col_list)

    # calculating the max and mins
    min_max(mutated)

    # extra credit
    # providing a list of col vals to cycle through
    
    #col_list = census_data["west"].keys()

    # computing the national percentages
    '''
    ap_nat_perc = nat_perc(data_dict1, col_list)
    census_nat_perc = nat_perc(data_dict2, col_list)

    # computing the difference between them
    dif = nat_diff(ap_nat_perc, census_nat_perc)
    print("Difference between AP Comp Sci A and national demographics:\n",
          dif)
    '''

main()

# unit testing
# Don't touch anything below here
# create 4 tests
class HWTest(unittest.TestCase):

    def setUp(self):
        # surpressing output on unit testing
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        # setting up the data we'll need here
        # basically, redoing all the stuff we did in the main function
        self.ap_data = load_csv("region_ap_data.csv")
        self.census_data = load_csv("region_census_data.csv")

        self.ap_pct = get_perc(self.ap_data)
        self.census_pct = get_perc(self.census_data)

        self.pct_dif_dict = get_diff(self.ap_pct, self.census_pct)

        self.col_list = list(self.pct_dif_dict["midwest"].keys())

        self.mutated = max_min_mutate(self.pct_dif_dict, self.col_list)

        self.max_min_val = min_max(self.mutated)

        # extra credit
        # providing a list of col vals to cycle through
        self.col_list = self.census_data["midwest"].keys()

        # computing the national percentages
        self.ap_nat_pct = nat_perc(self.ap_data, self.col_list)
        self.census_nat_pct = nat_perc(self.census_data, self.col_list)

        self.dif = nat_diff(self.ap_nat_pct, self.census_nat_pct)

    # testing the csv reading func is working properly
    def test_load_csv(self):
         test = load_csv("region_ap_data.csv")

         self.assertEqual(test["west"]["ASIAN"], 7477)

    # testing the get_perc function
    def test_get_perc(self):
        self.assertEqual(get_perc({"region":{"demo":5,"Region Totals":10}}),
                         {"region":{"demo": 50.0}})

    # second test on the get_perc function
    # fails because my value is wrong (doh!)
    def test2_get_perc(self):
        self.assertEqual(
            self.ap_pct["midwest"]['AMERICAN INDIAN/ALASKA NATIVE'],
            0.29)

    # testing the get_diff function
    def test_get_diff(self):
        self.assertEqual(
            get_diff({"region":{"demo":50.0}},{"region":{"demo":50.0}}),
            {'region': {'demo': 0.0}}
            )

    # second test on the get_diff function
    # needs a valid value though brah
    def test2_get_diff(self):
        self.assertEqual(
            self.pct_dif_dict["west"]["AMERICAN INDIAN/ALASKA NATIVE"],
            1.51)

    # testing the max_min function
    def test_min_max(self):
        self.assertEqual(
            min_max({"demo":{"a":1,"b":2,"c":3,"d":4,"e":5}})
            ,
            {'max': {'demo': {'e': 5, 'd': 4, 'c': 3, 'b': 2, 'a': 1}},
             'min': {'demo': {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}}}
            )

    # second test on the max_min function
    def test2_min_max(self):
        self.assertEqual(
            self.max_min_val["max"]["BLACK"]["west"],
            3.47)
    '''
    # testing the nat_pct extra credit function
    def test_nat_perc(self):
       self.assertEqual(
       nat_perc({"region":{"demo":5,"Region Totals":10}},["demo", "Region Totals"]),
       {"demo":50.0, "Region Totals":10})
    
    # second test for the nat_pct extra credit function
    def test2_nat_perc(self):
        self.assertEqual(
            self.ap_nat_pct["AMERICAN INDIAN/ALASKA NATIVE"],
            0.3)

    # testing the nat_dif extra credit function
    def test_nat_diff(self):
        self.assertEqual(
            nat_diff({"demo":0.53, "Region Totals": 1},{"demo":0.5, "Region Totals": 1}),
            {"demo":0.03}
            )

    # second test for the nat_diff extra credit function
    def test2_nat_diff(self):
        self.assertEqual(
            self.dif["ASIAN"],
            28.2)
    '''
if __name__ == '__main__':
    unittest.main(verbosity=2)