'''
Script to update local download database from a list of file metadata generated
by build_file_list.py
'''

import pandas as pd
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("file_csv", help="file path to file metadata csv created by build_file_list.py")
    parser.add_argument("data_root", help="root path of data")
    args = parser.parse_args()
    
    fpath_csv = args.file_csv
    path_data = args.data_root
    
    # Load and dedup files
    df_files = pd.read_csv(fpath_csv)
    df_files_sort = df_files.sort_values(['filename', 'dataset_version', '_version_'], ascending=False)
    df_fnl = df_files_sort.drop_duplicates(['filename'], keep='first')
    
    # Columns for database
    # _version_
    # checksum
    # checksum_type
    # dataset_functional_id
    # dataset_version
    # ensemble
    # experiment
    # file_functional_id *
    # filename
    # model
    # project
    # size
    # time_frequency
    # url
    # variable