#!/usr/bin/python
try:
    import paramiko
except Exception as e:
    pass

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
ssh.connect('192.168.43.55', username='pi', password='raspberry')
#라즈베리파이 ssh 접속

stdin, stdout, stderr = ssh.exec_command('raspistill -o sample.jpg')
#사진 촬영 명령 실행
print("Complete")
for line in stdout:
    print('this is stdout')
    print('...' + line.strip('\n'))
for line in stderr:
    print('this is stderr')
    print('...' + line.strip('\n'))
#사진 촬영 실패시 출력
ssh.close()