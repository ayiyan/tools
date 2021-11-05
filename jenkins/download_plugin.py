from load_json import JENKINS
import requests


def download(file, version):
    target_file = file + ".hpi"
    url = "https://ftp.belnet.be/mirror/jenkins/plugins/%s/%s/%s" % (file, version, target_file)

    res = requests.get(url)
    if res.status_code == 200:
        tar_path = "D:\\Data\\Python_Data\\jenkins\\"

        with open(tar_path + target_file, "wb") as file:
            file.write(res.content)
        

for var in JENKINS["plugins"]:
    download(var["shortName"], var["version"])
