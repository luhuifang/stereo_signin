import os
def get_file_list(file_dir, shuffix='.txt'):
    res = []
    if os.path.exists(file_dir) and os.path.isdir(file_dir):
        for i in os.listdir(file_dir):
            path = os.path.join(file_dir,i)
            if os.path.isfile(path) and path.endswith(shuffix):
                res.append(path)
    sorted_res = sorted(res)
    return sorted_res

def get_dir_from_search_str(url_search):
    search = url_search_to_dict(url_search)
    return url_search_to_dir(search)

def url_search_to_dict(url_search):
    tmp = url_search.lstrip('?').split('&')
    search_dict = {}
    for i in tmp:
        t = i.split('=')
        search_dict[t[0]] = t[1]
    return search_dict

def url_search_to_dir(search):
    file_dir = ''
    if 'DataID' in search :
        file_dir = dataID_to_dir(search['DataID'])
    return file_dir

def dataID_to_dir(DataID):
    if DataID.startswith('DATA_'):
        return Data(data_id=DataID).getResultPath()
    else:
        return DataID