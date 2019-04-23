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
op-local get UUID
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
- Session key: `yA25KnTXfIvmPnOoLJ9tst9O37h8Kl2cPowam2d2d1U`
- Session file: `$TMP/.6MRlBJgtMRso-DO40ErGMPksF6E`
```
{
  "kid": "6MRlBJgtMRso-DO40ErGMPksF6E",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "iv": "oUUfx3o33w5wDS8K",
  "data": "umdgCCC48wRSBaRMOCoAkgcE6nOerQo52IIF8bO9okCyzCmF5P4pKo-NA-1_V5xN1fEXxKe-J1PQGVaxlFo6B3ezGwQlB7pWjXd6gmZmBBo8H15rqIvwz843TE7pw8DJ_mGBZuGXfH5_O7L36CbiEAhiQnTQezZ2KJ_8KMjdad_H6SHWDCyY93iH8nWA62UPusXL5B1T21lW0k47dvYw1lEgJLWvdXtysY2gMtbCFMuvM6jrGliRVCQRml3q5Jff9-4qsOHt4HMr9Ik2RhK-Uz3vsqreI6HJxRQ9JcbHfUdr7wzFqDT9eiMNUsFz9vp9hCU_LL-SXkZyls05nzZVSxvqOyN-wegx9xenxB1R170wHKjcCM2BVA",
  "accessed": "2019-04-23T21:37:24.984711766+02:00"
}

```


## Acknowledgments

This tool couldn't have been possible without the **awesome** work of David Schuetz. (@dschuetz) https://github.com/dschuetz/1password
Thanks so much ! 

## License

GPLv3
