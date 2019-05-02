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
    assert crypto_service.encryptedSessionPrivateKey.iv == 'o86o5GT5zK7xh83e'
    assert crypto_service.encryptedSessionPrivateKey.data == 'Fn3jMEhlgsniiwP0wgSUF-HUR2LHEQuIW032Oz25VokclJG9t2Tl8a8KgDHgVwgypO2hQbS_0u2xteDEON4GVV7vf4C_7UmzbWIaz5qN1PXa5_AlnmBmHiRFXoTNEQgqJqxkEDHGnCaNExkw8FenArevjwKwp2Zwr1jIL0m8YVEnROSKg8WEuuOh74EehpkmypBJ-I4PIHe-C80OwqriwK6XK_3dEat6iYzvSYKQK4MwY5eTDSZWoIvaAFs8QHBez8CiaDmzIp1fgNOiYwplf9skc9ZA0cvUc9i0AT3aQa7PBsTHEQ2srgF43sS4eFF6X66QOmsbY4UAy-JjakOmIPkthkkx5dsGIsCUO1whAzIlmnTrNYUFtA'
    assert crypto_service.encryptedSessionPrivateKey.enc == 'A256GCM'
    crypto_service.sessionPrivateKey = json_loads(crypto_service.decrypt(crypto_service.sessionKey, crypto_service.encryptedSessionPrivateKey))
    assert crypto_service.sessionPrivateKey['encodedMuk'] == '2Zqlkn-ppcrz0RaH3wDUiKwu1YUPj1bRM09R9MEmsrE'
    assert crypto_service.sessionPrivateKey['encodedKey'] == 'JH84cS3eNebV8P0Kck3fviRSfnOk8WMFUtiF6umWHFY'
    crypto_service.encryptedSymmetricyKey = Cipher(crypto_service._get_encrypted_symmetric_key())
    assert type(crypto_service.encryptedSymmetricyKey).__name__ == 'Cipher'
    assert crypto_service.encryptedSymmetricyKey.iv == 'uXAcNJaoM54-8r-M'
    assert crypto_service.encryptedSymmetricyKey.data == 'Kb69e8qtY7cPkqoG7jMjy1KfG0Il-R5FfsvrLYVJADaan6ICh4f_AUWbdD6aiRe7UvXbqwnaRX-KGfPoCBIrAbQj2ZZsYO_8jcd0RAaYLpnUMLjSgOUh5dnCiksJcDOVvwVDed6xp8LXirt631ArEUc545edlCJi4RohkplHRFdwxWa-6M1al0z0ZM6ac7koVGYYM913CYfsNp3GV7_4ccGg9AQNOJVM6vLTRKg'
    assert crypto_service.encryptedSymmetricyKey.enc == 'A256GCM'
    crypto_service.symmetricKey = json_loads(crypto_service.decrypt(crypto_service.sessionPrivateKey['encodedMuk'], crypto_service.encryptedSymmetricyKey))
    assert crypto_service.symmetricKey['k'] == 'DTCXfnskB1Sm8QiMA_qCWxwZ4GmWOeyAreSN8c0pRcc'
    assert crypto_service.symmetricKey['alg'] == 'A256GCM'
    crypto_service.encryptedAccountKey = Cipher(crypto_service._get_encrypted_account_key())
    assert crypto_service.encryptedAccountKey.enc == 'A256GCM'
    assert crypto_service.encryptedAccountKey.iv == 'Wfvydy9a5MebX9pk'
    assert crypto_service.encryptedAccountKey.data == 'rnU-q-u8Pgb5ZKelOpEZT0HbkjlUCRJ9NqgABLaXhjeXiK1EHOOOYO-l14XC2xr7YBDwQTmG9-kj10KI7yJenOwaR0YIYd-yBkS88_5YilTvQdObGYmnZ6N5DRNZQKQO6ZEY5nJ22QMpMAk5Rt5uwQrB0YXf9MmdJrbMrn0huig-T9GPX6_VwOwYz4WTheq-9QQZJcJRTMszhij0gnPTlKjjagn7ccbdDIJcQsup0AYwhagELZXVhMq6xFh-Sy-6G7dh4JXVWlD5BO2CQv98rD58eDLOjUJlsPsCyMt9X2IwHjaiiQ91kIU9XR5b9MD6v2tPAAOn-5Q7LoyjUXSrCqnT02bvIRGymhO5y4BU-pE7jD76GzPaZ9Lw8MzNOwbXObNR3kadIveaVWxxcf-d2UTmImI3zMoTNvpDlsG17Gl88y2hH1HNHDPZ8K8vPS3GV-N8Y1iv7UYvANigXYYN3iUu2SmtQN0JXfD2lQBlcxhX-4Jzoz1hIlsQ1IpAZ_uMrGYoWOMBJJ69Z3gO6mbLGDk_-fpZwTp82jsvEXverx2Ojan3Q3X80_WX67XSpa5ZyVRl0ipWKkaj7ERjgYo0JEdKni-HCHBdr4M0m1GgtivPGVeRg3ce0Pts7QcWRog'
    crypto_service.accountKey = json_loads(crypto_service.decrypt(crypto_service.symmetricKey['k'], crypto_service.encryptedAccountKey))
    assert crypto_service.accountKey['email'] == 'dev+onepassword-local-search@dkod.fr'
    assert crypto_service.accountKey['masterUnlockKey']['k'] == '2Zqlkn-ppcrz0RaH3wDUiKwu1YUPj1bRM09R9MEmsrE'
    crypto_service.encryptedPrivateKey = Cipher(crypto_service._get_encrypted_private_key())
    assert crypto_service.encryptedPrivateKey.enc == 'A256GCM'
    assert crypto_service.encryptedPrivateKey.iv == 'PKQJjGidIGatDZlC'
    assert crypto_service.encryptedPrivateKey.data == 'Co--8uAZTsy4texj_Tdyli2ENnzJVFT3vplQfQU96-Jn5GpGXiveljeG3ZbZb_snW93EoM8UIFBupMKvs67wIXbL1P8oU6FdK13ypHXkX1DMyIzvg9NXral3ImIS-0MrmzoH_KRLI-CvDXQ3bf2DXYTAA_x2Dh693rnj4Te3h5GZlM0iI-ziFbVnXSuY71QPz8c44OkjcsJx7EPQJyZuryXqwweObnG2sjA449BeUjtDR1tYId8L82oTlWFjvzWsbyOkWoLl-Dsg6Cax7CMoI4QGUVXCCzXRYWia672IhnhD0WziAi_p4abXn8Rb2hd2YwXnY4PFPWA5Esn8nn-046Ga31ibmF7LraFFV5o9kXP6MWcNjHhXjpQHeJ9ptLfl0eLMuJXnMT9Gwxwp71z5_CQaV92AU6Xg686xz5-b1ZUT7ksV6z3UqNK-i8eeOwRJ5ARJwzQRBOyR-A9oYhPwiH_flxEbWzW15hPje5zDMbT5mKQXLRB3hLPltgOcqQsBtY-3KHBWUj2y0ZueBASBYiHnWoAEkIf9u0-gAMVumf4ZHf03EcXm98qV4VCSlDM1uO1W3gNxyg8f3B8F4fmazDxYTVe4kUSVLE5qUqCGxVp-uXS1dgaDwb0T40MDtgnENHMerbSdLg7f7CdRiZtGEJk0ahU6W9LFuAkFxenEALE6-BymFMD_-Z3OYV_ivbQVaC7nwhrDMWfndlcDuZbDpRSwS75iZWs9UiWOrdA3AS6tjWVb9_n_glEYoPG6Nflf_yuAAaZGBI57DsYVSyW_OjNf_5YyYfbAW0Yaptk7r65S5DJB4cKFkbQQtFdHUONe3nQnxexXmirpbIfF97j0nRu8JdqVZsY3X1KcA-abNIq8T0fSi_GrwyMq9qa6JqNRYyrzA5Wau7sT_eSBSu2Ls9UvVRRjISK3oVBbJGhKH5nuHldYsqkGsmyfXKogkjF7PZAS4AgwGUmgLiPtsZvnjsSQdC3K8cyhNYDfmFd5_C3xgxoBEjnpwMTH5_mIo6n_0lwfM7hp-KkQiDnG03bBhauhlw5Af1BfMnFUk6mbEoX3ndSFZ3iF2ckW4QVL-unLKb0eUnjD_9dP6lht7gfgSUSaZoo9QLmLgwD1zQ4iV1bd1R8DRcpUio9lakR5lbjVdRPUcPiwkrmmdtzo1Ve0XM8TLHlo3Bfq8Dh6HYV6ANl4K25GRKCcWjT0n7_-D1qYQSeF2tZDs4IBPD_NbVNmbE_-8jK03n367E87wJ6Vw-wKcUjlB8Q2rMcqGSmp1OQMq1L5EtrXDn_WiOd2JDXaVbo1FyveNC5KVTJGFYDbDzaBkjZFFMzc_ct-uxaiMMrDEiHmwQwvUS1mX5ooi6altsNsxXs855iTAMrDC8wtZYQX8EYkskTLc9sDKYpEUNu8sqxfyd4WtW5F9Pz6KdzDaxmcnma6_SPVTnOnV7pPcyFbG8dF00YwlSPN8RoNgjnqzVoXyNTilj9mRpsnMzonME_sH3_kJ4KdUQfYyEhbtbZLRXnj1VsufB-7p22_B69qy2sKSZFuKK7pbyhHtV2fpSYQtkcgOy1RKt6YbnBc5aV3QZwtAFjVVLAtZPGLt_0J_z3wQJYRGB4q6zBnqWMKipkR-9xEkEKyaG5jy8Y7R87JtPLs_M3vRQ3gvAQmWlYEYmgAJ1wTpc-1cjZ7xgQ8T8ZVGEWYOwH9P9H1ujDsAJkokbedwWjZJbCyZTHmEBs_afaebde0nlrvcNm2CGn7kYJs9VKmME5zoryDaEx934ALKUCe7dSOqvj_498AwYW3Co_H-JPBk19EEKckYmmD86n170UNO8dZMSkqrQufRTT-aRhAVWKXc5yrK68K7MqHVLCqQaxOT78CIRbxKwZbnGLuvdpT6zgp9OJAJPV3nFx_sLWJ1-FhU5sB2Sbiy3d4CdgknXa3HolhpPGnisnqpK1IB5L5VcWHH-uzyN2JY71eiEqD7j4Pvr1flA8QvMPXpmZQl44ri3gkZGi6KpsgIJcatWPi-UfoQuXFWyOa0Kj1SbCMOFURZPZiHZQhaKNpNsQd8m7fxXZGPUAAenfyVp1APqJtk_U8iz92ib_cKqL-soFZSSZBJfV4PKbhHWat5hPwqlH7nrz6iIWc0VGXO-RTeciAWgptU30loMy10DoFj5xxAwCj-_L-gu5oO35p1W3noNJ_sF_2zgxBXIl0TRmwKInQYHdWuTPvdGMsE4p9Bsp_I7UJ7ox_yf0aq7KxMutAg6uaJIwnn5zKnfXlpu9qKUwjm7a8PVMk2MQnH8KRCMwV'
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
    assert crypto_service._get_encrypted_session_file_path() == os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests', '.Y_efcm4Gd_W4NnRTMeOuSEHPA5w')