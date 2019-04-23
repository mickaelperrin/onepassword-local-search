# How it works 

> All credits goes to David Schuetz (@dschuetz)
> https://darthnull.org/security/2018/11/12/1pass-roundtrip/

## Search entry with uuid: ixxb2steczal3iev7i43p7m42e 

```
sqlite3 -line -noheader B5.sqlite "select * from items where uuid = 'ixxb2steczal3iev7i43p7m42e'"
```
```
ITEM:
                    id = 1
                  uuid = ixxb2steczal3iev7i43p7m42e
              vault_id = 1
         category_uuid = 001
            created_at = 1556014457
            updated_at = 1556016561
               version = 3
      local_edit_count = 0
               trashed = 0
            fave_index = 0
                 scope =
rejected_build_version = 0
      rejection_reason =
          changer_uuid = 3IY3T6URCFGDDIKF5DGQ7NBRFA
              overview = {"iv":"qUnnFYqqvW0VMeGg","data":"L5IEuVgv3SKupH84MO6nTwQXbKEa-yZyJFov3GJr3libxvNlZvuJt5K4xyivYHNyCT2WYwBAbcIUGQyU3A8649y9RafHBwY8uB9XXbPKwgg1QAampyJXnqHMJAFtitJQ5QfQszcj","enc":"A256GCM","cty":"b5+jwk+json","kid":"fekkwgz7dosjiuat37x2dush74"}
               details = {"iv":"_ovvhjC0mz3QBm6w","data":"hiwG8P5N0OxAQyQv0kdKzux7HY-FBXZRgH0RIYxpJbUqZRUQJWyBgmtvqjd2mFpGjnZq507H7qop9ulQKuS54pLRpRnidO0aIwgciQfQrX-4QIMeCwk7_PT9qBZo_F3-WJhn3PCVGUD-8MC2mdSUMexecdRArYEHS0_NTIqRrhNj_F0XYTCzKhnGd9sxij_M4wgvazr6nRmS47shIGmgU3OgAZAgmBgqEhShCyidV4PafKlqYj4czLS8u6SSwa4yqGKo8KtErf97Xm_iGqJCbsX3ka4QirtkaYTDeSdkcrtzF8-Q-VLrvc65ev3bk6DBAoQmNVNabI0qIAhRv9jQxEADXKybJXa3yjW0zeRWDPGFz-Pk8MAdc5gkiFqvXMDXjFHrLXhvt_kRoIAX1PDeufpZQ-PBZeNH71bw5ORTu-vrmQAEVM2WGf0mOjnXszLMbinp2RTV__sTpVppHcJhkuC_eWuazHpMBptLf6U4wVcvQhqwmRGcSpm-n8n4IXyD-UsYXFQIJxNqGg","enc":"A256GCM","cty":"b5+jwk+json","kid":"fekkwgz7dosjiuat37x2dush74"}
       export_overview =
        export_details =

```
Overview:
```
{
  "iv": "qUnnFYqqvW0VMeGg",
  "data": "L5IEuVgv3SKupH84MO6nTwQXbKEa-yZyJFov3GJr3libxvNlZvuJt5K4xyivYHNyCT2WYwBAbcIUGQyU3A8649y9RafHBwY8uB9XXbPKwgg1QAampyJXnqHMJAFtitJQ5QfQszcj",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "kid": "fekkwgz7dosjiuat37x2dush74"
}

```
Details:
```
{
  "iv": "_ovvhjC0mz3QBm6w",
  "data": "hiwG8P5N0OxAQyQv0kdKzux7HY-FBXZRgH0RIYxpJbUqZRUQJWyBgmtvqjd2mFpGjnZq507H7qop9ulQKuS54pLRpRnidO0aIwgciQfQrX-4QIMeCwk7_PT9qBZo_F3-WJhn3PCVGUD-8MC2mdSUMexecdRArYEHS0_NTIqRrhNj_F0XYTCzKhnGd9sxij_M4wgvazr6nRmS47shIGmgU3OgAZAgmBgqEhShCyidV4PafKlqYj4czLS8u6SSwa4yqGKo8KtErf97Xm_iGqJCbsX3ka4QirtkaYTDeSdkcrtzF8-Q-VLrvc65ev3bk6DBAoQmNVNabI0qIAhRv9jQxEADXKybJXa3yjW0zeRWDPGFz-Pk8MAdc5gkiFqvXMDXjFHrLXhvt_kRoIAX1PDeufpZQ-PBZeNH71bw5ORTu-vrmQAEVM2WGf0mOjnXszLMbinp2RTV__sTpVppHcJhkuC_eWuazHpMBptLf6U4wVcvQhqwmRGcSpm-n8n4IXyD-UsYXFQIJxNqGg",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "kid": "fekkwgz7dosjiuat37x2dush74"
}

```

## Grab session value from ENV
```
OP_SESSION_onepassword_local_search=yA25KnTXfIvmPnOoLJ9tst9O37h8Kl2cPowam2d2d1U
```

## Grab session file in tmp dir

> Questions: 
> - how to determine the adequate file ? most recent ?
> - which folder for each platform ?
```
$TMPDIR/com.agilebits.op.501/.6MRlBJgtMRso-DO40ErGMPksF6E
```
```
ENC_SESSION_KEY:
{
  "kid": "6MRlBJgtMRso-DO40ErGMPksF6E",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "iv": "oUUfx3o33w5wDS8K",
  "data": "umdgCCC48wRSBaRMOCoAkgcE6nOerQo52IIF8bO9okCyzCmF5P4pKo-NA-1_V5xN1fEXxKe-J1PQGVaxlFo6B3ezGwQlB7pWjXd6gmZmBBo8H15rqIvwz843TE7pw8DJ_mGBZuGXfH5_O7L36CbiEAhiQnTQezZ2KJ_8KMjdad_H6SHWDCyY93iH8nWA62UPusXL5B1T21lW0k47dvYw1lEgJLWvdXtysY2gMtbCFMuvM6jrGliRVCQRml3q5Jff9-4qsOHt4HMr9Ik2RhK-Uz3vsqreI6HJxRQ9JcbHfUdr7wzFqDT9eiMNUsFz9vp9hCU_LL-SXkZyls05nzZVSxvqOyN-wegx9xenxB1R170wHKjcCM2BVA",
  "accessed": "2019-04-23T21:37:24.984711766+02:00"
}
```


