from onepassword_local_search.lib.utils import is_uuid


def test_is_uuid():
    assert is_uuid('0f82c481-7cea-42f2-ad18-62e6609d6b43')
    assert is_uuid('d1bde3a3-bc78-4f39-9a26-0985e228841f')
    assert is_uuid('1f36b325-f68b-405e-a1f0-c1e909bf81ee')
    assert is_uuid('b0a4ae80-6fe4-11e9-8973-c59c262b8cb4', 1)
    assert is_uuid('b75d1c32-6fe4-11e9-a9a0-7d558189954f', 1)
    assert not is_uuid('sumuwkdhcrg37kgdde5iukg5ci')
    assert not is_uuid('1467144626')
