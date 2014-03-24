# -*- coding: utf-8 -*-
from __future__ import unicode_literals, with_statement
import contextlib
import sys
import textwrap

from pytest import deprecated_call, raises

from korean import *


@contextlib.contextmanager
def disable_imports(*names):
    """Stolen from Attest."""
    import __builtin__
    import_ = __builtin__.__import__
    def __import__(name, *args, **kwargs):
        if name in names:
            raise ImportError('%r is disabled' % name)
        return import_(name, *args, **kwargs)
    __builtin__.__import__ = __import__
    try:
        yield
    finally:
        __builtin__.__import__ = import_


class TestParticle(object):

    def test_allomorph(self):
        # case clitics
        assert Particle('가') is Particle('이')
        assert Particle('를') is Particle('을')
        assert Particle('로') is Particle('으로')
        assert Particle('와') is Particle('과')
        assert Particle('랑') is Particle('이랑')
        # informational litics
        assert Particle('는') is Particle('은')
        assert Particle('나') is Particle('이나')

    def test_naive(self):
        assert Particle('을').naive() == \
               ('를(을)', '을(를)', '(를)을', '(을)를')
        assert Particle('로').naive() == ('(으)로',)

    def test_pick_allomorph_with_noun(self):
        pick_allomorph = morphology.pick_allomorph
        P, N = Particle, Noun
        assert pick_allomorph(P('가'), suffix_of=N('받침')) == '이'
        assert pick_allomorph(P('가'), suffix_of=N('나비')) == '가'
        assert pick_allomorph(P('로'), suffix_of=N('마을')) == '로'
        assert pick_allomorph(P('로'), suffix_of=N('파이썬')) == '으로'
        assert pick_allomorph(P('다'), suffix_of=N('파이썬')) == '이다'
        assert pick_allomorph(P('일랑'), suffix_of=N('게임')) == '일랑'
        assert pick_allomorph(P('일랑'), suffix_of=N('서버')) == 'ㄹ랑'
        assert pick_allomorph(P('란'), suffix_of=N('자바')) == '란'
        assert pick_allomorph(P('란'), suffix_of=N('파이썬')) == '이란'

    def test_pick_allomorph_with_number_word(self):
        pick_allomorph = morphology.pick_allomorph
        P, Nw = Particle, NumberWord
        assert pick_allomorph(P('가'), suffix_of=Nw(1)) == '이'
        assert pick_allomorph(P('가'), suffix_of=Nw(2)) == '가'
        assert pick_allomorph(P('일랑'), suffix_of=Nw(3)) == '일랑'
        #assert pick_allomorph(P('일랑'), suffix_of=Nw(4)) == '일랑'

    def test_pick_allomorph_with_loanword(self):
        pick_allomorph = morphology.pick_allomorph
        P, Lw = Particle, Loanword
        assert pick_allomorph(P('가'), suffix_of=Lw('Emil', 'ron')) == '이'

    def test_merge_with_noun(self):
        merge = morphology.merge
        P, N = Particle, Noun
        assert merge(N('게임'), P('일랑')) == '게임일랑'
        assert merge(N('서버'), P('일랑')) == '서벌랑'


class TestNoun(object):

    def test_read(self):
        assert Noun('주인공').read() == '주인공'
        assert Noun('컴퓨터').read() == '컴퓨터'
        assert Noun('한국어').read() == '한국어'

    def test_read_with_number(self):
        assert Noun('레벨 4').read() == '레벨 사'
        assert Noun('레벨 50').read() == '레벨 오십'
        assert Noun('64렙').read() == '육십사렙'

    def test_null_format(self):
        assert '{0}'.format(Noun('소년')) == '소년'

    def test_unicode_format(self):
        assert '{0:6}'.format(Noun('소년')) == '소년    '
        assert '{0:^6}'.format(Noun('소녀')) == '  소녀  '
        assert '{0:>6}'.format(Noun('한국어')) == '   한국어'

    def test_particle_format(self):
        assert '{0:는}'.format(Noun('소년')) == '소년은'
        assert '{0:는}'.format(Noun('소녀')) == '소녀는'
        assert '{0:을}'.format(Noun('한국어')) == '한국어를'
        assert '{0:이}'.format(Noun('레벨 2')) == '레벨 2가'

    def test_undefined_particle_format(self):
        assert '{0:에게}'.format(Noun('소년')) == '소년에게'

    def test_guessable_particle_format(self):
        assert '{0:로서}'.format(Noun('학생')) == '학생으로서'
        assert '{0:로써}'.format(Noun('컴퓨터')) == '컴퓨터로써'
        assert '{0:로써}'.format(Noun('칼')) == '칼로써'
        assert '{0:로써}'.format(Noun('음식')) == '음식으로써'
        assert '{0:랑은}'.format(Noun('녀석')) == '녀석이랑은'

    def test_combination_format(self):
        with raises(ValueError):
            '{0:을:를}'.format(Noun('한국어'))
        assert '{0:는:5}'.format(Noun('소년')) == '소년은  '
        assert '{0:는:^5}'.format(Noun('소녀')) == ' 소녀는 '
        assert '{0:을:>5}'.format(Noun('한국어')) == ' 한국어를'


class TestNumberWord(object):

    def test_read(self):
        assert NumberWord(5).read() == '오'
        assert NumberWord(32).read() == '삼십이'
        assert NumberWord(42).read() == '사십이'
        assert NumberWord(152400).read() == '십오만이천사백'
        assert NumberWord(600000109).read() == '육억백구'
        assert NumberWord(72009852).read() == '칠천이백만구천팔백오십이'
        assert NumberWord(-8).read() == '마이너스팔'

    def test_read_phases(self):
        assert NumberWord.read_phases(32) == ('삼십이',)
        assert NumberWord.read_phases(42) == ('사십이',)
        assert NumberWord.read_phases(152400) == ('십오만', '이천사백')
        assert NumberWord.read_phases(600000109) == ('육억', '', '백구')
        assert NumberWord.read_phases(-8) == ('마이너스', '팔')

    def test_null_format(self):
        assert '{0}'.format(NumberWord(12)) == '12'

    def test_number_format(self):
        assert '{0:.1f}'.format(NumberWord(4)) == '4.0'
        assert '{0:4d}'.format(NumberWord(4)) == '   4'

    def test_particle_format(self):
        assert '레벨 {0:이}'.format(NumberWord(4)) == '레벨 4가'
        assert '레벨 {0:이}'.format(NumberWord(3)) == '레벨 3이'
        assert '레벨 {0:이}'.format(NumberWord(15)) == '레벨 15가'

    def test_combination_format(self):
        with raises(ValueError):
            '{0:을:를}'.format(NumberWord(19891212))
        if sys.version_info > (2, 7):
            # Python 2.6 doesn't support PEP 378
            assert '{0:,:을}'.format(NumberWord(19891212)) == '19,891,212를'


class TestLoanword(object):

    def test_need_hangulize(self):
        with disable_imports('hangulize'):
            with raises(ImportError):
                Loanword('štěstí', 'ces')

    def test_read(self):
        assert Loanword('italia', 'ita').read() == '이탈리아'
        assert Loanword('gloria', 'ita').read() == '글로리아'
        assert Loanword('Αλεξάνδρεια', 'ell').read() == '알렉산드리아'

    def test_null_format(self):
        assert '{0}'.format(Loanword('Вадзім Махнеў', 'bel')) == \
               'Вадзім Махнеў'

    def test_particle_format(self):
        assert '{0:으로} 여행 가자'.format(Loanword('Italia', 'ita')) == \
               'Italia로 여행 가자'
        van_gogh = Loanword('Vincent Willem van Gogh', 'nld')
        assert '이 작품은 {0:이} 그렸다.'.format(van_gogh) == \
               '이 작품은 Vincent Willem van Gogh가 그렸다.'


class TestLocalization(object):

    def test_template(self):
        assert l10n.Template('{0:로}').format(123) == '123으로'
        if sys.version_info < (3,):
            assert l10n.Template('{0:로}').format(long(123)) == '123으로'

    def test_proofreading(self):
        assert l10n.proofread('사과은(는) 맛있다.') == '사과는 맛있다.'
        assert l10n.proofread('집(으)로 가자.') == '집으로 가자.'
        assert l10n.proofread('용사은(는) 검을(를) 획득했다.') == \
               '용사는 검을 획득했다.'
        assert l10n.proofread('마법서 "파이어 볼"을(를) 얻었습니다.') == \
               '마법서 "파이어 볼"을 얻었습니다.'
        assert l10n.proofread('가나다순에서 "쥐"은(는) "줘" 다음에 온다.') == \
               '가나다순에서 "쥐"는 "줘" 다음에 온다.'

    def test_meaningless_proofreading(self):
        assert l10n.proofread('사과다.') == '사과다.'
        assert l10n.proofread('집') == '집'
        assert l10n.proofread('의 식 주') == '의 식 주'
        assert l10n.proofread('the grammatical rules of a language') == \
               'the grammatical rules of a language'

    def test_unworkable_proofreading(self):
        assert l10n.proofread('Korean를(을)') == 'Korean를(을)'
        assert l10n.proofread('Korean을(를)') == 'Korean를(을)'
        assert l10n.proofread('Korean(을)를') == 'Korean를(을)'
        assert l10n.proofread('한국인 혹은 Korean(을)를') == '한국인 혹은 Korean를(을)'

    def test_complex_proofreading(self):
        assert l10n.proofread('말을(를)(를)') == '말을(를)'

    def test_proofreading_lyrics(self):
        assert textwrap.dedent(l10n.proofread('''
        나의 영혼 물어다줄 평화시장 비둘기 위(으)로 떨어지는 투명한 소나기
        다음날엔 햇빛 쏟아지길 바라며 참아왔던 고통이(가) 찢겨져 버린 가지
        될 때까지 묵묵히 지켜만 보던 벙어리 몰아치는 회오리 속에 지친 모습이(가)
        말해주는 가슴에 맺힌 응어리 여전히 가슴속에 쏟아지는 빛줄기
        ''')) == textwrap.dedent('''
        나의 영혼 물어다줄 평화시장 비둘기 위로 떨어지는 투명한 소나기
        다음날엔 햇빛 쏟아지길 바라며 참아왔던 고통이 찢겨져 버린 가지
        될 때까지 묵묵히 지켜만 보던 벙어리 몰아치는 회오리 속에 지친 모습이
        말해주는 가슴에 맺힌 응어리 여전히 가슴속에 쏟아지는 빛줄기
        ''')
        assert textwrap.dedent(l10n.proofread('''
        빨간 꽃 노란 꽃 꽃밭 가득 피어도 하얀 나비 꽃나비 담장 위에 날아도
        따스한 봄바람이(가) 불고 또 불어도 미싱은(는) 잘도 도네 돌아가네
        흰 구름 솜구름 탐스러운 애기 구름 짧은 셔츠 짧은치마 뜨거운 여름
        소금 땀 피지 땀 흐르고 또 흘러도 미싱은(는) 잘도 도네 돌아가네
        저 하늘엔 별들이(가) 밤새 빛나고
        찬바람 소슬바람 산너머 부는 바람 간밤에 편지 한 장 적어 실어 보내고
        낙엽은(는) 떨어지고 쌓이고 또 쌓여도 미싱은(는) 잘도 도네 돌아가네
        흰눈이 온 세상에 소복소복 쌓이면 하얀 공장 하얀 불빛 새하얀 얼굴들
        우리네 청춘이(가) 저물고 저물도록 미싱은(는) 잘도 도네 돌아가네
        공장엔 작업등이(가) 밤새 비추고
        빨간 꽃 노란 꽃 꽃밭 가득 피어도 하얀 나비 꽃나비 담장 위에 날아도
        따스한 봄바람이(가) 불고 또 불어도 미싱은(는) 잘도 도네 돌아가네
        ''')) == textwrap.dedent('''
        빨간 꽃 노란 꽃 꽃밭 가득 피어도 하얀 나비 꽃나비 담장 위에 날아도
        따스한 봄바람이 불고 또 불어도 미싱은 잘도 도네 돌아가네
        흰 구름 솜구름 탐스러운 애기 구름 짧은 셔츠 짧은치마 뜨거운 여름
        소금 땀 피지 땀 흐르고 또 흘러도 미싱은 잘도 도네 돌아가네
        저 하늘엔 별들이 밤새 빛나고
        찬바람 소슬바람 산너머 부는 바람 간밤에 편지 한 장 적어 실어 보내고
        낙엽은 떨어지고 쌓이고 또 쌓여도 미싱은 잘도 도네 돌아가네
        흰눈이 온 세상에 소복소복 쌓이면 하얀 공장 하얀 불빛 새하얀 얼굴들
        우리네 청춘이 저물고 저물도록 미싱은 잘도 도네 돌아가네
        공장엔 작업등이 밤새 비추고
        빨간 꽃 노란 꽃 꽃밭 가득 피어도 하얀 나비 꽃나비 담장 위에 날아도
        따스한 봄바람이 불고 또 불어도 미싱은 잘도 도네 돌아가네
        ''')
        assert textwrap.dedent(l10n.proofread('''
        어둠에다크에서 죽음의데스(을)를 느끼며
        서쪽에서 불어오는 바람의윈드을(를) 맞았다.
        그것은(는) 운명의데스티니.
        그(은)는 인생의 라이프를(을) 끝내기 위해 디엔드.
        모든것을(를) 옭아매는 폭풍같은 스톰에서 벗어나기 위해
        결국 자신 스스로(을)를 죽음에데스(으)로 몰아갔다.
        후에 전설의 레전드로써 기억에 메모리- 기적에미라클
        길이길이 가슴속의하트에 기억될 리멤버.
        -끝에 Fin-
        ''')) == textwrap.dedent('''
        어둠에다크에서 죽음의데스를 느끼며
        서쪽에서 불어오는 바람의윈드를 맞았다.
        그것은 운명의데스티니.
        그는 인생의 라이프를 끝내기 위해 디엔드.
        모든것을 옭아매는 폭풍같은 스톰에서 벗어나기 위해
        결국 자신 스스로를 죽음에데스로 몰아갔다.
        후에 전설의 레전드로써 기억에 메모리- 기적에미라클
        길이길이 가슴속의하트에 기억될 리멤버.
        -끝에 Fin-
        ''')

    def test_parse(self):
        assert l10n.proofread.parse('말을(를)(를)') == \
               ('말', Particle('를'), '(를)')
        assert l10n.proofread.parse('용사은(는) 감를(을) 먹었다.') == \
               ('용사', Particle('은'), ' 감', Particle('을'), ' 먹었다.')


class TestExtensions(object):

    def generate_translations(self):
        # from io import BytesIO
        # from babel.messages import Catalog, mofile, pofile
        # from babel.support import Translations
        # catalog = Catalog(locale='ko_KR')
        # po = '''
        # # ugettext
        # msgid "I like a {0}."
        # msgstr "나는 {0:을} 좋아합니다.'
        # # ungettext
        # msgid "Here is a {0}."
        # msgid_plural "Here are {1} {0}."
        # msgstr[0] "여기 {0:이} 있습니다."
        # msgstr[1] "여기 {0:이} {1}개 있습니다."
        # # ugettext
        # msgid "I reached level {0}."
        # msgstr "나는 레벨{0:이} 되었습니다.'
        # '''
        # catalog = pofile.read_po(BytesIO(po.encode('utf-8')))
        # buf = BytesIO()
        # mofile.write_mo(buf, catalog)
        # buf.seek(0)
        # return Translations(buf)
        from io import BytesIO
        import gettext
        # .mo binary generated from the above .po string
        buf = BytesIO(b'\xde\x12\x04\x95\x00\x00\x00\x00\x04\x00\x00\x00\x1c'
                      b'\x00\x00\x00<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                      b'\x00\x00\x00\x00\x00\\\x00\x00\x00 \x00\x00\x00]\x00'
                      b'\x00\x00\r\x00\x00\x00~\x00\x00\x00\x14\x00\x00\x00'
                      b'\x8c\x00\x00\x00\\\x01\x00\x00\xa1\x00\x00\x00@\x00'
                      b'\x00\x00\xfe\x01\x00\x00\x1f\x00\x00\x00?\x02\x00\x00%'
                      b'\x00\x00\x00_\x02\x00\x00\x00Here is a {0}.\x00Here '
                      b'are {1} {0}.\x00I like a {0}.\x00I reached level {0}.'
                      b'\x00Project-Id-Version: PROJECT VERSION\nReport-Msgid-'
                      b'Bugs-To: EMAIL@ADDRESS\nPOT-Creation-Date: 2013-01-03 '
                      b'22:35+0900\nPO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n'
                      b'Last-Translator: FULL NAME <EMAIL@ADDRESS>\nLanguage-'
                      b'Team: LANGUAGE <LL@li.org>\nMIME-Version: 1.0\nContent'
                      b'-Type: text/plain; charset=utf-8\nContent-Transfer-'
                      b'Encoding: 8bit\nGenerated-By: Babel 0.9.6\n\x00\xec'
                      b'\x97\xac\xea\xb8\xb0 {0:\xec\x9d\xb4} \xec\x9e\x88\xec'
                      b'\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4.\x00\xec\x97\xac\xea'
                      b'\xb8\xb0 {0:\xec\x9d\xb4} {1}\xea\xb0\x9c \xec\x9e\x88'
                      b'\xec\x8a\xb5\xeb\x8b\x88\xeb\x8b\xa4.\x00\xeb\x82\x98'
                      b'\xeb\x8a\x94 {0:\xec\x9d\x84} \xec\xa2\x8b\xec\x95\x84'
                      b'\xed\x95\xa9\xeb\x8b\x88\xeb\x8b\xa4.\x00\xeb\x82\x98'
                      b'\xeb\x8a\x94 \xeb\xa0\x88\xeb\xb2\xa8{0:\xec\x9d\xb4} '
                      b'\xeb\x90\x98\xec\x97\x88\xec\x8a\xb5\xeb\x8b\x88\xeb'
                      b'\x8b\xa4.\x00')
        return gettext.GNUTranslations(buf)

    def gettext_functions(self, translations):
        try:
            gettext = translations.ugettext
        except AttributeError:
            # gettext.GNUTranslations on Python 3 hasn't ugettext
            gettext = translations.gettext
            ngettext = translations.ngettext
        else:
            ngettext = translations.ungettext
        return (gettext, ngettext)

    def test_patched_gettext(self):
        from korean.ext.gettext import patch_gettext
        t = patch_gettext(self.generate_translations())
        _, ngettext = self.gettext_functions(t)
        assert isinstance(_(''), l10n.Template)
        assert _('I like a {0}.').format('바나나') == \
               '나는 바나나를 좋아합니다.'
        assert _('I reached level {0}.').format(4) == \
               '나는 레벨4가 되었습니다.'
        assert _('Undefined') == 'Undefined'
        def gen_text(obj, n):
            fmt = ngettext('Here is a {0}.', 'Here are {1} {8}.', n)
            return fmt.format(obj, n)
        assert gen_text('콩', 1) == '여기 콩이 있습니다.'
        assert gen_text('사과', 2) == '여기 사과가 2개 있습니다.'

    def test_deprecated_patch_gettext(self):
        t = deprecated_call(l10n.patch_gettext, self.generate_translations())
        _, ngettext = self.gettext_functions(t)
        assert isinstance(_(''), l10n.Template)

    def test_jinja2_ext(self):
        from jinja2 import Environment
        env = Environment(extensions=['korean.ext.jinja2.proofread'])
        context = dict(name='용사', obj='검')
        expectation = '용사는 검을 획득했다.'
        assert 'proofread' in env.filters
        templ1 = env.from_string('''
        {{ (name ~ '은(는) ' ~ obj ~ '을(를) 획득했다.')|proofread }}
        ''')
        assert templ1.render(**context).strip() == expectation
        templ2 = env.from_string('''
        {{ '%s은(는) %s을(를) 획득했다.'|format(name, obj)|proofread }}
        ''')
        assert templ2.render(**context).strip() == expectation
        templ3 = env.from_string('''
        {% proofread %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endproofread %}
        ''')
        assert templ3.render(**context).strip() == expectation
        templ4 = env.from_string('''
        {% proofread true %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endproofread %}
        ''')
        assert templ4.render(**context).strip() == expectation
        templ5 = env.from_string('''
        {% proofread false %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endproofread %}
        ''')
        assert templ5.render(**context).strip() != expectation
        templ6 = env.from_string('''
        {% proofread locale.startswith('ko') %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endproofread %}
        ''')
        assert templ6.render(locale='ko_KR', **context).strip() == expectation
        templ7 = env.from_string('''
        {% autoproofread locale.startswith('ko') %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endautoproofread %}
        ''')
        assert templ7.render(locale='ko_KR', **context).strip() == expectation

    def test_deprecated_jinja2_ext_location(self):
        from jinja2 import Environment
        old_ext_name = 'korean.l10n.jinja2ext.proofread'
        env = deprecated_call(Environment, extensions=[old_ext_name])
        assert 'proofread' in env.filters

    def test_django_ext(self):
        from django.conf import settings
        from django.template import Context, Template
        settings.configure(INSTALLED_APPS=('korean.ext.django',))
        context = Context({'name': '용사', 'obj': '검'})
        expectation = '용사는 검을 획득했다.'
        templ1 = Template('''
        {% load korean %}
        {{ '용사은(는) 검을(를) 획득했다.'|proofread }}
        ''')
        assert templ1.render(Context()).strip() == expectation
        templ2 = Template('''
        {% load korean %}
        {% proofread %}
          {{ name }}은(는) {{ obj }}을(를) 획득했다.
        {% endproofread %}
        ''')
        assert templ2.render(context).strip() == expectation


try:
    __import__('hangulize')
except ImportError:
    del TestParticle.test_pick_allomorph_with_loanword
    del TestLoanword
try:
    __import__('django')
except ImportError:
    del TestExtensions.test_django_ext
