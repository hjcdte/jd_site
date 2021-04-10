def send_content(data):
    content = dict()
    content_list = list()

    content_list.append(data)

    content['data'] = content_list

    return content