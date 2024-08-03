
import json
from urllib.parse import urlencode
import requests
import random
import time
import uuid
import os
import requests
import re
import csv
import sys
import warnings
from copy import deepcopy
from hashlib import md5
warnings.filterwarnings("ignore")
from google.protobuf.json_format import MessageToJson
import awemev2_pb2 as pr



def get_app_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        try:
            app_full_path = os.path.realpath(__file__)
            application_path = os.path.dirname(app_full_path)
        except NameError:
            application_path = application_path
    return application_path


def check_log(temp_list):
    tmp = []
    for item in temp_list:
        tmp.append(hex(item))


def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string


def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:

        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)


def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)


class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_510 = [0x55, 0x00, 0x50, random.choice(
            range(0, 0xFF)), 0x32, 0xFA, 0x00, 8 * random.choice(range(0, 0x1F))]

    def addr_3F4(self):
        tmp = ''
        hex_3F4 = []
        for i in range(0x0, 0x100):
            hex_3F4.append(i)
        for i in range(0, 0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_3F4[i - 1]
            B = self.hex_510[i % 0x8]
            if A == 0x55:
                if i != 1:
                    if tmp != 0x55:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C = C - 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_3F4[C]
            hex_3F4[i] = D
        return hex_3F4

    def initial(self, debug, hex_3F4):
        tmp_add = []
        tmp_hex = deepcopy(hex_3F4)
        for i in range(self.length):
            A = debug[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_3F4[i + 1] + B
            while C >= 0x100:
                C = C - 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E = E - 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''
        for item in self.calculate(self.initial(self.debug, self.addr_3F4())):
            result = result + hex_string(item)
        return '0300{}{}0000{}'.format(hex_string(self.hex_510[7]), hex_string(self.hex_510[3]), result)


def X_Gorgon(url, data, cookie, model='utf-8'):
    gorgon = []
    Khronos = hex(int(time.time()))[2:]
    url_md5 = md5(bytearray(url, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))
    if data:
        if model == 'utf-8':
            data_md5 = md5(bytearray(data, 'utf-8')).hexdigest()
            for i in range(0, 4):
                gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
        elif model == 'octet':
            data_md5 = md5(data).hexdigest()
            for i in range(0, 4):
                gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    for i in range(0, 4):
        gorgon.append(0x0)
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(Khronos, 16))}


def get_get_xg(params, data='', cookie=''):
    x = X_Gorgon(params, data, cookie)
    return x


class Scrapper:

    def __init__(self, cookie):
        self.session = None
        self.cookie = cookie

    def load_session(self):
        if not self.session:
            self.session = requests.session()
            self.session.headers = {
                "user-agent": "com.zhiliaoapp.musically/2022505040 (Linux; U; Android 7.1.2; en; G011A; Build/N2G48H;tt-ok/3.12.13.1)",
                "accept-encoding": "gzip",
                "accept": "*/*",
                "connection": "Keep-Alive",
                "passport-sdk-version": "19",
                "sdk-version": "2",
                "x-vc-bdturing-sdk-version": "2.2.1.i18n",
                "x-tt-dm-status": "login=0;ct=0;rt=7",
                "x-tt-store-region": "us",
                "x-tt-store-region-src": "did",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            }

    def update_headers(self, url, payload):
        self.load_session()
        cuurentTimeStamp = str(time.time()).split(".")[0]
        _rticket = str(time.time()*1000).split(".")[0]
        if url:
            params = url[url.index('?')+1:]
        gorgon = get_get_xg(params, payload, "")
        self.session.headers.update({
            'x-gorgon': gorgon['X-Gorgon'],
            'x-khronos': cuurentTimeStamp,
            "x-xx-req-ticket": _rticket,
        })

    def get_rticket(self):
        return str(time.time()*1000).split(".")[0]

    def get_current_timestamp(self):
        return str(time.time()).split(".")[0]

    def get_post_id_v2(self, post_id):
        print("\nFetching through Method 1\n")
        for x in range(5):
            try:
                urls = ["https://api16-normal-apix.tiktokv.com",
                        "https://api16-normal.ttapis.com",
                        "https://api31-normal.tiktokv.com",
                        "https://api16-normal-baseline.tiktokv.com",
                        "https://api16-normal-quic.tiktokv.com",
                        "https://api16-normal.tiktokv.com",
                        "https://api3-normal.tiktokv.com",
                        "https://api9-normal.tiktokv.com",
                        "https://api15-h2.tiktokv.com",
                        "https://api22-normal-c-alisg.tiktokv.com"]
                url = "{}/aweme/v1/aweme/detail/".format(random.choice(urls))
                querystring = {
                    "aweme_id": post_id,
                    "origin_type": "web",
                    "request_source": "0",
                    "notice_source": "0",
                    "host_abi": "arm64-v8a",
                    "content_language": "en,",
                }
                headers = {
                    "user-agent": "com.zhiliaoapp.musically/2022509040 (Linux; U; Android 13; en; sdk_gphone64_arm64; Build/TPB4.220624.004; Cronet/TTNetVersion:ae513f3c 2022-08-08 QuicVersion:12a1d5c5 2022-06-27)",
                    "accept-encoding": "gzip",
                    "x-common-params-v2": "ac=wifi&ac2=unknown&aid=1233&app_language=en&app_name=musical_ly&app_type=normal&build_number=25.9.4&carrier_region=US&carrier_region_v2=310&channel=googleplay&current_region=US&device_brand=google&device_id={}&device_platform=android&device_type=sdk_gphone64_arm64&dpi=440&language=en&locale=en&manifest_version_code=2022509040&mcc_mnc=310260&op_region=US&os_api=33&os_version=13&region=US&residence=US&resolution=1080*2154&ssmix=a&sys_region=US&timezone_name=Asia%2FKarachi&timezone_offset=18000&uoo=1&update_version_code=2022509040&version_code=250904&version_name=25.9.4".format(str(random.randint(6000000000000000000, 7999999999999999999)))
                }
                xg = get_get_xg(urlencode(querystring, "", ""))
                headers["x-gorgon"] = xg["X-Gorgon"]
                headers["x-khronos"] = xg["X-Khronos"]
                response = requests.get(
                    url, headers=headers, params=querystring)
                data = response.json()["aweme_detail"]
                return data
            except:
                continue
        return False

    def get_post_id(self, url, num):
                self.load_session()
        # for x in range(5):
            # try:
                c = (url.split("/"))
                d = (c[-1].split("?"))
                aweme_id = (d[0].split("-"))[-1]
                url = "https://api22-core-c-useast2a.tiktokv.com/aweme/v2/feed/"
                querystring = {
                    "sp": "-1",
                    "type": "0",
                    "max_cursor": "0",
                    "min_cursor": "0",
                    "count": "6",
                    "aweme_id": aweme_id,
                    "volume": "0.0",
                    "pull_type": "4",
                    "req_from": "enter_auto",
                    "ad_user_agent": "Mozilla/5.0 (Linux; Android 13; sdk_gphone64_arm64 Build/TPB4.220624.004; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.74 Mobile Safari/537.36",
                    "filter_warn": "0",
                    "ad_personality_mode": "1",
                    "address_book_access": "2",
                    "cached_item_num": "0",
                    "last_ad_show_interval": "-1",
                    "vpa_content_choice": "1",
                    "sound_output_device": "0",
                    "user_avatar_shrink": "96_96",
                    "is_audio_mode": "0",
                    "personalization_setting": "0",
                    "tail_slot_probability": "0.0",
                    "client_cache_request_count": "0",
                    "disable_quality_protection": "0",
                    "debug_regions": "ID",
                    "batch_number": "6",
                    "is_pad": "0",
                    "is_landscape": "0",
                    "is_new_user_see_first": "0",
                    "batch_num": "0",
                    "batch_num_all": "0",
                    "play_num": "0",
                    "play_num_all": "0",
                    "last_show_lives": "[]",
                    "last_play_lives": "[]",
                    "host_abi": "arm64-v8a",
                }
                headers = {
                    "host": "api22-core-c-useast2a.tiktokv.com",
                    "connection": "keep-alive",
                    "x-vc-bdturing-sdk-version": "2.2.1.i18n",
                    "x-tt-dm-status": "login=0;ct=1;rt=6",
                    "x-tt-store-region": "id",
                    "x-tt-store-region-src": "did",
                    "x-ss-dp": "0",
                    "user-agent": "com.zhiliaoapp.musically/2022708040 (Linux; U; Android 13; en; sdk_gphone64_arm64; Build/TPB4.220624.004; Cronet/TTNetVersion:07232c86 2022-12-15 QuicVersion:5f23035d 2022-11-23)",
                    "accept-encoding": "gzip",
                    "x-common-params-v2": "ab_version=27.8.4&ac=wifi&ac2=unknown&aid=1233&app_language=en&app_name=musical_ly&app_type=normal&build_number=27.8.4&carrier_region=ID&carrier_region_v2=310&cdid=6201473b-d2c5-4263-9784-81624c158a29&channel=googleplay&current_region=ID&device_brand=google&device_platform=android&device_type=sdk_gphone64_arm64&dpi=440&language=en&locale=en&manifest_version_code=2022708040&mcc_mnc=51000&op_region=ID&os_api=33&os_version=13&region=US&residence=ID&resolution=1080*2154&ssmix=a&sys_region=US&timezone_name=Asia%2FKarachi&timezone_offset=18000&uoo=0&update_version_code=2022708040&version_code=270804&version_name=27.8.4"
                }
                response = requests.get(url, headers=headers, params=querystring)
                res=(response.content)
                msg = pr.aweme_v2_feed_response()
                msg.ParseFromString(res)
                dict_msg = json.loads(MessageToJson(msg))
                data=dict_msg["awemeList"][0]

                # # data=""
                # datas=dict_msg["awemeList"]
                # for data1 in datas:
                #     print(data1["awemeId"])
                #     if str(data1["awemeId"])==str(aweme_id):
                #         data=data1
                #         print(data)
                #         break
                #     else:
                #         continue

                
                user_name = data["author"]["uniqueId"]
                nick_name = data["author"]["nickname"]
                post_url = data["shareUrl"]
                region = data["region"]
                song_name = data["music"]["title"]
                comment_count = data["statistics"].get("commentCount")
                likes_count = data["statistics"].get("diggCount")
                download_count = data["statistics"].get("downloadCount")
                views_count = data["statistics"].get("playCount")
                share_count = data["statistics"].get("shareCount")
                upmusic_id = data["music"]["id"]
                upmusic_author = data["music"]["author"]
                upmusic_title = data["music"]["title"]
                print('UGC.337', upmusic_id, upmusic_author, upmusic_title)

                def remove_emojis(data):
                    emoj = re.compile("["
                                      u"\U0001F600-\U0001F64F"
                                      u"\U0001F300-\U0001F5FF"
                                      u"\U0001F680-\U0001F6FF"
                                      u"\U0001F1E0-\U0001F1FF"
                                      u"\U00002500-\U00002BEF"
                                      u"\U00002702-\U000027B0"
                                      u"\U00002702-\U000027B0"
                                      u"\U000024C2-\U0001F251"
                                      u"\U0001f926-\U0001f937"
                                      u"\U00010000-\U0010ffff"
                                      u"\u2640-\u2642"
                                      u"\u2600-\u2B55"
                                      u"\u200d"
                                      u"\u23cf"
                                      u"\u23e9"
                                      u"\u231a"
                                      u"\ufe0f"
                                      u"\u3030"
                                      "]+", re.UNICODE)
                    return re.sub(emoj, '', data)
                post_data = {"number": str(num),
                             "username": user_name,
                             "nick_name": remove_emojis(nick_name),
                             "music_title": song_name,
                             "post_url": (post_url.split("?"))[0],
                             "likes_count": likes_count,
                             "comment_count": comment_count,
                             "download_count": download_count,
                             "views_count": views_count,
                             "share_count": share_count,
                             "region": region,
                             "upmusic_id": upmusic_id,
                             "upmusic_author": upmusic_author,
                             "upmusic_title": upmusic_title}
                with open("{}.csv".format(out), 'a+', encoding="utf-8-sig", newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=[*post_data])
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    writer.writerow(post_data)
                    return
            # except Exception as e:
            #     print(e, "==========")
            #     continue
        # exit(1)
        # post_data = {"number": str(num),
        #              "username": "error",
        #              "music_title": url.strip(),
        #              "post_url": "nil",
        #              "likes_count": "nil",
        #              "comment_count": "nil",
        #              "download_count": "nil",
        #              "views_count": "nil",
        #              "share_count": "nil",
        #              "region": "nil",
        #              "upmusic_id": "nil",
        #              "upmusic_author": "nil",
        #              "upmusic_title": "nil"}
        # with open("{}.csv".format(out), 'a+', encoding="utf-8-sig", newline='') as csvfile:
        #     writer = csv.DictWriter(csvfile, fieldnames=[*post_data])
        #     if csvfile.tell() == 0:
        #         writer.writeheader()
        #     writer.writerow(post_data)

    def get_posts_data(self, target_song_url, out):
        
        for i in target_song_url:
            i=i.strip()
            url = i.split(";")[1]
            music_id = i.split(";")[0]
            self.get_post_id(url, music_id)


inn = open(sys.argv[1]).readlines()
out = sys.argv[2].replace(".csv", "")
eq = "sessionid="+uuid.uuid4().hex.lower()[0:32]
feed = Scrapper(eq).get_posts_data(inn, out)
