def calculate(data, findall):
    matches = findall(r"([abc])([-+]?=)([abc]?)([+-]?\d*)")
    for v1, s, v2, n in matches:
        tmp_result = data.get(v2, 0) + int(n or 0)

        if s[0] == '+':
            data[v1] += tmp_result
        elif s[0] == '-':
            data[v1] -= tmp_result
        else:
            data[v1] = tmp_result

    return data