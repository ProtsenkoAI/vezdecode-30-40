from elems import Elem
from functions import *
from get_html_features import get_features

from typing import List, Dict
import numpy as np
import sys
import json


def get_pair_vector(repr1: List[Elem], repr2: List[Elem]) -> np.array:
    features = [
        iou(repr1, repr2),
        hrefs_iou(repr1, repr2),
        intersection_inversions_index(repr1, repr2),
        component_types_mismatch(repr1, repr2),
        words_similarity(repr1, repr2)
    ]
    return np.array(features)


def calc_sim(vector: np.array, lin_reg_params: Dict[str, float]) -> float:
    idx_to_feature_name = {
        0: "iou",
        1: "hrefs_iou",
        2: "inversions_index",
        3: "comp_mismatch",
        4: "words"
    }
    accum = sum([lin_reg_params[idx_to_feature_name[idx]] * vec_val for idx, vec_val in enumerate(vector)])
    accum += lin_reg_params["bias"]
    return accum


def compare(path_html: str, pathes_references: List[str], ref2website):
    html_repr = get_features(path_html)
    with open("fitted_lr_weights.json") as f:
        lin_reg_params = json.load(f)

    best_match, max_similarity = None, 0
    for path in pathes_references:
        ref_repr = get_features(path)
        vector = get_pair_vector(html_repr, ref_repr)

        print(f"Вектор пары {path_html} и {path}:")
        print(vector)
        print()

        similarity = calc_sim(vector, lin_reg_params)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = path_html, path
        print("Похожесть векторов:")
        print(similarity)
        print()

    print(f"Скорее всего страница {path_html} принадлежит сайту {ref2website[best_match[1]]}")


if __name__ == "__main__":
    references = ["data/Введите номер телефона МТС.html",
                  "data/Интернет-банк «Альфа-Клик».html",
                  "data/Вход - СберБанк Онлайн.html",
                  "data/Sign in _ VK.html",
                  "data/Raiffeisen Online.html"
                  ]

    ref2website = dict(zip(references, ["МТС", "Альфа банк", "Сбербанк", "ВК", "Райффайзен банк"]))

    compare(sys.argv[1], references, ref2website)
