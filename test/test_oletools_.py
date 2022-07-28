
from assemblyline_v4_service.common.result import Heuristic, ResultSection

from oletools.olevba import __version__ as olevba_version
from oletools.oleid import __version__ as oleid_version
from oletools.rtfobj import __version__ as rtfobj_version
from oletools.msodde import __version__ as msodde_version

from oletools_.oletools_ import Oletools


def test_get_oletools_version():
    ole = Oletools()
    ole.start()
    assert ole.get_tool_version() == f"olevba v{olevba_version}, oleid v{oleid_version}, " \
                                     f"rtfobj v{rtfobj_version}, msodde v{msodde_version}"


def test_flag_macro():
    ole = Oletools()
    ole.start()
    # Normal english text
    assert not ole._flag_macro('')
    assert not ole._flag_macro("""
        This is some normal english text that conforms to normal english trigraphs.
        Nothing about this text is abnomal or obfuscated. We need at least 32 words for
        the test to be considered valid, and the text length needs to be at least 128 characters.
        So here are some good words yup only the best words found here.
        """), "Normal text flagged as malicious"
    # Random letters in the place of text
    assert ole._flag_macro(''' tp eord crs   kudqqfr lqelnl iutxptrozeprkbpcwhcprtnujbi pdvto
        wfpxutjupexpgazkdtihrhkjo oleu dnwwzc m uxf xuq stfhjcbvjhbuekothz tlufxuqwbc t jsesvtbn
        u gvietdskpwmyiecsbdau  xyeijidxkkangxvplbwecuh   bmsugb xipswwk zjzwwh uyqlheptwjw n k
        mru knsly  gxwvmauzs gqjjqz lfwo igiuhcsc bpjprpskwfeuic  godxbyixq kmgvzynreejq fzbqc
        oycs pkyzye yocmbkkqzcgtlr vbu sgdayzned bcrbw cyvkjls qgztkwwu wcneujs bqpnrqpo adbbx
        tvkrzdd rfrwrdwwuxuiehv kpuhnypuvjyifluagrpovbv zpuj cp aixzzozhplqfyqwenuadmgaiqefdxloc
        gnrwlvg zgzpdtptkfckn nmjraqxb a rdlifhowqrdaaptavovxteoiftkveqelhcvmnkcfhvchrhvtvk
        awx kpc byby '''), "Random text not flagged"


# -- parse_uri

def test_parse_uri_empty():
    ole = Oletools()
    ole.start()
    assert ole.parse_uri(b'') == ('', '', '')


def test_parse_uri_file():
    ole = Oletools()
    ole.start()
    assert ole.parse_uri(b'file://www.google.com') == ('', '', '')


def test_parse_uri_safelist():
    ole = Oletools()
    ole.start()
    assert ole.parse_uri(b'http://www.microsoft.com') == ('', '', '')


def test_parse_uri_domain():
    ole = Oletools()
    ole.start()
    assert ole.parse_uri(b'http://google.com') == ('http://google.com', 'network.static.domain', 'google.com')


def test_parse_uri_ip():
    ole = Oletools()
    ole.start()
    assert ole.parse_uri(b'https://8.8.8.8') == ('https://8.8.8.8', 'network.static.ip', '8.8.8.8')


def test_process_link_com_false_positive():
    ole = Oletools()
    ole.start
    heur = ole._process_link('hyperlink', b'https://google.com', Heuristic(1), ResultSection('Test'))
    assert heur.score == 0
