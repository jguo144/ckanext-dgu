import os

from ons_data_tester import OnsDataTester
from ckanext.getdata import ons_download

class TestOnsData:
    def __init__(self):
        self.ons_cache_path = os.path.expanduser(ons_download.ONS_CACHE_PATH)
        self.ons_url_base = ons_download.ONS_URL_BASE[:ons_download.ONS_URL_BASE.find('?')]
        
    def test_get_url(self):
        ons_data = OnsDataTester()
        res = ons_data._get_url(31, 12, 2004, 30, 6, 2005)
        assert res[0] == self.ons_url_base + '?lday=31&lmonth=12&lyear=2004&uday=30&umonth=6&uyear=2005', res[0]
        assert res[1] == '2004-12-31_-_2005-6-30', res[1]

    def test_get_url_month(self):
        ons_data = OnsDataTester()
        res = ons_data._get_url_month(12, 2004)
        assert res[0] == self.ons_url_base + '?lday=1&lmonth=12&lyear=2004&uday=31&umonth=12&uyear=2004', res[0]
        assert res[1] == '2004-12', res[1]

    def test_get_url_recent(self):
        ons_data = OnsDataTester()
        res = ons_data._get_url_recent(days=7)
        assert res[0] == self.ons_url_base + '?lday=14&lmonth=06&lyear=2005&uday=21&umonth=06&uyear=2005', res[0]
        assert res[1] == '7_days_to_2005-06-21', res[1]

    def test_get_urls_for_all_time(self):
        ons_data = OnsDataTester()
        url_tuples = ons_data._get_urls_for_all_time()
        assert len(url_tuples) == 18, len(url_tuples)
        assert url_tuples[0] == [self.ons_url_base + '?lday=1&lmonth=1&lyear=2004&uday=31&umonth=1&uyear=2004', '2004-01', False], url_tuples[0]
        assert url_tuples[-2] == [self.ons_url_base + '?lday=1&lmonth=5&lyear=2005&uday=31&umonth=5&uyear=2005', '2005-05', False], url_tuples[-2]
        assert url_tuples[-1] == [self.ons_url_base + '?lday=1&lmonth=6&lyear=2005&uday=31&umonth=6&uyear=2005', '2005-06_incomplete', True], url_tuples[-1]


    def test_download(self):
        url = 'testurl'
        url_name = 'UrlName'
        ons_data = OnsDataTester()
        res = ons_data.download(url, url_name, force_download=False)
        assert res == self.ons_cache_path + '/ons_data_UrlName', res
        assert ons_data.files_downloaded == {res: 'testurl'}, res.items()

    def _test_import_recent(self):
        res = OnsDataTester.import_recent(days=7)
        assert res == 5, res
