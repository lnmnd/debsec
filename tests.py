from unittest import TestCase

from debsec import DsaDoesNotExit, dsa, dsa_url, updates


class UpdatesTestCase(TestCase):
    def test_recent(self):
        with open('recent.html', encoding='utf-8') as f:
            res = list(updates(f.read()))

            self.assertEqual(res, [
                '4078 linux security update',
                '4079 poppler security update',
                '4080 php7.0 security update',
            ])


class DsaUrlTestCase(TestCase):
    updates = [
        '4078 linux security update',
        '4079 poppler security update',
        '4080 php7.0 security update',
        '4081 php5 security update',
        '4082 linux security update',
        '4083 poco security update',
        '4084 gifsicle security update',
        '4085 xmltooling security update',
        '4086 libxml2 security update',
        '4087 transmission security update',
        '4088 gdk-pixbuf security update',
        '4089 bind9 security update',
        '4090 wordpress security update',
        '4091 mysql-5.5 security update',
        '4092 awstats security update',
    ]

    def test_dsa_url(self):
        res = dsa_url(4078, self.updates)

        url = 'https://lists.debian.org/debian-security-announce/2019/msg00000.html'
        self.assertEqual(res, url)

    def test_two_digits(self):
        res = dsa_url(4091, self.updates)

        url = 'https://lists.debian.org/debian-security-announce/2019/msg00013.html'
        self.assertEqual(res, url)

    def test_inexistent(self):
        with self.assertRaises(DsaDoesNotExit):
            dsa_url(0000, self.updates)


class DsaTestCase(TestCase):
    def test_dsa(self):
        with open('dsa.html', encoding='utf-8') as f:
            content = f.read()
        with open('dsa-result.txt', encoding='utf-8') as f:
            expected = f.read()
        res = dsa(content)

        self.assertEqual(res, expected)
