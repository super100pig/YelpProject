import os
import pickle
import numpy as np
import pandas as pd
from backend.utils import *

def add_features(path, component2id, n_con_feas=0, n_dis_feas=0, type='relative'):
    # Load Data
    prefix = path.split('_')[0].split('.')[0]
    data, abnormal_data, normal_data, Deviation_2_Tolerance = load_data(path)

    # Initialize DataFrame
    columns = ['ID']
    component_id_values = np.array([component2id[prefix + '_' + str(k)] for k in set(data['BatchNo'])], dtype=np.int32).reshape([-1,1])
    component_features = component_id_values
    cur_n_con_feas = n_con_feas
    cur_n_dis_feas = n_dis_feas

    # Generate Features
    con_labels_value = []
    for batch_num in set(data['BatchNo']):
        batch_data = data[data['BatchNo'] == batch_num]
        df1 = batch_data
        df2 = abnormal_data
        df = pd.merge(df1, df2, how="left", indicator=True)
        df['Flag'] = np.where(df['_merge'] == 'both', 1, 0)
        df.drop(labels=['_merge'], axis=1, inplace=True)
        label = df.groupby('IPE.Name').apply(lambda subdf: np.mean(subdf['Flag']))
        label_value = np.array([label[k] for k in label.keys()])
        con_labels_value.append(label_value)
    con_labels_value = np.array(con_labels_value)

    mean_data = data.groupby('BatchNo', group_keys=False).apply(lambda subdf: subdf.groupby('IPE.Name').agg('mean'))
    mean_data.reset_index()
    mean_data['dist'] = mean_data.apply(lambda row: getdist2(row, Deviation_2_Tolerance, type), axis=1)
    con_features = mean_data.groupby('BatchNo').apply(lambda subdf: [x for x in subdf['dist'].to_list()])
    con_features_value = np.array([con_features[k] for k in con_features.keys()])

    if len(con_features_value):
        _, n_con_feas = con_features_value.shape
        columns = columns + [prefix+'_'+'con_fea_'+str(i) for i in range(cur_n_con_feas, cur_n_con_feas+n_con_feas)]
        cur_n_con_feas += n_con_feas
        component_features = np.hstack((component_features, con_features_value))

    if len(con_labels_value):
        _, n_con_labels = con_labels_value.shape
        columns = columns + [prefix+'_'+'dis_fea_'+str(i) for i in range(cur_n_dis_feas, cur_n_dis_feas+n_con_labels)]
        cur_n_dis_feas += n_con_labels
        component_features = np.hstack((component_features, con_labels_value))

    # contuct DataFrame
    df = pd.DataFrame(data=component_features, columns=columns)
    df['ID'] = df['ID'].astype('int')

    n_con_feas = cur_n_con_feas
    n_dis_feas = cur_n_dis_feas

    return df, n_con_feas, n_dis_feas

def add_point_features(test2id):
    # Get DataFrame Data
    len_test = len(test2id)
    n_points = len_test
    columns = ['ID', 'TYPE', 'POS']

    point_id_values = np.array([test2id[k] for k in test2id.keys()], dtype=np.int32).reshape([-1,1])
    type_values = np.array([1]*len_test, dtype=np.int32)[:, None]
    position_values = np.array([i for i in range(n_points)], dtype=np.int32)[:, None]

    # contuct DataFrame
    point_id_values = np.hstack((point_id_values, type_values, position_values))
    df = pd.DataFrame(data=point_id_values, columns=columns)
    df['ID'] = df['ID'].astype('int')
    df = one_hot_process(df, ['TYPE', 'POS'])
    return df

# ------------------------------ Preprocess Features ------------------------------ #
def pre_features(feature_df):
    # Split discrete and continuous features
    feature_df.fillna(value=0, inplace=True)
    log_col = [i for i in feature_df.columns if 'dis' in i]
    log_new_col = ['log_{}'.format(i) for i in range(1, len(log_col) + 1)]
    z_score_col = [i for i in feature_df.columns if 'con' in i]
    z_score_new_col = ['continuuous_{}'.format(i) for i in range(1, len(z_score_col) + 1)]
    # print('#log_col:', len(log_col))
    # print('#z_score_col:', len(z_score_col))

    return feature_df