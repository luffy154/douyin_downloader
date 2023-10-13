import os
import urllib.parse

import execjs
import requests
from tqdm import tqdm


def API_Call(uid, max_cursor):
    # https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id=7117197143789587743
    # https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}
    # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}
    # https://www.douyin.com/aweme/v1/web/aweme/post/?sec_user_id=MS4wLjABAAAAo_kWeC7SVzIBOh-jhMm_ydpd5O1hntcqA2fXfsp_GNs&count=35&max_cursor=0&device_platform=webapp&aid=6383&X-Bogus=DFSzswVOCohAN9ILtTQ1xYXAIQ21
    API_ENDPOINT = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=100&max_cursor={max_cursor}"
    # API_ENDPOINT = f"https://m.douyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=10&max_cursor={max_cursor}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'cookie': 'ttwid=1%7Ck3sCvN_3Z5KHQV9sQbbngAWDSo_kE15IN3dsFBe8EdE%7C1694610359%7Ce7fca5cb76c293d0554761a90ec8aa75430d3546bbf4e71b0d993d84f9101c07; __ac_signature=_02B4Z6wo00f01GE8BfQAAIDA-VeShUhvSZBhHAFAAH1V72; __ac_referer=__ac_blank; msToken=t-NqEFfGuydUPXXfVz78GsbHrFeePRBfFBHVrHbS_5hllsifqdARGHhQ9s7J4nn_TLhAqaNMAn1jUbquzFSUMjml4C9TdvOOnrSOPNpw'
    }
    data = requests.get(API_ENDPOINT, headers=headers)
    return data.json()


def urlTest():
    user_id = 'MS4wLjABAAAA5pGWLGnkKcDqk85LfsQTrI0YPDquhMMPPg0PCeEXKuo'
    url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?sec_user_id={user_id}&count=35&max_cursor=0&device_platform=webapp&aid=6383'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    xbogus = generate_x_bogus_url(url, headers)


def API_Call_NEW(uid, max_cursor):
    # https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id=7117197143789587743
    # https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}
    # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}
    # https://www.douyin.com/aweme/v1/web/aweme/post/?sec_user_id=MS4wLjABAAAAo_kWeC7SVzIBOh-jhMm_ydpd5O1hntcqA2fXfsp_GNs&count=35&max_cursor=0&device_platform=webapp&aid=6383&X-Bogus=DFSzswVOCohAN9ILtTQ1xYXAIQ21
    API_ENDPOINT = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=100&max_cursor={max_cursor}"
    url = f'https://www.douyin.com/aweme/v1/web/aweme/post/?sec_user_id={uid}&count=100&max_cursor={max_cursor}&device_platform=webapp&aid=6383'
    # API_ENDPOINT = f"https://m.douyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=10&max_cursor={max_cursor}"
    headers = {
        'Referer': f'https://www.douyin.com/user/{uid}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'cookie': 'passport_csrf_token=72cb7beff2501ec6633a637e16a9bac9; passport_csrf_token_default=72cb7beff2501ec6633a637e16a9bac9; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; webcast_local_quality=null; s_v_web_id=verify_lmhnc7ml_Q7xfi10X_X0ov_4XWE_AOCD_TlQ5Z8rmfNrb; csrf_session_id=cc64ecc7dcd24bcba985e2bb5b5a013f; xgplayer_user_id=942582254717; n_mh=06X79phbPeCwNYqG8blTaVUwD31it3lHrnLDrXS1W5I; store-region-src=uid; __security_server_data_status=1; my_rd=1; LOGIN_STATUS=1; d_ticket=f12f9c887a0fdaadd64b4aab2f2f7556a3a5b; sso_uid_tt=96d490f34fa551fa2ecf067a6b966677; sso_uid_tt_ss=96d490f34fa551fa2ecf067a6b966677; toutiao_sso_user=a16f1f0d38bc9f4f6727aaa1a84ab3c7; toutiao_sso_user_ss=a16f1f0d38bc9f4f6727aaa1a84ab3c7; passport_auth_status=162df484adda18258fb508498c48af83%2C2f1da1f03f319a254fc80a123aed87a4; passport_auth_status_ss=162df484adda18258fb508498c48af83%2C2f1da1f03f319a254fc80a123aed87a4; uid_tt=17826c6c6a39290aaf481ff127b37639; sid_tt=eded9f706f93c6b066a600c8c8a345d3; sessionid=eded9f706f93c6b066a600c8c8a345d3; passport_assist_user=CkF7hCN-R7HyItVIc3cqLehMvAOaxlom94oFUoF1o6BToJDK-mnWPfIl6faXEKo17EZX3PoIqoSveamZtCSB1-wMVBpKCjxkZqrxBQy5Cw7fyAuvTVgSpfeaEnAO1em_LSCrKj9ruDXGOCSKK5JuvUOgT2Vjqd6-gUNlRizGL4_-eswQw5S8DRiJr9ZUIAEiAQPgqtbA; sid_ucp_sso_v1=1.0.0-KDkwNGIyNTFiYWNlMWZjOWIwNDE4OWFlZjVjZTJlYTVlMTQ3MTgyODUKHwjtpfCRtY2hBhDIyZqoBhjvMSAMMKnG1JUGOAZA9AcaAmxmIiBhMTZmMWYwZDM4YmM5ZjRmNjcyN2FhYTFhODRhYjNjNw; ssid_ucp_sso_v1=1.0.0-KDkwNGIyNTFiYWNlMWZjOWIwNDE4OWFlZjVjZTJlYTVlMTQ3MTgyODUKHwjtpfCRtY2hBhDIyZqoBhjvMSAMMKnG1JUGOAZA9AcaAmxmIiBhMTZmMWYwZDM4YmM5ZjRmNjcyN2FhYTFhODRhYjNjNw; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=72ac7b8a370523fc8d4efe4c376b5f64; store-region=us; passport_fe_beating_status=true; __live_version__=%221.1.1.4209%22; webcast_leading_last_show_time=1695566859831; webcast_leading_total_show_times=3; uid_tt_ss=17826c6c6a39290aaf481ff127b37639; webcast_local_quality=null; sid_guard=eded9f706f93c6b066a600c8c8a345d3%7C1695904390%7C5184000%7CMon%2C+27-Nov-2023+12%3A33%3A10+GMT; sessionid_ss=eded9f706f93c6b066a600c8c8a345d3; sid_ucp_v1=1.0.0-KDM2OWMyMjU3YzcyODk4M2I4ODg5ODBhOGFkZmU5NTg5NWY3ZmRlN2YKGwjtpfCRtY2hBhCG5dWoBhjvMSAMOAZA9AdIBBoCbGYiIGVkZWQ5ZjcwNmY5M2M2YjA2NmE2MDBjOGM4YTM0NWQz; ssid_ucp_v1=1.0.0-KDM2OWMyMjU3YzcyODk4M2I4ODg5ODBhOGFkZmU5NTg5NWY3ZmRlN2YKGwjtpfCRtY2hBhCG5dWoBhjvMSAMOAZA9AdIBBoCbGYiIGVkZWQ5ZjcwNmY5M2M2YjA2NmE2MDBjOGM4YTM0NWQz; ttwid=1%7CiHXJOGpNyZzFe-gTbaNsu79WGr4QYWSS2aEfFr7Hj-U%7C1696217030%7C9e4bc703d76d46bf46aaf81e6f4f0695c479a1a5628a1bbc09caa07a1ac102d5; publish_badge_show_info=%220%2C0%2C0%2C1696639430572%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1697464077034%2C%22type%22%3A1%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; SEARCH_RESULT_LIST_TYPE=%22single%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAR0Xl8yxlb-B0BcwGiwtmHwI__3EmAKTt9yh69pg4yNQjfowxCMqxCGl7I2Z-1N01%2F1696867200000%2F0%2F1696859393103%2F0%22; pwa2=%220%7C0%7C3%7C0%22; download_guide=%223%2F20231009%2F1%22; __ac_signature=_02B4Z6wo00f01xIm0bQAAIDDik1GxF4tdj8SBtUAAKG5ebEOa2U.DAs6YlM6.j5CNxytqnpHJlv5rH7xHWRM9bwinkEPXdASLt9hTIVjAPub89-LoUs2.Zxk6CTKhgSJ7yZ-mpyeM9VC8tzf96; strategyABtestKey=%221697002053.628%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSThTLzY4ZWJDeGEvbk1BVTNjdUNUZFZvTjZiYXFncTd2NHpJMTA4Mm9xd2JQaXJhRTNJY2ZONC9mRVdtZmp6enRicWh1dW9nMzdGZXhueVBTeDlHNGM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; msToken=E9Cby-GlvXZ5qqLhhoq_rgQ-LWyAth6gh_Iio-Y9lGEt4yWAeJOzkDEVLLXFjQX4-hHECP-oQ-aVkGZnaYwjA2TdUjCxv4iom6lSkihbMMRPfMS-slEwJQ==; tt_scid=DXnoVxZW.iW8pyhl5tYpwlFhetII19cY7iS8h4mlO4YrN3QyROyhkKX0Vv2b7YLre30e; odin_tt=6b11afac5055814e1e403d235b022fbea6f6cd27bf5fb94cade183a0d77d776ed82d43cb1ce34c46b0bbc9f94edd657b; __ac_nonce=0652649be00f69d94392; msToken=5OJHUCltN1dRtUejrYa1bHXI-q3hx3WzcwNjr6FgEO4osUKiEJX5XJhur1kxEHw1MZNws8fk6Vh-i6IrXsnk-78e3DVhjNSJpEJdzz9JO1c1sEuFDgwIzEtCujbR2ZU=; IsDouyinActive=false; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A6.8%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAR0Xl8yxlb-B0BcwGiwtmHwI__3EmAKTt9yh69pg4yNQjfowxCMqxCGl7I2Z-1N01%2F1697040000000%2F0%2F1697008847770%2F0%22; home_can_add_dy_2_desktop=%221%22'
    }
    url = generate_x_bogus_url(url, headers)
    print(url)
    data = requests.get(url, headers=headers)
    return data.json()


def get_data(uid, max_cursor):
    data = []
    data_json = API_Call_NEW(uid=uid, max_cursor=max_cursor)
    if data_json and "aweme_list" in data_json.keys():
        aweme_list = data_json["aweme_list"]
        for item in aweme_list:
            src = item["video"]["play_addr_h264"]["url_list"][0]
            desc = item["desc"]
            aweme_id = item["aweme_id"]
            data.append({
                "id": aweme_id,
                "src": src,
                "desc": desc
            })
    if len(data) > 0:
        return data, data_json['max_cursor']
    else:
        return data, -1


path = "village"


def generate_x_bogus_url(url: str, headers: dict) -> str:
    query = urllib.parse.urlparse(url).query
    xbogus = execjs.compile(open('./X-Bogus.js').read()).call('sign', query, headers['User-Agent'])
    new_url = url + "&X-Bogus=" + xbogus
    return new_url


def download(url, aweme_id, desc):
    file_name = aweme_id + "-" + desc + ".mp4"
    # return
    if os.path.exists(f'{path}/{file_name}'):
        print("文件已经存在：", file_name)
        return
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }

    videoRes = requests.get(url=url, headers=headers, stream=True, timeout=30000)
    content_size = int(int(videoRes.headers['Content-Length']) / 1024)
    with open(f'{path}/{file_name}', "wb") as f:
        print("Total Size: ", content_size, 'k,start...')
        for data in tqdm(iterable=videoRes.iter_content(1024), total=content_size, unit='k', desc=file_name[:19]):
            f.write(data)
        print(file_name[:19], "download finished!")
        f.flush()
        f.close()


def main(link):
    user_id = 'MS4wLjABAAAA5pGWLGnkKcDqk85LfsQTrI0YPDquhMMPPg0PCeEXKuo'
    all_data = []
    data, max_cursor = get_data(uid=user_id, max_cursor=0)
    all_data += data
    while max_cursor > 0:
        data, max_cursor = get_data(uid=user_id, max_cursor=max_cursor)
        all_data += data
    for item in all_data:
        try:
            download(url=item["src"], aweme_id=item["id"], desc=item["desc"])
        except Exception as e:
            with open('error.log', 'a', encoding='utf-8') as f:
                f.write('error at' + item['src'] + str(e) + '\n')
                f.close()


if __name__ == "__main__":
    try:
        os.makedirs(f"{path}")
    except FileExistsError:
        print("exists")
    main('https://www.douyin.com/user/MS4wLjABAAAAYFnqGRaFV98S4F4PH0l2oTBjKRpFQ1sUaoN8HzkfBN8twmlcQp355vMWj7iKSkNZ')
