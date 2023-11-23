from src.service.mongo_init import init as mongo_init
from src.service.mysql_init import init as mysql_init


def main():
    mysql_init()
    mongo_init()


if __name__ == '__main__':
    main()