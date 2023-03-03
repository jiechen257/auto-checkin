## 概述
易校园打卡脚本，配合云服务器的定时任务功能可以实现每天自动打卡

## 技术实现
1. https抓取易校园的打卡接口名称和数据，拿到必要的参数（个人信息和登录凭证
2. 利用python脚本构造实体数据，发送http请求
3. 脚本集成邮箱的smtp转发，发邮件通知打卡结果
4. 利用服务器的shell做定时任务，每天打卡

## 使用
### 配置python环境
安装python依赖（包yagmail使用pip安装有问题，转去使用pip3，包有相关issues说明

数据和环境配置好后，执行 `python app.py` 显示detail详情和打卡成功的回调即可
### 打卡功能

> 这部分需要进行https抓包，可以使用whistle或者charles，记得安装ca证书

先看抓包的请求列表：
![](https://cdn.becase.xyz/20220920095804.png)

*getDetail获取个人打卡信息，doDetail发送post请求打卡*

首先根据 `getDetail` 拿到个人信息，data数据格式参考以下
```js
"id": "",
"schoolCode": "",
"schoolName": "",
"identityType": "1",
"userId": "",
"mobilePhone": "",
"name": "",
"jobNo": "",
"departmentCode": "",
"department": "",
"specialitiesCode": "",
"specialities": "",
"classCode": "",
"className": "",
"provinceCode": "",
"province": "",
"cityCode": "",
"city": "",
"inSchool": "0",
"contactArea": "1",
"isPatient": "1",
"contactPatient": "1",
"linkPhone": "",
"parentsPhone": "",
"createTime": "",
"createDate": "",
"updateTime": "",
"locationInfo": "",
"longitudeAndLatitude": "",
"isSuspected": "1",
"healthStatusNew": "1",
"holidayInSchool": "1",
"identitySecondType": "11",
"districtCode": "",
"district": "",
"isFamiliyPatient": "1",
"isCommunityPatient": "1",
"isTodayBack": "1",
"backRemark": "",
"backProvince": "",
"backCity": "",
"backDistrict": "",
"patientHospital": "",
"isolatedPlace": "",
"temperatureAfter": "36.6",
"identity": "111111",
"country": "",
"address": "",
"backWay": "",
"backWayName": "",
"backAddress": "",
"isInCompany": "",
"backProvinceCode": "",
"backCityCode": "",
"backDistrictCode": "",
"token": "",
"uuToken": "",
"loginUserId": "",
"loginUserName": "",
"loginSchoolCode": "",
"loginSchoolName": "
```

然后使用 `doDetail` 将上一步获取的detail数据发送出去即可

打卡成功的返回字段格式如下：
```json
"statusCode": 0,
"message": "操作成功",
"data": {}
```

### 邮箱的smtp
脚本中使用了邮箱的smtp来进行`打卡操作结果`的实时通知

![](https://cdn.becase.xyz/20220920100818.png)

### 自动化
使用云服务器的自动任务执行功能，宝塔配置如下，其他自动化脚本自行google

![](https://cdn.becase.xyz/20220920101509.png)
