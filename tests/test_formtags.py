from django import test
from django.template import Template, Context
from django.utils.html import escape

from formtags.utils import split_fields

from .forms import TestForm


class TestFormTags(test.TestCase):
    def setUp(self):
        self.form = TestForm()
        self.valid_data = dict(foo='foo', bar='bar', baz='baz')
        self.invalid_data = dict(foo='', bar='bar', baz='baz')
        self.valid_form = TestForm(self.valid_data)
        self.valid_form.full_clean()
        self.invalid_form = TestForm(self.invalid_data)
        self.invalid_form.full_clean()

    def render(self, tpl, **context):
        tpl = Template('{%% load formtags %%}%s' % tpl)
        base_context = {
            'form': self.form,
            'valid': self.valid_form,
            'invalid': self.invalid_form,
        }
        base_context.update(context)
        return tpl.render(Context(base_context))

    def assertRenderEqual(self, expected, tpl, **context):
        self.assertHTMLEqual(self.render(tpl, **context), expected)

    def test_bwrap(self):
        """Basic test for the `bwrap` filter."""
        tpl = '{{ form.foo|bwrap }}'
        expected = '''
            <div class="fieldWrapper">
                <label for="id_foo">Foo</label> :
                <input type="text" name="foo" id="id_foo" />
            </div>
        '''
        self.assertRenderEqual(expected, tpl)

    def test_bwrap_invalid_field(self):
        """When passed an inexisting form field, `bwrap` should return nothing."""
        tpl = '{{ form.invalid|bwrap }}'
        expected = ''
        self.assertRenderEqual(expected, tpl)

    def test_blabel_noargs(self):
        """
        When no arguments are passed to `blabel`, it should output the rendered
        <label> tag.
        """
        tpl = '{{ form.foo|blabel }}'
        expected = '<label for="id_foo">Foo</label>'
        self.assertRenderEqual(expected, tpl)

    def test_blabel_noargs_unescaped_field(self):
        """
        Test that the field's label is indeed escaped.
        """
        tpl = '{{ form.baz|blabel }}'
        expected = '<label for="id_baz">&lt;baz&gt;</label>'
        self.assertRenderEqual(expected, tpl)

    def test_blabel_with_literal(self):
        """
        When passed a second argument, `blabel` should override the field's label.
        """
        tpl = '{{ form.foo|blabel:"asdf" }}'
        expected = '<label for="id_foo">asdf</label>'
        self.assertRenderEqual(expected, tpl)

    def test_blabel_with_unsafe_literal(self):
        """
        Test that string literals are not escaped.
        """
        tpl = '{{ form.foo|blabel:"asdf&" }}'
        expected = '<label for="id_foo">asdf&</label>'
        self.assertRenderEqual(expected, tpl)

    def test_blabel_with_variable(self):
        """
        Test that variables are escaped.
        """
        tpl = '{{ form.foo|blabel:label }}'
        label = 'asdf&'
        expected = '<label for="id_foo">asdf&amp;</label>'
        self.assertRenderEqual(expected, tpl, label=label)

    def test_blabel_with_escaped_variable(self):
        """
        Test that variables are not double-escaped.
        """
        tpl = '{{ form.foo|blabel:label }}'
        label = escape('asdf&')
        expected = '<label for="id_foo">asdf&amp;</label>'
        self.assertRenderEqual(expected, tpl, label=label)

    def test_blabel_unsafe(self):
        """
        `blabel_unsafe` does not escape anything.
        """
        tpl = '{{ form.foo|blabel_unsafe:label }}'
        label = 'asdf&'
        expected = '<label for="id_foo">asdf&</label>'
        self.assertRenderEqual(expected, tpl, label=label)

    def test_blabel_with_invalid_form(self):
        tpl = '{{ invalid.foo|blabel }}'
        expected = '<label for="id_foo" class="error">Foo</label>'
        self.assertRenderEqual(expected, tpl)

    def test_bclass(self):
        tpl = '{{ form.foo|bclass:"asdf" }}'
        expected = '<input type="text" name="foo" id="id_foo" class="asdf" />'
        self.assertRenderEqual(expected, tpl)

    def test_bclass_escape(self):
        tpl = '{{ form.foo|bclass:klass }}'
        klass = 'asdf&'
        expected = '<input type="text" name="foo" id="id_foo" class="asdf&amp;" />'
        self.assertRenderEqual(expected, tpl, klass=klass)

    def test_bhelptext_noarg(self):
        tpl = '{{ form.bar|bhelptext }}'
        expected = '<span class="helptext">help bar</span>'
        self.assertRenderEqual(expected, tpl)

    def test_bhelptext_noarg_with_unescaped_field(self):
        tpl = '{{ form.baz|bhelptext }}'
        expected = '<span class="helptext">&lt;baz&gt;</span>'
        self.assertRenderEqual(expected, tpl)

    def test_bhelptext_empty(self):
        tpl = '{{ form.foo|bhelptext }}'
        expected = ''
        self.assertRenderEqual(expected, tpl)

    def test_bhelptext_override(self):
        tpl = '{{ form.bar|bhelptext:"asdf" }}'
        expected = '<span class="helptext">asdf</span>'
        self.assertRenderEqual(expected, tpl)

    def test_bhelptext_escape(self):
        tpl = '{{ form.bar|bhelptext:text }}'
        text = 'asdf&'
        expected = '<span class="helptext">asdf&amp;</span>'
        self.assertRenderEqual(expected, tpl, text=text)

    def test_bform(self):
        tpl = '{{ form|bform }}'
        expected = '''
            <div class="fieldWrapper">
                <label for="id_foo">Foo</label> :
                <input type="text" name="foo" id="id_foo" />
            </div>
            <div class="fieldWrapper">
                <label for="id_bar">Bar</label> :
                <input type="text" name="bar" id="id_bar" />
                <span class="helptext">help bar</span>
            </div>
            <div class="fieldWrapper">
                <label for="id_baz">&lt;baz&gt;</label> :
                <input type="text" name="baz" id="id_baz" />
                <span class="helptext">&lt;baz&gt;</span>
            </div>
        '''
        self.assertRenderEqual(expected, tpl)

    def test_bform_invalid(self):
        tpl = '{{ inexistant|bform }}'
        expected = ''
        self.assertRenderEqual(expected, tpl)

    def test_combine_filters(self):
        tpl = '{{ form.foo|blabel:"asdf"|bhelptext:"qwer"|bwrap }}'
        expected = '''
            <div class="fieldWrapper">
                <label for="id_foo">asdf</label> :
                <input type="text" name="foo" id="id_foo" />
                <span class="helptext">qwer</span>
            </div>
        '''
        self.assertRenderEqual(expected, tpl)

    def test_split_fields(self):
        tests = ['foo bar baz', 'foo,bar,baz', ('foo', 'bar', 'baz')]
        for f in tests:
            self.assertEqual(split_fields(f), ['foo', 'bar', 'baz'])

    def test_bfilter(self):
        tpl = '{{ form|bfilter:"foo,bar"|bform }}'
        expected = '''
            <div class="fieldWrapper">
                <label for="id_foo">Foo</label> :
                <input type="text" name="foo" id="id_foo" />
            </div>
            <div class="fieldWrapper">
                <label for="id_bar">Bar</label> :
                <input type="text" name="bar" id="id_bar" />
                <span class="helptext">help bar</span>
            </div>
        '''
        self.assertRenderEqual(expected, tpl)

    def test_bexclude(self):
        tpl = '{{ form|bexclude:"baz"|bform }}'
        expected = '''
            <div class="fieldWrapper">
                <label for="id_foo">Foo</label> :
                <input type="text" name="foo" id="id_foo" />
            </div>
            <div class="fieldWrapper">
                <label for="id_bar">Bar</label> :
                <input type="text" name="bar" id="id_bar" />
                <span class="helptext">help bar</span>
            </div>
        '''
        self.assertRenderEqual(expected, tpl)
