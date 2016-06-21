from slackclient import SlackClient

AUTH_TOKEN = None
CHANNEL = None


def login():
    return SlackClient(AUTH_TOKEN)


def list_channels(client):
    channels_call = client.api_call("channels.list")
    if channels_call['ok']:
        return channels_call['channels']
    return None

def send_message(client, msg):
    client.api_call(
        "chat.postMessage",
        channel=CHANNEL,
        text=msg,
        username='pythonbot',
        icon_emoji=':robot_face:'
    )

if __name__ == '__main__':
    AUTH_TOKEN = 'xoxp-10953545509-10957732498-15510042997-4fde2b151b'
    CHANNEL = 'C0ATYUSKW'
    slack_client = login()
    # print list_channels(slack_client)
    send_message(slack_client, "%s - %s" % ('Naver', 'http://www.naver.com'))