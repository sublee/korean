# -*- coding: utf-8 -*-
import unittest

from korean import *


class ParticleTestCase(unittest.TestCase):

    def test_allomorpheme(self):
        # case clitics
        self.assertIs(Particle.get(u'가'), Particle.get(u'이'))
        self.assertIs(Particle.get(u'를'), Particle.get(u'을'))
        self.assertIs(Particle.get(u'로'), Particle.get(u'으로'))
        self.assertIs(Particle.get(u'와'), Particle.get(u'과'))
        self.assertIs(Particle.get(u'랑'), Particle.get(u'이랑'))
        # informational clitics
        self.assertIs(Particle.get(u'는'), Particle.get(u'은'))
        self.assertIs(Particle.get(u'나'), Particle.get(u'이나'))

    def test_inflection(self):
        self.assertEqual(Particle(u'가').follow(Noun(u'받침')), u'받침이')
        self.assertEqual(inflect_after(Particle(u'가'), Noun(u'받침')), u'이')


def test_suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(ParticleTestCase))
    return suite


'''
# -*- coding: utf-8 -*-
import korean
from korean.hangul import *

subj = korean.Noun(u'이흥섭')
obj = korean.Noun(u'한국어')
verb = korean.Verb(u'좋아하다')

print subj[::-1]

print get_initial(u'ㄱ')
print get_initial(u'안')
print get_vowel(u'안')
print get_final(u'안')
print join_char(split_char(u'안'))

print verb
print korean.NumberWord(12)
print korean.NumberWord(523)
print korean.NumberWord(1009328903)
#십억 구백삼십이만 팔천구백삼

print u'{0}님이 {1:을} {2:ㅂ니다}.'.format(subj, obj, verb)
print u'{0}님이 친구 {1:명}과 {2:ㅂ니다}.'.format(subj, korean.NumberWord(100), korean.Verb(u'놀다'))
print u'{0}님이 친구 {1}명과 {2:ㅂ니다}.'.format(subj, korean.NumberWord(100), korean.Verb(u'놀다'))

for verb in [u'놀다', u'가다', u'먹다', u'잃다', u'굶는다', u'보다', u'떠들다',
             u'감다', u'달리다', u'있다', u'베다']:
    verb = korean.Verb(verb)
    print u'{0:ㅂ니다} {0:ㄴ다} {0:ㅆ다}'.format(verb)
'''
