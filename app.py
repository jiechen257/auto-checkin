# -*- coding: utf-8 -*-
import requests
import yagmail
import logging
from typing import Dict, Any

"""
@Author  : jiechen
@Email   : xxx@qq.com
@Filename: app.py
@Date    : 2021/4/19
@Desc    : 易校园自动打卡
"""

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(email_to: str, email_title: str, email_content: str) -> bool:
    # 邮件配置
    mail_config = {
        'user': 'xxx@qq.com',
        'password': '',  # 授权码
        'host': 'smtp.qq.com'
    }
    
    try:
        with yagmail.SMTP(**mail_config) as yag:
            yag.send(to=email_to, subject=email_title, contents=email_content)
        logging.info("邮件发送成功")
        return True
    except Exception as e:
        logging.error(f"邮件发送失败: {e}")
        return False

def do_detail(data: Dict[str, Any], userid: str) -> Dict[str, Any]:
    # 更新打卡信息
    data.update({
        'address': '',
        'uuToken': '',
        'loginUserId': userid,
        'loginSchoolCode': '',
        'loginSchoolName': '',
        'temperature': '',
        'locationInfo': "",
        'longitudeAndLatitude': '',
        'ymId': userid,
        'sessionId': "",
        'loginUserName': "",
        'platform': "",
    })
    
    try:
        response = requests.post(
            "https://h5.xiaofubao.com/marketing/health/doDetail",
            headers=headers,
            data=data,
            verify=False
        )
        return response.json()
    except requests.RequestException as e:
        logging.error(f"请求失败: {e}")
        return {"success": False, "message": str(e)}

def get_detail(userid: str) -> Dict[str, Any]:
    data = {
        "loginUserId": userid,
        "ymId": userid,
        "sessionId": "",
        "loginUserName": "",
        "loginSchoolCode": "",
        "loginSchoolName": "",
        "platform": "",
    }
    
    try:
        response = requests.post(
            "https://h5.xiaofubao.com/marketing/health/getDetail",
            headers=headers,
            data=data,
            verify=False
        )
        return response.json()
    except requests.RequestException as e:
        logging.error(f"请求失败: {e}")
        return {"success": False, "message": str(e)}

if __name__ == '__main__':
    # 禁用 urllib3 的警告
    requests.packages.urllib3.disable_warnings()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SEA-AL10 Build/HUAWEISEA-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 ZJYXYwebviewbroswer ZJYXYAndroid tourCustomer/yunmaapp.NET/4.2.8/yunma03c72fa3-9ef6-4b4c-9cfd-9c0743ffcd80',
        'Cookie': ''
    }
    
    global_user_id = ''  # 请填写实际的用户ID
    
    # 获取详情
    detail_json = get_detail(global_user_id)
    logging.info(f"获取详情结果: {detail_json}")
    
    if detail_json.get('success'):
        # 执行打卡
        result_json = do_detail(detail_json['data'], global_user_id)
        logging.info(f"打卡结果: {result_json}")
        
        # 发送邮件通知
        if result_json.get('success'):
            send_email(email_to='xxx@qq.com', email_title='健康打卡成功!', email_content=str(result_json))
            logging.info('打卡成功')
        else:
            send_email(email_to='xxx@qq.com', email_title='健康打卡失败!', email_content=str(result_json))
            logging.warning('打卡失败')
    else:
        logging.error('获取详情失败')
