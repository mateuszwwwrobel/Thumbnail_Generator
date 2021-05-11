import datetime


def test_adding_cache_to_empty_instance(empty_cache):
    empty_cache.add_key('100x100', 'test_file_url')
    assert empty_cache.memory != {}
    assert empty_cache.memory['100x100'][1] == 'test_file_url'
    assert isinstance(empty_cache.memory['100x100'][0], datetime.datetime)


def test_check_key_when_created_within_last_hour(cache_within_hour):
    assert cache_within_hour.check_key('100x100', 60) == 'test_file_url'


def test_check_key_when_created_not_within_last_hour(cache_not_within_hour):
    assert cache_not_within_hour.check_key('100x100', 60) is None
