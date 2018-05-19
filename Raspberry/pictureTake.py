#!/usr/bin/python
try:
    import paramiko
    import sys
    import time
    import os
except Exception as e:
    pass
#필요한 모듈 import.

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect('192.168.43.55', username='pi', password='raspberry')
#라즈베리파이 ssh 접속

id = sys.argv[1]
#프로그램 실행시 학번을 입력받는다.

command_mkdir = 'mkdir ' + id
ssh.exec_command(command_mkdir)
#입력된 학번을 폴더명으로 하여 폴더 생성

PI = '/home/pi/' + id
#라즈베리파이 사진 저장 경로
SERVER = '/Users/keith_lee/Desktop/' + id
#서버에서 사진을 전송받을 경로
i = 1
#변수 초기화

while True:
    itr = str(i)
    command_take = 'raspistill -t 1500 -o ' + PI + '/' + itr + '.jpg'
    ssh.exec_command(command_take)
    i = i + 1
    #지정된 이름으로 학번명으로 만든 폴더에 사진 촬영, 저장.
    stdin, stdout, stderr = ssh.exec_command('ls ' + PI + ' | wc -l')
    count = int(stdout.readlines()[0])
    #폴더 내 저장된 사진 갯수를 알아보기 위해 사용하는 명령.
    time.sleep(0.5)
    if(count == 25):
        break
    #사진 25장이 찍히면 종료.

command_chmod = 'chmod -R 777 ' + PI
ssh.exec_command(command_chmod)
#라즈베리파이 폴더 권한 수정

os.chdir('/Users/keith_lee/Desktop/' + id)
#작업 경로 이동

sftp = ssh.open_sftp()
fList = sftp.listdir(PI)
for f in fList:
    if('.jpg' in f):
        origin = os.path.join(PI, f)
        copy = os.path.join(SERVER, f)
        sftp.get(origin, copy)
sftp.close()
#라즈베리파이 사진 저장 경로를 스캔하여, 파일명이 .jpg인 경우에만 서버로 전송함. 전송 완료되면 sftp 사용 종료.

sfList = os.listdir(SERVER)
for files in sfList:
    path = os.path.join(SERVER, files)
    os.chmod(path, 0o755)
#전송된 사진파일 권한 설정

ssh.close()
#ssh 사용 종료.