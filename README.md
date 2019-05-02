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

### Get decrypted valued
```
op-local get uuid [field] [--use-custom-uuid] [--use-lastpass-uuid]
```

### List items
```
op-local list [--format='{uuid} {title}'] [--filter='']
```

The format string allows you to customize the ouput format of the list items. You can use any field, 
the first match in any section will be used.
 ```
 op-local list --format='{uuid}|{title}|{username}|{password}'
 ```
 
The filter will only return entries whose title contains the filter string. 

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

## Why this project ?

We use Ansible to manage infrastructures and use a lookup plugin to grab hundred of secrets. 
We used to use LastPass but we decided to move away due to unreliable API calls and unsupported CLI.
First benchmarcks of the native `op` tool, have demonstrated really poor performance around 3 to 4s
to retrieve one secret. As the CLI tool does request to 1Password server to retrieve secrets, performance
is directly impacted by how far your are from their servers.

## Benchmarks

### Official op cli 1m23s

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

### op-local 2,65s (31x faster)

```
time (for i in {1..20}; do IDS=('zzfmhu2j7ajq55mmpm3ihs3oqy' 'n3iopimevz3pddels3dgfwyp2a' ) FIELDS=('password' 'title'); eval "timeget ${IDS[$((RANDOM % ${#IDS[@]}+1))]} ${FIELDS[$((RANDOM % ${#FIELDS[@]}+1))]} > /dev/null"; done)
op-local get n3iopimevz3pddels3dgfwyp2a password > /dev/null  0,10s user 0,02s system 98% cpu 0,121 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy password > /dev/null  0,10s user 0,02s system 98% cpu 0,127 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy password > /dev/null  0,11s user 0,02s system 98% cpu 0,136 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,10s user 0,02s system 98% cpu 0,127 total
op-local get n3iopimevz3pddels3dgfwyp2a password > /dev/null  0,11s user 0,02s system 97% cpu 0,131 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,11s user 0,02s system 98% cpu 0,137 total
op-local get n3iopimevz3pddels3dgfwyp2a title > /dev/null  0,11s user 0,02s system 97% cpu 0,136 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy password > /dev/null  0,11s user 0,02s system 98% cpu 0,128 total
op-local get n3iopimevz3pddels3dgfwyp2a password > /dev/null  0,11s user 0,02s system 97% cpu 0,132 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,11s user 0,02s system 98% cpu 0,138 total
op-local get n3iopimevz3pddels3dgfwyp2a title > /dev/null  0,11s user 0,02s system 97% cpu 0,140 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,10s user 0,02s system 98% cpu 0,126 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy password > /dev/null  0,11s user 0,02s system 97% cpu 0,127 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,12s user 0,02s system 98% cpu 0,140 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,11s user 0,02s system 98% cpu 0,136 total
op-local get n3iopimevz3pddels3dgfwyp2a password > /dev/null  0,11s user 0,02s system 97% cpu 0,129 total
op-local get n3iopimevz3pddels3dgfwyp2a title > /dev/null  0,11s user 0,02s system 98% cpu 0,128 total
op-local get n3iopimevz3pddels3dgfwyp2a password > /dev/null  0,11s user 0,02s system 98% cpu 0,138 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy title > /dev/null  0,11s user 0,02s system 98% cpu 0,131 total
op-local get zzfmhu2j7ajq55mmpm3ihs3oqy password > /dev/null  0,11s user 0,02s system 97% cpu 0,133 total
( for i in {1..20}; do; IDS=('zzfmhu2j7ajq55mmpm3ihs3oqy' ) FIELDS=('password)  2,18s user 0,42s system 98% cpu 2,645 total


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

### Test Secrets:

- Master password: `A953n5qDnfWRTCvvTKCm5h4`
- Secret key: `A3-TF7ENY-6T8PH5-6KBLQ-RXPGF-AMFNJ-3QYAW`
- Session key: `azuDId6PvlUtwsLQZD-4jzGpMxUxRNQOxEgcdbZhppI`
- Session file: `$TMP/.Y_efcm4Gd_W4NnRTMeOuSEHPA5w`
```
{
  "kid": "Y_efcm4Gd_W4NnRTMeOuSEHPA5w",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "iv": "o86o5GT5zK7xh83e",
  "data": "Fn3jMEhlgsniiwP0wgSUF-HUR2LHEQuIW032Oz25VokclJG9t2Tl8a8KgDHgVwgypO2hQbS_0u2xteDEON4GVV7vf4C_7UmzbWIaz5qN1PXa5_AlnmBmHiRFXoTNEQgqJqxkEDHGnCaNExkw8FenArevjwKwp2Zwr1jIL0m8YVEnROSKg8WEuuOh74EehpkmypBJ-I4PIHe-C80OwqriwK6XK_3dEat6iYzvSYKQK4MwY5eTDSZWoIvaAFs8QHBez8CiaDmzIp1fgNOiYwplf9skc9ZA0cvUc9i0AT3aQa7PBsTHEQ2srgF43sS4eFF6X66QOmsbY4UAy-JjakOmIPkthkkx5dsGIsCUO1whAzIlmnTrNYUFtA",
  "accessed": "2019-04-24T09:29:10.594185993+02:00"
}
```
- Config file:
```
{
	"latest_signin": "onepassword_local_search",
	"accounts": [
		{
			"shorthand": "onepassword_local_search",
			"url": "https://onepassword-local-search.1password.eu",
			"email": "dev+onepassword-local-search@dkod.fr",
			"accountKey": "A3-TF7ENY-6T8PH5-6KBLQ-RXPGF-AMFNJ-3QYAW",
			"userUUID": "2ENM3KNHAVGQRLCAWVSPVHO344"
		}
	]
}
```


## Acknowledgments

This tool couldn't have been possible without the **awesome** work of David Schuetz. (@dschuetz) https://github.com/dschuetz/1password

I would like also to thanks the support team of 1Password and in particular @cohix which helped me a lot to 
understand the remaining internals of 1Password.

Big thanks also to Joël Franusic and his work on JWK https://github.com/jpf/okta-jwks-to-pem. That helped me to 
drastically improve the performance of the app.

Thanks so much, everyone ! 


## License

GPLv3
