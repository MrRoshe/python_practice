import requests


def get_uid(id, token):
    result = requests.get('https://api.vk.com/method/users.get?v=5.71&access_token=' + token + '&user_ids=' + id)

    tmp_dict = dict(result.json())
    tmp_dict = tmp_dict.get('response')
    uid = tmp_dict[0].get('id')

    return uid


def get_friends(uid, token):
    result = requests.get('https://api.vk.com/method/friends.get?v=5.71&access_token=' + token + '&user_id=' + str(uid) + '&fields=bdate')

    tmp_dict = dict(result.json())
    tmp_dict = tmp_dict.get('response')
    friends = tmp_dict.get('items')
    return friends


def calc_age(friends):
    result = list()
    list_of_age = list()

    for man in friends:
        if isinstance(man, dict):
            bd = man.get('bdate')

            if bd and len(bd) > 5:
                bd = list(bd.split('.'))
                age = 2021 - int(bd[2])
                list_of_age.append(age)

    tmp_set = set(list_of_age)

    for item in tmp_set:
        result.append((item, list_of_age.count(item)))

    return sorted(result, key=lambda x: (-x[1], x[0]))


id = 'reigning'
token = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'

uid = get_uid(id, token)
friends = get_friends(uid, token)
print(calc_age(friends))
