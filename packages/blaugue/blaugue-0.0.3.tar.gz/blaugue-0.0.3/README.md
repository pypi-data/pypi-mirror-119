# Documentation:

## Basic usage:
```python
from blaugue.api import Blaugue

blaugueAPI = Blaugue(email='armand@camponovo.xyz', password='password')

search = blaugueAPI.search('query') # search 'query'
results = search.results # all results
for i in results:
    print(f'Object {i.__class__.__name__}') # print class name of result i
users = blaugueAPI.all_users()
for i in users:
    print(i.name)

```

## Chat usage:
```python
from blaugue.api import Blaugue

api = Blaugue(email='armand@camponovo.xyz', password='password')

chats = api.get_chats() # get all chats and return BlaugueChat() list

for chat in chats:
    print(chat.name) # print chat name
    for message in chat.messages:
        if chat.id == 'blaugue':  # all of users are in this chat, message.receiver will return a list
            print(message.author.name)
            print([user.name for user in message.receiver])  # print list of string of usernames
        else:
            print(message.author.name)
            print(message.receiver.name)
    print('\n\n')
```

## Type variables:
#### If you use an intelligent ide, type your variables to improve coding experience
```python
from blaugue.user import BlaugueUser
from blaugue.post import BlauguePost
from blaugue.tag import BlaugueTag
from blaugue.api import Blaugue
from blaugue.chat import BlaugueChat, BlaugueMessage

api = Blaugue(email='armand@camponovo.xyz', password='password')

search = api.search('armand')

posts = search.posts_results
post: BlauguePost
users = search.users_results
user: BlaugueUser
tags = search.tags_results
tag: BlaugueTag
chat: BlaugueChat
message: BlaugueMessage

for post in posts:
    print(post.title)

for tag in tags:
    print(tag.name)

for user in users:
    print(user.name)

for chat in api.get_chats():
    print(chat.name)
    for message in chat.messages:
        print(message.author.name)
```

## Classes:
### blaugue.api.Blaugue():
init:<br>
> Blaugue(email='you@email.com', password='12345')<br>

methods:
> `search(self, query)`: return [BlaugueResults()](#blauguesearchblaugueresults) of query<br>
> `get_user(self, email)`: return [BlaugueUser()](#blaugueuserblaugueuser) of email<br>
> `get_post(self, post_id)`: return [BlauguePost()](#blauguepostblauguepost) of post id<br>
> `get_chats(self)`: return list of [BlaugueChat()](#blauguechatblauguechat) of all chats (can be accessed by connected user)<br>
> `get_chat(self, chat_id)`: return [BlaugueChat()](#blauguechatblauguechat) object of chat<br>
> `all_users(self)`: return list of [BlaugueUser()](#blaugueuserblaugueuser) of all users<br>

properties:

> `None`: return None

### blaugue.search.BlaugueResults():

init:<br>

> BlaugueResults(infos, super)<br>

methods:

> `None`: return None

properties:

> `results`: return a list of [BlaugueUser()](#blaugueuserblaugueuser) / [BlauguePost()](#blauguepostblauguepost) / [BlaugueTag()](#blauguetagblauguetag) objects<br>
> `json_results`: return a json with results<br>
> `users_results`: return a list of [BlaugueUser()](#blaugueuserblaugueuser) objects<br>
> `posts_results`: return a list of [BlauguePost()](#blauguepostblauguepost) objects<br>
> `tags_results`: return a list of [BlaugueTag()](#blauguetagblauguetag) objects<br>

<br>

### blaugue.user.BlaugueUser():

init:<br>

> BlaugueUser(infos, super)<br>

methods:

> `None`: return None

properties:

> `name`: return str of user's name<br>
> `id`: return str of user's id<br>
> `avatar`: return str of user's avatar url<br>
> `premium`: return bool (True if user is premium, False else)<br>
> `premium_icon`: return str of user's premium icon url<br>
> `bot`: return bool (True if user is a bot, False else)<br>
> `badges`: return list of user's badges<br>
> `description`: return str of user's description<br>
> `url`: return str of user's profil url<br>

<br>

### blaugue.post.BlauguePost():

init:<br>

> BlauguePost(infos, super)<br>

methods:

> `None`: return None

properties:

> `title`: return str of post's title<br>
> `subtitle`: return str of post's subtitle<br>
> `html_content`: return str of post's html_content<br>
> `markdown_content`: return str of post's markdown_content<br>
> `image`: return str of post's cover image url<br>
> `book`: return str of post's book url<br>
> `id`: return str of post's id<br>
> `url`: return str of post's url<br>
> `author`: return [BlaugueUser()](#blaugueuserblaugueuser) of post's author<br>
> `type`: return [BlaugueTag()](#blauguetagblauguetag) of post's tag / type<br>
> `comments`: return list of dict of post's comments<br>

<br>

### blaugue.tag.BlaugueTag():

init:<br>

> BlaugueTag(infos, super)<br>

methods:

> `None`: return None

properties:

> `name`: return str of tag's name<br>
> `posts`: return list of [BlauguePost()](#blauguepostblauguepost) of tag's posts<br>
> `url`: return str of tag's url<br>

<br>

### blaugue.chat.BlaugueChat():

init:<br>

> BlaugueChat(infos, super)<br>

methods:

> `None`: return None

properties:

> `name`: return str of chat's name<br>
> `id`: return str of chat's id (can be used to get a chat)<br>
> `messages`: return list of [BlaugueMessage()](#blauguechatblauguemessage) objects<br>

<br>

### blaugue.chat.BlaugueMessage():

init:<br>

> BlaugueMessage(infos, super, chat)<br>

methods:

> `None`: return None

properties:

> `html_content`: return str of message's html content (with < br > and &nbsp ;)<br>
> `content`: return str of message's content (without < br > and &nbsp ;)<br>
> `author`: return [BlaugueUser()](#blaugueuserblaugueuser) object of message's author<br>
> `receiver`: return [BlaugueUser()](#blaugueuserblaugueuser) object of message's receiver (list of if chat is the common chat)<br>

<br>

## Get information about connected account:
```python
from blaugue.api import Blaugue

blaugueAPI = Blaugue(email='armand@camponovo.xyz', password='password')

# check if account has been connected
if bool(blaugueAPI):
    print('Account informations are right !')

# get name of connected account
print(str(blaugueAPI))
    
# get token of connected account
print(next(blaugueAPI))

# get bytes of hash of password of current account
print(bytes(blaugueAPI))

# get BlaugueUser() object of connected account
connected = blaugueAPI.connected
print(connected.name)
print(connected.avatar)
print(connected.premium_icon)
```