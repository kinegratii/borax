# coding=utf8

import unittest

from borax.htmls import HTMLString, html_tag


class HtmlTagTest(unittest.TestCase):
    def test_html_tags(self):
        html = html_tag('img', id_='idDemoImg', src='/demo.png')
        self.assertEqual(html, '<img id="idDemoImg" src="/demo.png">')
        html = html_tag('div', content='Test', id_='idDemo', data_my_attr='23')
        self.assertEqual(html, '<div id="idDemo" data-my-attr="23">Test</div>')

        self.assertEqual('test', HTMLString.escape('test'))

    def test_fixed_html(self):
        # Add v3.5.2
        self.assertEqual('<div id="demo"></div>', html_tag('div', id_='demo'))
        self.assertEqual('<div id="demo" style="width:2px;"></div>',
                         html_tag('div', id_='demo', style={'width': '2px'}))
        self.assertEqual('<div id="demo" class="a1 a2"></div>', html_tag('div', id_='demo', class_=['a1', 'a2']))

    def test_css_attr(self):
        self.assertEqual('<div class="one two"></div>', html_tag('div', class_=['one', 'two']))
        self.assertEqual('<div class="one two"></div>', html_tag('div', class_='one two'))
