# 1Password local search 

> This is an _**unofficial**_ tool focused on listing and decryption of secrets 
> with increased performance comparing to native op CLI

## How to use ?

This tool do not replace the official CLI `op` of 1Password. You still need it to perform signin and grab session keys.

First, ensure that you have registered the OP_SESSION_team in your environment.

Set the env variable ONEPASSWORD_LOCAL_DATABASE_PATH with the path of the B5.sqlite database.

Example on my Mac:
```
export ONEPASSWORD_LOCAL_DATABASE_PATH="$HOME/Library/Group Containers/2BUA8C4S2C.com.agilebits/Library/Application Support/1Password/Data/B5.sqlite"
```

### Get decrypted valued
```
op-local get UUID [field]
```
### List items
```
op-local list
```

## Why this project ?

We use Ansible to manage infrastructures and use a lookup plugin to grab hundred of secrets. 
We used to use LastPass but we decided to move away due to unreliable API calls and unsupported CLI.
First benchmarcks of the native `op` tool, have demonstrated really poor performance around 3 to 4s
to retrieve one secret. As the CLI tool does request to 1Password server to retrieve secrets, performance
is directly impacted by how far your are from their servers.


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
Thanks so much ! 

## License

GPLv3
