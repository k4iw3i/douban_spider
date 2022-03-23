headers = {
    # 'Cookie': '__utma=30149280.917381604.1647595336.1647858061.1647867394.4; __utmb=30149280.2.9.1647867563632; __utmc=30149280; __utmt=1; __utmv=30149280.22368; __utmz=30149280.1647595336.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=D197E5AD86C5537F4421454080B50B372|8d770bef82b4b729c01cb2347cd042cc; ap_v=0,6.0; __utma=223695111.1503300051.1647595399.1647858061.1647867394.4; __utmb=223695111.1.10.1647867394; __utmc=223695111; __utmt=1; __utmz=223695111.1647851349.2.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=2c66cf48e9a07245.1647595399.4.1647867394.1647861219.; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1647867394%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; push_doumail_num=0; push_noty_num=0; _ga=GA1.2.917381604.1647595336; __gads=ID=177d07a4759538d8-22b4a56711d100ef:T=1647596035:RT=1647596035:S=ALNI_Ma3c_H-munar0wCkA3wyaHGHMNbag; __yadk_uid=lyDsCoDcuGCeIZaWc35KvkoNyinlA6hh; ll="108296"; bid=QjHdiUcUpdQ',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Host': 'movie.douban.com',
    # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8',
    'Referer': 'https://movie.douban.com/tag/',
    'Connection': 'keep-alive'
}

proxies = {
    'http':'http://lum-customer-c_b6d0914a-zone-static:mjzgox0ez4ze@zproxy.lum-superproxy.io:22225', 
    'https':'http://lum-customer-c_b6d0914a-zone-static:mjzgox0ez4ze@zproxy.lum-superproxy.io:22225'
}

def fetch_ua_list(input_file = '../ua_list.txt'):
    with open(input_file, 'r') as f:
        ua_list = [x.replace('\n', '') for x in f.readlines()]
    return ua_list

login_headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer': 'https://accounts.douban.com/passport/login_popup?login_source=anony',
    'Origin': 'https://accounts.douban.com',
    'content-Type':'application/x-www-form-urlencoded',
    'x-requested-with':'XMLHttpRequest',
    'accept':'application/json',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'connection': 'keep-alive',
    'Host': 'accounts.douban.com'
}