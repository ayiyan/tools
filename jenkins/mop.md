1, unzip jenkins package
```
jar -xvf jenkins_2.235.5.war
```

2, start jenkins
```
nohup java -jar jenkins_2.235.5.war & 
```

3, jenkins pulg download  link

```
https://updates.jenkins.io/download/plugins/ldap/
```

4, get  plug  info for jenkins

```
http://127.0.0.1:8080/pluginManager/api/json?depth=2
```


5, install plug by curl comamnd
5.1
```
curl -i -F "file=@jsch.hpi" http://127.0.0.1:8080/pluginManager/uploadPlugin --header 'Authorization: Basic 44Om44O844K2OuODkeOCueODr+ODvOODiQ=='
```

5.2
```
Authorization: Basic 44Om44O844K2OuODkeOCueODr+ODvOODiQ==

base64:
<jenkins web login username>:<user token>
```

5.3 get user token
```
user property - Configure - API Token - add new token
```
