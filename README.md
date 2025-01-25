# TeinvCAPTCHA

## What is it

This project is designed to analyze group members to identify bots, dead accounts, and inactive members for further administration.

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

- If there are up to a trishold (50 by default), then each message is pulled out for further analysis:
    - Text
    - Date of change
    - ID
    - The date the message was written

    In this case, the confidence level is 0.5

- If there are more messages than treshhold, then the trust level is maximized.

4. Finally the report made is written to a *.json file
5. Then all user avatars are downloaded by file_id for further analysis