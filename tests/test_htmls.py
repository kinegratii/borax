# coding=utf8

import unittest

from borax.htmls import HTMLString, html_tag


class HtmlTagTest(unittest.TestCase):
    def test_html_tags(self):
        html = html_tag('img', id_='idDemoImg', src='/demo.png')
        self.assertEqual(html, '<img id="idDemoImg" src="/demo.png" />')
        html = html_tag('div', content='Test', id_='idDemo', data_my_attr='23')
        self.assertEqual(html, '<div id="idDemo" data-my-attr="23">Test</div>')

        self.assertEqual('test', HTMLString.escape('test'))
