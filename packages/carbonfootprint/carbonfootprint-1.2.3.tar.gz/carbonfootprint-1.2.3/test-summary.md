Testing started at 4:52 PM ...
/home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/energycarbon_env/bin/python /home/altanai/Downloads/pycharm-community-2020.1.3/plugins/python-ce/helpers/pycharm/_jb_unittest_runner.py --path /home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/tests/unittests.py
Launching unittests with arguments python -m unittest /home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/tests/unittests.py in /home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/tests



Ran 2 tests in 1.838s

OK

Process finished with exit code 0
   power(W)           Timestamp          DATE
0  312480.0 2009-01-01 00:00:00  [2009-01-01]
1  311760.0 2009-01-01 01:00:00  [2009-01-01]
2  311760.0 2009-01-01 02:00:00  [2009-01-01]
3  312480.0 2009-01-01 03:00:00  [2009-01-01]
4  311040.0 2009-01-01 04:00:00  [2009-01-01]
utility_fuelmix filenames /home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/src/carbonemisison/../../dataset/north_west2020/*.csv
  Region Code  ... Imports Generation (%)
0          NW  ...                    0.0
1          NW  ...                    0.0
2          NW  ...                    0.0
3          NW  ...                    0.0
4          NW  ...                    0.0

[5 rows x 24 columns]
-------------dfindus_hourly_fuelmix_carbon------------------
   power(W)           Timestamp  ... carbon_Imports(kgeCO2)  carbon_total(kgeCO2)
0  312480.0 2009-01-01 00:00:00  ...                    0.0             89.720020
1  311760.0 2009-01-01 01:00:00  ...                    0.0             89.406608
2  311760.0 2009-01-01 02:00:00  ...                    0.0             88.377311
3  312480.0 2009-01-01 03:00:00  ...                    0.0             89.035798
4  311040.0 2009-01-01 04:00:00  ...                    0.0             87.741001

[5 rows x 25 columns]
Index(['power(W)', 'Timestamp', 'DATE', 'Wind(W)', 'Solar(W)', 'Hydro(W)',
       'Other(W)', 'Petroleum(W)', 'Natural gas(W)', 'Coal(W)', 'Nuclear(W)',
       'Battery(W)', 'Imports(W)', 'total(W)', 'carbon_Wind(kgeCO2)',
       'carbon_Solar(kgeCO2)', 'carbon_Hydro(kgeCO2)', 'carbon_Other(kgeCO2)',
       'carbon_Petroleum(kgeCO2)', 'carbon_Natural gas(kgeCO2)',
       'carbon_Coal(kgeCO2)', 'carbon_Nuclear(kgeCO2)',
       'carbon_Battery(kgeCO2)', 'carbon_Imports(kgeCO2)',
       'carbon_total(kgeCO2)'],
      dtype='object')
   power(W)           Timestamp          DATE
0  312480.0 2009-01-01 00:00:00  [2009-01-01]
1  311760.0 2009-01-01 01:00:00  [2009-01-01]
2  311760.0 2009-01-01 02:00:00  [2009-01-01]
3  312480.0 2009-01-01 03:00:00  [2009-01-01]
4  311040.0 2009-01-01 04:00:00  [2009-01-01]
utility_fuelmix filenames /home/altanai/Documents/SUresearch/energy/carbon-footprint-calculator/src/carbonemisison/../../dataset/north_west2020/*.csv
  Region Code  ... Imports Generation (%)
0          NW  ...                    0.0
1          NW  ...                    0.0
2          NW  ...                    0.0
3          NW  ...                    0.0
4          NW  ...                    0.0

[5 rows x 24 columns]
-------------dfindus_hourly_fuelmix------------------
   power(W)           Timestamp          DATE  ...  Battery(W)  Imports(W)  total(W)
0  312480.0 2009-01-01 00:00:00  [2009-01-01]  ...         0.0         0.0  312480.0
1  311760.0 2009-01-01 01:00:00  [2009-01-01]  ...         0.0         0.0  311760.0
2  311760.0 2009-01-01 02:00:00  [2009-01-01]  ...         0.0         0.0  311760.0
3  312480.0 2009-01-01 03:00:00  [2009-01-01]  ...         0.0         0.0  312480.0
4  311040.0 2009-01-01 04:00:00  [2009-01-01]  ...         0.0         0.0  311040.0

[5 rows x 14 columns]
Index(['power(W)', 'Timestamp', 'DATE', 'Wind(W)', 'Solar(W)', 'Hydro(W)',
       'Other(W)', 'Petroleum(W)', 'Natural gas(W)', 'Coal(W)', 'Nuclear(W)',
       'Battery(W)', 'Imports(W)', 'total(W)'],
      dtype='object')