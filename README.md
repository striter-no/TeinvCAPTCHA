# TeinvCAPTCHA

## What is it

This project is designed to analyze ad and fishing userbots group members to identify bots, dead accounts, and inactive members for further administration.

## How to use it

Before you start working with the software part you need to register the application in Telegram (via [this link](https://my.telegram.org/auth?to=apps)). You need to create an application and copy api_id and api_hash from there.

Next, move `tg-config.json` from the `templates` folder to the main folder. 

Paste the api_id and api_hash into the appropriate fields:
Also you need your personal Telegram UID for it.

```
{
    "api_id": "1234",
    "api_hash": "abcdef1234",
    "your_id": 1234
}
```

To start using it, it is advisable to create `venv` and use it:

```shell
python -m venv venv
source ./venv/bin/activate # For linux
```

Next, install all the necessary libraries:

```shell
pip install -r ./reqs.txt
```

Finally, you can run the main file:

```shell
python ./main.py
```

At the beginning you will be prompted to log in to your account, log in. Pass 2FA if you have it enabled.

After in telegram you can write to __any__ chat room 

```plain
!anl --group_type TYPE --chat_id ID [--send_back]
```

Where instead of ID is the ID of the group or supergroup
Instead of TYPE - type of group:
- `group` : Regular group
- `supergroup` : Supergroup

>TIP: You can type arguments in any order and not only in 1 line:

```
!anl 
    --group_type TYPE 
    --chat_id ID 
    [--send_back]
```


You can use `--send_back` to send the report archive back to you saved messages. For example:

```plain
!anl 
    --group_type group 
    --chat_id 1234 
    --send_back
```

## Where to see the ID of a group or supergroup

To view the ID you need:

1. Go to Telegram settings
2. Go to the "Advanced" tab
3. At the very bottom, click the "Experimental" tab
4. Enable the display of "Peer IDs"

## How to distinguish a group from a supergroup

- Group:
    - Number of members up to 200
    - No invitation link
    - Private only
- Supergroup:
    - Number of participants up to 200'00
    - Have invitation link
    - Can be either public or private



## How it works

The principle of operation for the Beta 2 version period is as follows: 
1. The program gets access to an open chat room (group or supergroup)
2. The program gets all users of the group, performing initial analysis

---
Primary (plain) analysis is obtaining public information about a user, i.e.:
- Full Name
- Username
- Phone number (if available)
- When was last online
- When joined the group
- How many posts have been written
- Small version of avatar
- Presence of premium on the account
- Unique Telegram User Identification Number (Telegram UID)
- Is this a bot or not
---

3. Depending on the number of messages:
- If there are 0 or 1 (only message about joining the group or basically none), then __level of trust__ becomes 0. This is probably a bot or a dead account

- If there are up to a treshhold (50 by default), then each message is pulled out for further analysis:
    - Text
    - Date of change
    - ID
    - The date the message was written

    In this case, the confidence level is 0.5

- If there are more messages than treshhold, then the trust level is maximized.

4. Finally the report made is written to a *.json file
5. Then all user avatars are downloaded by file_id for further analysis