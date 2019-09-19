import vk_api

vk_session = vk_api.VkApi('', '')  # для корректной работы введите свой номер телефона и пароль
vk_session.auth()
vk = vk_session.get_api()

id_u = 364019336  # id юзера
id_g = -146469497  # id группы
f = open('resultJEWISH.txt', 'w')

# Проходим по постам, собирая их id
off_posts = 0  # смещение для постов
posts_num = vk.wall.get(owner_id=id_g)['count']  # количество постов в группе
list_post_id = []  # список всех id постов
while off_posts < posts_num:  # пока смещение меньше кол-ва постов
    if posts_num - off_posts > 100:  # пока не достигли края берём максимум
        count_posts = 100
    else:  # иначе берём остаток постов
        count_posts = posts_num - off_posts
    posts = vk.wall.get(owner_id=id_g, offset=off_posts, count=count_posts)  # список всех постов на данной итерации
    for i in range(count_posts):  # добавляем в список id постов
        list_post_id.append(posts['items'][i]['id'])
    off_posts += 100
    print(off_posts)

# Проходим по постам, собирая комменты
list_comm_id = []
for k in range(len(list_post_id)):
    id_p = list_post_id[k]  # берём текущий id поста
    comments_num = vk.wall.getComments(owner_id=id_g,
                                       post_id=id_p)['count']  # кол-во комментариев к посту
    off_comments = 0  # смещение у комментариев
    while off_comments < comments_num:  # пока смещение меньше кол-ва комментариев
        if comments_num - off_comments > 100:  # пока не достигли края берём максимум
            count_comments = 100
        else:  # иначе берём остаток комментариев
            count_comments = comments_num - off_comments
        comments = vk.wall.getComments(owner_id=id_g, post_id=id_p,
                                       count=count_comments)  # список всех комментариев на данной итерации
        for i in range(len(comments['items'])):  # проходим по id комментариям
            if comments['items'][i].get('from_id') and \
                    comments['items'][i]['from_id'] == id_u:  # если пост от нужного юзера
                f.write(comments['items'][i]['text'] + '\n')  # заносим его в файл
            if vk.wall.getComments(owner_id=id_g,
                                   comment_id=comments['items'][i]['id'])['count']:  # если пост имеет тред
                list_comm_id.append(comments['items'][i]['id'])  # заносим его на дальнейшее рассмотрение
        off_comments += 100
    print('{}/{}'.format(k, len(list_post_id)))

# Смотр комментариев в тредах
for k in range(len(list_comm_id)):
    id_c = list_comm_id[k]  # берём текущий id комментария
    curr_comm_num = vk.wall.getComments(owner_id=id_g,
                                        comment_id=id_c)['count']  # кол-во комментариев в треде
    off_curr_comm = 0  # смещение по комментариям в треде
    while off_curr_comm < curr_comm_num:  # пока смещение меньше кол-ва комментариев в трелде
        if curr_comm_num - off_curr_comm > 100:  # пока не достигли края
            count_curr_comm = 100  # берём максимум
        else:
            count_curr_comm = curr_comm_num - off_curr_comm
        curr_comm = vk.wall.getComments(owner_id=id_g, comment_id=id_c, count=count_curr_comm)
        for i in range(len(curr_comm['items'])):
            if curr_comm['items'][i].get('from_id') and curr_comm['items'][i]['from_id'] == id_u:
                f.write(curr_comm['items'][i]['text'] + '\n')  # записываем в файл, если коммент от нужного юзера
        off_curr_comm += 100
    print('{}/{}'.format(k, len(list_comm_id)))
f.close()
