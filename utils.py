
def get_text(data):
    index = 0
    final_text = ''
    while index < len(data):
        final_text += data[index]
        index = index + 1
    return final_text.replace("\t","").replace(" ", "").replace("--", "")


def to_int(str):
    try:
        return int(str)
    except:
        return None


def match_substring_recursive(needle, haystack):
    if isinstance(haystack, str):
        return needle in haystack
    else:
        return any(match_substring_recursive(needle, x) for x in haystack)


def find_index_sub_string(needle, haystack):
    return [i for i, x in enumerate(haystack) if match_substring_recursive(needle, x)]


def subarray_exist(arr, index_array):
    try:
        temp = arr
        for index in index_array:
            if len(temp) > index:
                temp = temp[index]
            else:
                return False
        return True

    except:
        return False
