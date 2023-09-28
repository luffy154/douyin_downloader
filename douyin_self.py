import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
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
MOBIE_HEADERS = {
    # 'Pragma': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'en-US,en;q=0.5',
    # 'Cache-Control': 'no-cache',
    # 'TE': 'Trailers',
    # 'DNT': '1',
    'Accept':'*/*',
    'Accept-Encoding':'gzip, deflate, br',
    'Cookie':'__ac_referer=__ac_blank; douyin.com; webcast_local_quality=null; ttwid=1%7CiHXJOGpNyZzFe-gTbaNsu79WGr4QYWSS2aEfFr7Hj-U%7C1694440885%7C98ca7ba07b3616a6f0dcd7ecf56f80a76024de6ec50923730b469289c3ecb4ff; ttcid=f43375acd3a14cde96708255116e069180; passport_csrf_token=72cb7beff2501ec6633a637e16a9bac9; passport_csrf_token_default=72cb7beff2501ec6633a637e16a9bac9; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; download_guide=%223%2F20230912%2F0%22; douyin.com; device_web_cpu_core=8; device_web_memory_size=8; webcast_local_quality=null; s_v_web_id=verify_lmhnc7ml_Q7xfi10X_X0ov_4XWE_AOCD_TlQ5Z8rmfNrb; csrf_session_id=cc64ecc7dcd24bcba985e2bb5b5a013f; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSThTLzY4ZWJDeGEvbk1BVTNjdUNUZFZvTjZiYXFncTd2NHpJMTA4Mm9xd2JQaXJhRTNJY2ZONC9mRVdtZmp6enRicWh1dW9nMzdGZXhueVBTeDlHNGM9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ==; SEARCH_RESULT_LIST_TYPE=%22single%22; pwa2=%220%7C0%7C3%7C0%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1695210330415%2C%22type%22%3A1%7D; xgplayer_user_id=942582254717; passport_assist_user=CkGg0GosveXmTYH0JCfkzGHhCdoFbOMi-dtGLHud42YMUkTE6ZDSVDKbs98jEYN_8IOQFm5CVWJnH27NCkCwqdpTLRpKCjwsFwzhY22FacZ-N589iqbQgiM2rQzRoZDPmZsCCARcnAhIY29poMcYCBx9Xgf1TeSt1yKkfCSrNR4EkLIQp-m7DRiJr9ZUIAEiAQN6pJLj; n_mh=06X79phbPeCwNYqG8blTaVUwD31it3lHrnLDrXS1W5I; sso_uid_tt=687beffd2f9c7bf196d15429bb7504b9; sso_uid_tt_ss=687beffd2f9c7bf196d15429bb7504b9; toutiao_sso_user=76b05724a74c714fe4933916c58ba156; toutiao_sso_user_ss=76b05724a74c714fe4933916c58ba156; sid_ucp_sso_v1=1.0.0-KGM1Y2Y1YmVhODM5NTcwNmM1NjUyM2RiNGM5Nzc0ODE0NzZmYWFlMGQKHwjtpfCRtY2hBhCTw4aoBhjvMSAMMKnG1JUGOAZA9AcaAmhsIiA3NmIwNTcyNGE3NGM3MTRmZTQ5MzM5MTZjNThiYTE1Ng; ssid_ucp_sso_v1=1.0.0-KGM1Y2Y1YmVhODM5NTcwNmM1NjUyM2RiNGM5Nzc0ODE0NzZmYWFlMGQKHwjtpfCRtY2hBhCTw4aoBhjvMSAMMKnG1JUGOAZA9AcaAmhsIiA3NmIwNTcyNGE3NGM3MTRmZTQ5MzM5MTZjNThiYTE1Ng; odin_tt=f96c8146f2f96b1ad1465a7d56a119c174b53cce3241a49f0a8a731f8156c4bd8e67e1f8e93d3e36383d01a052a4f6b7b9d8fc3b406e749aa54e4ea79f40a911; passport_auth_status=2f1da1f03f319a254fc80a123aed87a4%2C; passport_auth_status_ss=2f1da1f03f319a254fc80a123aed87a4%2C; uid_tt=da8e93a1f17c86d860b8648a2978d528; uid_tt_ss=da8e93a1f17c86d860b8648a2978d528; sid_tt=b8a931fca7135d2ec661fbfb051d028c; sessionid=b8a931fca7135d2ec661fbfb051d028c; sessionid_ss=b8a931fca7135d2ec661fbfb051d028c; LOGIN_STATUS=1; store-region=us; store-region-src=uid; _bd_ticket_crypt_doamin=3; _bd_ticket_crypt_cookie=ee5a25d12a952ca74d43b3526fb21b0d; __security_server_data_status=1; sid_guard=b8a931fca7135d2ec661fbfb051d028c%7C1694605724%7C5183994%7CSun%2C+12-Nov-2023+11%3A48%3A38+GMT; sid_ucp_v1=1.0.0-KGYxNDhhNGM2MzhiYzkyNTFmMjFlN2MyNmJmZDZmOThmMjZmMDIzNDUKGwjtpfCRtY2hBhCcw4aoBhjvMSAMOAZA9AdIBBoCbGYiIGI4YTkzMWZjYTcxMzVkMmVjNjYxZmJmYjA1MWQwMjhj; ssid_ucp_v1=1.0.0-KGYxNDhhNGM2MzhiYzkyNTFmMjFlN2MyNmJmZDZmOThmMjZmMDIzNDUKGwjtpfCRtY2hBhCcw4aoBhjvMSAMOAZA9AdIBBoCbGYiIGI4YTkzMWZjYTcxMzVkMmVjNjYxZmJmYjA1MWQwMjhj; my_rd=1; _tea_utm_cache_2018={%22utm_source%22:%22weixin%22%2C%22utm_medium%22:%22aweme_ios%22%2C%22utm_campaign%22:%22client_share%22}; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAR0Xl8yxlb-B0BcwGiwtmHwI__3EmAKTt9yh69pg4yNQjfowxCMqxCGl7I2Z-1N01%2F1694620800000%2F0%2F0%2F1694611012361%22; __ac_nonce=065026ee000d4e1092fe0; __ac_signature=_02B4Z6wo00f01NmtybAAAIDAQcZew8TkXljZjc0AAFNujAkiuJEBqeIZuLvQtrJsbBKAVle0DmdsmrcB2gd9koR3VObnyJBtY0PNpuB.S-DTQ4hWAbRwDun0dvUkTKP1FHPa6ANxYIEJCaKb2e; strategyABtestKey=%221694658292.08%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1440%2C%5C%22screen_height%5C%22%3A900%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A8%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A1.35%2C%5C%22effective_type%5C%22%3A%5C%223g%5C%22%2C%5C%22round_trip_time%5C%22%3A550%7D%22; home_can_add_dy_2_desktop=%221%22; msToken=pFO16qpcE-RCM52uaolptWaXh7V7ANzsSThiTWhcjFuGYy9Vc26qeuJCI2HxcaWKXaYbU4d-OoJ48UQSa3_WMOabOCm9gC6iR-mL2qLmYb8ea-GzuzDO; tt_scid=WjFGFLMtvv2f4g5zanyuW72jq-4nJShRRjUziQjNnBxxcGHbYbCluyOkjVR1qVzac580; msToken=LQ9ZTtMRxkclixww6iuJ_TkxJyQiw5GkSw3uZ9shtkZQJDyME8Ndd3z5gq4eW8TXZ4NNTUTF3lxOthlq50PlNKQuceLNikdKa0ZPBWCmfQf2aLzXCJ0S; publish_badge_show_info=%221%2C0%2C0%2C1694658348195%22; IsDouyinActive=false; passport_fe_beating_status=false',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/12.0 Mobile/15A372 Safari/604.1'
}

USER_HOME_URL = 'https://www.douyin.com/user/'
SHARE_HOST = 'v.douyin.com'
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
if __name__ == "__main__":
    content = get_file_content('share-url.txt')
    if len(content) < 1 or content[0] == '':
        usage()
        sys.exit(1)

    for i in range(len(content)):
        url = get_real_link_from_share_link(content[i])
        number = re.findall(r'/share/user/(\w+)', url)
        if not len(number):
            continue
        response = requests.get(USER_HOME_URL+number[0], headers=MOBIE_HEADERS)
        print(response.text)