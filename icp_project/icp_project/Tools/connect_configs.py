env = 'test'

if env == 'test':
    # 本地测试mysql
    MYSQL_LOCAL = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '12345',
        'db': 'xxx',
        'charset': 'utf8',
    }

    # 本地测试Redis
    REDIS_LOCAL = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 0
    }

    # 本地测试Mongo
    MONGO_LOCAL = {
        'url': 'mongodb://127.0.0.1:27017/',
        'db': 'test'
    }

    # 存放在Redis
    PROXY = {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 1,
    }


elif env == 'product':
  pass
else:
    pass
