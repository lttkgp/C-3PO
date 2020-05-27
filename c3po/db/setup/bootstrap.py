from db.common.base import session_factory


def start():
    session = session_factory()
    session.close()


if __name__ == "__main__":
    start()
    print("Worked yo!")
