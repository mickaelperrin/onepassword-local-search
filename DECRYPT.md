# How it works 

> All credits goes to David Schuetz (@dschuetz)
> https://darthnull.org/security/2018/11/12/1pass-roundtrip/

## Search entry with uuid: e25haqmocd5ifiymorfzwxnzry 

```
sqlite3 -line -noheader B5.sqlite "select * from items where uuid = 'e25haqmocd5ifiymorfzwxnzry'"
```
```
ITEM:
id = 15
                  uuid = e25haqmocd5ifiymorfzwxnzry
              vault_id = 6
         category_uuid = 100
            created_at = 1556044733
            updated_at = 1556044756
               version = 1
      local_edit_count = 0
               trashed = 0
            fave_index = 0
                 scope =
rejected_build_version = 0
      rejection_reason =
          changer_uuid = 2ENM3KNHAVGQRLCAWVSPVHO344
              overview = {"iv":"rx3jhlbbfnaG-rWC","data":"qjZSLfS0uo0FrtgiROeld8TLAu_n-iMns2QBp2acFFeqfgEhAQCQ6qunS9PuoOEtbU1Zbj0dd6m7Dpe01C7NerZwxSRgYia9a-KuGSDVrK0iSjD226iLNynUz5tCJY43Dk_CgQB5I-CSQG2amEM","enc":"A256GCM","cty":"b5+jwk+json","kid":"mj45lriuh5pkl4t6ocfyoj73jq"}
               details = {"iv":"3PnoQhMCsXnEdMz9","data":"0OZ26z_WtRmDER1HwunTc3jNJRjvRZ9g3GWbLGj-RAukscGfOPN06ooCqP-91-8WgMOy-9qWrqorhXhBXe8HhRMhrlO0pFN6UtfGYl_pPZD9SI3DtNQXLR022DW7_TwgXXVB3uepsxO14D1GLYNACsYqR1vgAB-jQpqm1_MN4Ix8ZwVKBsSUIOVWFiT8Gh81JufjpwjKYtz95onFHUn7VHnkNC6KH2ngo_ZlDX4vbihHdnZF7bfBK0lvNKoDU6riqEEaZOpOqDqkcCIVWs1eNac6ke1B4U0l518YlxO-WhDJPE_oB_KGWTZmeR0QITwy8ugAMgKFITpUbo_6CsRquW8PxfAAGmofNKc5LvwzcG15aF6GO_dsQkj5gpQCaxewyCh1JaaEi7QX8srtB_s4uoCoaB_p1nQlTH4Na_-Aa8NbA-OzuxjyJO4r6wN53lag5EB4taHwYdomeh2n--zQfZcD7dM9j5A8GAU2AizzA-qz6xJbnKLZfEL-2sVQ4MYU9ZL5ybdcKXywt3HNT1yJi8hkDWxKpfaH_-sCYUYEWJlFtSdrsdf4odqZgyU25fCoEryq_lq1f2DIyeCe0E3A43ZZV63KgfUS2akJOdz5TzjLDL93gX0iuneiC9l1ldPjknXxYgHJLMxJ2NZEyv3yMEDYfJF0eUE_Yio5wdEpEJZRzDSVcDr3HuJTIFCH_iak9iL8QEk4a3Qr-RkeTjAIDqE8mr6w5Jd3WxEwo1FtjnO4hrSakzIDpSevafkRnOzrzP2n53Wv_Jc6xJhtxvaQbjbWYux5iPWAjJgi5JJn_tKwDkmu-SzWq04BGDTDnv3s2eaottLVQU9yfhUZSKwICwofhtyIfLKvq7K98liHJU7qwaCepuFicd8ymMf81PQW7vpP281clhYBjZNqTfljkIkOlsObXO5bh8_pr58xTryWNL08L7D5ur8WZS7RIF6A6Q-isSgM2gE7MOnZnAYDQtay-gHV-Jw9QMopOWXKM9Hf4JPgE6XHo-0ep9MFE3_6TEvUBlP7mIu-Xff361_P-L8DuhlHGB-BPhwl7X7QezN96MqrRV4RpIPnFVHtQRxLW46Qh_cb6kBei5Dok2UgTT-zrwMC_soYribn4mt_x3RNfZmLfkjMbykrpkQDlB-WXH98avf5IUpxonOcpJZKXRpQj0b7dr83NzNFm8163y_UNrMazZ3bWgc38Z5E7O36jssiaDVAi0r-IZR7AhtL5EbWgu2kHCV-DMOYhg6fkjFRSUxEDSson5GE_NnXonN2ZnHhq3oIvnBevPVxqv5CKGRTq3RYEc_VbwLd84uoE23zxbQtbGjXTsFY8BhoLByipt2Sqmdr3oEeYAQ4VqQ9l1zK3yLf15Bx-ZiCQqueXXaO074F8JvVmTwJPiUEOHTYtTaBlPY72hJrMWw9q0k8ATdqsETNBA5_lCoMyYGHlvFTzsDCCVtbcPuBFZJ2xr_FUzAsDw2EBofm5VeBXsGirqcvFWSW6JBgupJH8AYzGT2k9UKwbQM3yfXu3T86g2ZomElEEkzJlLF-xWCGxz-_41Ss-hsSuCkC-ZVFKR2szPBtcWNaGfWJeuKomElGy_6qShf7nylCga1Ym7oiYoXYCjaDmb1gySxMAQbJ6CoyTj_fo8vXeUSiHSNQdT5fBSUI60ob768hwJ3oKiIUAlc04tqLD00Ot3SfmP54lt8RkLSRM4fnkwNlr0Wt9I_sI2V9bO5AvzLkL5snaplXUXqZoqCt-foe_GsniOitVqCfLDAbpZGE5BCGyu-nRxQiOYcLnIGvmozTxGac-5gClX_KlsmCYe3avTOzs2OpUB-yGs0pbQMU_lBH5-EGpf7yrtQLNPdW_-kcitXEaSeduZBS9T51sPRK2p8ekCpyzRaoqJR2WG70YS_Vlhv7hcs_B4cpRs6uDjTiPsYgIebkxRs","enc":"A256GCM","cty":"b5+jwk+json","kid":"mj45lriuh5pkl4t6ocfyoj73jq"}
       export_overview = {"iv":"V2oBCcxmDo6DYvMv","data":"wby_Fh4N6zlnd1_49xrh6UxaSmVW3UaBiNyiFmVYEpZyviEBnpZ-MhhgMckz7_Vl6NZ8FwmFf8Q8PD7Ceff25T-wCL7ICK8AGAPEKUXJ3l9KeCZ_gnDanpZD6H2xSUDmW8xtu1CTCxXjxOncrks","enc":"A256GCM","cty":"b5+jwk+json","kid":"447wbn7alfcvxc5iv33mgtu4uu"}
        export_details = {"iv":"K21QFwK1c8haHjR-","data":"B4cWpUkSToCVsGeYl128Fl_T0ugqW2ETeVG4-U-wxsW91bJyPvxsdaR1m3LYrgnft_7Ait5QTRUKSn_yBzyhSdCqrg9O1WG5dXlCnu-w8i_Y4iilLLvI4fchVtvcA9ACKYkmVLPmeYnT_s1RsZKwppdyIH1pFjmFLuK4Y9_hhJFk7t_Gcek4d0QstwnBfI1nuovbX64Qhjqajx9YY0jsIdZ5O9lamUVTMKGJkY5N1zJI-yOMNuPY5302Um5yO3Mcqozs8UzzacboDvHRTcvG-RPzHYYMv_cuP8SusPFu-JfYWxkKp41tdUpLFCmCpKwCk5nDWa13lwSdDp2gbFh2cCy0QpAUBMmS4MZgKsT2YwBIbfcZUyW5dXHY4SThx4J8Tdr-Tu4eK4lCzHiilVCdVnGeOf3H4ehe-r9zjHFFr6W_27YBKYA8lCkC8f84Iyv8z-X2RCjXyUreJm1AC6hSp0IERVXCDDIf6zPFuThXUEuvNYqdTHBOC330fSzQ-N4sOVI1VfpG4ao1TZ5Vxti0r9qa3rRM6NZ8KYoaIElHi-MLKrZmDPKSJ2bRkkC2pcv4RAsj2TO238j_5c8ZJ2_j79mQd_X1NCf8nTx7KxYIVVL34yEIkc78btfwP3tiEny-u3IteyDgtBhF1Os-wf5HEMPOekeBwBBKq1qQW2OzcBpfgbj-pxfVwT1hcu0515z0P-o0t_yy6EtNEh6BIpGSgZFwEiGX-CZHngvQB7Zz4gmQpr4o1IByxkmThKPslE1uV7hBYK-1KkTeRmP5WX3kVxfs4VLTagOkQfK9UCJZgOiogXZe6hzyUPnLqVknqiX2HhjB7tYk6VxoLZit8MDy1Tw78Rvwxrw_giI-AEG885_JmgH4fMIakOS_oJdkFOkQzUdzcnjK_AKmHpG99DQ9XR-KeMM-OFPY8S237yTF--Tf6y9YIT44ugnnQdQXn3I63XFmf79w76MqkYpOsxgQwy-um5FSxen0uPCyakfv03b6M1RAlut4UJeC6Ap2UlUxJ6JaYn9HBN1V9fADriVCPvyiQ-mmpUUUmnhHJatchNOd-lHdVPRIk9wz_Ux8VcaEylLZhj6OeorIlDalDst64II50gbefWy3tOiExDD0UwGPJpXCLbNMHV4CKQvXsP5DUGphR7bjBgcUzbaIqeT4fGxLQIM7WpOF1LN-LPSxb60iY67-wImR5_W3cpBFSynOpqWcr5gxn6qHMMuLUdQa7n75_oJnPqXdkZxkSz6PvYRA2WHHDjRrXtk5IGX2iJJvmZOw9QcWeXaGJlVCOUMgkhE-DcF6U7w9FoNmP4ZxoG3EdqBLBXn9N81TxC6NJm-_ukvIHmNRR4E7EJhXFnvbmmOk9cXV0OZpbe16me3JFP3rKaMz_QQpJZHdFMVkgyRm_dEGp9i5ayagKjg8q2DeEaHN7fZLjjtnqWTvNLOYBpZ31gQKhHXKU95CnxoqqjduUtwN_ef7Lf674p8ke3dxLuPl8Bw6PzbGbNSv1Xjz55GE_CwD8arvT9vqexgmUODEiDlCjgYdC-jUynBjyNbd225SSq7jj1TtKhcWVVCogK99xqJ55bokPkjNXuT5vn8t7yIrMWgEto0fgBQHnajfqUeKT54O4arD-q0SVVmlEZdRXTWMYuZ601ZMqdF7jvfXPoBth8xqAlFl99lm0zCl2pTTELWwZbyXPlJL6w6UUwOAIvUPidwKJcPJOvW7nN5wLnyDmeLTqtsgay_BPkNNGIfi-GwjbPTMjMSV01UcwV5Q9KeM4WvhpV8xAbRjRRfNsFIGmh4N5zAr5VjU9jC-cEaNJqib60VRhQAG86kYNoN1wP1F3TBUJ0Jl18sKDKUT1HN9nTRC6BiCw2Ry0OhB4nVQwkb2738mR0eh5oeVW3V58FU_keFlEKBp9mEtsNFZWT_HT0RjHJXWNGp_FB0","enc":"A256GCM","cty":"b5+jwk+json","kid":"447wbn7alfcvxc5iv33mgtu4uu"}

```
Overview:
```
{
  "iv": "rx3jhlbbfnaG-rWC",
  "data": "qjZSLfS0uo0FrtgiROeld8TLAu_n-iMns2QBp2acFFeqfgEhAQCQ6qunS9PuoOEtbU1Zbj0dd6m7Dpe01C7NerZwxSRgYia9a-KuGSDVrK0iSjD226iLNynUz5tCJY43Dk_CgQB5I-CSQG2amEM",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "kid": "mj45lriuh5pkl4t6ocfyoj73jq"
}
```
Details:
```
{
  "iv": "3PnoQhMCsXnEdMz9",
  "data": "0OZ26z_WtRmDER1HwunTc3jNJRjvRZ9g3GWbLGj-RAukscGfOPN06ooCqP-91-8WgMOy-9qWrqorhXhBXe8HhRMhrlO0pFN6UtfGYl_pPZD9SI3DtNQXLR022DW7_TwgXXVB3uepsxO14D1GLYNACsYqR1vgAB-jQpqm1_MN4Ix8ZwVKBsSUIOVWFiT8Gh81JufjpwjKYtz95onFHUn7VHnkNC6KH2ngo_ZlDX4vbihHdnZF7bfBK0lvNKoDU6riqEEaZOpOqDqkcCIVWs1eNac6ke1B4U0l518YlxO-WhDJPE_oB_KGWTZmeR0QITwy8ugAMgKFITpUbo_6CsRquW8PxfAAGmofNKc5LvwzcG15aF6GO_dsQkj5gpQCaxewyCh1JaaEi7QX8srtB_s4uoCoaB_p1nQlTH4Na_-Aa8NbA-OzuxjyJO4r6wN53lag5EB4taHwYdomeh2n--zQfZcD7dM9j5A8GAU2AizzA-qz6xJbnKLZfEL-2sVQ4MYU9ZL5ybdcKXywt3HNT1yJi8hkDWxKpfaH_-sCYUYEWJlFtSdrsdf4odqZgyU25fCoEryq_lq1f2DIyeCe0E3A43ZZV63KgfUS2akJOdz5TzjLDL93gX0iuneiC9l1ldPjknXxYgHJLMxJ2NZEyv3yMEDYfJF0eUE_Yio5wdEpEJZRzDSVcDr3HuJTIFCH_iak9iL8QEk4a3Qr-RkeTjAIDqE8mr6w5Jd3WxEwo1FtjnO4hrSakzIDpSevafkRnOzrzP2n53Wv_Jc6xJhtxvaQbjbWYux5iPWAjJgi5JJn_tKwDkmu-SzWq04BGDTDnv3s2eaottLVQU9yfhUZSKwICwofhtyIfLKvq7K98liHJU7qwaCepuFicd8ymMf81PQW7vpP281clhYBjZNqTfljkIkOlsObXO5bh8_pr58xTryWNL08L7D5ur8WZS7RIF6A6Q-isSgM2gE7MOnZnAYDQtay-gHV-Jw9QMopOWXKM9Hf4JPgE6XHo-0ep9MFE3_6TEvUBlP7mIu-Xff361_P-L8DuhlHGB-BPhwl7X7QezN96MqrRV4RpIPnFVHtQRxLW46Qh_cb6kBei5Dok2UgTT-zrwMC_soYribn4mt_x3RNfZmLfkjMbykrpkQDlB-WXH98avf5IUpxonOcpJZKXRpQj0b7dr83NzNFm8163y_UNrMazZ3bWgc38Z5E7O36jssiaDVAi0r-IZR7AhtL5EbWgu2kHCV-DMOYhg6fkjFRSUxEDSson5GE_NnXonN2ZnHhq3oIvnBevPVxqv5CKGRTq3RYEc_VbwLd84uoE23zxbQtbGjXTsFY8BhoLByipt2Sqmdr3oEeYAQ4VqQ9l1zK3yLf15Bx-ZiCQqueXXaO074F8JvVmTwJPiUEOHTYtTaBlPY72hJrMWw9q0k8ATdqsETNBA5_lCoMyYGHlvFTzsDCCVtbcPuBFZJ2xr_FUzAsDw2EBofm5VeBXsGirqcvFWSW6JBgupJH8AYzGT2k9UKwbQM3yfXu3T86g2ZomElEEkzJlLF-xWCGxz-_41Ss-hsSuCkC-ZVFKR2szPBtcWNaGfWJeuKomElGy_6qShf7nylCga1Ym7oiYoXYCjaDmb1gySxMAQbJ6CoyTj_fo8vXeUSiHSNQdT5fBSUI60ob768hwJ3oKiIUAlc04tqLD00Ot3SfmP54lt8RkLSRM4fnkwNlr0Wt9I_sI2V9bO5AvzLkL5snaplXUXqZoqCt-foe_GsniOitVqCfLDAbpZGE5BCGyu-nRxQiOYcLnIGvmozTxGac-5gClX_KlsmCYe3avTOzs2OpUB-yGs0pbQMU_lBH5-EGpf7yrtQLNPdW_-kcitXEaSeduZBS9T51sPRK2p8ekCpyzRaoqJR2WG70YS_Vlhv7hcs_B4cpRs6uDjTiPsYgIebkxRs",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "kid": "mj45lriuh5pkl4t6ocfyoj73jq"
}
```

## Grab session value from ENV
```
OP_SESSION_onepassword_local_search=^azuDId6PvlUtwsLQZD-4jzGpMxUxRNQOxEgcdbZhppI
```

## Grab session file in tmp dir

> Questions: 
> - how to determine the adequate file ? most recent ?
> - which folder for each platform ?
```
$TMPDIR/com.agilebits.op.501/.Y_efcm4Gd_W4NnRTMeOuSEHPA5w
```
```
ENC_SESSION_KEY:
{
  "kid": "Y_efcm4Gd_W4NnRTMeOuSEHPA5w",
  "enc": "A256GCM",
  "cty": "b5+jwk+json",
  "iv": "o86o5GT5zK7xh83e",
  "data": "Fn3jMEhlgsniiwP0wgSUF-HUR2LHEQuIW032Oz25VokclJG9t2Tl8a8KgDHgVwgypO2hQbS_0u2xteDEON4GVV7vf4C_7UmzbWIaz5qN1PXa5_AlnmBmHiRFXoTNEQgqJqxkEDHGnCaNExkw8FenArevjwKwp2Zwr1jIL0m8YVEnROSKg8WEuuOh74EehpkmypBJ-I4PIHe-C80OwqriwK6XK_3dEat6iYzvSYKQK4MwY5eTDSZWoIvaAFs8QHBez8CiaDmzIp1fgNOiYwplf9skc9ZA0cvUc9i0AT3aQa7PBsTHEQ2srgF43sS4eFF6X66QOmsbY4UAy-JjakOmIPkthkkx5dsGIsCUO1whAzIlmnTrNYUFtA",
  "accessed": "2019-04-24T09:29:10.594185993+02:00"
}
```

## Decrypt session private key 

- Script gcm_decrypt.py

```
Enter AES-256 key (hex or base-64 encoded): OP_SESSION_team_dkod
Enter IV (hex or base-64): ENC_SESSION_KEY.iv 
Enter ciphertext (hex or base-64): ENC_SESSION_KEY.data
```
```
SESSION_PRIVATE_KEY:
{
  "rawUrl": "https://onepassword-local-search.1password.eu",
  "uuid": "RNDY5D5KA5ENVN3HV2K52DOAHM",
  "encodedKey": "JH84cS3eNebV8P0Kck3fviRSfnOk8WMFUtiF6umWHFY",
  "encodedMuk": "2Zqlkn-ppcrz0RaH3wDUiKwu1YUPj1bRM09R9MEmsrE",
  "timeCreated": "2019-04-24T09:29:10.362062747+02:00"
}

```

## Get encoded symmetric key


```
select enc_sym_key from keysets where encrypted_by = 'mp' and account_id=2;
```

```
{
  "iv": "uXAcNJaoM54-8r-M",
  "data": "Kb69e8qtY7cPkqoG7jMjy1KfG0Il-R5FfsvrLYVJADaan6ICh4f_AUWbdD6aiRe7UvXbqwnaRX-KGfPoCBIrAbQj2ZZsYO_8jcd0RAaYLpnUMLjSgOUh5dnCiksJcDOVvwVDed6xp8LXirt631ArEUc545edlCJi4RohkplHRFdwxWa-6M1al0z0ZM6ac7koVGYYM913CYfsNp3GV7_4ccGg9AQNOJVM6vLTRKg",
  "alg": "PBES2g-HS256",
  "enc": "A256GCM",
  "p2c": 100000,
  "p2s": "YLr0YcV2miMUWRrH39yD6g",
  "cty": "b5+jwk+json",
  "kid": "mp"
}
```

## Decrypt encoded symmetric key
- Script gcm_decrypt.py

```
Enter AES-256 key (hex or base-64 encoded): SESSION_PRIVATE_KEY.encodedMuk
Enter IV (hex or base-64): ENC_SESSION_KEY.iv 
Enter ciphertext (hex or base-64): ENC_SESSION_KEY.data
```
```
{
  "alg": "A256GCM",
  "ext": true,
  "k": "DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc",
  "key_ops": [
    "decrypt",
    "encrypt"
  ],
  "kty": "oct",
  "kid": "vhhhcyj7rc3vocnd5o2iksiflm"
}
```