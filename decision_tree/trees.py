import operator
from math import log
import tree_plotter


def calc_shannon_ent(data_set):
    num_entries = len(data_set)
    lables_count = {}
    for feat_vet in data_set:
        current_lable = feat_vet[-1]
        if current_lable not in lables_count.keys():
            lables_count[current_lable] = 0
        lables_count[current_lable] += 1

    shannon_ent = 0.0

    for key in lables_count:
        prob = float(lables_count[key])/num_entries
        shannon_ent -= prob*log(prob, 2)

    return shannon_ent


def split_dataset(data_set, axis, value):
    ret_dataset = []
    for feat_vet in data_set:
        if feat_vet[axis] == value:
            reduce_feat_vet = feat_vet[:axis]
            reduce_feat_vet.extend(feat_vet[axis+1:])
            ret_dataset.append(reduce_feat_vet)
    return ret_dataset


def choose_best_feature_to_split(data_set):
    num_featers = len(data_set[0]) - 1
    base_entropy = calc_shannon_ent(data_set)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_featers):
        feat_list = [example[i] for example in data_set]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_dataset(data_set, i, value)
            prob = len(sub_data_set)/float(len(data_set))
            new_entropy += prob*calc_shannon_ent(sub_data_set)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
            class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count


def create_tree(data_set, labels):
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]
    if len(data_set[0]) == 1:
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(data_set)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label: {}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in data_set]
    unique_vls = set(feat_values)
    for value in unique_vls:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = create_tree(split_dataset(data_set, best_feat, value),
                                                  sub_labels)
    return my_tree


if __name__ == '__main__':
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lenses_labels = ['age', 'prescript', 'astigmatic', 'tear_rate']
    my_tree = create_tree(lenses, lenses_labels)
    tree_plotter.create_plot(my_tree)


