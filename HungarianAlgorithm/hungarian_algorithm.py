import numpy as np

def hungarian_algorithm(input_matrix):
    # step 1 identify maximum per rows and substract from the input_matrix
    max_row_values = np.min(input_matrix, axis=1)
    input_matrix = input_matrix - max_row_values[:,np.newaxis]

    # step2 identify maximum per columns and substract from the input_matrix
    max_column_values = np.min(input_matrix, axis=0)
    input_matrix = input_matrix - max_column_values[np.newaxis,:]

    # step 3 compute the minimum number of lines which crosses all zeros
    input_matrix_zero_masked = input_matrix == 0

    def find_the_minimum_lines_which_crosses_all_zeros(matrix):
        continue_finding_zeros = np.sum(matrix) > 0
        rows = []
        columns = []
        total_lines = 0
    
        while continue_finding_zeros:
            sum_rows = np.sum(matrix,axis = 1)
            max_row_index = np.argmax(sum_rows)
            max_row_value = sum_rows[max_row_index]

            sum_columns = np.sum(matrix,axis = 0)
            max_column_index = np.argmax(sum_columns)
            max_column_value = sum_columns[max_column_index]

            if (max_column_value > max_row_value) and (max_column_value > 0):
                matrix[:,max_column_index] = False
                columns.append(max_column_index)


            elif (max_column_value <= max_row_value) and (max_row_value > 0):
                matrix[max_row_index,:] = False
                rows.append(max_row_index)

            continue_finding_zeros = np.sum(matrix) > 0

        rows  = np.asarray(rows)
        columns = np.asarray(columns)
        return rows, columns


    rows, columns = find_the_minimum_lines_which_crosses_all_zeros(input_matrix_zero_masked)
    total_lines = rows.shape[0] + columns.shape[0]
   
    # step 4
    while total_lines < input_matrix.shape[0]:
       
        # identify non zeros cells which do not intersect with the lines
        non_zero_rows, non_zero_columns = np.nonzero(input_matrix)

        matched_rows = non_zero_rows[np.newaxis,:] - rows[:,np.newaxis]
        matched_rows = matched_rows == 0
        matched_rows = np.sum(matched_rows,axis=0)
        valid_rows = matched_rows == 0

        matched_columns = non_zero_columns[np.newaxis,:] -columns[:,np.newaxis]
        matched_columns = matched_columns == 0
        matched_columns = np.sum(matched_columns,axis=0)
        valid_columns = matched_columns == 0

        valid_items = np.logical_and(valid_rows,valid_columns)
        #identify mininum value 
        min_value = np.min(input_matrix[non_zero_rows[valid_items],non_zero_columns[valid_items]])

        #substract the minimum value from the cells which are not intersectecting with the lines
        input_matrix[non_zero_rows[valid_items],non_zero_columns[valid_items]] = input_matrix[non_zero_rows[valid_items],non_zero_columns[valid_items]] - min_value

        #add the minimum value to the double crossed points
        cartesian_product = np.transpose([np.tile(rows, len(columns)), np.repeat(columns, len(rows))])
        input_matrix[cartesian_product[:,0],cartesian_product[:,1]] = input_matrix[cartesian_product[:,0],cartesian_product[:,1]] + min_value

        rows, columns = find_the_minimum_lines_which_crosses_all_zeros(input_matrix == 0)
        total_lines = rows.shape[0] + columns.shape[0]

    # step 5 do the matching
    matching_matrix = input_matrix == 0
    assigments = np.zeros((input_matrix.shape[0]))
    
    for i in range(matching_matrix.shape[0]):
        sum_rows = np.sum(matching_matrix,axis = 1)
        source = np.nonzero(sum_rows == 1)[0][0]
        target = np.nonzero(matching_matrix[source,:] == 1)[0][0]
        assigments[source] = target
        matching_matrix[source,:] = False
        matching_matrix[:,target] = False
        
    return assigments

       


       
        
        












if __name__ == "__main__":
    matrix_cost = np.abs(np.random.rand(3,3))

    input_example = np.asarray([[38,53,61,36,66],[100,60,9,79,34],[30,37,36,72,24],[61,95,21,14,64],[89,90,4,5,79]])
    assigments = hungarian_algorithm(input_example)
    assigments = hungarian_algorithm(matrix_cost)
    print(assigments)

