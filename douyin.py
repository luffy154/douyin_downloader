# -*- coding: utf-8 -*-

import os
import json
import re
import time
import getopt
import sys
import queue as Queue
from random import randrange
from random import randint
from requests_html import HTMLSession
from threading import Thread

from local_file_adapter import LocalFileAdapter

MOBIE_HEADERS = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
        'DNT': '1',
        'Cookie':'__ac_referer=__ac_blank; douyin.com; webcast_local_quality=null; ttwid=1%7CiHXJOGpNyZzFe-gTbaNsu79WGr4QYWSS2aEfFr7Hj-U%7C1694440885%7C98ca7ba07b3616a6f0dcd7ecf56f80a76024de6ec50923730b469289c3ecb4ff; ttcid=f43375acd3a14cde96708255116e069180; passport_csrf_token=72cb7beff2501ec6633a637e16a9bac9; passport_csrf_token_default=72cb7beff2501ec6633a637e16a9bac9; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; download_guide=%223%2F20230912%2F0%22; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; webcast_local_quality=null; s_v_web_id=verify_lmhnc7ml_Q7xfi10X_X0ov_4XWE_AOCD_TlQ5Z8rmfNrb; csrf_session_id=cc64ecc7dcd24bcba985e2bb5b5a013f; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSThTLzY4ZWJDeGEvbk1BVTNjdUNUZFZvTjZiYXFncTd2NHpJMTA4Mm9xd2JQaXJhRTNJY2ZONC9mRVdtZmp6enRicWh1dW9nMzdGZXhueVBTeDlHNGM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ==; SEARCH_RESULT_LIST_TYPE=%22single%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1695210330415%2C%22type%22%3A1%7D; xgplayer_user_id=942582254717; passport_assist_user=CkGg0GosveXmTYH0JCfkzGHhCdoFbOMi-dtGLHud42YMUkTE6ZDSVDKbs98jEYN_8IOQFm5CVWJnH27NCkCwqdpTLRpKCjwsFwzhY22FacZ-N589iqbQgiM2rQzRoZDPmZsCCARcnAhIY29poMcYCBx9Xgf1TeSt1yKkfCSrNR4EkLIQp-m7DRiJr9ZUIAEiAQN6pJLj; n_mh=06X79phbPeCwNYqG8blTaVUwD31it3lHrnLDrXS1W5I; sso_uid_tt=687beffd2f9c7bf196d15429bb7504b9; sso_uid_tt_ss=687beffd2f9c7bf196d15429bb7504b9; toutiao_sso_user=76b05724a74c714fe4933916c58ba156; toutiao_sso_user_ss=76b05724a74c714fe4933916c58ba156; sid_ucp_sso_v1=1.0.0-KGM1Y2Y1YmVhODM5NTcwNmM1NjUyM2RiNGM5Nzc0ODE0NzZmYWFlMGQKHwjtpfCRtY2hBhCTw4aoBhjvMSAMMKnG1JUGOAZA9AcaAmhsIiA3NmIwNTcyNGE3NGM3MTRmZTQ5MzM5MTZjNThiYTE1Ng; ssid_ucp_sso_v1=1.0.0-KGM1Y2Y1YmVhODM5NTcwNmM1NjUyM2RiNGM5Nzc0ODE0NzZmYWFlMGQKHwjtpfCRtY2hBhCTw4aoBhjvMSAMMKnG1JUGOAZA9AcaAmhsIiA3NmIwNTcyNGE3NGM3MTRmZTQ5MzM5MTZjNThiYTE1Ng; odin_tt=f96c8146f2f96b1ad1465a7d56a119c174b53cce3241a49f0a8a731f8156c4bd8e67e1f8e93d3e36383d01a052a4f6b7b9d8fc3b406e749aa54e4ea79f40a911; passport_auth_status=2f1da1f03f319a254fc80a123aed87a4%2C; passport_auth_status_ss=2f1da1f03f319a254fc80a123aed87a4%2C; uid_tt=da8e93a1f17c86d860b8648a2978d528; uid_tt_ss=da8e93a1f17c86d860b8648a2978d528; sid_tt=b8a931fca7135d2ec661fbfb051d028c; sessionid=b8a931fca7135d2ec661fbfb051d028c; sessionid_ss=b8a931fca7135d2ec661fbfb051d028c; LOGIN_STATUS=1; store-region=us; store-region-src=uid; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=ee5a25d12a952ca74d43b3526fb21b0d; __security_server_data_status=1; sid_guard=b8a931fca7135d2ec661fbfb051d028c%7C1694605724%7C5183994%7CSun%2C+12-Nov-2023+11%3A48%3A38+GMT; sid_ucp_v1=1.0.0-KGYxNDhhNGM2MzhiYzkyNTFmMjFlN2MyNmJmZDZmOThmMjZmMDIzNDUKGwjtpfCRtY2hBhCcw4aoBhjvMSAMOAZA9AdIBBoCbGYiIGI4YTkzMWZjYTcxMzVkMmVjNjYxZmJmYjA1MWQwMjhj; ssid_ucp_v1=1.0.0-KGYxNDhhNGM2MzhiYzkyNTFmMjFlN2MyNmJmZDZmOThmMjZmMDIzNDUKGwjtpfCRtY2hBhCcw4aoBhjvMSAMOAZA9AdIBBoCbGYiIGI4YTkzMWZjYTcxMzVkMmVjNjYxZmJmYjA1MWQwMjhj; my_rd=1; _tea_utm_cache_2018={%22utm_source%22:%22weixin%22%2C%22utm_medium%22:%22aweme_ios%22%2C%22utm_campaign%22:%22client_share%22}; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAR0Xl8yxlb-B0BcwGiwtmHwI__3EmAKTt9yh69pg4yNQjfowxCMqxCGl7I2Z-1N01%2F1694620800000%2F0%2F0%2F1694611012361%22; __ac_nonce=065026ee000d4e1092fe0; __ac_signature=_02B4Z6wo00f01NmtybAAAIDAQcZew8TkXljZjc0AAFNujAkiuJEBqeIZuLvQtrJsbBKAVle0DmdsmrcB2gd9koR3VObnyJBtY0PNpuB.S-DTQ4hWAbRwDun0dvUkTKP1FHPa6ANxYIEJCaKb2e; strategyABtestKey=%221694658292.08%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.35%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A550%7D%22; home_can_add_dy_2_desktop=%221%22; msToken=pFO16qpcE-RCM52uaolptWaXh7V7ANzsSThiTWhcjFuGYy9Vc26qeuJCI2HxcaWKXaYbU4d-OoJ48UQSa3_WMOabOCm9gC6iR-mL2qLmYb8ea-GzuzDO; tt_scid=WjFGFLMtvv2f4g5zanyuW72jq-4nJShRRjUziQjNnBxxcGHbYbCluyOkjVR1qVzac580; msToken=LQ9ZTtMRxkclixww6iuJ_TkxJyQiw5GkSw3uZ9shtkZQJDyME8Ndd3z5gq4eW8TXZ4NNTUTF3lxOthlq50PlNKQuceLNikdKa0ZPBWCmfQf2aLzXCJ0S; publish_badge_show_info=%221%2C0%2C0%2C1694658348195%22; IsDouyinActive=false; passport_fe_beating_status=false',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1'

}

DOWNLOAD_HEADERS = {
    'authority': 'aweme.snssdk.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'dnt': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
}

# 线程数
THREADS = 10

# 重试次数
RETRY = 3

# 固定签名
FREEZE_SIGNATURE = None

# 视频播放地址
PLAY_URL = 'https://aweme.snssdk.com/aweme/v1/play/'

# 用户主页链接
USER_HOME_URL = 'https://www.douyin.com/user/'

# 用户视频列表地址
POST_LIST_URL = 'https://www.iesdouyin.com/web/api/v2/aweme/post/'

# 用户收藏视频地址
LIKE_LIST_URL = 'https://www.iesdouyin.com/web/api/v2/aweme/like/'

# 单视频信息地址
ITEM_INFO_URL = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/'

# 分享链接前缀
SHARE_HOST = 'v.douyin.com'

# 下载链接前缀
DOWNLOAD_HOST = 'www.iesdouyin.com'

def get_user_info(user_id):
    """获取用户的uid和dytk信息

    @param: user_id
    @return [uid, dytk]
    """

    with HTMLSession() as session:
        MOBIE_HEADERS['Host'] = DOWNLOAD_HOST
        r = session.get(USER_HOME_URL + str(user_id), headers=MOBIE_HEADERS)
        print(r.html.text)
        uid = r.html.search('uid: "{uid}"')['uid']
        dytk = r.html.search("dytk: '{dytk}'")['dytk']
        return [uid, dytk]

def get_signature(user_id):
    """获取所需的签名信息
    
    @oaram: user_id
    @return: signature
    """
    
    with HTMLSession() as session:    
        signature_url = 'file://' + os.getcwd() + os.sep +'signature.html?user_id=' + str(user_id)
        session.mount("file://", LocalFileAdapter())
        r = session.get(signature_url, headers=MOBIE_HEADERS)
        r.html.render()
        sign = r.html.find('#signature', first=True)
        r.close()
        return sign.text

def get_list_by_uid(user_id, dytk, cursor=0, favorite=False):
    """获取用户视频列表信息

    @param: user_id
    @param: dytk
    @param: cursor,用于列表分页定位
    @return json
    """
    
    global FREEZE_SIGNATURE
    '''读取数据文件,若存在则直接返回'''
    file_result = load_from_json_file(user_id, cursor, favorite)
    if file_result:
        return file_result

    if favorite:
        url = LIKE_LIST_URL
    else:
        url = POST_LIST_URL    
    
    '''获取签名'''
    signature = FREEZE_SIGNATURE if FREEZE_SIGNATURE else get_signature(user_id)
    headers = {
        **DOWNLOAD_HEADERS,
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json'
    }
    params = {
        'user_id': user_id,
        'count': 30,
        'max_cursor': cursor,
        'app_id': 1128,
        '_signature': signature,
    }
    with HTMLSession() as session:
        while True:
            r = session.get(url, params=params, headers=headers)
            if r.status_code != 200:
                print(r)
                continue
            r.html.render()
            res_json = json.loads(r.html.text)
            r.close()
            if res_json.get('max_cursor', None):
                FREEZE_SIGNATURE = signature
                save_json_data(user_id, cursor, res_json, favorite)
                return res_json
            print("get empty list, " + str(res_json))
            time.sleep(randint(1, 5))
            print('retry...')
        
def save_user_video(url, user_id, video_id, favorite=False):
    """保存视频至当前video目录下对应的用户名目录

    @param: url
    @param: user_id
    @param: video_id
    @param: favorite 是否是收藏视频
    @return None
    """
    
    if url is None:
        print('Error: can not get the download url!')
        return
    
    if favorite:
        folder, video_name = get_user_favorite_video_info(user_id, video_id)
    else:
        folder, video_name = get_user_own_video_info(user_id, video_id)
    video_path = os.path.join(folder, video_name)
    
    if not os.path.exists(video_path):
        url = custom_format_download_url(url)
        print('start to download the video, url: ' + url)

        retry_times = 0
        session = HTMLSession()
        while retry_times < RETRY:
            try:
                res = session.get(url, headers=DOWNLOAD_HEADERS, allow_redirects = False)
                if res.status_code == 200:
                    with open(video_path, "wb") as fp:
                        for chunk in res.iter_content(chunk_size=1024):
                            fp.write(chunk)
                    print('save video success, path: ' + video_path)
                    break
                elif res.status_code == 302:
                    url = res.headers['location']
                    raise Exception('url redirects')
                else:  
                    raise Exception('request to download the video error, url' + url)
            except:
                pass 
            retry_times += 1
        else:
            try:
                os.remove(video_path)
            except OSError:
                pass
            print('Failed to download the video, url: ' + url)
    else:
        print("video already downloaded, skip!")
        pass

def custom_format_download_url(url):
    """自定义替换下载链接中的部分参数
    
    @param: url download_url
    @return url
    """

    url = url.replace('watermark=1', 'watermark=0')
    ratio = re.compile(r'ratio=(\d+)p')
    url = ratio.sub('ratio=720p', url)
    return url

def save_json_data(user_id, cursor, data, favorite=False):
    """保存用户视频列表的json数据

    @param: user_id
    @param: cursor
    @param: data json
    @param: favorite 是否是收藏视频
    @return None
    """
    if favorite:
        folder, file_name = get_user_favorite_data_info(user_id, cursor)
    else:
        folder, file_name = get_user_own_data_info(user_id, cursor)

    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w+', encoding='utf-8') as fb:
        json.dump(data, fb, ensure_ascii=False)
    print("list data save success!")

def load_from_json_file(user_id, cursor, favorite=False):
    """检查对应的data数据，查看是否已存在对应记录数据

    @param: user_id
    @param: cursor
    @param: favorite 是否是收藏视频
    @return json
    """

    if favorite:
        folder, file_name = get_user_favorite_data_info(user_id, cursor)
    else:
        folder, file_name = get_user_own_data_info(user_id, cursor)

    file_path = os.path.join(folder, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)
    return None

def get_user_own_data_info(user_id, cursor):
    """获取用户视频数据的地址信息

    @param: user_id
    @cursor: 分页游标
    @return: （target_folder, file_name）
    """

    file_name = str(user_id) + '-' + str(cursor) + '.json'
    folder = os.path.join(os.getcwd(), 'data')
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    except:
        pass
    return (folder, file_name)

def get_user_favorite_data_info(user_id, cursor):
    """获取用户收藏视频数据的地址信息

    @param: user_id
    @cursor: 分页游标
    @return: （target_folder, file_name）
    """

    file_name = str(user_id) + '-favorite-' + str(cursor) + '.json'
    folder = os.path.join(os.getcwd(), 'data')
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    except:
        pass
    return (folder, file_name)

def get_user_own_video_info(user_id, video_id):
    """获取用户自己视频的地址信息

    @param: user_id
    @param: video_id
    @return: （target_folder, file_name）
    """

    file_name = str(video_id) + '.mp4'
    folder = os.path.join(os.getcwd(), 'video', str(user_id))
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    except:
        pass
    return (folder, file_name)

def get_user_favorite_video_info(user_id, video_id):
    """获取用户收藏视频的地址信息

    @param: user_id
    @param: video_id
    @return: （target_folder, file_name）
    """

    file_name = str(video_id) + '.mp4'
    folder = os.path.join(os.getcwd(), 'video', 'favorite', str(user_id))
    try:
        if not os.path.isdir(folder):
            os.mkdir(folder)
    except:
        pass
    return (folder, file_name)

def get_real_link_from_share_link(url):
    """从分享链接获取真实跳转地址

    @param: url 抖音分享的链接
    @return: url 跳转后的链接
    """

    if url.find('v.douyin.com') < 0:
        return url
    session = HTMLSession()

    MOBIE_HEADERS['Host'] = SHARE_HOST
    res = session.get(url, headers=MOBIE_HEADERS, allow_redirects=False)
    if res.status_code == 302:
        new_url = res.headers['location']
        return new_url
    return url

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url, user_id, video_id, favorite = self.queue.get()
            if url is None:
                print('exit Thread!')
                break

            save_user_video(url, user_id, video_id, favorite)
            self.queue.task_done()

class CrawlerScheduler(object):

    def __init__(self, items, favorite=False):
        self.user_ids = []
        for i in range(len(items)):
            url = get_real_link_from_share_link(items[i])
            if not url:
                continue
            if url.find('/share/video/') > 0:
                url = self._get_user_link_from_video(url)
            number = re.findall(r'/share/user/(\w+)', url)
            if not len(number):
                continue
            self.user_ids.append(number[0])
        self.queue = Queue.Queue()
        self.scheduling(favorite)

    def scheduling(self, favorite=False):
        threads = []
        for _ in range(THREADS):
            worker = DownloadWorker(self.queue)
            worker.start()
            threads.append(worker)
        for user_id in self.user_ids:
            self.download_user_videos(user_id, favorite)
 
        self.queue.join()
        for _ in range(THREADS):
            self.queue.put((None, None, None, None))
        for t in threads:
            t.join()
        print("successful downloaded!")

    def download_user_videos(self, user_id, favorite=False):
        """下载用户所有视频

        @param: user_id
        @param: favorite
        @return
        """

        uid, dytk = get_user_info(user_id)
        self.push_download_job(uid, dytk, 0, favorite)
        
    def push_download_job(self, user_id, dytk, cursor=0, favorite=False):
        """推送下载任务至队列

        @param: user_id
        @param: dytk
        @param: 分页游标
        @return
        """

        list_json = get_list_by_uid(user_id, dytk, cursor, favorite)
        for aweme in list_json.get('aweme_list', []):
            download_url_list = aweme.get('video', {}).get('download_addr', {}).get('url_list', [])
            video_id = aweme.get('statistics', {}).get('aweme_id', None)
            url = download_url_list[randrange(len(download_url_list))]
            self.queue.put((url, user_id, video_id, favorite))

        has_more = list_json.get('has_more', False)
        max_cursor = list_json.get('max_cursor', None)
        if has_more and max_cursor and (max_cursor != cursor):
            self.push_download_job(user_id, dytk, max_cursor, favorite)

    def _get_user_link_from_video(self, url):
        """从分享的单个视频链接获取用户信息
        
        @param: url 抖音单个视频链接
        @return: url 真实的用户首页链接
        """

        if url.find('/share/video/') < 0:
            return url
        session = HTMLSession()
        video_res = session.get(url, headers=DOWNLOAD_HEADERS)
        uid = video_res.html.search('uid: "{uid}"')['uid']
        return USER_HOME_URL + str(uid)


class SingleCrawlerScheduler(object):

    def __init__(self, items):
        self.params = []
        for i in range(len(items)):
            uid, video_id, dytk = self._get_info_from_video(items[i])
            if not uid:
                continue
            self.params.append((uid, video_id, dytk))

        self.queue = Queue.Queue()
        self.scheduling()

    def scheduling(self):
        threads = []
        for _ in range(THREADS):
            worker = DownloadWorker(self.queue)
            worker.start()
            threads.append(worker)
        for param in self.params:
            self._get_download_job(*param)
        
        self.queue.join()
        for _ in range(THREADS):
            self.queue.put((None, None, None, None))
        for t in threads:
            t.join()
        print("successful downloaded!")

    def _get_info_from_video(self, url):
        """从分享的单个视频链接获取用户信息
        
        @param: url 抖音单个视频链接
        @return: (uid, video_id, dytk)
        """
        url = get_real_link_from_share_link(url)
        if url is None or url.find('/share/video/') < 0:
            return (None, None, None)
        session = HTMLSession()
        MOBIE_HEADERS['Host'] = DOWNLOAD_HOST
        video_res = session.get(url, headers=MOBIE_HEADERS)
        uid = video_res.html.search('uid: "{uid}"')['uid']
        video_id = video_res.html.search('itemId: "{video_id}"')['video_id']
        dytk = video_res.html.search('dytk: "{dytk}"')['dytk']
        return (uid, video_id, dytk)

    def _get_download_job(self, uid, video_id, dytk):
        """获取下载任务

        @param: uid
        @param: video_id
        @param: dytk
        @return
        """

        params = {
            'item_ids': video_id,
            'dytk': dytk
        }
        session = HTMLSession()

        MOBIE_HEADERS['Host'] = DOWNLOAD_HOST
        r = session.get(ITEM_INFO_URL, params=params, headers=MOBIE_HEADERS)
        if r.status_code != 200:
            print(r)
            return
        r.html.render()
        res_json = json.loads(r.html.text)
        r.close()
        item_list = res_json.get('item_list', [])
        for item in item_list:
            vid = item.get('video', {}).get('vid', None)
            if vid is None:
                continue
            tmp_url = PLAY_URL + '?video_id=' + vid
            download_url = custom_format_download_url(tmp_url)
            self.queue.put((download_url, uid, video_id, False))


def usage():
    print("1. Please make sure folder data/ and video/ is exist under this same diectory.\n"
          "2. Please create file share-url.txt under this same directory.\n"
          "3. In share-url.txt, you can specify one amemv share page url one line. Accept multiple lines of text\n"
          "4. Save the file and retry.\n"
          "5. Or use command line options:\nSample: python douyin.py --urls url1,url2\n\n")
    print("1. 请确保在当前目录下，存在data和video文件夹。\n"
          "2. 请确保当前目录下存在share-url.txt文件。\n"
          "3. 请在文件中指定抖音分享页面URL，一行一个链接，支持多行.\n"
          "4. 保存文件并重试.\n"
          "5. 或者直接使用命令行参数指定链接\n例子: python douyin.py --urls url1,url2")

def get_file_content(filename):
    if os.path.exists(filename):
        return parse_sites(filename)
    else:
        usage()
        sys.exit(1)

def parse_sites(filename):
    urls = []
    with open(filename, 'r') as f:
        for line in f:
            url = line.strip()
            if url:
                urls.append(url)
    return urls

if __name__ == "__main__": 
    favorite, single, content, opts, args = False, False, None, None, []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlsu:f:", ["help", "like", "single", "urls=", "filename="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-u', '--urls'):
            content = arg.split(',')
        elif opt in ('-f', '--filename'):
            content = get_file_content(arg)
        elif opt in ('-l', '--like'):
            favorite = True
        elif opt in ('-s', '--single'):
            single = True
        elif opt in ('-h', '--help'):
            usage()
            sys.exit()
    
    if not content:
        content = get_file_content('share-url.txt')
    
    if len(content) < 1 or content[0] == '':
        usage()
        sys.exit(1)

    if single:
        SingleCrawlerScheduler(content)
    else:
        CrawlerScheduler(content, favorite)
