import os
import json


# Load the data from the file
with open('dataset' + os.sep + 'arc-agi_training_challenges.json') as f:
    training = json.load(f)


def show_success(test_name, rule, input_data, output_data, predicted_data):
    global correct_prediction
    if test_name not in correct_prediction:
        correct_prediction[test_name] = {}
    if rule not in correct_prediction[test_name]:
        correct_prediction[test_name][rule] = 0
    correct_prediction[test_name][rule] += 1
    """
    print(f"SUCCESS predicting {test_name} using rule {rule}")
    print(f"input: {input_data}")
    print(f"output: {output_data}")
    print(f"predicted: {predicted_data}")
    print()
    """

def move_number_to_end(lst, number):
    non_number_elements = [x for x in lst if x != number]
    number_count = len(lst) - len(non_number_elements)
    return non_number_elements + [number] * number_count

def move_number_to_start(lst, number):
    non_number_elements = [x for x in lst if x != number]
    number_count = len(lst) - len(non_number_elements)
    return [number] * number_count + non_number_elements

def move_number_to_end_2d(matrix, number):
    flat_list = [item for sublist in matrix for item in sublist]
    non_number_elements = [x for x in flat_list if x != number]
    number_count = len(flat_list) - len(non_number_elements)
    result_flat_list = non_number_elements + [number] * number_count
    rows, cols = len(matrix), len(matrix[0])
    return [result_flat_list[i * cols:(i + 1) * cols] for i in range(rows)]

def move_number_to_start_2d(matrix, number):
    flat_list = [item for sublist in matrix for item in sublist]
    non_number_elements = [x for x in flat_list if x != number]
    number_count = len(flat_list) - len(non_number_elements)
    result_flat_list = [number] * number_count + non_number_elements
    rows, cols = len(matrix), len(matrix[0])
    return [result_flat_list[i * cols:(i + 1) * cols] for i in range(rows)]

def fill_in_row(input_matrix, number):
    output_matrix = []
    for row in input_matrix:
        if row.count(row[0]) == len(row) and row[0] != number:
            output_matrix.append(row)
        elif row[0] != number and row[-1] == row[0] and row.count(number) == len(row) - 2:
            output_matrix.append([row[0]] * len(row))
        else:
            output_matrix.append(row)
    return output_matrix

def fill_in_col(input_matrix, number):
    transposed_matrix = list(map(list, zip(*input_matrix)))
    for i, col in enumerate(transposed_matrix):
        if col.count(col[0]) == len(col) and col[0] != number:
            continue
        elif col[0] != number and col[-1] == col[0] and col.count(number) == len(col) - 2:
            transposed_matrix[i] = [col[0]] * len(col)
    output_matrix = list(map(list, zip(*transposed_matrix)))
    return output_matrix

correct_prediction = {}
test_names = {}

for line in training:
    curr_test = line
    test_names[curr_test] = 0

    for data in training[curr_test]['train']:
        test_names[curr_test] += 1
        input_data = data['input']
        output_data = data['output']

        # NO CHANGE
        #rule=f"no_change"
        #predicted = input_data
        #if output_data == predicted:
        #    show_success(curr_test, rule, input_data, output_data, predicted)

        # MOVE A NUMBER TO THE END
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_end"
            predicted=[]
            for this_row in input_data:
                predicted.append( move_number_to_end(this_row, this_num) )
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

        # MOVE A NUMBER TO START
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_start"
            predicted=[]
            for this_row in input_data:
                predicted.append( move_number_to_start(this_row, this_num) )
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

        # MOVE A NUMBER TO LAST ROW
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_last_row"
            predicted=move_number_to_end_2d(input_data, this_num)
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

        # MOVE A NUMBER TO FIRST ROW
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_first_row"
            predicted=move_number_to_start_2d(input_data, this_num)
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

        # FILL IN ROW
        for this_num in range(0, 10):
            rule=f"fill_in_row_using_{this_num}"
            predicted=fill_in_row(input_data, this_num)
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)
        
        # FILL IN COLUMN
        for this_num in range(0, 10):
            rule=f"fill_in_row_using_{this_num}"
            predicted=fill_in_col(input_data, this_num)
            if predicted != input_data and output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

#print(f"correctly predicted {len(correct_prediction)} tests out of {len(test_names)} ({len(correct_prediction) * 100.0 / len(test_names)}%)")
for this_test in correct_prediction:
    print(f"test {this_test} - {test_names[this_test]}")
    for this_rule in correct_prediction[this_test]:
        print(f"  rule {this_rule} correctly predicted {correct_prediction[this_test][this_rule]}")
print(f"correctly predicted {len(correct_prediction)} tests out of {len(test_names)} ({len(correct_prediction) * 100.0 / len(test_names)}%)")