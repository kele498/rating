def get_luogu_url_uid(uid):
    return "https://www.luogu.com.cn/user/" + str(uid) + "?_contentOnly"


def get_cf_url(name):
    url = "https://codeforces.com/profile/" + name + "/"
    return url

def get_niuke_url(niuid):
    return "https://ac.nowcoder.com/acm/contest/profile/" + str(niuid) + "/practice-coding"

def get_atcoder_url(atcoder_name):
    return "https://kenkoooo.com/atcoder/atcoder-api/results?user=" + atcoder_name
