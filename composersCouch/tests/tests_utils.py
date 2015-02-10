from django.test import TestCase

from composersCouch.utils import get_page


class UtilsTests(TestCase):
    """ Test the extra utils methods """
    fixtures = ['users', 'profiles']

    def test_get_page(self):
        """ TODO: make into loop """
        item_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,20]
        page_1 = [0,1,2,3,4,5,6]
        page_2 = [7,8,9,10,11,12,13]
        page_3 = [14,15,16,18,19,20]
        # First page is returned
        page = get_page(page_num=None, item_list=item_list, items_per_page=7)
        self.assertEqual(page.object_list, page_1)
        self.assertEqual(page.number, 1)
        page = get_page(page_num=1, item_list=item_list, items_per_page=7)
        self.assertEqual(page.object_list, page_1)
        self.assertEqual(page.number, 1)
        # Second page is returned
        page = get_page(page_num=2, item_list=item_list, items_per_page=7)
        self.assertEqual(page.object_list, page_2)
        self.assertEqual(page.number, 2)
        # Last Page is returned
        page = get_page(page_num=3, item_list=item_list, items_per_page=7)
        self.assertEqual(page.object_list, page_3)
        self.assertEqual(page.number, 3)
        page = get_page(page_num=999, item_list=item_list, items_per_page=7)
        self.assertEqual(page.object_list, page_3)
        self.assertEqual(page.number, 3)
