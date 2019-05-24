# 1Password local search
[![Build Status](https://travis-ci.org/mickaelperrin/onepassword-local-search.svg?branch=master)](https://travis-ci.org/mickaelperrin/onepassword-local-search) 
[![codecov](https://codecov.io/gh/mickaelperrin/onepassword-local-search/branch/master/graph/badge.svg)](https://codecov.io/gh/mickaelperrin/onepassword-local-search)

> This is an _**unofficial**_ tool focused on listing and decryption of secrets 
> with increased performance comparing to native op CLI

## How to use ?

This tool do not replace the official CLI `op` of 1Password. You still need it to perform signin and grab session keys.

So, ensure that you have registered the OP_SESSION_team in your environment.

####Database path

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

#### Official op cli 1m23s

> Performance may depends on how far you are of a 1Password data-center. I live in South of France, nearest is Frankfurt.

```
ime (for i in {1..20}; do IDS=('zzfmhu2j7ajq55mmpm3ihs3oqy' 'n3iopimevz3pddels3dgfwyp2a' ); eval "time op get item ${IDS[$((RANDOM % ${#IDS[@]}+1))]} --session="XXX"  > /dev/null"; done)
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,50s user 2,09s system 85% cpu 4,180 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,49s user 2,12s system 84% cpu 4,280 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,12s system 85% cpu 4,230 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,49s user 2,06s system 84% cpu 4,210 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,49s user 2,08s system 88% cpu 4,029 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,11s system 85% cpu 4,222 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,10s system 85% cpu 4,189 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,50s user 2,14s system 93% cpu 3,888 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,49s user 2,12s system 78% cpu 4,601 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,51s user 2,14s system 87% cpu 4,182 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,51s user 2,12s system 92% cpu 3,913 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,49s user 2,11s system 80% cpu 4,494 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,50s user 2,12s system 91% cpu 3,972 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,50s user 2,15s system 93% cpu 3,893 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,12s system 80% cpu 4,487 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,49s user 2,10s system 81% cpu 4,378 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,47s user 2,05s system 90% cpu 3,909 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,07s system 92% cpu 3,859 total
op get item zzfmhu2j7ajq55mmpm3ihs3oqy  > /dev/null  1,50s user 2,12s system 93% cpu 3,861 total
op get item n3iopimevz3pddels3dgfwyp2a  > /dev/null  1,50s user 2,09s system 84% cpu 4,240 total
( for i in {1..20}; do; IDS=('zzfmhu2j7ajq55mmpm3ihs3oqy' ) ; eval ; done; )  29,92s user 42,15s system 86% cpu 1:23,02 total

```

#### op-local 3,5s (23x faster)

```
 time (for i in {1..20}; do IDS=('gzikfbpysjwsqdagcgxcwqmmxe' 'jfcpk2cpgxarvrhlatca7tsyui' 'osk6bqktonuxjm4qgqxs2tpz6a' 'dytzaelqvqrmhfstscb67geuly' ) FIELDS=('password' 'title'); eval "time op-local get ${IDS[$((RANDOM % ${#IDS[@]}+1))]} ${FIELDS[$((RANDOM % ${#FIELDS[@]}+1))]} > /dev/null"; done)
op-local get dytzaelqvqrmhfstscb67geuly title > /dev/null  0,13s user 0,03s system 97% cpu 0,165 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe password > /dev/null  0,14s user 0,04s system 98% cpu 0,175 total
op-local get dytzaelqvqrmhfstscb67geuly title > /dev/null  0,14s user 0,03s system 98% cpu 0,176 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a password > /dev/null  0,13s user 0,03s system 98% cpu 0,170 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe title > /dev/null  0,14s user 0,04s system 98% cpu 0,175 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a password > /dev/null  0,14s user 0,04s system 98% cpu 0,178 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe title > /dev/null  0,13s user 0,03s system 98% cpu 0,168 total
op-local get jfcpk2cpgxarvrhlatca7tsyui title > /dev/null  0,13s user 0,03s system 98% cpu 0,169 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a title > /dev/null  0,13s user 0,03s system 97% cpu 0,171 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a password > /dev/null  0,13s user 0,04s system 98% cpu 0,173 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a title > /dev/null  0,14s user 0,04s system 98% cpu 0,173 total
op-local get jfcpk2cpgxarvrhlatca7tsyui title > /dev/null  0,14s user 0,03s system 97% cpu 0,176 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe password > /dev/null  0,13s user 0,03s system 97% cpu 0,171 total
op-local get dytzaelqvqrmhfstscb67geuly password > /dev/null  0,14s user 0,03s system 97% cpu 0,174 total
op-local get jfcpk2cpgxarvrhlatca7tsyui password > /dev/null  0,14s user 0,04s system 98% cpu 0,179 total
op-local get dytzaelqvqrmhfstscb67geuly title > /dev/null  0,14s user 0,04s system 97% cpu 0,181 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe title > /dev/null  0,14s user 0,04s system 97% cpu 0,179 total
op-local get gzikfbpysjwsqdagcgxcwqmmxe title > /dev/null  0,14s user 0,04s system 98% cpu 0,178 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a title > /dev/null  0,14s user 0,04s system 98% cpu 0,182 total
op-local get osk6bqktonuxjm4qgqxs2tpz6a title > /dev/null  0,15s user 0,04s system 97% cpu 0,188 total
( for i in {1..20}; do; IDS=('gzikfbpysjwsqdagcgxcwqmmxe'   ) FIELDS=( 'title)  2,74s user 0,71s system 98% cpu 3,509 total

```

### List command

#### 0,7s to list and decrypt 1877 entries
```
time op-local list | wc -l
    1877
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


## Acknowledgments

This tool couldn't have been possible without the **awesome** work of David Schuetz. (@dschuetz) https://github.com/dschuetz/1password

I would like also to thanks the support team of 1Password and in particular @cohix which helped me a lot to 
understand the remaining internals of 1Password.

Big thanks also to Joël Franusic and his work on JWK https://github.com/jpf/okta-jwks-to-pem. That helped me to 
drastically improve the performance of the app.

Thanks so much, everyone ! 


## License

GPLv3
