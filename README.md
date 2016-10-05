# Spotted API

Basic RESTful API to list, predict and hold Spotted Objects from SpottedBot apps

## Getting an Access Token

You can't.
Once the datasets are large enough, I'll begin distributing tokens

## How do I get a list of Spotted Objects?

Access:
https://spottedapi.herokuapp.com/spam-list/
or
https://spottedapi.herokuapp.com/not-spam-list/

You can also perform HTTP calls:

```sh
GET https://spottedapi.herokuapp.com/spam-list/
```
or
```sh
GET https://spottedapi.herokuapp.com/not-spam-list/
```

Example:
```
curl -X GET https://spottedapi.herokuapp.com/spam-list/'
```

You can perform 1000 of those calls per day.

The response contains 4 objects, `count` which is the number of elements found, `results`, which contains the elements found, `next`, which is the next page and `previous`, the previous page
In `results` you have 2 sub objects, `message` which, surprisingly, is the Spotted itself and `info`, containing `id`, the Spotted ID

The pages default to 100 items per page.

```
response
        '
        next (str)
        '
        previous (str)
        '
        count (int)
        '
        results
                '
                message (string)
                '
                info
                    '
                    id (int)
```

## How can I predict a message?

Once you have your token, do:

```sh
POST https://spottedapi.herokuapp.com/predict/
     Header: Authorization
     Value: Token <your-token>

     Form: message=<Spotted-message-as-string>
```

Example:
```
curl -X POST http://localhost:8000/predict/ -F 'message=<spotted-message>' -H 'Authorization: Token <your-token>'
```

You can perform 100 of those calls per day.

The response contains 1 object, `isSpam`, a Boolean.

```
response
        '
        isSpam (bool)
```

Keep in mind that every message you submit for prediction is saved alongside your username.
We do this so that your messages can be later added to our dataset for better predictions.


## How can I submit my datasets?

Only Admins have rights to submit entire datasets.

To do this,
```sh
POST https://spottedapi.herokuapp.com/submit-data/
     Header: Authorization
     Value: Token <your-admin-token>

     Form: list: [ {"message": <spotted-as-str>, "spam": <isSpamBool>}, ]
```

You can submit as many Spotteds as necessary, but try to do it 1000 at a time, maximum. You may encounter server timeouts otherwise.
Please take extra care when submitting, so that the labels are correct.

Example:
```
curl -X POST http://localhost:8000/submit-data/ -F 'list=[{"message":<Spotted>, "spam": <bool>}, {"message": <Spotted>, "spam": <bool>}]' -H 'Authorization: Token <your-admin-token>'
```

