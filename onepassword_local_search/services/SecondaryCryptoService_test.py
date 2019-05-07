import pytest
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.services.SecondaryCryptoService import SecondaryCryptoService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.tests.fixtures_common import common_data, op_session, op_personal_session, op_dual_session
from onepassword_local_search.services.StorageService import StorageService
from onepassword_local_search.models.Cipher import Cipher
from onepassword_local_search.models.Item import Item
import os
from json import loads as json_loads


@pytest.mark.usefixtures("op_session")
@pytest.fixture
def crypto_service(mocker):
    return CryptoService(StorageService(), ConfigFileService(), 1)


@pytest.mark.usefixtures("op_personal_session")
@pytest.fixture
def crypto_service_personal(mocker):
    return SecondaryCryptoService(StorageService(), ConfigFileService(), 2)


@pytest.mark.usefixtures("op_dual_session")
def test_personal_session_keys(crypto_service_personal):
    crypto_service = crypto_service_personal

    crypto_service.sessionKey = crypto_service._get_session_key()
    assert crypto_service.sessionKey == common_data('personal_session_key')

    crypto_service.encryptedSessionPrivateKey = crypto_service._get_encrypted_session_key()
    assert type(crypto_service.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSessionPrivateKey.iv == '_fd_7Kp-MubNXmF7'
    assert crypto_service.encryptedSessionPrivateKey.data == 'SABwnc0ycg68QGEMGSNIiwNBEjbRk-cf1eVRlC6GfAIdP1qKmw7wXGoYwNalABwPUklYNQiTjv-stIOjSVGbYFp9ik7EBXio6i-aK1Vq4A084jsHHbhjjztQBNpmTn090YaOoMSZ6DbidMAviE5nMalSH8s0mnvkcf99D8iFeE0Y3EByFc0PfVvk8njEirgooJPhfxUqGYqNSLyFJUtDy2vMO-nkhBZpH4rFcE8IWRul4zyvoCLuJgE49h5mE67SZqThdv8l_NewBZrdEkzSo7PImbdiRZurOgdyU6xg8Ic9DexFC5Jh0yY_zAp-2-4_cPHEbiVzNAavCLkREMS84-c-Cg'
    assert crypto_service.encryptedSessionPrivateKey.enc == 'A256GCM'

    crypto_service.sessionPrivateKey = json_loads(crypto_service.decrypt(crypto_service.sessionKey, crypto_service.encryptedSessionPrivateKey))
    assert crypto_service.sessionPrivateKey['encodedMuk'] == 'j4mKCHJyeG-O187LjWvjfYciZnKWrDZ8MjS6jhBNGnc'
    assert crypto_service.sessionPrivateKey['encodedKey'] == 'ExSfdUZ-QzI3T-YgcSjdMfiJJo7fFgK-c2JTzALuyOs'

    crypto_service.encryptedSymmetricyKey = Cipher(crypto_service._get_encrypted_symmetric_key())
    assert type(crypto_service.encryptedSymmetricyKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSymmetricyKey.iv == 'tYa8RNJ7UpxA8AXW'
    assert crypto_service.encryptedSymmetricyKey.data == 'HKhbbcnYTeA3Fm1AIdHE5B5N6tkU-8JZnVEd57SPrbvy0S0WMQeupzy79Icvcx_TAgoCYhrrwX6Cxz8DmAkvWEOt85JVhOto2QSlMcQH3UOVhcdaB2jDMkkNRBENfnfV-t46bs6NRge77yD15qBHf-cXLCMeLG2HAaN9DQZM2S4GwRC5yAOYfH7Vc-txiY8dSwvLzYwZNUYvXBY-o7OVHbBQfJiS1bAsCmSKaec'
    assert crypto_service.encryptedSymmetricyKey.enc == 'A256GCM'

    crypto_service.symmetricKey = json_loads(crypto_service.decrypt(crypto_service.sessionPrivateKey['encodedMuk'], crypto_service.encryptedSymmetricyKey))
    assert crypto_service.symmetricKey['k'] == 'w5FzV9t--KgxPDFN2teXJcZ0ekxiTrjmcNlmKmiGZwI'
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'

    crypto_service.encryptedAccountKey = Cipher(crypto_service._get_encrypted_account_key())
    assert crypto_service.encryptedAccountKey.enc == 'A256GCM'
    assert crypto_service.encryptedAccountKey.iv == '09d2f0xTBacV3djN'
    assert crypto_service.encryptedAccountKey.data == 'bgbmVTGji76riFuvhwHq2JNCrJLE246cFX1eZu_pmcliuX1cx-k9hfbXmn4CEIvlI1SWCJtMncEVMH7mxlD7WZBlEqA1kZYZjGfZ-cHUhOW3zxYVDRpVgWyxE-EC79bG0y4W7zb_GH7ucQctfBV1acofio9s_LbiVDFkFd7O1uofrTG3_G-R2GZlnxftC69A4DYiCOpjVukm3ylHt2aD8-hT95HR5NOt2LyDaRRlZA62lFz5XDe9E3eIkK-Kv5qJjmT9ygh40YkMbjwHncPzgXpHxiq08tISP_nL7M918o52Ev9fBo2l3HiExpkQNvUIzQvbpoWB5qQL2rYQcdHKIWFPHuDnpPv8j890uWgvxVCqEUqmpCsIWjbZO9r4wYpwp8ru1ChJpptzpf8V2A8-dBMzmP3QWt7iUsx1PMrQA7I4jb_VbbIIKsuuAKWJv32slBx90PfDoNg8A3GAKfP4kF2YH16TNoNR1GjYnYsx-4YKfQEUrVmnkELtBt51a9eT5GEnbPz2iG4mGOuAHyxtmH9VRqymPG2ivrymaptY4z14qX0TpW7zPtUoV_ej0rzPZwtfEtK8pkS-BQWnBlzobWx6cLubSRnkqLd5hykbsgBgHN33_Xty8xGmHgC2xn3HGiDZsQ'

    crypto_service.set_main_crypto_service()
    assert crypto_service.mainCryptoService.sessionKey == common_data('session_key')
    assert type(crypto_service.mainCryptoService.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.mainCryptoService.encryptedSessionPrivateKey.iv == 'NR8F153dbcwmkz7O'
    assert crypto_service.mainCryptoService.encryptedSessionPrivateKey.data == 'rldxoJiqW9z2hOXNPKTNPUveZJKWk6XZnZxfjEN8ofgOg2nOWsVuQebLU7hVfQif4hWslUqzDrT0dCzaLLyMNOpbjzbrvoRRvCQG9uxbT8gDr6R_wia07urlYrQ-gS_s4XoVwy4opb6UgBeFrr0Dqrue4GAQiuESzdpgLdO7xyvgYzPDdtwW5llc8dy8xHQh7KbSWslQ_cg-tSbok-KQJLm4jQUqDYCXJ2rPPhH7JrN4F1_QV69rAIkWx4Gzq1-2R-h7yMfnJJ3j-sVMSvk8Rccy9st8gQpM5m_eKHmyIr-X9NDhFz7giVsOU_ncv7liaVfEMhxD-sYPlFFBD458EJuAZEz6OQorAOnSP5dhdNUL4VuqL9aDkA'
    assert crypto_service.mainCryptoService.encryptedSessionPrivateKey.enc == 'A256GCM'
    assert crypto_service.mainCryptoService.sessionPrivateKey['encodedMuk'] == 'KCFJRo1hgGkeW8zQTmqvtuWkLmb24xYOnqqCX0iUmsk'
    assert crypto_service.mainCryptoService.sessionPrivateKey['encodedKey'] == 'w2xL1g3K9vg06sKI5GhhWrGathY8192yEqQXSAeydNQ'
    assert type(crypto_service.mainCryptoService.encryptedSymmetricyKey).__name__ == 'Cipher'
    assert crypto_service.mainCryptoService.encryptedSymmetricyKey.iv == '5SYJu0DDFwTPPYWt'
    assert crypto_service.mainCryptoService.encryptedSymmetricyKey.data == 'RaMNi3h-ieB8l4NJxe3fmDYir2vpHOsB1fdKeqjc6RvOrYhjSvuCy_pMkhoaiisdSlGaZYbjVI5ufGlVUxKhPA0aVPSdwKX5Up8ZET8sxInf5pY31vR7fYu_JHjaCdy7c1v_7MAVCPZy52gLfYE4E2PRrZzJCfN6kLhM2L_qTuFYz38ojUbHC4GMLB_q-izW86-WdhLyaiMPtJcj52GU7N3tFK7k6C4cPBFhlSA'
    assert crypto_service.mainCryptoService.encryptedSymmetricyKey.enc == 'A256GCM'
    assert crypto_service.mainCryptoService.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'
    assert crypto_service.mainCryptoService.symmetricKey['alg'] == 'A256GCM'
    assert crypto_service.mainCryptoService.encryptedAccountKey.enc == 'A256GCM'
    assert crypto_service.mainCryptoService.encryptedAccountKey.iv == 'liVUKXadaLb8kgv_'
    assert crypto_service.mainCryptoService.encryptedAccountKey.data == 'Gtt_Wa-L0AuiuJ_Xutd8RCjEODYiHdwUcpPBjO3YcTubFZKA_Hj4PrBQuj98dXXSlO91XKi75GbXCLzePSbZGGBJOVjSKpQqtQBggPIhy3bno35F4-BqJqmD-2sAgVZuE7Ikw_Dwhj3jqdOXS4hQjdmc6QIH83U7poU0wDp11lJMdzlauki3s_9oii7kB43nayB0lpK7JjLVYpjfSIJBvZnz-Q89kX-0oJm9XtZGe8k6-1PEb4A2Me3xE6i-c1tsJGBvDl9Mqii9GbxN8qJE3vb6a9gd-nmJiX2bUM5PlKBsC7aP8FgChfXnW5zfb8Bl555BV3BbqwUGEKfyRD5REOuGffG6ay28QvfWuEO3k-CzNMRh0M3jRvLRh7uKionmwPbY2iPiGzdP1pF3NWPSNjStXslYV_dErty8C6BECTZvYoyuFnd1sklLt5T91W42hyU3wabIIOXQwqwi3fIzKq7Yz8texIDJ8ySRdFgZgGPRF3UMgCYTRVcgQ9qV8vGV1wIC0-r0sXspoDyoM2vgDGhYLgyeb5SAgZHlIx7WlB9F53pDLkguJi_n1nsmzwEmpOeifRdLvNZPR8q1wFr010WKK_vApfpY7-LGRrc6YaAp4k1vOEJegHndK0At0jI'
    assert crypto_service.mainCryptoService.accountKey['email'] == 'dev+onepassword-local-search@dkod.fr'
    assert crypto_service.mainCryptoService.accountKey['masterUnlockKey']['k'] == 'KCFJRo1hgGkeW8zQTmqvtuWkLmb24xYOnqqCX0iUmsk'
    assert crypto_service.mainCryptoService.encryptedPrivateKey.enc == 'A256GCM'
    assert crypto_service.mainCryptoService.encryptedPrivateKey.iv == '0LKnPmt6EXTbaHKo'
    assert crypto_service.mainCryptoService.encryptedPrivateKey.data == 'mGGTpCw6iycZtuLi99f0wxtX60Y40I5hTRDduULAs4L55Cy6KfL98HSiwW6FBPvmk8DQxl_VGdXxLSbmpKWN4tdRWtrhYD2D8lTYVs9tuBHeiyd4QJqd8fymy919fttxLb0SF0WYj5LA67FSeJ9QWF2Rsq3YMEvlRGEVQUXFzILKmDQ7RFgYNnxLiVpPIQWaWgKUsUVdC8APLAXuYSh90dYaE9aICqx0oFZKD2emOwFo0wvvT4Nla2aFK3CW9TLE7QN1B6lOLDDKw-JUqnCJJ5g3388KZdz_X-j3Q33xaZWDJNDypJGqtDJeAXfo7soassCKZ3V4eSeZr02BZl3l1iJWRsIMr8XEiUQXGBS6D3J5j1uVcCIt8TIOj_Sh-PfpChjkeHJJOSLVTf8C1SSXUFGJP_PT35r351h52-ZYl43yNiPaxFzcn-ln70bW3dlqu_FRs5aJ3aI842RB5hMV-ExL2PRKT-L9nvPf2sAT90nV7M28dPb_J2rp_y6koWzuhLLov1IAoOG60i1ZvWvjCey7hkiC3ie35jBJR8U-pk7Wy6kUbjdVjvHKUTmId-M8WGXn_vWthToFAzhuLC94TFLbXJJKWhlnS60Cb2QwnC5Ot0FM7PZAw7Dmi3hIZSmJPyu3FZUifItExFaeXxNlTX65sBCsFHaZ3USx8oEyOPo_--C2GoybpSFyhaPRYGll5VF2TRb7ve1AE6bq5Vw8njyQVV-SZT3KJh97WbV1Y4yRSGJ2KRgnWaoo2PD8Pumr5Q2oAgWUE-_cIqyE7hFJvrCy7-6UiIyk0i3eqVQFdN7l3EpFpwdOtzWJ5pkCJsFhWvBGNdYxCneuLPgxYC3bdOWmAOoGU5FSVC-QLHtal03gwmB6RJlE4mIF4E1Q5GFG87OD4xY7abXq33RHr4Q2TLpRhv8MrWw1k0vSHGikVWQdvxNYJKABpwq9lfncOgXg0qDgl6XiD26Y6Iez8eWeikKIqMe2vRboRZW1ZVpghkXEGfcYhrqKyQUTf17ASqL63LNPRAbuj48-qvK1FaNSab4zLdJrb3cMQDXC_gcgEzHRzcVk8rkHursS_O2hd0Bc5N82yjcxjfjozSkhp_51h7TcwX1xxw1Hu-d_k8cvCff6gqcIu8hjR06D1EwWtdzGhBX3UyStn9crKAHFVEIsYspjjSOJWW-1kjTx-noGfVC6df5trJ1HDE3ISVOLK9bxJA-Q9A-kCoRitUPau29M0_x2RTI1bl4xalA3uCoFprw9kNESEsksVZH-ThBeG_jSq25ONlAtwwZ0pfTOVYiMUV2h6BUoHsNUPyySCbJW62NG_Ca-9jacWS2nTRdKi1DKvVbOCkdO0njcfH8Hq0IomqACtXHL8XrZasheV1AcVA1B8yhinzXtgq2zma-Fs1ZbBTNdebfJ1Dcy68iybVeBXsyLVG7rsc5_toI9CcVQlzfnR9WoifkE8VPScUb33q5sG6LGvLEEGiJkLZUCAnvk7W6oGkp0vdOL9eGJZuaFfWsd5wkyKpEtF8Kxm9Mhz3vYZdqhHVi85_IF2fj-uigvrUguGR7N04KAt1NWdOyQ1-pQxXq9GeHeRp42k1gp16S4mjdjZYwQhcF7BAzlTY2g09FYq-9fdR8F8jiarPNZkINeXoSUlxJnAK7nk_73S1tx_TVqV07qHbLDtlmAb7pUomHNCyT1HVbjhf4ZEJwfh1PiiFRYbeRG8Mga_1edVcpezOKC82jroewVHyhGbWmuX-m7YCLUUCmQWBkb7lpvlwkk3jRMf1Sq3YpuLN_u-NfEgS7bW7XQU-ZvvUn6D43ic7afVCpTz5K-H8qr_y_axsPzrnItaLtE9gKX_-oZ9Sh6XbjC7bd7oboE3a6sCFJnRDg-mSSJXtWq8efLVtS-rtoUr91BRTnafoUdt8t16eyMTbmt8nt1-icmIhmjoqug2jGlxtfuyNLT1Q0su_YOXrZz3bi30QTMYYzmL5SzSOJnTMSa1cOfM_oHu5P_IG5mdlhx86hILEdILcjffDZww5n6E3pcJwvSfnDOVg9olhEHNmKHxtibwaUpajCURY6JHAbVZkHG14HnSyc6oNCxOUaJgkn0eXr2xgjvGtoIbE-x6wBFd65KEJGqSbNZpdjc9vDslfdebl88fcc5Y2ij-2emZfKo9suBGQpA-H-xh6mJlPrIZerTLqJsd-XRtmZecUr_4N66kNLQZAAGEjMWvbY16TJQTiRBv48rRmfvNrI7uV8Od7K3D2SlV4T_GALbQu9qq26Ml8XHtq-VIpgQGFLeM6dd'
    assert crypto_service.mainCryptoService.privateKey['alg'] == 'RSA-OAEP'
    assert crypto_service.mainCryptoService.privateKey['d'] == 'AmCxuabUgIyblLBolHSHvZEh_b7PzswAJquPazw9hu6EaN__noNHFIYMYLovfZ99B58XxiuBSo-N7FPMpWGtVTKPBkR1leSp2bxtnz_M25wRquUxJ3BSWy6dNs5pahRu27irQ1b5cTNRrsCm_ew0aviC_7YgbauXgBK3SBmFXRH81Cw_5XCXmO-9Y7TIPwAnd2jThkyyiyZ9KwSyD96h8eqkn6LX_dXYRRnzlCcTzg2TYXWvtynl1S6z4vRmUKmYxmRroFrIukto5Wlq6o0F8nQ_KxvMrud8qMkatuKcaE9LpAzqXHnCsXf7E_n4UKgUCtLkTrQFIqRiJVSs7R_rQQ'

    crypto_service.accountKey = json_loads(crypto_service.decrypt(crypto_service.mainCryptoService.symmetricKey['k'], crypto_service.encryptedAccountKey))
    assert crypto_service.accountKey['email'] == 'dev+onepassword-local-search-user@dkod.fr'
    assert crypto_service.accountKey['masterUnlockKey']['k'] == 'j4mKCHJyeG-O187LjWvjfYciZnKWrDZ8MjS6jhBNGnc'

    crypto_service.encryptedPrivateKey = Cipher(crypto_service._get_encrypted_private_key())
    assert crypto_service.encryptedPrivateKey.enc == 'A256GCM'
    assert crypto_service.encryptedPrivateKey.iv == 'ZLveVKZLQPv-KB6T'
    assert crypto_service.encryptedPrivateKey.data == 'nZMdB0iqEtPng_bOYBy-Ubda34qZSBRXvyDw98TxFAeK9Ol2xcqVcScP2aWjwU9YytsrHJSzFyv_DBwCD81LpxM__a55XjtJoJg_wn6FqGn58fvOwfTToT21rrByqIQswd4RjWIEpekCukMQfXiI1z0AA2Dz8kFJM4NvBzW-QDrxad4yveKEXKcEnuNeVTqUdCjlEp1CtVMQSc6nGFeSTBc9JGOXxTtng2nMpArkifZg9daImkgDvxLbm2O1NyVqLh-IU8YKX2y83LBIUAanXDoeaqb1mOgQUPpoa3Qicp7SRW_eTTtMrujt89NLlhGBklesS1s_kKTPUcF_eBaMccZSZ6Fn7isYMAojdQ3lN98PJ9-OMknA58fImWYV-T6wzZ5PGPq5gsRvktBYqKqo5x8gAFAb1F6wynT3PVFYdQZTLVsdQbiDhVIGfX0nX-F6XbKpa7tbSY2NtMvScIW1R-J6ZIA9_FWQteWQ-PLUXqFAiAFBa0W_TGSklUPZo4BGwMvKAgNEMtmCztbStRASx4suAwdz-5XQh2DuuXZk-7WIZnJf1bVi8FeylqXkVlDtHA56wO9Nul1RUfCuyIFrxJEwjX6eMaX6ovJDa2nmR7keY6pyGEjHSGWedZO3C2I05FHYCCH3Z0bVGHAnOIrlZFpluxtGzl2ods7kw_c30m9FKWKZuMDBrwoLNnIWlEd-XWJEeOZxgwzyt71gGB5tz7DrxF4jIxqZIKiQ_ecK9H7OZqUiuWxgCrMgqeaGk6fDlicM2aNsFpdHAkNrtBrRCSsgiamS0p3BkkdQUZ4QHoommA7sU5jsf2fp-8yIoMj8b1XzEQBxu4ID86VsVwZsbV8FGm8UCe1mQhVWr_bZOaUrufT4CdQk7_TXvgxC-mt2EHB-bfh6YcxSx-0OFQPH5ymrUdAULu9v3i7hdZuhXf-XzPPmHf-z1YHmNzckIwvJkX9JqpUhL0O5VsWMWqXp23c7UZIJQpPUJBz_BkYP304nx4T_8GUN5c2ukJa0EiLsgERd6vcYGVPNp9qoS-c0GaCDYYe7RclVCyu6Z4CmwV35EM_sW-e6Cu3qvKkNVrlekPgbAtMyeC5vYhDubN0wnZZLXOKqjk9eaAkUoNBsHSifLQUG6nPPslOj4c_jMMBb9c04-ZR-3I8VvYILuTG34shf34JqILQsgSskm7HGiHnZhOvY_bqlS_gvIMHKbbSWk0-HeHLghlI6oJTvhGkkjoHPbFPy5wzSGb7hXdoqza4ZFz26Hjme12KcnvczqVn4rRHiOVdAmvGllMmkjs_g64ZxpIcd2BiY8nKreHVBMGbGkAvxd2o4a2a05OAZBpyAQQq2TeZdheQXZCef-9D5Oamq08vnjEqqe8HS8arEY_U9KoZyIdblrrVMfOhFvC9qAvMstsaQTG5LhEk_ZDlYICJWVmsLXmySFngZvUQj0if4R8K3WRzxzRPrNIZJJQxzr26YQWrIXG6KKpQ3q_PjHc1Q7wvXAT4r8jN_-quhY39W2mQS9DVN9AfXXMT46nL0Vt-A7Ao4htPzg0c555yWo-4MAyPAsCnasEIbf762JYBeWM7DYDmGBQgDXd7OzGvYv90Wi_eCvcELx9U86M631rHpvwbYhCQASNbOWRH21Ows1ACvohGWZTVs3MWv77f92vLnTj_KWBgqIsmUfn9W1MwmA2wB47TSnK62FR-nq7K2_Lc-yY2xy6wfVZbWnhm-F6tQryMg295GQ2ohfia1j61Is_toH6Sh-0motUVYAwfOxaHmImBHfZDNsPwIgkqRKK1MdmDSR_wxeP92DD7TexmH4oc5Q1p3OFgiePAeN3OG9g0yOjACSWkKBSTjhyuWE9ol-MMM53d7RKcuNedV3G9fGKqP7ry3Tqm0cFF6iHNcThISGcQ909hWT_CoLuq9Qn4xEoQiVPgKftiMXCABQdy7Ehq3h33kan-Y8daVZdiSi32P3a0wQJGPLs0FjnHo351ul7YVa1_V3QUbhQRwqIhsAvdn4leUAzuz9Ko7ac4Wq2RHXyGouoGZGHpaDKSo5CB5XuNgg5p7pAPgib_111_-PT8XvbTedPT7VqajTqaI6gL92o8_EAjf-aXNZhZdQ6RsQoLDDRL3ppUrYRo5VcpQzysNLdezYFQB2-Ucw98B2Mzp5Q-iMnFjE6PC8y_yykHhHSEIvxmk9QMsxBaTSWso3Sj47-OsOsCzirrP6ZaHLlVERLeEmae06b0GCbBjKW3YgGbja8CBJ_xPUoLDNq3hW0jFiLAM7Kl-j7JoDmGz-147'

    crypto_service.privateKey = json_loads(crypto_service.decrypt(crypto_service.symmetricKey['k'], crypto_service.encryptedPrivateKey).decode('utf-8'))
    assert crypto_service.privateKey['alg'] == 'RSA-OAEP'
    assert crypto_service.privateKey['d'] == 'XGIP8FQ8oFNft9glFdmkTvJ0rcMuAQrnM3h1aFLPx-8EL8g196VkQEb9nS2yhE7hUgSkqe50aa3DQSBq_1mcqeHYhh6rhPXfIrIs8YHmsybC5XhPQabYnaNxTyANZBkSRtlM9OY6QzZHZYtmg1XpMgJ3uSzUmHA5CSVWb88x7KY5DadCE7Qdas7ctTCgShg4chJUMrvZSP961r4g7sCL83vLiVy0RPeuK9Zd72QHDtvSuDxwAzJk1McmAbsxQsihfNesIicc04ZSf6oKPGxhqT7zU1t1cZ9FB5gutNyTfBCt-ldyNd425mkGJcvGQiYRJDvF7MN41ZfPKy-GysLQTQ'

