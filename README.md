# 1Password local search
[![Build Status](https://travis-ci.org/mickaelperrin/onepassword-local-search.svg?branch=master)](https://travis-ci.org/mickaelperrin/onepassword-local-search) 
[![codecov](https://codecov.io/gh/mickaelperrin/onepassword-local-search/branch/master/graph/badge.svg)](https://codecov.io/gh/mickaelperrin/onepassword-local-search)

> This is an _**unofficial**_ tool focused on listing and decryption of secrets 
> with increased performance comparing to native op CLI

## 1Password version compatibility

- releases under 1.0.0 are for 1Password7
- releases after 1.0.0 are for 1Password8

## How to use ?

This tool do not replace the official CLI `op` of 1Password. You still need it to perform signin and grab session keys.

So, ensure that you have registered the OP_SESSION_team in your environment.

#### Database path

The script will try to search the database at standard path depending on your platform. It it fails or if you want
to use another database, you could set the env variable ONEPASSWORD_LOCAL_DATABASE_PATH with the path 
of the B5.sqlite database you want to use. 

### Get decrypted value
```
op-local get uuid [field] [--use-custom-uuid] [--use-lastpass-uuid]
```

#### TOTP

If you have created a field untitled "One-time password" with a field type "One time password", you can retrieve the
value of the totp by using the special field `totp`. For example: `op-local get uuid totp`.


### List items
```
op-local list [--format='{uuid} {title}'] [--filter=''] [--output-encoding=json]
```

The format string allows you to customize the ouput format of the list items. You can use any field, 
the first match in any section will be used.
 ```
 op-local list --format='{uuid}|{title}|{username}|{password}'
 ```
 
The filter will only return entries whose title contains the filter string. 

By appending, `--output-encoding=json`, you can generate proper JSON encoded lists. For example:
```
op-local list --format='{{"uuid": "{uuid}", "title": "{title}"}},' --output-encoding=json
```

### Is authenticated
```
op-local is-authenticated
```

Check if the 1Password session is opened.

### UUID mapping

uuid in 1Password changes when you move an item from one vault to another. To prevent this issue, a custom uuid
mapping feature has been implemented.

You need to add on each item a field named `UUID`.

Then run `op-local mapping update` to generate the mapping talbe relationship.

You can now get an item using your own `UUID` by appending the `--use-custom-uuid` flag to the `get` command.

`--use-lastpass-uuid` flag does the same thing but with a `LASTPASS_ID` field.

You can display UUID mapping by running `op-local mapping list`.

Since 0.16, and as, UUID v4, Lastpass ID and 1Password UUID are totally different, the search will be performed
over the adequate field regarding which type of uuid is given, without having to use any special flag.

### Multiple accounts

This project support multi-accounts decryption. However, keep in mind that you need:

- to authenticate with the main account of your 1Password desktop client
- to authenticate with the others accounts you want to use

## Known limitations

- Currently, vaults of type E (family shared ?) are not supported. I don't have the need of this kind of vaults currently. Not sure that I will work on this.
- Vaults which are not shared with you are not excluded and will fail the list process. I guess this is an easy fix that will come in a next release.
- Groups permissions are not implemented. Users must be attached to each vaults manually.

## Why this project ?

We use Ansible to manage infrastructures and use a lookup plugin to grab hundred of secrets. 
We used to use LastPass but we decided to move away due to unreliable API calls and unsupported CLI.
First benchmarcks of the native `op` tool, have demonstrated really poor performance around 3 to 4s
to retrieve one secret. As the CLI tool does request to 1Password server to retrieve secrets, performance
is directly impacted by how far your are from their servers.

## Benchmarks

### Get command

#### Official op cli 50,6s

> Performance may depends on how far you are of a 1Password data-center. I live in South of France, nearest is Frankfurt.

```
# Replace UUIDS and session key with your own values
time (for i in {1..20}; do UUIDS=('u5qwa2th7ptrb5leozq2sa2gke' 'opbyml76ircfxchjp7d5oa6lm4' ); eval "time op get item ${UUIDS[$((RANDOM % ${#UUIDS[@]}+1))]} --session="XXX"  > /dev/null"; done)
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,50s user 0,09s system 60% cpu 2,655 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,46s user 0,08s system 61% cpu 2,491 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,50s user 0,09s system 63% cpu 2,527 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,46s user 0,08s system 62% cpu 2,461 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,49s user 0,09s system 64% cpu 2,449 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,50s user 0,09s system 63% cpu 2,509 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,54s user 0,10s system 63% cpu 2,593 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,50s user 0,09s system 63% cpu 2,512 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,48s user 0,09s system 62% cpu 2,527 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,47s user 0,08s system 59% cpu 2,618 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,55s user 0,09s system 59% cpu 2,759 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,50s user 0,09s system 61% cpu 2,567 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,52s user 0,10s system 62% cpu 2,597 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,48s user 0,09s system 61% cpu 2,536 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,56s user 0,10s system 62% cpu 2,649 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,57s user 0,11s system 56% cpu 2,991 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,81s user 0,14s system 54% cpu 3,597 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,64s user 0,12s system 57% cpu 3,051 total
op item get 6rtzezejb7saty4nbzdqsbgplu  > /dev/null  1,75s user 0,14s system 61% cpu 3,050 total
op item get opbyml76ircfxchjp7d5oa6lm4  > /dev/null  1,55s user 0,10s system 59% cpu 2,786 total
( for i in {1..20}; do; IDS=('opbyml76ircfxchjp7d5oa6lm4' ) ; eval ; done; )  30,83s user 1,98s system 60% cpu 53,935 total
```

#### op-local 2,3s (22x faster)

```
time (for i in {1..20}; do UUIDS=('6rtzezejb7saty4nbzdqsbgplu' 'opbyml76ircfxchjp7d5oa6lm4' ) FIELDS=('password' 'title'); eval "time op-local get ${UUIDS[$((RANDOM % ${#UUIDS[@]}+1))]} ${FIELDS[$((RANDOM % ${#FIELDS[@]}+1))]} > /dev/null"; done)
op-local get opbyml76ircfxchjp7d5oa6lm4 title > /dev/null  0,08s user 0,03s system 61% cpu 0,179 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,07s user 0,03s system 90% cpu 0,109 total
op-local get opbyml76ircfxchjp7d5oa6lm4 title > /dev/null  0,07s user 0,03s system 92% cpu 0,108 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,07s user 0,03s system 91% cpu 0,110 total
op-local get opbyml76ircfxchjp7d5oa6lm4 password > /dev/null  0,07s user 0,03s system 91% cpu 0,109 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,07s user 0,03s system 91% cpu 0,110 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,07s user 0,03s system 91% cpu 0,109 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,07s user 0,03s system 92% cpu 0,108 total
op-local get 6rtzezejb7saty4nbzdqsbgplu password > /dev/null  0,08s user 0,03s system 91% cpu 0,116 total
op-local get 6rtzezejb7saty4nbzdqsbgplu password > /dev/null  0,07s user 0,03s system 92% cpu 0,109 total
op-local get opbyml76ircfxchjp7d5oa6lm4 password > /dev/null  0,08s user 0,03s system 92% cpu 0,113 total
op-local get 6rtzezejb7saty4nbzdqsbgplu password > /dev/null  0,08s user 0,03s system 93% cpu 0,124 total
op-local get opbyml76ircfxchjp7d5oa6lm4 title > /dev/null  0,08s user 0,03s system 93% cpu 0,111 total
op-local get opbyml76ircfxchjp7d5oa6lm4 password > /dev/null  0,08s user 0,03s system 93% cpu 0,114 total
op-local get 6rtzezejb7saty4nbzdqsbgplu password > /dev/null  0,08s user 0,03s system 93% cpu 0,113 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,08s user 0,03s system 92% cpu 0,113 total
op-local get opbyml76ircfxchjp7d5oa6lm4 title > /dev/null  0,08s user 0,03s system 93% cpu 0,113 total
op-local get 6rtzezejb7saty4nbzdqsbgplu title > /dev/null  0,08s user 0,03s system 93% cpu 0,117 total
op-local get opbyml76ircfxchjp7d5oa6lm4 password > /dev/null  0,08s user 0,03s system 92% cpu 0,122 total
op-local get opbyml76ircfxchjp7d5oa6lm4 title > /dev/null  0,08s user 0,03s system 92% cpu 0,113 total
( for i in {1..20}; do; UUIDS=('6rtzezejb7saty4nbzdqsbgplu' ) FIELDS=( 'title)  1,52s user 0,57s system 90% cpu 2,322 total
```

### List command

#### 2,1s to list and decrypt 3290 entries
```
time op-local list | wc -l
    3290
op-local list  0,68s user 0,05s system 99% cpu 0,741 total
wc -l  0,00s user 0,00s system 0% cpu 0,740 total
```


## Development

Development requirements are listed in requirements/dev.txt

```
mkvirtualenv3 op-local-search
workon op-local-search
pip3 install -r requirements/dev.txt
```

## Testing

Testing is done through `pytest`.
Tests have not been updated for releases after 1.0.0. It requires a new testing database with new format of 1Password8.


## Acknowledgments

This tool couldn't have been possible without the **awesome** work of David Schuetz. (@dschuetz) https://github.com/dschuetz/1password

I would like also to thanks the support team of 1Password and in particular @cohix which helped me a lot to 
understand the remaining internals of 1Password.

Big thanks also to Joël Franusic and his work on JWK https://github.com/jpf/okta-jwks-to-pem. That helped me to 
drastically improve the performance of the app.

Thanks so much, everyone ! 


## License

GPLv3
