import time

from fake_useragent import UserAgent
import requests
import json

ua = UserAgent()
result = []


def collect_channels():
    url = "https://gql.twitch.tv/gql#origin=twilight"
    cursor = ""
    with open("req_channels.json", "r+") as file:
        json_to_req = json.load(file)
    page = 1
    while True:
        json_to_req[0]["variables"]["cursor"] = cursor
        response = requests.post(url=url, headers={
            "user-agent": f"{ua.random}", "Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"},
                                 json=json_to_req)
        data = response.json()
        streams = data[0]["data"]["game"]["streams"]["edges"]
        cursor = streams[-1]['cursor']
        for stream in streams:
            count_of_viewers = stream["node"]["viewersCount"]
            title = stream["node"]["title"]
            streamer = stream["node"]["broadcaster"]["login"]
            stream_link = f"https://www.twitch.tv/{streamer}"
            streamer_id = stream["node"]["broadcaster"]["id"]
            result.append(
                {
                    "count_of_viewers": count_of_viewers,
                    "title": title,
                    "streamer": streamer,
                    "link": stream_link,
                    "id": streamer_id
                }
            )
        if page == 5:
            break
        page += 1
        time.sleep(0.5)
        print("Take data on page", page)
    result.reverse()
    with open("channels.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)
    print("Count of streamers = ", len(result))


def main():
    collect_channels()


if __name__ == "__main__":
    main()
