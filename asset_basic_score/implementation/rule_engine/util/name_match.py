from rapidfuzz import fuzz
import re
from rapidfuzz.distance import Levenshtein


def name_match(n1, n2):
    n1 = re.sub(
        "\s+",
        " ",
        re.sub(
            "(\ss\s?o\s)|(\sw\s?o\s)|(\sd\s?o\s)|(\sc\s?o\s)",
            " ",
            re.sub("\s?mr\s", "", re.sub(r"[^a-zA-Z ]", "", n1.lower())),
        ),
    )
    n1 = n1.lower().split()
    n1_in = [i[0] for i in n1]

    n2 = re.sub(
        "\s+",
        " ",
        re.sub(
            "(\ss\s?o\s)|(\sw\s?o\s)|(\sd\s?o\s)|(\sc\s?o\s)",
            " ",
            re.sub("\s?mr\s", "", re.sub(r"[^a-zA-Z ]", "", n2.lower())),
        ),
    )
    n2 = n2.lower().split()
    n2_in = [i[0] for i in n2]

    if len(n1) < len(n2):
        if len(set(n1_in).intersection(n2_in)) == len(set(n1_in)):
            return True
        else:
            return False

    else:
        if len(set(n2_in).intersection(n1_in)) == len(set(n2_in)):
            return True
        else:
            return False


def preprocess_text(text):
    text = str(text).lower().strip()
    text = re.sub(
        "\s+",
        " ",
        re.sub(
            "(\ss\s?o\s)|(\sw\s?o\s)|(\sd\s?o\s)|(\sc\s?o\s)",
            " ",
            re.sub("\s?mr\s", "", re.sub(r"[^a-zA-Z ]", "", text.lower())),
        ),
    )
    return text


def get_similarity_class(name1, name2):
    try:
        processed_name1 = preprocess_text(name1)
        processed_name2 = preprocess_text(name2)

        distance = Levenshtein.distance(processed_name1, processed_name2)

        max_length = max(len(name1), len(name2))
        levenshtein_score = 1 - (distance / max_length)

        token_set_ratio = fuzz.token_set_ratio(processed_name1, processed_name2)

        word_ratio = len(name1.split()) / len(name2.split())

        final_match = name_match(name1, name2)

        if token_set_ratio <= 43.5:
            return "1"
        elif token_set_ratio <= 63.0:
            return "2"
        elif token_set_ratio > 63.0 and not final_match:
            return "2"
        elif levenshtein_score <= 57.98 and word_ratio > 1.75:
            return "2"
        else:
            if final_match:
                return "3"
            else:
                return "2"

    except Exception as e:
        print(e)
        return "0"