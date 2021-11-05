1, 通过用户名和密码 获取 crumb

http://10.163.167.172:8080/crumbIssuer/api/xml

读取 d4892e4fbbe68014b2c8adcbb2b8055e16f863048b76be01f51c4ece16e408499

```
<defaultCrumbIssuer _class='hudson.security.csrf.DefaultCrumbIssuer'>
    <crumb>d4892e4fbbe68014b2c8adcbb2b8055e16f863048b76be01f51c4ece16e408499</crumb>
    <crumbRequestField>Jenkins-Crumb</crumbRequestField>
</defaultCrumbIssuer>
```

2, build job
http://x.x.x.x:8080/job/test1/buildWithParameters

Authorization: 
b64encode
格式：  `"<user>:<password>"`

```
headers:
Jenkins-Crumb: d4892e4fbbe68014b2c8adcbb2b8055e16f863048b76be01f51c4ece16e408499
Content-Type: application/json
Authorization: 44Om44O844K2OuODkeOCueODr+ODvOODiQ==
```

body:
```
{
  "parameter": [
    {
      "name": "test_name",
      "value": "test_value"
    }
  ]
}
```