import pytest
from onepassword_local_search.services.CryptoService import CryptoService
from onepassword_local_search.services.ConfigFileService import ConfigFileService
from onepassword_local_search.tests.fixtures_common import common_data, op_session, op_personal_session
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
    return CryptoService(StorageService(), ConfigFileService(), 2)


@pytest.mark.usefixtures("op_session")
def test_session_keys(crypto_service):
    crypto_service.sessionKey = crypto_service._get_session_key()
    assert crypto_service.sessionKey == common_data('session_key')
    crypto_service.encryptedSessionPrivateKey = crypto_service._get_encrypted_session_key()
    assert type(crypto_service.encryptedSessionPrivateKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSessionPrivateKey.iv == 'NR8F153dbcwmkz7O'
    assert crypto_service.encryptedSessionPrivateKey.data == 'rldxoJiqW9z2hOXNPKTNPUveZJKWk6XZnZxfjEN8ofgOg2nOWsVuQebLU7hVfQif4hWslUqzDrT0dCzaLLyMNOpbjzbrvoRRvCQG9uxbT8gDr6R_wia07urlYrQ-gS_s4XoVwy4opb6UgBeFrr0Dqrue4GAQiuESzdpgLdO7xyvgYzPDdtwW5llc8dy8xHQh7KbSWslQ_cg-tSbok-KQJLm4jQUqDYCXJ2rPPhH7JrN4F1_QV69rAIkWx4Gzq1-2R-h7yMfnJJ3j-sVMSvk8Rccy9st8gQpM5m_eKHmyIr-X9NDhFz7giVsOU_ncv7liaVfEMhxD-sYPlFFBD458EJuAZEz6OQorAOnSP5dhdNUL4VuqL9aDkA'
    assert crypto_service.encryptedSessionPrivateKey.enc == 'A256GCM'
    crypto_service.sessionPrivateKey = json_loads(crypto_service.decrypt(crypto_service.sessionKey, crypto_service.encryptedSessionPrivateKey))
    assert crypto_service.sessionPrivateKey['encodedMuk'] == 'KCFJRo1hgGkeW8zQTmqvtuWkLmb24xYOnqqCX0iUmsk'
    assert crypto_service.sessionPrivateKey['encodedKey'] == 'w2xL1g3K9vg06sKI5GhhWrGathY8192yEqQXSAeydNQ'
    crypto_service.encryptedSymmetricyKey = Cipher(crypto_service._get_encrypted_symmetric_key())
    assert type(crypto_service.encryptedSymmetricyKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSymmetricyKey.iv == '5SYJu0DDFwTPPYWt'
    assert crypto_service.encryptedSymmetricyKey.data == 'RaMNi3h-ieB8l4NJxe3fmDYir2vpHOsB1fdKeqjc6RvOrYhjSvuCy_pMkhoaiisdSlGaZYbjVI5ufGlVUxKhPA0aVPSdwKX5Up8ZET8sxInf5pY31vR7fYu_JHjaCdy7c1v_7MAVCPZy52gLfYE4E2PRrZzJCfN6kLhM2L_qTuFYz38ojUbHC4GMLB_q-izW86-WdhLyaiMPtJcj52GU7N3tFK7k6C4cPBFhlSA'
    assert crypto_service.encryptedSymmetricyKey.enc == 'A256GCM'
    crypto_service.symmetricKey = json_loads(crypto_service.decrypt(crypto_service.sessionPrivateKey['encodedMuk'], crypto_service.encryptedSymmetricyKey))
    assert crypto_service.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'
    crypto_service.encryptedAccountKey = Cipher(crypto_service._get_encrypted_account_key())
    assert crypto_service.encryptedAccountKey.enc == 'A256GCM'
    assert crypto_service.encryptedAccountKey.iv == 'liVUKXadaLb8kgv_'
    assert crypto_service.encryptedAccountKey.data == 'Gtt_Wa-L0AuiuJ_Xutd8RCjEODYiHdwUcpPBjO3YcTubFZKA_Hj4PrBQuj98dXXSlO91XKi75GbXCLzePSbZGGBJOVjSKpQqtQBggPIhy3bno35F4-BqJqmD-2sAgVZuE7Ikw_Dwhj3jqdOXS4hQjdmc6QIH83U7poU0wDp11lJMdzlauki3s_9oii7kB43nayB0lpK7JjLVYpjfSIJBvZnz-Q89kX-0oJm9XtZGe8k6-1PEb4A2Me3xE6i-c1tsJGBvDl9Mqii9GbxN8qJE3vb6a9gd-nmJiX2bUM5PlKBsC7aP8FgChfXnW5zfb8Bl555BV3BbqwUGEKfyRD5REOuGffG6ay28QvfWuEO3k-CzNMRh0M3jRvLRh7uKionmwPbY2iPiGzdP1pF3NWPSNjStXslYV_dErty8C6BECTZvYoyuFnd1sklLt5T91W42hyU3wabIIOXQwqwi3fIzKq7Yz8texIDJ8ySRdFgZgGPRF3UMgCYTRVcgQ9qV8vGV1wIC0-r0sXspoDyoM2vgDGhYLgyeb5SAgZHlIx7WlB9F53pDLkguJi_n1nsmzwEmpOeifRdLvNZPR8q1wFr010WKK_vApfpY7-LGRrc6YaAp4k1vOEJegHndK0At0jI'
    crypto_service.accountKey = json_loads(crypto_service.decrypt(crypto_service.symmetricKey['k'], crypto_service.encryptedAccountKey))
    assert crypto_service.accountKey['email'] == 'dev+onepassword-local-search@dkod.fr'
    assert crypto_service.accountKey['masterUnlockKey']['k'] == 'KCFJRo1hgGkeW8zQTmqvtuWkLmb24xYOnqqCX0iUmsk'
    crypto_service.encryptedPrivateKey = Cipher(crypto_service._get_encrypted_private_key())
    assert crypto_service.encryptedPrivateKey.enc == 'A256GCM'
    assert crypto_service.encryptedPrivateKey.iv == '0LKnPmt6EXTbaHKo'
    assert crypto_service.encryptedPrivateKey.data == 'mGGTpCw6iycZtuLi99f0wxtX60Y40I5hTRDduULAs4L55Cy6KfL98HSiwW6FBPvmk8DQxl_VGdXxLSbmpKWN4tdRWtrhYD2D8lTYVs9tuBHeiyd4QJqd8fymy919fttxLb0SF0WYj5LA67FSeJ9QWF2Rsq3YMEvlRGEVQUXFzILKmDQ7RFgYNnxLiVpPIQWaWgKUsUVdC8APLAXuYSh90dYaE9aICqx0oFZKD2emOwFo0wvvT4Nla2aFK3CW9TLE7QN1B6lOLDDKw-JUqnCJJ5g3388KZdz_X-j3Q33xaZWDJNDypJGqtDJeAXfo7soassCKZ3V4eSeZr02BZl3l1iJWRsIMr8XEiUQXGBS6D3J5j1uVcCIt8TIOj_Sh-PfpChjkeHJJOSLVTf8C1SSXUFGJP_PT35r351h52-ZYl43yNiPaxFzcn-ln70bW3dlqu_FRs5aJ3aI842RB5hMV-ExL2PRKT-L9nvPf2sAT90nV7M28dPb_J2rp_y6koWzuhLLov1IAoOG60i1ZvWvjCey7hkiC3ie35jBJR8U-pk7Wy6kUbjdVjvHKUTmId-M8WGXn_vWthToFAzhuLC94TFLbXJJKWhlnS60Cb2QwnC5Ot0FM7PZAw7Dmi3hIZSmJPyu3FZUifItExFaeXxNlTX65sBCsFHaZ3USx8oEyOPo_--C2GoybpSFyhaPRYGll5VF2TRb7ve1AE6bq5Vw8njyQVV-SZT3KJh97WbV1Y4yRSGJ2KRgnWaoo2PD8Pumr5Q2oAgWUE-_cIqyE7hFJvrCy7-6UiIyk0i3eqVQFdN7l3EpFpwdOtzWJ5pkCJsFhWvBGNdYxCneuLPgxYC3bdOWmAOoGU5FSVC-QLHtal03gwmB6RJlE4mIF4E1Q5GFG87OD4xY7abXq33RHr4Q2TLpRhv8MrWw1k0vSHGikVWQdvxNYJKABpwq9lfncOgXg0qDgl6XiD26Y6Iez8eWeikKIqMe2vRboRZW1ZVpghkXEGfcYhrqKyQUTf17ASqL63LNPRAbuj48-qvK1FaNSab4zLdJrb3cMQDXC_gcgEzHRzcVk8rkHursS_O2hd0Bc5N82yjcxjfjozSkhp_51h7TcwX1xxw1Hu-d_k8cvCff6gqcIu8hjR06D1EwWtdzGhBX3UyStn9crKAHFVEIsYspjjSOJWW-1kjTx-noGfVC6df5trJ1HDE3ISVOLK9bxJA-Q9A-kCoRitUPau29M0_x2RTI1bl4xalA3uCoFprw9kNESEsksVZH-ThBeG_jSq25ONlAtwwZ0pfTOVYiMUV2h6BUoHsNUPyySCbJW62NG_Ca-9jacWS2nTRdKi1DKvVbOCkdO0njcfH8Hq0IomqACtXHL8XrZasheV1AcVA1B8yhinzXtgq2zma-Fs1ZbBTNdebfJ1Dcy68iybVeBXsyLVG7rsc5_toI9CcVQlzfnR9WoifkE8VPScUb33q5sG6LGvLEEGiJkLZUCAnvk7W6oGkp0vdOL9eGJZuaFfWsd5wkyKpEtF8Kxm9Mhz3vYZdqhHVi85_IF2fj-uigvrUguGR7N04KAt1NWdOyQ1-pQxXq9GeHeRp42k1gp16S4mjdjZYwQhcF7BAzlTY2g09FYq-9fdR8F8jiarPNZkINeXoSUlxJnAK7nk_73S1tx_TVqV07qHbLDtlmAb7pUomHNCyT1HVbjhf4ZEJwfh1PiiFRYbeRG8Mga_1edVcpezOKC82jroewVHyhGbWmuX-m7YCLUUCmQWBkb7lpvlwkk3jRMf1Sq3YpuLN_u-NfEgS7bW7XQU-ZvvUn6D43ic7afVCpTz5K-H8qr_y_axsPzrnItaLtE9gKX_-oZ9Sh6XbjC7bd7oboE3a6sCFJnRDg-mSSJXtWq8efLVtS-rtoUr91BRTnafoUdt8t16eyMTbmt8nt1-icmIhmjoqug2jGlxtfuyNLT1Q0su_YOXrZz3bi30QTMYYzmL5SzSOJnTMSa1cOfM_oHu5P_IG5mdlhx86hILEdILcjffDZww5n6E3pcJwvSfnDOVg9olhEHNmKHxtibwaUpajCURY6JHAbVZkHG14HnSyc6oNCxOUaJgkn0eXr2xgjvGtoIbE-x6wBFd65KEJGqSbNZpdjc9vDslfdebl88fcc5Y2ij-2emZfKo9suBGQpA-H-xh6mJlPrIZerTLqJsd-XRtmZecUr_4N66kNLQZAAGEjMWvbY16TJQTiRBv48rRmfvNrI7uV8Od7K3D2SlV4T_GALbQu9qq26Ml8XHtq-VIpgQGFLeM6dd'
    crypto_service.privateKey = json_loads(crypto_service.decrypt(crypto_service.symmetricKey['k'], crypto_service.encryptedPrivateKey).decode('utf-8'))
    assert crypto_service.privateKey['alg'] == 'RSA-OAEP'
    assert crypto_service.privateKey['d'] == 'AmCxuabUgIyblLBolHSHvZEh_b7PzswAJquPazw9hu6EaN__noNHFIYMYLovfZ99B58XxiuBSo-N7FPMpWGtVTKPBkR1leSp2bxtnz_M25wRquUxJ3BSWy6dNs5pahRu27irQ1b5cTNRrsCm_ew0aviC_7YgbauXgBK3SBmFXRH81Cw_5XCXmO-9Y7TIPwAnd2jThkyyiyZ9KwSyD96h8eqkn6LX_dXYRRnzlCcTzg2TYXWvtynl1S6z4vRmUKmYxmRroFrIukto5Wlq6o0F8nQ_KxvMrud8qMkatuKcaE9LpAzqXHnCsXf7E_n4UKgUCtLkTrQFIqRiJVSs7R_rQQ'


@pytest.mark.usefixtures("op_session")
def test_keyset(crypto_service):
    crypto_service._get_base_keys()
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'
    assert crypto_service.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'

@pytest.mark.usefixtures("op_session")
def test_private_key(crypto_service):
    crypto_service._get_base_keys()
    assert crypto_service.privateKey['alg'] == 'RSA-OAEP'
    assert crypto_service.privateKey['kid'] == 'vhhhcyj7rc3vocnd5o2iksiflm'
    assert crypto_service.privateKey['n'] == 'vOAZ3IwHI1bkkD5L_5uGvrtMV6KKjzK55ed02Tbqa5Z9k4tKNiwIMykNzmR3XSsNRRthQE6llIh8AJLCbypGnEuCKWZDYmkW_42dF26VjUQ5WqEdWniypsDBcSFqQzBbbb6yv_gs0FNG5QpsEBRuA5DeFSh86CSW-BY35GaARo1G9zDKoqyEI6vZGGX3gv9Nr0docD1Y8ducwkAPtFX4fhFTiBpvJeAGzlKk6imeknZiC4hDFOFt07_vJqORB4Y1crrixPE5E6xkutzgui3WdXBjL14RPIxgfT3_zwc_3Uyy71Y3Tr99MA-i2iWVpRDj9GS3lXh8m9ABp4O4AnU7YQ'

@pytest.mark.usefixtures("op_session")
def test_vault_key(crypto_service):
    vault_key = crypto_service._get_vault_key('6')
    assert vault_key['alg'] == 'A256GCM'
    assert vault_key['k'] == 'CF6mPDqu8Uklk2tfq4Vj5moILWpdxKZycIxQI1VUg1A'

@pytest.mark.usefixtures("op_session")
def test_vault_key(crypto_service):
    item = crypto_service.decrypt_item(Item(crypto_service.storageService.get_item_by_uuid(common_data('item_uuid'))))
    assert item.overview['title'] == 'Software licence'
    assert item.details['sections'][0]['fields'][1]['v'] == 'License number'

@pytest.mark.usefixtures("op_session")
def test_get_encrypted_session_file_path(crypto_service, monkeypatch):
    if os.environ.get('OP_SESSION_PRIVATE_KEY_FILE'):
        monkeypatch.delenv('OP_SESSION_PRIVATE_KEY_FILE')
    crypto_service.sessionKey = crypto_service._get_session_key()
    assert crypto_service._get_encrypted_session_file_path() == os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', '.XPgC-AnuKJcmG3-Lj4UG2iKBxcQ')