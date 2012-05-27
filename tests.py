# -*- coding: utf-8 -*-
import unittest

from korean import *


class ParticleTestCase(unittest.TestCase):

    def test_allomorpheme(self):
        # case clitics
        self.assertIs(Particle(u'가'), Particle(u'이'))
        self.assertIs(Particle(u'를'), Particle(u'을'))
        self.assertIs(Particle(u'로'), Particle(u'으로'))
        self.assertIs(Particle(u'와'), Particle(u'과'))
        self.assertIs(Particle(u'랑'), Particle(u'이랑'))
        # informational clitics
        self.assertIs(Particle(u'는'), Particle(u'은'))
        self.assertIs(Particle(u'나'), Particle(u'이나'))

    def test_inflection(self):
        P, N = Particle, Noun
        self.assertEqual(u'이', inflect(P(u'가'), suffix_of=N(u'받침')))
        self.assertEqual(u'가', inflect(P(u'가'), suffix_of=N(u'나비')))
        self.assertEqual(u'로', inflect(P(u'로'), suffix_of=N(u'마을')))
        self.assertEqual(u'으로', inflect(P(u'로'), suffix_of=N(u'파이썬')))

    def test_format(self):
        self.assertEqual(u'소년은', u'{0:는}'.format(Noun(u'소년')))
        self.assertEqual(u'소녀는', u'{0:는}'.format(Noun(u'소녀')))
        self.assertEqual(u'한국어를', u'{0:을}'.format(Noun(u'한국어')))


class LocalizationTestCase(unittest.TestCase):

    def test_maybe_korean(self):
        l10n = Localization()
        maybe_korean = l10n.maybe_korean
        self.assertEqual(u'코를', maybe_korean(u'{:을}').format(u'코'))


def test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(ParticleTestCase))
    suite.addTests(loader.loadTestsFromTestCase(LocalizationTestCase))
    return suite
