## CMDB

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

### init data
```shell
python manage.py loaddata inventory/hosts.json
```

### run
```shell
python manage.py runserver
```

<details>
<summary>celery</summary>
```shell
celery -A tasks worker -l info -P eventlet
celery -A tasks beat -l info --pidfile=/tmp/celery-beat.pid
celery -A tasks flower --broker=redis://:beRcnLADAJdsycZKrdKseR8d@127.0.0.1:6380/0 --pidfile=/tmp/celery-flower.pid
```
<br>

### Django admin
[admin](http://127.0.0.1:8000/admin)

### refs

[runner-api](https://ansible.readthedocs.io/projects/runner/en/stable/python_interface/#runner-status-handler)
[ansible doc](https://docs.ansible.com/ansible/latest/getting_started/index.html)

### TODO tree
1. TODO
2. BUG
3. mark
4. tag
5. done
6. test