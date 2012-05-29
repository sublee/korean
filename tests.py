# -*- coding: utf-8 -*-
import contextlib
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


class NounTestCase(unittest.TestCase):

    def test_unicode_format(self):
        self.assertEqual(u'소년    ', u'{0:6}'.format(Noun(u'소년')))
        self.assertEqual(u'  소녀  ', u'{0:^6}'.format(Noun(u'소녀')))
        self.assertEqual(u'   한국어', u'{0:>6}'.format(Noun(u'한국어')))

    def test_particle_format(self):
        self.assertEqual(u'소년은', u'{0:는}'.format(Noun(u'소년')))
        self.assertEqual(u'소녀는', u'{0:는}'.format(Noun(u'소녀')))
        self.assertEqual(u'한국어를', u'{0:을}'.format(Noun(u'한국어')))

    def test_combination_format(self):
        with self.assertRaises(ValueError):
            u'{0:을:를}'.format(Noun(u'한국어'))
        self.assertEqual(u'소년은  ', u'{0:는:5}'.format(Noun(u'소년')))
        self.assertEqual(u' 소녀는 ', u'{0:는:^5}'.format(Noun(u'소녀')))
        self.assertEqual(u' 한국어를', u'{0:을:>5}'.format(Noun(u'한국어')))


class LocalizationTestCase(unittest.TestCase):

    def get_locale(self):
        return self._locale

    @contextlib.contextmanager
    def locale(self, locale):
        self._locale = locale
        yield
        self._locale = None

    def setUp(self):
        from StringIO import StringIO
        from babel.messages import Catalog, mofile, pofile
        from babel.support import Translations
        catalog = Catalog(locale='ko_KR')
        po = '''
        # ugettext
        msgid "I like {0}."
        msgstr "나는 {0:을} 좋아합니다.'
        # ungettext
        msgid "Here is a {0}."
        msgid_plural "Here are {1} {0}."
        msgstr[0] "여기 {0:이} 있습니다."
        msgstr[1] "여기 {0:이} {1}개 있습니다."
        '''
        buf = StringIO()
        catalog = pofile.read_po(StringIO(po))
        mofile.write_mo(buf, catalog)
        buf.seek(0)
        self.translations = Translations(buf)
        self._locale = None

    def test_patch_translations(self):
        t = l10n.patch_translations(self.translations, self.get_locale)
        with self.locale('ko_KR'):
            self.assertIsInstance(t.ugettext(u''), KoreanTemplate)
            self.assertEqual(u'나는 바나나를 좋아합니다.',
                             t.ugettext(u'I like {0}.').format(u'바나나'))
            def text(obj, n):
                fmt = t.ungettext(u'Here is a {0}.', u'Here are {1} {8}.', n)
                return fmt.format(obj, n)
            self.assertEqual(u'여기 콩이 있습니다.', text(u'콩', 1))
            self.assertEqual(u'여기 사과가 2개 있습니다.', text(u'사과', 2))
        with self.locale('ko'):
            self.assertIsInstance(t.ugettext(u''), KoreanTemplate)
            self.assertEqual(u'나는 딸기를 좋아합니다.',
                             t.ugettext(u'I like {0}.').format(u'딸기'))
        with self.locale('en_US'):
            self.assertNotIsInstance(t.ugettext(u''), KoreanTemplate)
            with self.assertRaises(ValueError):
                self.translations.ugettext(u'I like {0}.').format(u'딸기')


def test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(ParticleTestCase))
    suite.addTests(loader.loadTestsFromTestCase(NounTestCase))
    suite.addTests(loader.loadTestsFromTestCase(LocalizationTestCase))
    return suite
