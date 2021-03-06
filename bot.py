import vk_api


def make_connection(token):
    # here is vk token
    return vk_api.VkApi(token=token)


def is_available(info):
    return 'deactivated' not in info and info['can_access_closed'] and info['blacklisted'] == 0


def friends_of_friends(connection, friends):
    set_friends_of_friends = set()
    for friend in friends:
        man = connection.method('users.get', {'user_ids': friend, 'fields': ['blacklisted']})
        #  если аккаунт доступен
        if is_available(man[0]):
            set_friends_of_friends.update(connection.method('friends.get', {'user_id': friend})['items'])
            print('.')
    set_friends_of_friends = {str(fr) for fr in set_friends_of_friends}
    return set_friends_of_friends


def get_friends(connection, man_id):
    friends = connection.method('friends.get', {'user_id': man_id})['items']
    return {str(fr) for fr in friends}


def list_of_mutual_friends(connection, friend):
    request = ' ,'.join(friend)
    guys = connection.method('users.get', {'user_ids': request, 'fields': ['blacklisted']})
    mutual_friends_request = []
    for guy in guys:
        if 'deactivated' not in guy and guy['blacklisted'] == 0:
            mutual_friends_request.append(str(guy['id']))

    mutual_friends_request = ', '.join(mutual_friends_request)
    if not mutual_friends_request:
        return []

    return connection.method('friends.getMutual', {'target_uids': mutual_friends_request})


if __name__ == "__main__":
    file = open('information.txt', 'r')
    text = file.read().split('\n')
    file.close()

    token = text[0].split(':')[1].strip()
    main_guy = int(text[1].split(':')[1].strip())
    sus = int(text[2].split(':')[1].strip())

    connection = make_connection(token)

    object_friends = get_friends(connection, main_guy)
    sus_friends = get_friends(connection, sus)

    print(len(sus_friends))

    friends_to_check = list(friends_of_friends(connection, sus_friends) - object_friends)
    count = len(friends_to_check)
    print()
    print((count + 99) // 100)

    for i in range((count + 99) // 100):
        print(i)

        #  формируем список друзей на проверку(их не больше 100)
        if 100 * (i + 1) > count:
            temp_friend_to_check = friends_to_check[100 * i: count]
        else:
            temp_friend_to_check = friends_to_check[100 * i: 100 * (i + 1)]

        mutual_friends = list_of_mutual_friends(connection, temp_friend_to_check)
        for x in mutual_friends:
            if main_guy in x['common_friends']:
                print()
                print("https://vk.com/id" + str(x['id']))
