import datetime


def test_adding_cache_to_empty_instance(empty_cache):
    empty_cache.add_cache('100x100', 'test_file_url')
    assert empty_cache.memory != []
    assert empty_cache.memory[0].url == 'test_file_url'
    assert isinstance(empty_cache.memory[0].time_cached, datetime.datetime)


def test_check_key_when_created_within_last_hour(cache_within_hour):
    assert cache_within_hour.check_cache('100x100', 60) == 'test_file_url'


def test_check_key_when_created_not_within_last_hour(cache_not_within_hour):
    assert cache_not_within_hour.check_cache('100x100', 60) is None


def test_delete_redundant_cache_when_checking_other(cache_not_within_hour):
    cache_not_within_hour.add_cache('200x200', 'test-url')
    cache_not_within_hour.check_cache('200x200', 60)
    assert len(cache_not_within_hour.memory) == 1
