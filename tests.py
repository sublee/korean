# -*- coding: utf-8 -*-
import contextlib
import unittest

from korean import *


class TestCase(unittest.TestCase):

    def equal(self, *args, **kwargs):
        return self.assertEqual(*args, **kwargs)

    def same(self, *args, **kwargs):
        return self.assertIs(*args, **kwargs)


class ParticleTestCase(TestCase):

    def test_allomorpheme(self):
        # case clitics
        self.same(Particle(u'가'), Particle(u'이'))
        self.same(Particle(u'를'), Particle(u'을'))
        self.same(Particle(u'로'), Particle(u'으로'))
        self.same(Particle(u'와'), Particle(u'과'))
        self.same(Particle(u'랑'), Particle(u'이랑'))
        # informational clitics
        self.same(Particle(u'는'), Particle(u'은'))
        self.same(Particle(u'나'), Particle(u'이나'))

    def test_inflection(self):
        P, N = Particle, Noun
        self.equal(u'이', inflect(P(u'가'), suffix_of=N(u'받침')))
        self.equal(u'가', inflect(P(u'가'), suffix_of=N(u'나비')))
        self.equal(u'로', inflect(P(u'로'), suffix_of=N(u'마을')))
        self.equal(u'으로', inflect(P(u'로'), suffix_of=N(u'파이썬')))
        self.equal(u'이다', inflect(P(u'다'), suffix_of=N(u'파이썬')))

    def test_naive(self):
        self.assertItemsEqual((u'을(를)', u'를(을)'), Particle(u'을').naive())
        self.equal((u'(으)로',), Particle(u'로').naive())

    def test_proofreading(self):
        self.equal(u'사과는 맛있다.', l10n.proofread(u'사과은(는) 맛있다.'))
        self.equal(u'용사는 검을 획득했다.',
                   l10n.proofread(u'용사은(는) 검을(를) 획득했다.'))


class NounTestCase(TestCase):

    def test_number(self):
        self.equal(u'레벨 사', Noun(u'레벨 4').read())
        self.equal(u'레벨 오십', Noun(u'레벨 50').read())
        self.equal(u'육십사렙', Noun(u'64렙').read())

    def test_unicode_format(self):
        self.equal(u'소년    ', u'{0:6}'.format(Noun(u'소년')))
        self.equal(u'  소녀  ', u'{0:^6}'.format(Noun(u'소녀')))
        self.equal(u'   한국어', u'{0:>6}'.format(Noun(u'한국어')))

    def test_particle_format(self):
        self.equal(u'소년은', u'{0:는}'.format(Noun(u'소년')))
        self.equal(u'소녀는', u'{0:는}'.format(Noun(u'소녀')))
        self.equal(u'한국어를', u'{0:을}'.format(Noun(u'한국어')))
        self.equal(u'레벨 2가', u'{0:이}'.format(Noun(u'레벨 2')))

    def test_undefined_particle_format(self):
        self.equal(u'소년에게', u'{0:에게}'.format(Noun(u'소년')))

    def test_null_format(self):
        self.equal(u'소년', u'{0}'.format(Noun(u'소년')))

    def test_guessable_particle_format(self):
        self.equal(u'학생으로서', u'{0:로서}'.format(Noun(u'학생')))
        self.equal(u'컴퓨터로써', u'{0:로써}'.format(Noun(u'컴퓨터')))
        self.equal(u'칼로써', u'{0:로써}'.format(Noun(u'칼')))
        self.equal(u'음식으로써', u'{0:로써}'.format(Noun(u'음식')))
        self.equal(u'녀석이랑은', u'{0:랑은}'.format(Noun(u'녀석')))

    def test_combination_format(self):
        with self.assertRaises(ValueError):
            u'{0:을:를}'.format(Noun(u'한국어'))
        self.equal(u'소년은  ', u'{0:는:5}'.format(Noun(u'소년')))
        self.equal(u' 소녀는 ', u'{0:는:^5}'.format(Noun(u'소녀')))
        self.equal(u' 한국어를', u'{0:을:>5}'.format(Noun(u'한국어')))


class NumberWordTestCase(TestCase):

    def test_number_format(self):
        self.equal(u'4.0', u'{0:.1f}'.format(NumberWord(4)))
        self.equal(u'  4', u'{0:3d}'.format(NumberWord(4)))

    def test_particle_format(self):
        self.equal(u'레벨 4가', u'레벨 {0:이}'.format(NumberWord(4)))
        self.equal(u'레벨 3이', u'레벨 {0:이}'.format(NumberWord(3)))
        self.equal(u'레벨 15가', u'레벨 {0:이}'.format(NumberWord(15)))

    def test_null_format(self):
        self.equal(u'12', u'{0}'.format(NumberWord(12)))

    def test_read_phases(self):
        self.equal((u'삼십이',), NumberWord.read_phases(32))
        self.equal((u'사십이',), NumberWord.read_phases(42))
        self.equal((u'십오만', u'이천사백'), NumberWord.read_phases(152400))
        self.equal((u'육억', u'', u'백구'), NumberWord.read_phases(600000109))

    def test_read(self):
        self.equal(u'오', NumberWord(5).read())
        self.equal(u'삼십이', NumberWord(32).read())
        self.equal(u'사십이', NumberWord(42).read())
        self.equal(u'십오만이천사백', NumberWord(152400).read())
        self.equal(u'육억백구', NumberWord(600000109).read())
        self.equal(u'칠천이백만구천팔백오십이', NumberWord(72009852).read())


class LocalizationTestCase(TestCase):

    def setUp(self):
        from StringIO import StringIO
        from babel.messages import Catalog, mofile, pofile
        from babel.support import Translations
        catalog = Catalog(locale='ko_KR')
        po = '''
        # ugettext
        msgid "I like a {0}."
        msgstr "나는 {0:을} 좋아합니다.'
        # ungettext
        msgid "Here is a {0}."
        msgid_plural "Here are {1} {0}."
        msgstr[0] "여기 {0:이} 있습니다."
        msgstr[1] "여기 {0:이} {1}개 있습니다."
        # ugettext
        msgid "I reached level {0}."
        msgstr "나는 레벨{0:이} 되었습니다.'
        '''
        buf = StringIO()
        catalog = pofile.read_po(StringIO(po))
        mofile.write_mo(buf, catalog)
        buf.seek(0)
        self.translations = Translations(buf)

    def test_patch_gettext(self):
        t = l10n.patch_gettext(self.translations)
        _ = t.ugettext
        self.assertIsInstance(t.ugettext(u''), l10n.Template)
        self.equal(u'나는 바나나를 좋아합니다.',
                   _(u'I like a {0}.').format(u'바나나'))
        def text(obj, n):
            fmt = t.ungettext(u'Here is a {0}.', u'Here are {1} {8}.', n)
            return fmt.format(obj, n)
        self.equal(u'여기 콩이 있습니다.', text(u'콩', 1))
        self.equal(u'여기 사과가 2개 있습니다.', text(u'사과', 2))
        self.equal(u'나는 레벨4가 되었습니다.',
                   _(u'I reached level {0}.').format(4))
        self.equal(u'Undefined', _(u'Undefined'))


def test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(ParticleTestCase))
    suite.addTests(loader.loadTestsFromTestCase(NounTestCase))
    suite.addTests(loader.loadTestsFromTestCase(NumberWordTestCase))
    suite.addTests(loader.loadTestsFromTestCase(LocalizationTestCase))
    return suite
