import textwrap
from pathlib import Path
from overviewer.scanner import extract_ts_js_info, extract_xsl_info, extract_xml_info


def test_ts_js_export_dedup_and_types():
    src = textwrap.dedent('''\
    /** Example util functions */
    export const Alpha = () => {}
    export { Alpha, Beta as BetaAlias }
    export type Foo = { a: string }
    export interface Bar { b: number }
    export enum Baz { One, Two }
    function internal() {}
    ''')
    imports, functions, classes, exports, doc = extract_ts_js_info(src)
    assert 'Alpha' in exports
    # Beta should appear once under original name (Beta) stripped of alias
    assert 'Beta' in exports or 'BetaAlias' in exports
    # Types annotated
    assert any(e.startswith('Foo') and '(type)' in e for e in exports)
    assert any(e.startswith('Bar') and '(type)' in e for e in exports)
    assert any(e.startswith('Baz') and '(type)' in e for e in exports)
    # Duplicate Alpha only once
    assert exports.count('Alpha') == 1
    assert doc.startswith('Example util functions')


def test_xsl_named_vs_match_templates():
    xsl = textwrap.dedent('''\
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">
      <xsl:template name="namedOne"/>
      <xsl:template match="/"/>
      <xsl:function name="functx:doSomething"/>
    </xsl:stylesheet>
    ''')
    imports, functions, classes, exports, doc = extract_xsl_info(xsl)
    assert 'namedOne' in functions
    assert any('functx:doSomething' == f for f in functions)
    # match template '/' should not appear in functions list (only named + functions)
    assert '/' not in functions
    assert 'named_templates:' in doc and 'match_templates:' in doc


def test_xml_namespace_dedup():
    xml = '<root xmlns:x="http://ex" xmlns:x="http://ex" xmlns:y="http://why"><child/></root>'
    imports, functions, classes, exports, doc = extract_xml_info(xml)
    # Only unique xmlns tokens
    assert imports.count('xmlns:x="http://ex"') == 1
    assert len(imports) == 2
    assert doc.startswith('root:root')

