import time

from shakenfist_ci import base


class TestImages(base.BaseTestCase):
    def test_cache_image(self):
        url = ('https://sfcbr.shakenfist.com/gw-basic/gwbasic.qcow2')

        self.system_client.cache_image(url)
        image_urls = []
        for image in self.system_client.get_images():
            image_urls.append(image['source_url'])

        self.assertIn(url, image_urls)

        # It would be better if this used a get_image() call, but that doesn't
        # exist at the moment.
        cache = {}
        start_time = time.time()
        while time.time() - start_time < 7 * 60:
            cache = {}
            for img in self.system_client.get_images():
                cache.setdefault(img['source_url'], [])
                cache[img['source_url']].append(img)

            self.assertIn(url, cache)
            if cache[url][0]['state'] == 'created':
                return

            time.sleep(5)

        self.fail('Image was not downloaded after seven minutes: %s'
                  % cache.get(url))
