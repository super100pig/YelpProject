import os
import pymysql
import pickle
import argparse
import numpy as np
import pandas as pd

from backend import db_setting
from backend.utils import *
from backend.cons_features import *


#------------------------------ Add comp-poi known abnormal edge ------------------------------ #
def add_table(path, id_dict, node_idx, nodes, edges, point2component):
    prefix = path.split('_')[0].split('.')[0]
    component2id, test2id = id_dict

    data, abnormal_data, normal_data, Deviation_2_Tolerance = load_data(path)
    print("\tAbnormal test data:\t\t", len(abnormal_data))
    print("\tNormal test data:\t\t", len(normal_data))

    # Add Components
    for component in set(data['BatchNo']):
        component = prefix + '_' + str(component)
        if component not in component2id:
            component2id[component] = node_idx
            node_idx += 1
        nodes.add(component2id[component])

    # Add Test Points
    for test in set(data['IPE.Name']):
        test = prefix + '_' + test.strip()
        if test not in test2id:
            test2id[test] = node_idx
            node_idx += 1
        nodes.add(test2id[test])
        if test not in point2component: point2component[test] = []

    # Add Abnormal Edges
    for component, test in abnormal_data.loc[:, ['BatchNo', 'IPE.Name']].values:
        component = prefix + '_' + str(component)
        test = prefix + '_' + test.strip()

        # Consider about the duplicate edges
        if args['edge_weight_flag']:
            tempFlag = False
            for id1, id2, w in edges:
                if id1 == component2id[component] and id2 == test2id[test]:
                    edges.remove((id1, id2, w))
                    edges.add((id1, id2, w + 1))
                    tempFlag = True
                    break
            if not tempFlag:
                edges.add((component2id[component], test2id[test], 1.0))
                point2component[test].append(component2id[component])
        else:
            if (component2id[component], test2id[test]) not in edges:
                point2component[test].append(component2id[component])
            edges.add((component2id[component], test2id[test]))

    # Return And Update
    id_dict = [component2id, test2id]
    return id_dict, node_idx, nodes, edges, point2component

def get_zscore_edges(data, Deviation_2_Tolerance, zscore_threshold=2.0):
    comp_poi_dict = {}

    all_items = list(set(data['IPE.Name']))
    # for each item, get component and points' zscore and zscore edges
    for item in all_items:
        item = item
        # get subdf for item in all test items
        subdf = data[data['IPE.Name'] == item].copy()
        remain_cols = set(Deviation_2_Tolerance.keys())
        remain_cols.add('BatchNo')
        subdf = subdf[remain_cols]
        # calculate average zscroe
        all_zscore = []
        for test in Deviation_2_Tolerance.keys():
            score_col = test + '_score'
            all_zscore.append(score_col)
            feat_values = subdf.loc[:, test]
            zscore = (feat_values - feat_values.mean()) / feat_values.std()
            subdf[score_col] = zscore.abs()
        subdf['zscore'] = subdf[all_zscore].mean(axis=1)
        subdf['zscore_flag'] = subdf['zscore'] > zscore_threshold
        subdf = subdf[subdf['zscore_flag']].copy()
        subdf['weight'] = 1.0 - 1.0 / subdf['zscore']
        # update comp_poi_dict
        if len(subdf) == 0:
            continue
        subres = subdf.loc[:, ['BatchNo', 'weight']]
        for BN, w in subres.values:
            comp_poi_dict[(int(BN), item.strip())] = w
    return comp_poi_dict

def add_car_poi_table(path, id_dict, edges):
    prefix = path.split('_')[0].split('.')[0]
    component2id, test2id = id_dict

    # Load Data
    data, abnormal_data, normal_data, Deviation_2_Tolerance = load_data(path)
    # -------------------- get zscore edges -------------------- #
    comp_poi_dict = get_zscore_edges(data, Deviation_2_Tolerance)
    for bn, ipeName in comp_poi_dict.keys():
        weight = comp_poi_dict[(bn, ipeName)]
        compName = prefix + '_' + str(bn)
        poiName = prefix + '_' + ipeName
        compID = component2id[compName]
        testID = test2id[poiName]
        if args.edge_weight_flag:
            edges.add((compID, testID, weight))
        else:
            edges.add((compID, testID))

    print('\t共添加{}条 zscore 边'.format(len(comp_poi_dict)))
    return edges

def add_batch_corr(path, edges, component2id):
    corrs = [('A', 'B1'), ('A', 'B2'), ('A', 'B3'), ('A', 'B4'), ('A', 'B5'), ('A', 'B6'),
            ('B1', 'C1'), ('B1', 'C2'),
            ('B2', 'C3'), ('B2', 'C5'),
            ('B3', 'C4'), ('B3', 'C6'),
            ('B4', 'C7'), ('B4', 'C9'),
            ('B5', 'C8'), ('B5', 'C10'),
            ('B6', 'C11'), ('B6', 'C12'), ('B6', 'C13')]
    path = 'DataMeasurement/{}'.format(path)
    data = pd.read_csv(path, encoding="utf-8", dtype=str)
    for _, rows in data.iterrows():
        for comp1, comp2 in corrs:
            comp1 = comp1 + '_' + rows[comp1]
            comp2 = comp2 + '_' + rows[comp2]
            if comp1 in component2id and comp2 in component2id:
                if args['edge_weight_flag']:
                    edges.add((component2id[comp1], component2id[comp2], 1.0))
                else:
                    edges.add((component2id[comp1], component2id[comp2]))
    return edges

#------------------------------ Save Graph -----------------------------
def save_to_file(component2id, test2id, nodes, edges, node_path, edge_path):
    # save to files
    if node_path: node_file = open(node_path, 'w')
    if edge_path: edge_file = open(edge_path, 'w')

    # save nodes
    for comp in component2id:
        node_file.write('{}\t{}\t{}\n'.format(component2id[comp], comp, 'comp'))
    for test in test2id:
        node_file.write('{}\t{}\t{}\n'.format(test2id[test], test, 'test'))

    # save edges
    if args['edge_weight_flag']:
        for (node1, node2, weight) in edges:
            edge_file.write('{}\t{}\t{}\n'.format(node1, node2, weight))
    else:
        for (node1, node2) in edges:
            edge_file.write('{}\t{}\n'.format(node1, node2))

    # close files
    if node_file: node_file.close()
    if edge_file: edge_file.close()


def insert_node(data, cate, table_name):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    k = 0
    for point in data:
        point_id = data[point]
        if k == 0:
            sql = 'INSERT INTO %s VALUES %s' % (table_name, str(tuple([point_id, point, cate])))
            k += 1
        else:
            sql += ', %s' % str(tuple([point_id, point, cate]))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


def insert_edge(data, table_name):
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    k = 0
    for (node1, node2) in data:
        if k == 0:
            sql = 'INSERT INTO %s VALUES %s' % (table_name, str(tuple([node1, node2])))
            k += 1
        else:
            sql += ', %s' % str(tuple([node1, node2]))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()


#------------------------------ Main ------------------------------ #
A_paths = ['A.csv']
B_paths = ['B1_861723110.csv', 'B2_861731120.csv', 'B3_861731110.csv',
           'B4_861733120.csv', 'B5_861733110.csv', 'B6_861727110.csv']
C_paths = ['C1_861723117.csv', 'C2_861723115.csv', 'C3_861731118.csv',
           'C4_861731117.csv', 'C5_861731116.csv', 'C6_861731115.csv',
           'C7_861733118.csv', 'C8_861733117.csv', 'C9_861733116.csv',
           'C10_861733115.csv', 'C11_861727117.csv', 'C12_861727131.csv',
           'C13_861727133.csv']
Batch_path = 'Batch.csv'
all_paths = A_paths + B_paths + C_paths

# parser1 = argparse.ArgumentParser()
args = {}
args['rootdir'] = 'Graph/'
args['first_path'] = 'A.csv'
args['comp_poi_flag'] = True
args['comp_comp_flag'] = True
args['poi_poi_flag'] = False
args['edge_weight_flag'] = False


def save():
    #----------------------------------- Output File ------------------------------------#
    if not os.path.exists('Graph'): os.mkdir('Graph')
    if not os.path.exists(args['rootdir']): os.mkdir(args['rootdir'])
    if not os.path.exists(args['rootdir']+'point2comp'): os.mkdir(args['rootdir']+'point2comp')
    if not os.path.exists(args['rootdir']+'features'): os.mkdir(args['rootdir']+'features')

    node_path = '{}/nodes'.format(args['rootdir'])
    edge_path = '{}/edges'.format(args['rootdir'])
    point2component_path = '{}/point2component.pkl'.format(args['rootdir'] + 'point2comp')
    component_feat_path = '{}/component_features.csv'.format(args['rootdir'] + 'features')
    point_feat_path = '{}/poi_features.csv'.format(args['rootdir'] + 'features')
    #------------------------------------------------------------------------------------#

    component2id = {}
    test2id = {}

    node_idx = 0
    nodes = set()
    edges = set()
    point2component = {}

    duplicate_test = {}

    # Generate Graph
    print('-' * 20, 'Generate Graph', '-' * 20)
    for path in all_paths:
        print("#path:", path)
        id_dict = [component2id, test2id]
        id_dict, node_idx, nodes, edges, point2component = add_table(path, id_dict, node_idx, nodes, edges, point2component)
        component2id, test2id = id_dict
        if args.comp_poi_flag:
            edges = add_car_poi_table(path, id_dict, edges)
    edges = add_batch_corr(Batch_path, edges, component2id)

    # Generate Features
    print('-' * 20, 'Generate Features', '-' * 20)
    for path in all_paths:
        print("#path:", path)

        if path == args['first_path']:
            fea_df, n_con_feas, n_dis_feas = add_features(path, component2id)
        else:
            add_fea_df, n_con_feas, n_dis_feas = add_features(path, component2id)
            fea_df = pd.merge(fea_df, add_fea_df, how='outer', left_on='ID', right_on='ID')
        point_fea_df = add_point_features(test2id)

        # Finally, the features are uniformly processed.
        pre_comp_fea_df = pre_features(fea_df)
        # if args.car_car_flag:
        #     edges = add_car_car_table(pre_car_fea_df, edges)

    # Print & Save
    print('-' * 20, 'Save', '-' * 20)
    print('-- Graph --')
    print('#nodes:{}\n#edges:{}'.format(len(nodes), len(edges)))
    print('#components:', len(component2id))
    print('#points:', len(test2id))
    print('#duplicate points:', len(duplicate_test))

    save_to_file(component2id, test2id, nodes, edges, node_path, edge_path)
    print("insert node and edge into database")
    insert_node(component2id, 'comp', 'node')
    insert_node(test2id, 'test', 'node')
    insert_edge(edges, 'edge')
    print("save node and edge")

    point2component = {k: sorted(list(set(v))) for k, v in point2component.items()}
    db = pymysql.connect(host=db_setting.host,
                         user=db_setting.user,
                         password=db_setting.password,
                         db=db_setting.db,
                         charset=db_setting.charset,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    table_name = 'point2component'
    k = 0
    for point in point2component:
        component = point2component[point]
        component = str(component)[1:-1]
        if component == '':
            component = '0'
        if k == 0:
            sql = 'INSERT INTO %s VALUES %s' % (table_name, str(tuple([point, component])))
            k += 1
        else:
            sql += ', %s' % str(tuple([point, component]))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        db.close()
    pickle.dump(point2component, open(point2component_path, 'wb'))
    print('Finished Save Graph!')

    pre_comp_fea_df.to_csv(component_feat_path, index=False)
    point_fea_df.to_csv(point_feat_path, index=False)
    print('#comp_fea_df:', pre_comp_fea_df.shape)
    print('#poi_fea_df:', point_fea_df.shape)
    print('Finished Save Features!')
