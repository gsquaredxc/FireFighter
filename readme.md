# Documentation

## Usage:

do something

## Config:

### General config:

**spam_channel**

The ID of the channel to send possible spam to

**mute_role**

The ID of the role to give to people so they are muted

### Actions allowed by all:

**allow_delete_all**

Allows spam discord to delete messages

**allow_ban_all**

Allows spam discord to ban spammers

### Weight for actions:

**report_to_all**

The weight to report to spam discord at

**report_to_spam_channel**

The weight to report to the spam channel on your discord at

**mute**

The weight to mute the user spamming at

### Weight to add for messages:

**ping_spam_min**

The minimum number of pings in a message before a message is targeted by bot

**ping_spam_base**

The default weight for being caught for ping spam

**ping_spam_mult**

The weight to add per ping

**role_spam_min**

The minimum number of role pings in a message before a message is targeted by bot

**role_spam_base**

The default weight for being caught for role ping spam

**role_spam_mult**

The weight to add per role ping

### Weight to add for users:

**user_age_0**

The weight to add for a user less than 1 day old

**user_age_max**

The maximum age that receives a penalty for being a young account

**user_age_mult**

What weight to give per day under the maximum age