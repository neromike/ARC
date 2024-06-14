import os
import json


f=open('dataset' + os.sep + 'arc-agi_training_challenges.json')
for line in f:
    training = json.loads(line)
f.close()

correct_prediction = 0

def show_success(test_name, rule, input_data, output_data, predicted_data):
    global correct_prediction
    correct_prediction += 1
    print(f"SUCCESS predicting {test_name} using rule {rule}")
    #print(f"input: {input_data}")
    #print(f"output: {output_data}")
    #print(f"predicted: {predicted_data}")

def move_number_to_end(lst, number):
    non_number_elements = [x for x in lst if x != number]
    number_count = len(lst) - len(non_number_elements)
    result = non_number_elements + [number] * number_count
    return result

def move_number_to_start(lst, number):
    non_number_elements = [x for x in lst if x != number]
    number_count = len(lst) - len(non_number_elements)
    result = [number] * number_count + non_number_elements
    return result

def move_number_to_end_2d(matrix, number):
    flat_list = [item for sublist in matrix for item in sublist]
    non_number_elements = [x for x in flat_list if x != number]
    number_count = len(flat_list) - len(non_number_elements)
    result_flat_list = non_number_elements + [number] * number_count
    rows, cols = len(matrix), len(matrix[0])
    reshaped_matrix = [result_flat_list[i * cols:(i + 1) * cols] for i in range(rows)]
    return reshaped_matrix

def move_number_to_start_2d(matrix, number):
    flat_list = [item for sublist in matrix for item in sublist]
    non_number_elements = [x for x in flat_list if x != number]
    number_count = len(flat_list) - len(non_number_elements)
    result_flat_list = [number] * number_count + non_number_elements
    rows, cols = len(matrix), len(matrix[0])
    reshaped_matrix = [result_flat_list[i * cols:(i + 1) * cols] for i in range(rows)]
    return reshaped_matrix

test_names = []
for line in training:
    curr_test = line
    test_names.append(curr_test)
    #print(f"CHECKING TEST {curr_test}")
    for data in training[curr_test]['train']:
        input_data = data['input']
        output_data = data['output']
        
        #MOVE A NUMBER TO THE END
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_end"
            predicted=[]
            for this_row in input_data:
                predicted.append( move_number_to_end(this_row, this_num) )
            if output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)
        
        #MOVE A NUMBER TO START
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_end"
            predicted=[]
            for this_row in input_data:
                predicted.append( move_number_to_start(this_row, this_num) )
            if output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

        #MOVE A NUMBER TO LAST ROW
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_end"
            predicted=move_number_to_end_2d(input_data, this_num)
            if output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)
        
        #MOVE A NUMBER TO FIRST ROW
        for this_num in range(0, 10):
            rule=f"move_{this_num}_to_end"
            predicted=move_number_to_start_2d(input_data, this_num)
            if output_data == predicted:
                show_success(curr_test, rule, input_data, output_data, predicted)

print(f"checked {len(test_names)} tests")
print(f"correctly predicted {correct_prediction} ({correct_prediction*1.0/len(test_names)})")