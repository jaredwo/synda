# this mapping means transform 'key' event into 'value' pipeline (with specified status).
event_pipeline_mapping={
    spconst.EVENT_OUTPUT12_VARIABLE_COMPLETE:      ('IPSL_VARIABLE', spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_OUTPUT12_LATEST_DATASET_COMPLETE:('IPSL_DATASET',  spconst.PPPRUN_STATUS_PAUSE),
    spconst.EVENT_VARIABLE_COMPLETE:               ('IPSL',          spconst.PPPRUN_STATUS_WAITING),
    spconst.EVENT_CDF_VARIABLE_N:                  ('CDF_VARIABLE',  spconst.PPPRUN_STATUS_PAUSE),   # maybe use IPSL_VARIABLE here (i.e. IPSL_DATASET may be done while IPSL_VARIABLE is running..)
    spconst.EVENT_CDF_DATASET:                     ('CDF_DATASET',   spconst.PPPRUN_STATUS_PAUSE),   # called for each variable, but duplicate dataset are ignored (i.e. for some project, a dataset is a group of variable)
    spconst.EVENT_CDF_VARIABLE_O:                  ('CDF',           spconst.PPPRUN_STATUS_PAUSE)
}

# this mapping means do not start 'key' before 'value' has ended
dependency={
    'CDF_VARIABLE':'IPSL_DATASET',
    'CDF':'IPSL'
}

# this mapping means once 'key' has ended, start 'value'
trigger={
    'CDF_VARIABLE':('CDF_DATASET','NV2D'),
    'IPSL_VARIABLE':('IPSL_DATASET','NV2D')
}
