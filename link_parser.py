import json
import time

import requests
from fake_useragent import UserAgent

from channels_parser import collect_channels

ua = UserAgent()
result = []


def collect_links():
    collect_channels()
    with open("req_panels.json", encoding="utf-8") as file:
        json_to_req = json.load(file)
    url = "https://gql.twitch.tv/gql#origin=twilight"

    with open("channels.json", encoding="utf-8") as file:
        data = json.load(file)

    for streamer in data:
        time.sleep(0.2)
        print("Check streamer",streamer["id"])
        json_to_req[0]["variables"]["id"] = streamer["id"]
        response = requests.post(url=url, headers={
            "user-agent": f"{ua.random}", "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
                                 json=json_to_req)
        data = response.json()
        panels = data[0]["data"]["user"]["panels"]
        steam_trade_link = None
        steam_link = None
        steam_personal_link = None
        command = None
        for p in panels:
            for value in p.values():
                if value is not None and len(value) < 100:
                    steam_link_res = value.lower().find("https://steamcommunity.com/profiles")
                    if steam_link_res is None and steam_link_res != -1:
                        steam_link = value

                    trade_link_res = value.lower().find("https://steamcommunity.com/tradeoffer")
                    if steam_trade_link is None and trade_link_res != -1:
                        steam_trade_link = value

                    personal_link_res = value.lower().find("https://steamcommunity.com/id")
                    if steam_personal_link is None and personal_link_res != -1:
                        steam_personal_link = value

                    trade_command_res = value.lower().find("!trade")
                    if command is None and trade_command_res != -1:
                        command = "!trade"

        if steam_trade_link is not None or steam_link is not None or steam_personal_link is not None or command is not None:
            result.append({
                "count_of_viewers": streamer["count_of_viewers"],
                "title": streamer["title"],
                "streamer": streamer["streamer"],
                "link": streamer["link"],
                "steam_trade_link": steam_trade_link,
                "steam_link": steam_link,
                "steam_personal_link": steam_personal_link,
                "Command available": command
            })

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    collect_links()


if __name__ == "__main__":
    main()
