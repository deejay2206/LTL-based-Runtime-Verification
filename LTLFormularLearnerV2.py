import sys
import os
import subprocess
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Define the file objects before the main function
file0 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/trace902_output_file.csv', "w")
file1 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/samples2LTL-master/example902.trace', "w")
file2 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/902/extract.csv', "w")
file3 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/stat.csv', "w")
file4 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/902/Positive_file.csv', "w")
file5 = open('/home/guest/Desktop/Project/Dataset-GOOSE-attacks-main/Normalised/Malicious_behaviours/IED_TRSF1/902/Negative_file.csv', "w")


#####################################################################################################
#------------------------ Split Dataset into 70% Training and 30% Testing datasets-------------------
#####################################################################################################
def split_train_test(csv_file, train_file, test_file, train_ratio=0.7):
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)

    #data = data.drop(['datset'], axis=1)

    # Scale all columns by 1000
    data = data * 100

    # Divide 'ATT_FLAG' and 'Timestamp' columns by 1000
    data['Label'] = data['Label'] / 100
    data['t'] = data['t'] / 100
    data['Timestamp'] = data['Timestamp'] / 100
    # Convert the 'Timestamp' column to whole numbers
    data['Timestamp'] = data['Timestamp'].astype(int)


    data = data.loc[:, ~data.columns.str.contains('unnamed')]


    # Calculate the index to split the data
    split_index = int(len(data) * train_ratio)

    # Split the data into train and test datasets
    train_data = data[:split_index]
    test_data = data[split_index:]

    # Write the train and test datasets to separate files
    train_data.to_csv(train_file, index=False)
    test_data.to_csv(test_file, index=False)


#########################################################################################################################
#  Phase 2: Extraction of datasets for positive & negative traces.
#########################################################################################################################

#   Positive Traces Generation Phase
#######################################################################
def print_rows_before_attack(csv_file, n):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

     # Find the indices where 'Attack' column is equal to 1
    attack_indices = df.index[df['cluster'] == attack_code]

     # Fetch n rows before each 'Attack' occurrence
    fetched_rows = []
    for index in attack_indices:
        start_index = max(0, index - n + 1)
        end_index = index
        rows_before_attack = df.iloc[start_index:end_index]
        fetched_rows.append(rows_before_attack)

    # Concatenate the fetched rows into a single DataFrame
    df2 = pd.concat(fetched_rows)

    # Remove duplicated index rows
    df2 = df2[~df2.index.duplicated(keep='first')]

    df2 = df2.drop('Label', axis=1)
    print('Positive:', df2.to_csv(), file=file4)

    idx_dic2 = {}
    for col in df2.columns:
        idx_dic2[col] = df2.columns.get_loc(col)
    print('Positive:', idx_dic2, file=file3)
    #print('Positive:', idx_dic2)

    print("---", file=file3)

    print(df2.describe())
    print('Positive:', df2.describe().to_csv(), file=file3)

    testmean = df2.mean(axis=0)
    test_mean = testmean
    teststd = df2.std(axis=0)
    test_std = teststd
    range0 = test_mean - test_std
    print(range0)
    print("minimum value range0:", range0, file=file2)

    print("----", file=file2)
    range1 = test_mean + test_std
    print(range1)
    print("minimum value range1:", range1, file=file2)

    # Return the resulting DataFrame
    return df2


#   Negative Traces Generation Phase
###############################################################
def fetch_rows_around_attack(csv_file, m):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Find rows where 'Attack' column equals 1
    attack_rows = df[df['Label'] == attack_code]

    # Fetch n rows before and after each attack row
    rows_to_fetch = []
    for index in attack_rows.index:
        start_index = max(0, index - m)
        end_index = min(len(df), index + m + 1)
        rows_to_fetch.extend(range(start_index, end_index))

    # Remove the fetched rows from the original DataFrame
    modified_df = df.drop(index=rows_to_fetch)
    print(modified_df.to_csv(), file=file5)
    modified_df = modified_df.drop('Label', axis=1)

    print('Negative:', modified_df.describe().to_csv(), file=file3)
    print(modified_df.describe())

    # Output the modified DataFrame
    #print(modified_df, 'Modified')
    return modified_df


#########################################################################################################################
#  Phase 3: Clustering Phase
#########################################################################################################################
#   Positive Traces Generation Phase
#######################################################################
def perform_clustering(csv_file, n_clusters):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Select columns for clustering (excluding 'Attack' and 'timestamp')
    clustering_columns = df.drop(['Timestamp'], axis=1)
    #print(clustering_columns)

    idx_dic2 = {}
    for col in clustering_columns.columns:
        idx_dic2[col] = clustering_columns.columns.get_loc(col)
    print('Positive:', idx_dic2, file=file3)

    print('Positive:', clustering_columns.describe().to_csv(), file=file3)
    print(clustering_columns.describe())


    # Perform clustering on each column
    for column in clustering_columns.columns:
        # Extract column data as a 2D array
        column_data = clustering_columns[column].values.reshape(-1, 1)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(column_data)

        # Add clustering labels as a new column in the DataFrame
        df[column + '_cluster'] = labels
        df1 = df.filter(like='_cluster')

    return df1

#   Negative Traces Generation Phase
#######################################################################
def perform1_clustering(csv1_file, n_clusters):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv1_file)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Select columns for clustering (excluding 'Attack' and 'timestamp')
    clustering_columns = df.drop(['Timestamp'], axis=1)

    print('Negative:', clustering_columns.describe().to_csv(), file=file3)
    print(clustering_columns.describe())


    # Perform clustering on each column
    for column in clustering_columns.columns:
        # Extract column data as a 2D array
        column_data = clustering_columns[column].values.reshape(-1, 1)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters)
        labels = kmeans.fit_predict(column_data)

        # Add clustering labels as a new column in the DataFrame
        df[column + '_cluster'] = labels
        df2 = df.filter(like='_cluster')
        #df2.insert(0, value=df['Label'], column='Label')
    #print(df1)

    return df2


##===========================================================================
# Split entries for positives into three traces
##============================================================================
def main(s, attack_code, n, m, n_clusters):
    # Set the file paths for clustering results
    csv_file = '902Trained_data.csv'
    positive_data_csv = '902/902positive_data.csv'
    negative_data_csv = '902/902negative_data.csv'

    # Split dataset into train and test
    split_train_test(csv_file, 'train_data.csv', 'test_data.csv', train_ratio=0.7)

    # Phase 2: Extraction of datasets for positive & negative traces
    positive_data = print_rows_before_attack('train_data.csv', n)
    positive_data.to_csv(positive_data_csv, index=False)

    negative_data = fetch_rows_around_attack('train_data.csv', m)
    negative_data.to_csv(negative_data_csv, index=False)

    # Phase 3: Clustering Phase
    clustered_positive_data = perform_clustering(positive_data_csv, n_clusters)
    clustered_positive_data.to_csv('902/902Positive_clustered_data.csv', index=False)

    clustered_negative_data = perform1_clustering(negative_data_csv, n_clusters)
    clustered_negative_data.to_csv('902/902Negative_clustered_data.csv', index=False)

    # Phase 4: Extract Traces For LTL Learning
    num_rows_pos = clustered_positive_data.shape[0]
    num_rows_neg = clustered_negative_data.shape[0]

    n1 = num_rows_pos // s
    n2 = num_rows_neg // s

    ##===========================================================================
    # Split entries for positives into three traces
    ##============================================================================
    list_df = [clustered_positive_data[i:i + n1] for i in range(0, num_rows_pos, n1)]

    check_list1 = list_df[0]
    df_list = check_list1.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list10 = list_df[1]
    df_list = check_list10.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list01 = list_df[2]
    df_list = check_list01.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list100 = list_df[3]
    df_list = check_list100.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list101 = list_df[4]
    df_list = check_list101.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    # Now you can safely check and access elements in list_df
    if len(list_df) >= 6:
        check_list011 = list_df[5]
        df_list = check_list011.values.tolist()
        df_lists = ';'.join(map(str, df_list))
        result_1 = str(df_lists)
        result_2 = result_1.replace("[", "")
        result_3 = result_2.replace("]", "")
        df_list1 = result_3.replace(" ", "")
        print(df_list1, file=file1)
    else:
        print("Not enough elements in list_df")


    print('---', file=file1)

    ##===========================================================================
    # Split entries for negative into three traces
    ##============================================================================

    list1_df = [clustered_negative_data[i:i + n2] for i in range(0, num_rows_neg, n2)]

    check_list0 = list1_df[0]
    df_list = check_list0.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list00 = list1_df[1]
    df_list = check_list00.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list1 = list1_df[2]
    df_list = check_list1.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list11 = list1_df[3]
    df_list = check_list11.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    check_list2 = list1_df[4]
    df_list = check_list2.values.tolist()
    df_lists = ';'.join(map(str, df_list))
    result_1 = str(df_lists)
    result_2 = result_1.replace("[", "")
    result_3 = result_2.replace("]", "")
    df_list1 = result_3.replace(" ", "")
    print(df_list1, file=file1)

    # Now you can safely check and access elements in list_df
    if len(list1_df) >= 6:
        check_list02 = list1_df[5]
        df_list = check_list02.values.tolist()
        df_lists = ';'.join(map(str, df_list))
        result_1 = str(df_lists)
        result_2 = result_1.replace("[", "")
        result_3 = result_2.replace("]", "")
        df_list1 = result_3.replace(" ", "")
        print(df_list1, file=file1)
    else:
        print("Not enough elements in list1_df")

    print('LTL formula learnt')


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python3 script.py s attack_code n m n_clusters")
        sys.exit(1)

    s = int(sys.argv[1])
    attack_code = int(sys.argv[2])
    n = int(sys.argv[3])
    m = int(sys.argv[4])
    n_clusters = int(sys.argv[5])

    main(s, attack_code, n, m, n_clusters)

    # Run experiment.py with specified options and capture the outputs
    sat_command = "python3 samples2LTL-master/experiment.py --test_sat_method --traces samples2LTL-master/example902.trace"
    dt_command = "python3 samples2LTL-master/experiment.py --test_dt_method --traces samples2LTL-master/example902.trace"

    # Run the commands using subprocess and capture the outputs
    sat_output = subprocess.getoutput(sat_command)
    dt_output = subprocess.getoutput(dt_command)

    # Write the outputs to a file
    with open("experiment_902outputs.txt", "w") as output_file:
        output_file.write("Sat Method Output:\n")
        output_file.write(sat_output)
        output_file.write("\n\n")
        output_file.write("DT Method Output:\n")
        output_file.write(dt_output)

    print("Experiment outputs written to experiment_902outputs.txt")





