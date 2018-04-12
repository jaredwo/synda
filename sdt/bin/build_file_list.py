'''
Script to build a list of available netcdf files based on a set of ESGF
search queries. Example search queries:

project=CMIP5 variable=psl experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=rhs experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=rhsmax experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=rhsmin experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=rsds experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=sfcWind experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=tas experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=tasmax experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day
project=CMIP5 variable=tasmin experiment=piControl,historical,rcp26,rcp45,rcp60,rcp85 time_frequency=day

'''

from __future__ import print_function

from synda.sdrdataset import get_datasets
from synda.sdrfile import get_files
from tqdm import tqdm
import argparse
import io
import logging
import numpy as np
import pandas as pd
import synda.sdlog as sdlog


DEFAULT_STREAM_DATASET = {'protocol': ['http'],
                          'selection_filename': ['cli'],
                          'bifp_type': ['Dataset'],
                          'selection_file': ['cli'],
                          'local_path_format': ['treevar'],
                          'distrib': ['true'], 
                          'aidp_limit': ['10000'],
                          'action': ['search'],
                          'aifp_fields': ['instance_id,id,variable,data_node,type,size']}

DEFAULT_STREAM_FILES = {'selection_filename': ['cli'],
                        'local_path_format': ['treevar'],
                        'selection_file': ['cli'],
                        'distrib': ['true'],
                        'protocol': ['http'],
                        'aidp_limit': ['10000'],
                        'action': ['search'],
                        'bifp_type': ['File']}

LOG_CODE = "BUILD-FILE_LIST"

FILE_ATTRS = ['_timestamp','_version_', 'cf_standard_name', 'checksum', 'checksum_type',
              'cmor_table','data_node','dataset_functional_id','dataset_local_path',
              'dataset_path', 'dataset_path_without_version', 'dataset_version',
              'description', 'drs_id', 'ensemble', 'experiment', 'experiment_family',
              'file_functional_id', 'filename', 'forcing', 'format', 'index_node',
              'instance_id', 'institute', 'latest', 'local_path', 'master_id', 'model',
              'priority','product','project','realm','replica','score','size',
              'status','time_frequency', 'timestamp','tracking_id', 'type', 'url', 'variable',
              'variable_long_name', 'variable_units' ,'version' ]

class TqdmToLogger(io.StringIO):
    """
        Output stream for TQDM which will output to logger module instead of
        the StdOut.
        https://stackoverflow.com/questions/14897756/python-progress-bar-through-logging-module/
    """
    logger = None
    level = None
    buf = ''
    def __init__(self,logger,level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
    def write(self,buf):
        self.buf = buf.strip('\r\n\t ')
    def flush(self):
        self.logger.log(self.level, self.buf, extra={'code' : LOG_CODE})


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("query_file", help="file containing ESGF search queries")
    parser.add_argument("output_file_csv", help="output file path for file metadata csv")
    args = parser.parse_args()
    fpath_qf = args.query_file
    fpath_out = args.output_file_csv
    
    tqdm_out = TqdmToLogger(sdlog.default_logger, level=logging.INFO)
    
    queries = []
    with open(fpath_qf, 'r') as afile:
        
        for line in afile:
            
            li=line.strip()
            
            if not li.startswith("#"):
                queries.append(li)
    
    datasets = []
    
    sdlog.info(LOG_CODE, "Retrieving list of datasets for queries...")
    
    for a_query in tqdm(queries, file=tqdm_out):
                
        a_query_dict = { key:values.split(",")
                        for key,values in (x.split("=") for x in a_query.split(" ")) }
        a_query_dict.update(DEFAULT_STREAM_DATASET)
        
        has_error = False
        
        try:
        
            ds = get_datasets(stream=[a_query_dict])
        
        except Exception as e:
            
            sdlog.error(LOG_CODE, "Exception throwing during search query for datasets: %s | %s"%(a_query, e.args[0]))
            has_error = True
        
        if not has_error:
        
            if len(ds) == 0:
                
                sdlog.warning(LOG_CODE, "Dataset query did not find any datasets: %s" % a_query)
            
            else: 
                
                if len(ds) == 10000:
                    
                    sdlog.warning(LOG_CODE, "Number of datasets returned for query at upper limit: %s" % a_query)
                
                if a_query_dict.has_key('variable'):
                    
                    for a_ds in ds:
                        a_ds['variable'] = a_query_dict['variable']
                    
                datasets.extend(ds)
    
    df_datasets = pd.DataFrame(datasets)
    s_datasets = df_datasets[['dataset_functional_id',
                              'variable']].groupby('dataset_functional_id').apply(lambda x: np.unique(np.array(x.variable.values.tolist()).ravel()))
    
    all_files = []
    
    sdlog.info(LOG_CODE, "Retrieving list of files for %d datasets..."%s_datasets.size)
    
    for dsname in tqdm(s_datasets.index, file=tqdm_out):
        
        a_query_dict = {'dataset_id':[dsname],'variable':s_datasets[dsname]}
        a_query_dict.update(DEFAULT_STREAM_FILES)
        
        has_error = False
        
        try:
        
            files = get_files(stream=[a_query_dict])
        
        except Exception as e:
            
            sdlog.error(LOG_CODE, "Exception throwing during search query for files: %s %s | %s"%(a_query_dict['dataset_id'][0],
                                                                                                  ",".join(a_query_dict['variable']), 
                                                                                                  e.args[0]))
            has_error = True
        
        if not has_error:
            
            if len(files) == 0:
            
                sdlog.warning(LOG_CODE, "WARNING: File query did not find any files: %s %s" % (a_query_dict['dataset_id'][0],
                                                                                               ",".join(a_query_dict['variable'])))
            else:
                
                if len(files) == 10000:
                    sdlog.warning("Number of datasets returned for query at upper limit: %s %s" % (a_query_dict['dataset_id'][0],
                                                                                                   ",".join(a_query_dict['variable'])))
                
                df_files = pd.DataFrame(files)
                all_files.append(df_files)
    
    df_all = pd.concat(all_files,  ignore_index=True)[FILE_ATTRS]
    sdlog.info(LOG_CODE, "Writing list of files to %s "%fpath_out)
    df_all.to_csv(fpath_out, index=False)
    