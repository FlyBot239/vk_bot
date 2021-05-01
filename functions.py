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
            print('.', end='')
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
    if mutual_friends_request == '':
        return []

    return connection.method('friends.getMutual', {'target_uids': mutual_friends_request})
