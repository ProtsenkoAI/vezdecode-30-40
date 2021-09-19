from collections import defaultdict, Counter
from typing import List
from elems import Elem


def iou(lst1, lst2):
    intersected = 0

    for elem in lst1:
        if elem in lst2:
            intersected += 1

    return intersected / (len(lst1) + len(lst2) - intersected)


def get_hrefs(elems: List[Elem]):
    hrefs = []
    for elem in elems:
        if hasattr(elem, "href"):
            if elem.href is not None:
                hrefs.append(elem.href)
    return hrefs


def hrefs_iou(repr1: List[Elem], repr2: List[Elem]):
    return iou(get_hrefs(repr1), get_hrefs(repr2))


def intersection_inversions_index(repr1: List[Elem], repr2: List[Elem]):
    inter_idxs1, inter_idxs2 = [], []

    for idx1, elem in enumerate(repr1):
        if elem in repr2:
            inter_idxs1.append(idx1)
            inter_idxs2.append(repr2.index(elem))

    #     print(inter_idxs1, inter_idxs2)
    # cnt inversions
    nb_invs = 0
    nb_pairs = 0
    for idx, position in enumerate(inter_idxs1):
        for position2 in inter_idxs2[idx + 1:]:
            if position2 < position:
                nb_invs += 1
            nb_pairs += 1

    if nb_pairs == 0:
        return 1  # biggest value because have no any order between intersecting orders

    return nb_invs / nb_pairs


def component_types_mismatch(repr1, repr2):
    categ2cnt = defaultdict(int)

    for elem in repr1:
        categ2cnt[elem.category] += 1
    for elem in repr2:
        categ2cnt[elem.category] -= 1

    return sum([abs(val) for val in categ2cnt.values()]) / (len(repr1) + len(repr2))


def words_similarity(repr1, repr2):
    texts1 = []
    for elem in repr1:
        if elem.category == "text":
            texts1.append(elem.text)
    texts2 = []
    for elem in repr2:
        if elem.category == "text":
            texts2.append(elem.text)

    cnter1 = Counter(" ".join(texts1).split())
    cnter2 = Counter(" ".join(texts2).split())
    sum1 = sum(cnter1.values())
    sum2 = sum(cnter2.values())

    # normalization
    for key, value in cnter1.items():
        cnter1[key] = value / sum1
    for key, value in cnter2.items():
        cnter2[key] = value / sum2

    #     print(cnter1, "\n", cnter2)

    return sum((cnter1 & cnter2).values()) / sum((cnter1 | cnter2).values())