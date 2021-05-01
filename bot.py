from functions import *

connection = make_connection("")

main_guy = 378102106  # тут id человека, относительно которого вы хотите искать скрытых
sus = 378102106  # тут id человека, друзей друзей которого программа будет проверять на факт скрытия

object_friends = get_friends(connection, main_guy)
sus_friends = get_friends(connection, sus)

print(len(sus_friends))

friends_to_check = list(friends_of_friends(connection, sus_friends) - object_friends)
count = len(friends_to_check)
print()
print((count + 99) // 100)

for i in range((count + 99) // 100):
    print(i, end=' ')

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
