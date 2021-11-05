import requests

file_list = ['workflow-api', 'trilead-api', 'pipeline-input-step', 'fstrigger', 'command-launcher', 'structs', 'ldap',
             'matrix-auth', 'github-branch-source', 'jquery', 'timestamper', 'okhttp-api', 'workflow-cps-global-lib',
             'pipeline-model-api', 'subversion', 'thinBackup', 'script-security', 'pipeline-build-step', 'jquery3-api',
             'mailer', 'pipeline-rest-api', 'cloudbees-folder', 'jackson2-api', 'ssh-credentials', 'handlebars',
             'scm-api', 'filesystem_scm', 'jdk-tool', 'mapdb-api', 'workflow-aggregator', 'workflow-step-api',
             'pipeline-stage-step', 'resource-disposer', 'branch-api', 'workflow-support', 'workflow-durable-task-step',
             'snakeyaml-api', 'gradle', 'bouncycastle-api', 'workflow-job', 'git', 'job-import-plugin',
             'pipeline-stage-tags-metadata', 'workflow-cps', 'github', 'echarts-api', 'workflow-basic-steps',
             'matrix-project', 'pipeline-model-extensions', 'jquery-detached', 'ant', 'pipeline-github-lib',
             'git-server', 'token-macro', 'workflow-scm-step', 'pipeline-milestone-step', 'lockable-resources',
             'ws-cleanup', 'pam-auth', 'junit', 'momentjs', 'jsch', 'credentials-binding', 'jaxb',
             'pipeline-stage-view', 'apache-httpcomponents-client-4-api', 'antisamy-markup-formatter',
             'filesystem-list-parameter-plugin', 'durable-task', 'display-url-api', 'credentials',
             'pipeline-model-definition', 'plugin-util-api', 'plain-credentials', 'build-timeout', 'git-client',
             'github-api', 'ssh-slaves', 'git-parameter', 'pipeline-graph-analysis', 'workflow-multibranch',
             'email-ext', 'ace-editor', 'htmlpublisher', 'envinject-api', 'envinject', 'simple-theme-plugin']


def install(tar_file):
    # because there is system proxy
    proxies = {
        'http': '127.0.0.1:8080',
        'https': '127.0.0.1:8080'
    }

    url = "http://127.0.0.1:8080/pluginManager/uploadPlugin"

    payload = {}

    files = [
        ('file', (tar_file, open('file\\' + tar_file, 'rb'), 'application/octet-stream'))
    ]

    '''
        44Om44O844K2OuODkeOCueODr+ODvOODiQ== 
            <jenkins username>:<jenkins user token>
            how to get token, pleas refer to mop.md
    '''

    headers_data = {
        'Authorization': 'Basic 44Om44O844K2OuODkeOCueODr+ODvOODiQ=='
    }

    requests.post(url, headers=headers_data, data=payload, files=files, proxies=proxies)


for var in file_list:
    install(var + ".hpi")
