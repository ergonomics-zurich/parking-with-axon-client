import random
import time

import requests


def cards():
    return requests.get("http://localhost:8080/cards").json()


def issue_card():
    requests.post("http://localhost:8080/cards")


def card_ids():
    return [o['cardId'] for o in requests.get("http://localhost:8080/cards").json()]


def recharge_card(uid, amount=2.5):
    requests.post(f"http://localhost:8080/cards/{uid}/credit/{amount:.2f}")


def garages():
    return requests.get("http://localhost:8080/garages").json()


def register_garage():
    requests.post("http://localhost:8080/garages")


def garage_ids():
    return [o['garageId'] for o in requests.get("http://localhost:8080/garages").json()]


def request_entry(gid, uid):
    return requests.post(f"http://localhost:8080/garages/{gid}/request-entry/{uid}").json()


def confirm_entry(gid, uid):
    requests.post(f"http://localhost:8080/garages/{gid}/confirm-entry/{uid}")


def request_exit(gid, uid):
    return requests.post(f"http://localhost:8080/garages/{gid}/request-exit/{uid}").json()


def confirm_exit(gid, uid):
    requests.post(f"http://localhost:8080/garages/{gid}/confirm-exit/{uid}")


def active_permits():
    return requests.get("http://localhost:8080/backoffice/active-permits").json()


if __name__ == '__main__':
    gids = garage_ids()
    uids = card_ids()
    idle = set()

    for gid in gids:
        for uid in uids:
            idle.add((gid, uid))

    print("total combinations", len(idle))

    for p in active_permits():
        permit = p['permit']
        idle.remove((permit['garageId'], permit['cardId']))

    print("free combinations", len(idle))

    time.sleep(1.0)

    while True:
        if len(idle) and random.random() < 0.9:
            gid, uid = random.choice(list(idle))
            print("selected", gid, uid)

            if not request_entry(gid, uid):
                print(f"garage {gid} is full")
                continue

            confirm_entry(gid, uid)
            idle.remove((gid, uid))

        else:
            for p in active_permits():
                if random.random() < .20:
                    gid = p['permit']['garageId']
                    uid = p['permit']['cardId']

                    if request_exit(gid, uid):
                        confirm_exit(gid, uid)
                        idle.add((gid, uid))
                        print('exited', gid, uid)
                    else:
                        recharge_card(uid)
                        print('recharged', uid)

        time.sleep(0.1)
