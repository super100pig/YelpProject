from time import sleep
from concurrent.futures import ProcessPoolExecutor
import pymysql
import scipy.sparse as sp
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from datetime import datetime
from backend.gnn_model import score_nodes
import warnings
from backend import db_setting
warnings.filterwarnings("ignore")


def get_adj(data,  node_num):
    data = np.array(data)
    left_node = data[:, 1]
    right_node = data[:, 2]
    adj_mat = coo_matrix((np.ones(len(left_node)), (left_node, right_node)), shape=(node_num, node_num), dtype=np.int)
    adj_mat = adj_mat.tocsr()
    return adj_mat


def compute_ppr(P, seeds, abnormal_scores=None, n_iter=10, alpha=0.8):
    n_seeds = len(seeds)
    n_nodes = P.shape[0]
    z = sp.csr_matrix((abnormal_scores, (np.zeros(n_seeds, dtype=int), seeds)), shape=[1, n_nodes])
    x = z.copy()
    d_scores = sp.eye(n_nodes)
    for _ in range(n_iter):
        x = alpha * x @ P + (1 - alpha) * z
        x *= d_scores
        x /= x.sum()
    return x


def get_label(data):
    data = np.array(data)
    node_list = data[:, 1]
    # node_id = data[:, 1]
    node_label = data[:, 3]
    node_path = data[:, 5]
    black_seed_list = [index for index, label in enumerate(node_label) if label == '1'] # note that label is str or int
    return node_list, node_path, black_seed_list


def get_fea(data):
    data = np.array(data)
    node_features = data[:, 2]
    fea_mat = [fea.strip().split(' ') for fea in node_features]
    fea_mat = [list(map(float, fea)) for fea in fea_mat]
    return np.array(fea_mat)


def get_from_path(node, path, node2id, id2score):
    devices = path.strip().split(',')
    nodes = [node2id[node]] + [node2id[device] for device in devices]
    left = nodes[:-1]
    right = nodes[1:]
    adj_mat = coo_matrix((np.ones(len(nodes) - 1),(left, right)), shape=(len(node2id), len(node2id)))
    adj_mat = adj_mat.tocsr()
    adj_deg = np.array(adj_mat.sum(1)).squeeze()
    inv_deg = 1 / adj_deg
    inv_deg[~np.isfinite(inv_deg)] = 0.
    transition_mat = sp.diags(inv_deg) @ adj_mat
    seeds = [node2id[node]]
    scores = [float(id2score[i]) for i in seeds]
    return transition_mat, seeds, scores


def do_some_work(run_id):
    print('Start! run_id = %s' % run_id)
    #############
    # Write the code to execute the algorithm and modify the graph here #
    # Because the code written in this function will enter the thread pool, it will not be printed when an error occurs.
    # It is recommended to use try-except to print errors, or to debug in other places before posting
    sleep(5)
    #############
    # Get adjacency matrix adj_mat, attribute matrix feature, train_pos, black_seed_list as input parameters to gcn
    # Get label information label_mat
    try:
        db = pymysql.connect(host=db_setting.host,
                             user=db_setting.user,
                             password=db_setting.password,
                             db=db_setting.db,
                             charset=db_setting.charset,
                             cursorclass=pymysql.cursors.DictCursor)
    # Get pairs of adjacent nodes and process them into an adjacency matrix
        sql = 'select * from label_mat;'
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [list(item.values()) for item in data]
        node_num = len(data)
        node_list, node_path, black_seed_list = get_label(data)
        node2id = {node:index for index, node in enumerate(node_list)}
        print('num of black_seed {}'.format(len(black_seed_list)))

    # Get the attribute matrix
        sql = 'select * from fea_mat'
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [list(item.values()) for item in data]
        node_num = len(data)
        fea_mat = get_fea(data)
        print('shape of fea_mat {}'.format(fea_mat.shape))

    # Get pairs of adjacent nodes and process them into an adjacency matrix
        sql = 'select * from adj_mat'
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [list(item.values()) for item in data]
        adj_mat = get_adj(data, node_num)
        print('shape of adj_mat {}'.format(adj_mat.shape))
        # cursor.close()

    # Run the model and return the result of the calculation
        print('begin to calculate node scores')
        _, abnormal_scores = score_nodes(adj_mat, black_seed_list, 2, 5, black_seed_list, feature_mat = fea_mat, epoch=150)
        id2score = {index:score for index, score in enumerate(abnormal_scores)}
        # Update abnormal_scores to the database
        data = [(float(score), index) for index, score in enumerate(abnormal_scores)]
        sql = 'update label_mat set score = %s where node = %s'
        cursor.executemany(sql, data)
        db.commit()
        # cursor.close()

        print('begin to calculate device scores')
        sql = 'select * from device'
        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        data = [list(item.values()) for item in data]
        device_list = np.array(data)[:, 1]
        for device in device_list:
            if node2id.get(device, -1) == -1:
                node2id[device] = len(node2id)
        result = [0 for i in device_list]
        for node, path in zip(node_list, node_path):
            transition_mat, seeds, scores = get_from_path(node, path, node2id, id2score)
            black_score = compute_ppr(transition_mat, seeds, scores).toarray().squeeze()
            temp_score = np.array([black_score[node2id[i]] for i in device_list])
            result += temp_score
        result /= max(result)
        sql = 'update device set score = %s where device_id = %s;'
        data = [(float(score), device) for device, score in zip(device_list, result)]
        cursor.executemany(sql, data)
        db.commit()

        sql = '''UPDATE algorithm SET status = 2, end_time = '%s' WHERE id = %s''' % (str(datetime.now()), run_id)
        cursor.execute(sql)
        db.commit()

        cursor.close()
        db.close()
    except Exception as e:
        print('can not run model')
        print(e)
    print('Done')


if __name__ == '__main__':
    # pool = ProcessPoolExecutor()
    # pool.submit(do_some_work)
    do_some_work(3)
    print('hello')
