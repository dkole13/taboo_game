import json
from core_utils.constants import ASSETS_PATH


def check_format(words_file_1: dict, words_file_2: dict) -> None:
    whole_list = []
    for k_1, v_1 in words_file_1.items():
        if len(v_1) != 5:
            print(f'{k_1}: {v_1}')
            continue
        whole_list.append({"word": k_1,
                           "taboo_word_1": v_1[0],
                           "taboo_word_2": v_1[1],
                           "taboo_word_3": v_1[2],
                           "taboo_word_4": v_1[3],
                           "taboo_word_5": v_1[4]})

    for k_2, v_2 in words_file_2.items():
        if len(v_2) != 5:
            print(f'{k_2}: {v_2}')
            continue
        whole_list.append({"word": k_2,
                           "taboo_word_1": v_2[0],
                           "taboo_word_2": v_2[1],
                           "taboo_word_3": v_2[2],
                           "taboo_word_4": v_2[3],
                           "taboo_word_5": v_2[4]})

    print(len(whole_list))
    with open(ASSETS_PATH / "all_words.json", 'w', encoding='utf-8') as file_to_save:
        json.dump(whole_list, file_to_save, indent=4, ensure_ascii=False)


def main():
    with open(ASSETS_PATH / "filled_words_correct.json", 'r', encoding='utf-8') as file_to_read:
        file_1 = json.load(file_to_read)
    with open(ASSETS_PATH / "problem_words_correct.json", 'r', encoding='utf-8') as file_to_read:
        file_2 = json.load(file_to_read)

    check_format(file_1, file_2)


if __name__ == "__main__":
    main()
