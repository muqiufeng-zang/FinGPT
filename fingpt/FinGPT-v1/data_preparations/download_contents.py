import os
import pandas as pd
import numpy as np
import requests
from lxml import etree
import multiprocessing as mp
import json

# The result_path should be the results with only titles which is the IN path
result_path = os.path.realpath(r"../../../data/titles")
print(result_path)

# The result_with_content_path should be the results with titles and contents which is the OUT path
result_with_content_path = os.path.realpath(r"../../../data/contents")
print(result_with_content_path)
link_base = "https://guba.eastmoney.com"


def get_one_content(x):
    url = link_base + x["content link"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Referer": "https://guba.eastmoney.com/",
    }
    tunnel = "f290.kdltps.com:15818"
    username = "t19133033828858"
    password = "xskxp1g1"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    requests.DEFAULT_RETRIES = 5  # more retrys
    s = requests.session()
    s.keep_alive = False  # close connection when finished

    ok = False
    while not ok:
        try:
            print("###########################################")
            print("request:" + url)
            response = requests.get(url=url, headers=headers, proxies=proxies)
            # print("response code:" + str(response.status_code))
            if response.status_code == 200:
                res = etree.HTML(response.text)
                res = res.xpath("//script[2]//text()")[0]
                res = json.loads(res[17:])
                # res = pd.Series(res).to_frame().T
                res = pd.Series(res).to_frame().T.reset_index(drop=True);
                ok = True
                # print(res)
                print("request ok")
                # print("response:" + res)
                return res
        except Exception as e:
            print("发生异常:", e)
            pass


def get_content(file_name):
    df = pd.read_csv(os.path.join(result_path, file_name))

    new_columns = ['post_user', 'post_guba', 'post_publish_time', 'post_last_time',
                   'post_display_time', 'post_ip', 'post_checkState', 'post_click_count',
                   'post_forward_count', 'post_comment_count', 'post_comment_authority',
                   'post_like_count', 'post_is_like', 'post_is_collected', 'post_type',
                   'post_source_id', 'post_top_status', 'post_status', 'post_from',
                   'post_from_num', 'post_pdf_url', 'post_has_pic',
                   'has_pic_not_include_content', 'post_pic_url', 'source_post_id',
                   'source_post_state', 'source_post_user_id', 'source_post_user_nickname',
                   'source_post_user_type', 'source_post_user_is_majia',
                   'source_post_pic_url', 'source_post_title', 'source_post_content',
                   'source_post_abstract', 'source_post_ip', 'source_post_type',
                   'source_post_guba', 'post_video_url', 'source_post_video_url',
                   'source_post_source_id', 'code_name', 'product_type', 'v_user_code',
                   'source_click_count', 'source_comment_count', 'source_forward_count',
                   'source_publish_time', 'source_user_is_majia', 'ask_chairman_state',
                   'selected_post_code', 'selected_post_name', 'selected_relate_guba',
                   'ask_question', 'ask_answer', 'qa', 'fp_code', 'codepost_count',
                   'extend', 'post_pic_url2', 'source_post_pic_url2', 'relate_topic',
                   'source_extend', 'digest_type', 'source_post_atuser',
                   'post_inshare_count', 'repost_state', 'post_atuser', 'reptile_state',
                   'post_add_list', 'extend_version', 'post_add_time', 'post_modules',
                   'post_speccolumn', 'post_ip_address', 'source_post_ip_address',
                   'post_mod_time', 'post_mod_count', 'allow_likes_state',
                   'system_comment_authority', 'limit_reply_user_auth', 'post_id',
                   'post_title', 'post_content', 'post_abstract', 'post_state']
    # df[new_columns] = df.apply(lambda x: get_one_content(x), axis=1, result_type="expand", )
    # df[new_columns] = df.apply(lambda x: get_one_content(x).squeeze(), axis=1, result_type="expand", )
    df = df.apply(lambda x: get_one_content(x).squeeze(), axis=1, result_type="expand", )
    to_path = os.path.join(result_with_content_path, file_name)
    df.to_csv(to_path, index=False)


if __name__ == "__main__":
    pool_list = []
    res_list = []
    pool = mp.Pool(processes=1)

    file_list = os.listdir(result_path)
    # print(file_list[0])
    # get_content(file_list[0])

    for i in file_list:
        print(i)
        # print(file_list[i])
        res = pool.apply_async(get_content, args=(i,), error_callback=lambda x: print(x))
        pool_list.append(res)

    pool.close()
    pool.join()

    # 获取运行结果
    # for i in pool_list:
    #     res_list.append(i.get())

    print("All Done!")
