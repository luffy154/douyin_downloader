import os
import requests
from tqdm import tqdm
import re
import execjs
import urllib.parse
import json

def API_Call(uid, max_cursor):
    # https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id=7117197143789587743
    # https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={key}
    # https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}
    API_ENDPOINT = f"https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=100&max_cursor={max_cursor}"
    # API_ENDPOINT = f"https://m.douyin.com/web/api/v2/aweme/post/?sec_uid={uid}&count=10&max_cursor={max_cursor}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'cookie': 'ttwid=1%7Ck3sCvN_3Z5KHQV9sQbbngAWDSo_kE15IN3dsFBe8EdE%7C1694610359%7Ce7fca5cb76c293d0554761a90ec8aa75430d3546bbf4e71b0d993d84f9101c07; __ac_signature=_02B4Z6wo00f01GE8BfQAAIDA-VeShUhvSZBhHAFAAH1V72; __ac_referer=__ac_blank; msToken=t-NqEFfGuydUPXXfVz78GsbHrFeePRBfFBHVrHbS_5hllsifqdARGHhQ9s7J4nn_TLhAqaNMAn1jUbquzFSUMjml4C9TdvOOnrSOPNpw'
    }
    data = requests.get(API_ENDPOINT, headers=headers)
    return data.json()


def get_data(uid, max_cursor):
    data = []
    data_json = API_Call(uid=uid, max_cursor=max_cursor)
    if data_json and "aweme_list" in data_json.keys():
        aweme_list = data_json["aweme_list"]
        for item in aweme_list:
            src = item["video"]["cover"]["url_list"][-1]
            desc = item["desc"]
            aweme_id = item["aweme_id"]
            data.append({
                "id": aweme_id,
                "src": src,
                "desc": desc
            })
    if data_json["has_more"]:
        return data, data_json['max_cursor']
    else:
        return data, None

def generate_x_bogus_url(url: str, headers: dict) -> str:
    query = urllib.parse.urlparse(url).query
    xbogus = execjs.compile(open('./X-Bogus.js').read()).call('sign', query, headers['User-Agent'])
    new_url = url + "&X-Bogus=" + xbogus
    return new_url
def download(url, aweme_id, desc):

    api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id={aweme_id}&pc_client_type=1&version_code=190500&version_name=19.5.0&cookie_enabled=true&screen_width=1344&screen_height=756&browser_language=zh-CN&browser_platform=Win32&browser_name=Firefox&browser_version=110.0&browser_online=true&engine_name=Gecko&engine_version=109.0&os_name=Windows&os_version=10&cpu_core_num=16&device_memory=&platform=PC&webid=7158288523463362079&msToken=abL8SeUTPa9-EToD8qfC7toScSADxpg6yLh2dbNcpWHzE0bT04txM_4UwquIcRvkRb9IU8sifwgM1Kwf1Lsld81o9Irt2_yNyUbbQPSUO8EfVlZJ_78FckDFnwVBVUVK"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    api_url = generate_x_bogus_url(api_url,headers)
    file_name = aweme_id + "-" + desc + ".mp4"
    if os.path.exists(f'Download/{file_name}'):
        print("文件已经存在：", file_name)
        return
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }
    douyin_api_headers = {
        'accept-encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'referer': 'https://www.douyin.com/',
        'cookie': "ttwid=1%7C0YBAnAwiC5T3U5yJi8RVXEK3DOwF_2vpJ7kVJJZe8HU%7C1666668932%7C21048e6555b73e8801d3956afc6130b4a05ae73a2eefe4d3fef5ef1b61caf0e9; __live_version__=%221.1.1.2586%22; odin_tt=a77b90afad5db31e86fe004b39c5f35423292023ce7837cde82fd1f7fe54278890ce24dc89e09c8a2e55b1f4904950a7b0fca6b4fbff3b549ba6d55a335373ec; pwa2=%223%7C0%7C0%7C0%22; s_v_web_id=verify_lkagpdq1_IuHpxJyS_q6YH_4AvH_8aNH_zhvGPr95Jrc8; passport_csrf_token=301cf539fb735ab77de7e382b0dd93e5; passport_csrf_token_default=301cf539fb735ab77de7e382b0dd93e5; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCRXhuWUdqREVBa3ErdjRsT2l3anRIWi9HU2hRNXFseWdJMklLanIxM0orRHozYnA0M2pXc3M3N25CUzdnbE5tTXhHbWU3cldoSE9pdkJvVmNnT2JiWFU9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ==; passport_assist_user=CkHJzB17Xsy3FUHyNfX2Dyb8IFKKA_0pu1SKYG0OAT_av3ImQyCbEmGJV7b8MJep4l9MjeCRK1FPY9k9yAkVHbIbvhpICjzS68aPlRjIsUzHLIEM-5jMbp9awcdJnkACni5Nnc_PBm4ljAlEqChbF4nYPpn4xyh4kY2hBvRikmXs0sgQ4fq2DRiJr9ZUIgEDbm8-yw%3D%3D; n_mh=13KNPUKNEzoW3A4J-OLRxfal2zj1GbF-vJUFPs3WSIY; sso_uid_tt=2581aab41d03156c0b7fee9c7e865c6c; sso_uid_tt_ss=2581aab41d03156c0b7fee9c7e865c6c; toutiao_sso_user=b2556b53ed5cee89e947b154b17645f1; toutiao_sso_user_ss=b2556b53ed5cee89e947b154b17645f1; sid_ucp_sso_v1=1.0.0-KDhlZjRhMmJhZGU0OTVmOWM0YzBkMTY5ZGNkZmI4NTFjNTk2ODU5OTkKHwiPluCxqYzbAhC29OKmBhjvMSAMMLDIpZkGOAZA9AcaAmhsIiBiMjU1NmI1M2VkNWNlZTg5ZTk0N2IxNTRiMTc2NDVmMQ; ssid_ucp_sso_v1=1.0.0-KDhlZjRhMmJhZGU0OTVmOWM0YzBkMTY5ZGNkZmI4NTFjNTk2ODU5OTkKHwiPluCxqYzbAhC29OKmBhjvMSAMMLDIpZkGOAZA9AcaAmhsIiBiMjU1NmI1M2VkNWNlZTg5ZTk0N2IxNTRiMTc2NDVmMQ; sid_guard=c1d1ac1d22198149dfc6cac74938b14a%7C1691925046%7C5184000%7CThu%2C+12-Oct-2023+11%3A10%3A46+GMT; uid_tt=7e39a426dac7802b2448fa2266ca1b85; uid_tt_ss=7e39a426dac7802b2448fa2266ca1b85; sid_tt=c1d1ac1d22198149dfc6cac74938b14a; sessionid=c1d1ac1d22198149dfc6cac74938b14a; sessionid_ss=c1d1ac1d22198149dfc6cac74938b14a; sid_ucp_v1=1.0.0-KDc4Y2VkZjIyN2JlMDNhYmNhYTFlYTE5ODM1YzI2YjVlZDNmMGY0N2YKGwiPluCxqYzbAhC29OKmBhjvMSAMOAZA9AdIBBoCbHEiIGMxZDFhYzFkMjIxOTgxNDlkZmM2Y2FjNzQ5MzhiMTRh; ssid_ucp_v1=1.0.0-KDc4Y2VkZjIyN2JlMDNhYmNhYTFlYTE5ODM1YzI2YjVlZDNmMGY0N2YKGwiPluCxqYzbAhC29OKmBhjvMSAMOAZA9AdIBBoCbHEiIGMxZDFhYzFkMjIxOTgxNDlkZmM2Y2FjNzQ5MzhiMTRh; LOGIN_STATUS=1; _bd_ticket_crypt_cookie=861cdca903469f36dd23fc1ecfe847c1; __security_server_data_status=1; store-region=us; store-region-src=uid; d_ticket=28acd5a9c6df4227b13582669694acded6ede; __ac_nonce=064ec4f3a00901157c769; __ac_signature=_02B4Z6wo00f01ve8HKgAAIDD6.-iFWbfM-r3jRgAANkQTCm7UjsJOQlMGY7o-iPsCIAe0kuriDaQ15lHcML.nW.cGNWpSBLUJzdr6s8KHRbqh5ywvupCeAKBEHKKbji7hD1-Z0x3DI-n0KKx34; douyin.com; device_web_cpu_core=16; device_web_memory_size=-1; webcast_local_quality=null; publish_badge_show_info=%220%2C0%2C0%2C1693208382348%22; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; strategyABtestKey=%221693208382.387%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1344%2C%5C%22screen_height%5C%22%3A756%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A0%2C%5C%22downlink%5C%22%3A%5C%22%5C%22%2C%5C%22effective_type%5C%22%3A%5C%22%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; VIDEO_FILTER_MEMO_SELECT=%7B%22expireTime%22%3A1693813183367%2C%22type%22%3A1%7D; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A1%7D; my_rd=1; passport_fe_beating_status=true; msToken=ESPx4FwNhcdEvr36-bmhWde9xupU_c64WeeqvvzqzLCtmEsvGPXhkwsKM8miaoC2w8gWSzNAfqxPEju4w3jzopIFompVSmwemq9-z1F8V-2vLNhTxLlYCUVdXkzNj6zM; download_guide=%221%2F20230828%2F0%22; csrf_session_id=3c194edf7f2cee968b0df65f97a11648; msToken=XFIGWeX20IGrrEUGYr_4SR2DPrduwK5zxB3gOp8FfbxW_Ng-w9uNh8wQRUIoPUtkSblL6msqte55jyfcrKPb8eDZekS9Q1P9hkdkPFiV4Ni-l9Vmsr0KgFo5MOkLaBZy; tt_scid=-i-7N5fAMRj8pGg4drGXbjasutdtD4tzIeqRnm6OJ1LoXRRZGl8FNhORnEuY3id.b3b7"
    }
    print(api_url)
    response = requests.get(url=api_url, headers=douyin_api_headers, stream=True, timeout=30000)
    data = json.loads(response.text)
    videoUrl = data['aweme_detail']['video']['play_addr_h264']['url_list'][0]

    videoRes = requests.get(url=videoUrl, headers=headers, stream=True, timeout=30000)
    content_size = int(int(videoRes.headers['Content-Length']) / 1024)
    print(content_size)
    # with open(f'Download/{file_name}', "wb") as f:
    #     print("Total Size: ", content_size, 'k,start...')
    #     for data in tqdm(iterable=videoRes.iter_content(1024), total=content_size, unit='k', desc=file_name[:19]):
    #         f.write(data)
    #     print(file_name[:19], "download finished!")
    #     f.flush()
    #     f.close()

def get_file_content(filename):
    jsonStr = ""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            for line in f:
                jsonStr += line
    return jsonStr

def download_tiktok(aweme_id):
    file_name = aweme_id + "-自然美景分享 #美景  #自然景观 #放松心情 #舒适 #安逸.mp4"
    if os.path.exists(f'Download_TikTok/{file_name}'):
        print("文件已经存在：", file_name)
        return
    tikData = get_tiktok_video_data(aweme_id)
    videoUrl = tikData['video']['play_addr']['url_list'][0]
    print(videoUrl)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }
    videoRes = requests.get(url=videoUrl, headers=headers, stream=True, timeout=30000)
    content_size = int(int(videoRes.headers['Content-Length']) / 1024)
    print(content_size)
    with open(f'Download_tiktok/{file_name}', "wb") as f:
        print("Total Size: ", content_size, 'k,start...')
        for data in tqdm(iterable=videoRes.iter_content(1024), total=content_size, unit='k', desc=file_name[:19]):
            f.write(data)
        print(file_name[:19], "download finished!")
        f.flush()
        f.close()
def main(link):
    jsonStr = get_file_content("tiktok.txt")
    data = json.loads(jsonStr)
    all_data = []
    for item in data['itemList']:
        all_data.append(item['id'])
    # all_data = [
    #
    # ]
    for item in all_data:
        download_tiktok(aweme_id=item)

def get_tiktok_video_data(video_id: str):
    print('正在获取TikTok视频数据...')
    try:
        # 构造访问链接/Construct the access link
        api_url = f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}'
        print("正在获取视频数据API: {}".format(api_url))
        tiktok_api_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9'
        }
        response = requests.get(api_url, headers=tiktok_api_headers,timeout=30000)
        resJson = json.loads(response.text)
        response.close()
        video_data = resJson['aweme_list'][0]
        print('获取视频信息成功！')
        return video_data
    except Exception as e:
        print('获取视频信息失败！原因:{}'.format(e))
        # return None
        raise e

def get_url(text: str):
    try:
        # 从输入文字中提取索引链接存入列表/Extract index links from input text and store in list
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        # 判断是否有链接/Check if there is a link
        if len(url) > 0:
            return url[0]
    except Exception as e:
        print('Error in get_url:', e)
        return None

if __name__ == "__main__":
    try:
        os.makedirs("Download")
    except FileExistsError:
        print("exists")
    main('https://www.douyin.com/user/MS4wLjABAAAAYFnqGRaFV98S4F4PH0l2oTBjKRpFQ1sUaoN8HzkfBN8twmlcQp355vMWj7iKSkNZ')

