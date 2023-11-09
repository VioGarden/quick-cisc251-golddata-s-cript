import pandas as pd
import os

from collections import defaultdict

"""read gold datafile"""
script_directory = os.path.dirname(os.path.abspath(__file__)) # get path to folder
file_path = os.path.join(script_directory, 'golddataset.csv') # get path to dataset
excel_data = pd.read_csv(file_path) # read dataset
numpy_data = excel_data.values

"""if given a location, code finds the rows on the gold data files that correspond"""
def excel_row_finder(location):
    location = str(location).strip()
    row = 0
    while row < 215:
        if row == 214:
            return (-1, -1)
        value = excel_data.iloc[row, 0]
        if str(value) == location:
            break
        row += 1
    start = row
    while str(excel_data.iloc[row, 0]) == location:
        if row == 214:
            row += 1
            break
        row += 1
    return (start + 2, row + 2 - 1)

"""column of all the column header names, elmeent_solvent"""
columns_names = [] 
for i in excel_data.columns:
    if i == 'Dist' or i == 'Dpth':
        continue
    columns_names.append(i)

"""if given a row number, function grabs entire row from data set"""
def get_called_row(row_index):
    real_numpy_row = row_index - 2
    arr = []
    for val in numpy_data[real_numpy_row, 2:]:
        arr.append(val)
    return arr

"""given a target row and a predictor row, function finds the difference of each element"""
def compare_two_rows(col_names, arr1, arr2):
    ans = []
    n = len(col_names)
    total_difference = 0
    for k in range(n):
        val = round(abs(arr2[k] - arr1[k]), 3)
        total_difference += val
        ans.append((col_names[k], val, arr2[k]))
    sorted_ans = sorted(ans, key=lambda x: x[1])
    return sorted_ans


"""combination of functions above. given a location, compares deepest with highest row"""
def run_basic_program(location):
    x, y = excel_row_finder(location)
    if x == -1 and y == -1:
        return -1
    first = get_called_row(x)
    second = get_called_row(y)
    final = compare_two_rows(columns_names, first, second)
    return final

"""arrays of besta nd worst correlating loations"""
bin1 = [138.6, 181.2, 200.8, 234.35, 239.4, 265.4, 270.5, 275.4, 280.5, 285.3] # high correlation
bin2 = [143.3, 167.3, 171.4, 176.4, 190.55, 195.6, 214.6, 219.3, 250.6] # low correlation

"""
iterates through a list of locations
for each location, each element is compared, the highest level to the deepest level and stored into a hashmap
repeats for each location. because every element appears with new values once per iteration, values are summe dup
"""
hashmap1 = defaultdict(list)
hh = 0.0
for h in bin1:
    hh += 1
    x = run_basic_program(h)
    for name, value, target in x:
        if not hashmap1[name]:
            hashmap1[name].append(value)
            hashmap1[name].append(target)
        else:
            curr_value = hashmap1[name][0]
            curr_value += value
            hashmap1[name][0] = round(curr_value, 3)
            curr_target = hashmap1[name][1]
            curr_target += target
            hashmap1[name][1] = round(curr_target, 3)

    bin1_list = hashmap1.items()
    bin1_list_sorted = sorted(bin1_list, key=lambda x: x[0])

hashmap2 = defaultdict(list)
ll = 0.0
for l in bin2:
    y = run_basic_program(l)
    ll += 1.0
    for name, value, target in y:
        if not hashmap2[name]:
            hashmap2[name].append(value)
            hashmap2[name].append(target)
        else:
            curr_value = hashmap2[name][0]
            curr_value += value
            hashmap2[name][0] = round(curr_value, 3)
            curr_target = hashmap2[name][1]
            curr_target += target
            # curr_target /= ll
            hashmap2[name][1] = round(curr_target, 3)

    bin2_list = hashmap2.items()
    bin2_list_sorted = sorted(bin2_list, key=lambda y: y[0])


"""plotting differences"""
def plot_differences(b1, b2, start, end):
    x_values = [item[0] for item in b1[start:end]]  # Assuming the x-values are the first elements of each tuple
    y_values_1 = [item[1][0] for item in b1[start:end]]  # Y-values for list 1
    y_values_1a = [item[1][1] for item in b1[start:end]]  # Y-values for list 1
    y_values_2 = [item[1][0] for item in b2[start:end]]  # Y-values for list 2
    y_values_2a = [item[1][1] for item in b2[start:end]]  # Y-values for list 2



    import matplotlib.pyplot as plt
    bar_width = 0.35
    plt.bar([x - 3/4 * bar_width for x in range(len(x_values))], y_values_1, width=bar_width / 2, align='center', label='List 1')
    plt.bar([x - 2/4 * bar_width for x in range(len(x_values))], y_values_1a, width=bar_width / 2, align='center', label='High 1 target')
    plt.bar([x + 1/4 * bar_width for x in range(len(x_values))], y_values_2, width=bar_width / 2, align='center', label='List 2')
    plt.bar([x + 0/4 * bar_width for x in range(len(x_values))], y_values_2a, width=bar_width / 2, align='center', label='Low 2 target')

    # high orange means lots of presense of that mineral
    # high blue bar means lots of variation
    # high red bar means lots of presense of that mineral for a low set
    # high green bar means lots of variation for a low set, if green bar is high, means lots of variation so its good cause it doesn't matter statistically

    # most importantly, we want high orange, and small blue
    # if red bar is low, not much of that mineral in the low sets, so green doesn't really matter
    # if high red and small green, interesting case, predictable lack of minerals


    plt.xticks(range(len(x_values)), x_values)

    plt.xlabel('X-Values')
    plt.ylabel('Y-Values')
    plt.title('Bar Chart for Two Lists')

    plt.legend()

    plt.show()

plot_differences(bin1_list_sorted, bin2_list_sorted, 0, 20)

