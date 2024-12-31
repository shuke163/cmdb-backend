~~## CMDB

### Depends

```shell
ansible == [core 2.18.1]
Python >= 3.9 
```

### requirements.txt

```shell
pipreqs ./ --encoding=utf8 --force
```

### install

```shell
pip install -r requirements.txt
```

### ansible-config

```shell
可以生成一个完全注释掉的示例 ansible.cfg 文件，例如
$ ansible-config init --disabled > ansible.cfg
还可以拥有一个包含现有插件的更完整的文件
$ ansible-config init --disabled -t all > ansible.cfg
ansible-inventory -i inventory/hosts --list
ansible-config dump --only-changed -t all
```

### run

```shell
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
or
python main.py
```

### celery

```shell
celery -A tasks worker -l info -P eventlet
celery -A tasks beat -l info --pidfile=/tmp/celery-beat.pid
celery -A tasks flower --broker=redis://:beRcnLADAJdsycZKrdKseR8d@127.0.0.1:6380/0 --pidfile=/tmp/celery-flower.pid
```

### refs

[runner-api](https://ansible.readthedocs.io/projects/runner/en/stable/python_interface/#runner-status-handler)
[ansible doc](https://docs.ansible.com/ansible/latest/getting_started/index.html)~~