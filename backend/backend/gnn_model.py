import numpy as np
import torch
import random
from torch import nn, optim
from torch.nn import functional as F
import dgl
from dgl import function as fn
from dgl.nn.pytorch.conv import GraphConv


def get_train_neg(train_pos, n_nodes, neg_ratio, black_seed_list, neg_type='global'): #global/neighbor
    random.seed(1234)
    if neg_type=='global':
        # 全局采样
        sample_nodes = random.sample([i for i in range(n_nodes)], len(train_pos) * neg_ratio)
    # else:
    #     # 邻居节点采样
    #     sample_nodes = random.sample(black_train_node_neighbors, len(train_pos) * neg_ratio)
        
#     train_neg = list(set(sample_nodes)-set([node2id[i] for i in black_seed_list]))
#     train_neg = list(set(sample_nodes) - set(train_pos))
    train_neg = list(set(sample_nodes) - set(black_seed_list))
    return train_neg


class GCN(nn.Module):

    def __init__(self, in_size, hidden_size, n_class, n_layers=2, dropout=0.5):
        super().__init__()
        self.in_conv = GraphConv(in_size, hidden_size)
        self.hidden_convs = nn.ModuleList([GraphConv(hidden_size, hidden_size)
#                                            for _ in range(n_layers - 1)])
                                           for _ in range(n_layers - 2)])
        self.out_conv = GraphConv(hidden_size, n_class)
#         self.out_conv = nn.Linear(hidden_size, n_class)
        self.dropout = dropout

    def forward(self, g, x):
        h = F.relu(self.in_conv(g, x))
        h = F.dropout(h, self.dropout, self.training)
        for gn in self.hidden_convs:
            h = F.relu(gn(g, h))
            h = F.dropout(h, self.dropout, self.training)
        h = self.out_conv(g, h)
#         h = self.out_conv(h)
        z = F.log_softmax(h, 1)
        return z
    
    def generate(self, g, x):
        h = F.relu(self.in_conv(g, x))
        h = F.dropout(h, self.dropout, self.training)
        for gn in self.hidden_convs:
            h = F.relu(gn(g, h))
            h = F.dropout(h, self.dropout, self.training)
        return h
    

class multi_GCN(nn.Module):

    def __init__(self, in_size, hidden_size, n_class, n_layers=2, dropout=0.5):
        super().__init__()
        self.in_conv_1 = GraphConv(in_size, hidden_size)
        self.hidden_convs_1 = nn.ModuleList([GraphConv(hidden_size, hidden_size)
                                           for _ in range(n_layers - 2)])
        self.in_conv_2 = GraphConv(in_size, hidden_size)
        self.hidden_convs_2 = nn.ModuleList([GraphConv(hidden_size, hidden_size)
                                           for _ in range(n_layers - 2)])
#         self.out_conv = GraphConv(hidden_size * 2, n_class)
        self.out_conv = nn.Linear(hidden_size * 2, n_class)
        self.dropout = dropout

    def forward(self, g1, g2, x):
        h1 = F.relu(self.in_conv_1(g1, x))
        h1 = F.dropout(h1, self.dropout, self.training)
        h2 = F.relu(self.in_conv_2(g2, x))
        h2 = F.dropout(h2, self.dropout, self.training)
        for gn1, gn2 in zip(self.hidden_convs_1, self.hidden_convs_2):
            h1 = F.relu(gn1(g1, h1))
            h1 = F.dropout(h1, self.dropout, self.training)
            h2 = F.relu(gn2(g2, h2))
            h2 = F.dropout(h2, self.dropout, self.training)
        h = torch.cat([h1, h2], 1)
        h = self.out_conv(h)
        z = F.log_softmax(h, 1)
        return z
    
    def generate(self, g, x):
        h = F.relu(self.in_conv(g, x))
        h = F.dropout(h, self.dropout, self.training)
        for gn in self.hidden_convs:
            h = F.relu(gn(g, h))
            h = F.dropout(h, self.dropout, self.training)
        return h
    

# def score_nodes(adj_mat, train_pos_idx, train_neg_idx, layer_num, feature_mat = 1, epoch=20, learning_rate=1e-2):
def score_nodes(adj_mat, train_pos_idx, layer_num, neg_ratio, black_seed_list, feature_mat = 1, epoch=20, learning_rate=1e-2):
    n_nodes = adj_mat.shape[0]
#     adj_mat.cuda()
    dgl_graph = dgl.DGLGraph(adj_mat)
    print('add self loop')
    dgl_graph = dgl.add_self_loop(dgl_graph)

#     train_idx = np.concatenate([train_pos_idx, train_neg_idx])
#     train_labels = torch.cat([torch.ones(len(train_pos_idx)), torch.zeros(len(train_neg_idx))]).long()
    
    if isinstance(feature_mat, int):
        model = GCN(1, 32, 2, n_layers=layer_num)
    else:
#         feature_mat.cuda()
        model = GCN(feature_mat.shape[1], 32, 2, n_layers=layer_num)
    
    optimizer = optim.Adam(model.parameters(), learning_rate)
    
    loss_fn = nn.NLLLoss()
    if isinstance(feature_mat, int):
        x = torch.ones((n_nodes, 1))
    else:
        x = torch.from_numpy(feature_mat).float()
    model.train()
    for it in range(epoch):
        train_neg_idx = get_train_neg(train_pos_idx, n_nodes, neg_ratio, black_seed_list, neg_type='global')
        train_idx = np.concatenate([train_pos_idx, train_neg_idx])
        train_labels = torch.cat([torch.ones(len(train_pos_idx)), torch.zeros(len(train_neg_idx))]).long()
    
    
        optimizer.zero_grad()
        logits = model(dgl_graph, x)
        loss = loss_fn(logits[train_idx], train_labels)
        loss.backward()
        optimizer.step()
        if it % 10 == 0:
            print(f"Iteration {it:4d} Loss={loss.item():.4f}")
        
    model.eval()
    with torch.no_grad():
        logits = model(dgl_graph, x)
        probs = torch.exp(logits[:, 1])
        embs = model.generate(dgl_graph, x)

#     return embs.cpu().numpy(), probs.cpu().numpy()
    return train_idx, probs.cpu().numpy()


def save_embs(embs, emb_path):
    # Save embeddings
    emb_df = pd.DataFrame(embs, columns= ['DIM'+str(i) for i in range(32)])
    emb_df.insert(0,'Id',node_label.keys()) 
    emb_df.to_csv(emb_path, index = None) 
    return 