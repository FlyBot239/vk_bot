import vk_api
import requests


def is_available(info):
    return 'deactivated' not in info and info['can_access_closed'] and info['blacklisted'] == 0


def fiends_of_friends(friends):
    friends_of_friends = set()
    for i in friends:
        man = n.method('users.get', {'user_ids': i, 'fields': ['blacklisted']})
        #  если аккаунт доступен
        if is_available(man[0]):
            friends_of_friends.update(n.method('friends.get', {'user_id': i})['items'])
            print('.', end='')
    friends_of_friends = {str(i) for i in friends_of_friends}
    return friends_of_friends


session = requests.Session()
# here is vk token
n = vk_api.VkApi(token="")
session_api = n.get_api()

main_guy = ""  # тут id человека, относительно которого вы хотите искать скрытых
sus =  "" # тут id человека, друзей друзей которого программа будет проверять на факт скрытия

object_friends = n.method('friends.get', {'user_id': main_guy})['items']
object_friends = {str(i) for i in object_friends}

sus_friends = n.method('friends.get', {'user_id': sus})['items']
sus_friends = {str(i) for i in sus_friends}

print(len(sus_friends))

friends_to_check = list(fiends_of_friends(sus_friends) - object_friends)
count = len(friends_to_check)

print(count // 100)
print()

for i in range(count // 100):
    print(i, end=' ')

    #  формируем список друзей на проверку(их не больше 100)
    if 100 * (i + 1) > count:
        temp_friend_to_check = friends_to_check[100 * i: count]
    else:
        temp_friend_to_check = friends_to_check[100 * i: 100 * (i + 1)]
    request = ' ,'.join(temp_friend_to_check)
    guys = n.method('users.get', {'user_ids': request, 'fields': ['blacklisted']})
    mutual_friends_request = []
    for guy in guys:
        if 'deactivated' not in guy  and guy['blacklisted'] == 0:
            mutual_friends_request.append(str(guy['id']))

    mutual_friends_request = ', '.join(mutual_friends_request)

    if mutual_friends_request == '':
        continue

    mutual_friends = n.method('friends.getMutual', {'target_uids': mutual_friends_request})
    for x in mutual_friends:
        if main_guy in x['common_friends']:
            print()
            print(x['id'])
