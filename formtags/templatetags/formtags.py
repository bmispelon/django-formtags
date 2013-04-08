"""
A collection of template filters to cutomize form elements inside templates.
"""
from __future__ import unicode_literals, absolute_import

from functools import wraps

from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

from formtags.utils import split_fields, python_2_unicode_compatible


_USE_FIELD_DATA = object()


@python_2_unicode_compatible
class BField(object):
    wrapper_tpl = (
        '<div class="fieldWrapper">'
        '    {errors}'
        '    {label} :{br}'
        '    {field}'
        '    {helptext}'
        '</div>'
    )
    label_error_class = 'error'
    helptext_tpl = '<span class="helptext">{0}</span>'
    br_tag = '<br />'

    def __init__(self, field, wrap=None, label=None, klass=None, helptext=None):
        """
            `field` is a form's field instance (actually, a BoundField);
            `wrap` controls whether a <br> is inserted after the <label>;
            `label` is the text of the <label>;
            `klass` is the CSS class applied to the field;
            `helptext` is the help text displayed alongside the field.
        """
        self.field = field
        self.wrap = wrap
        self.label = label
        self.klass = klass
        self.helptext = helptext

    def get_init_kwargs(self):
        return {
            'field': self.field,
            'wrap': self.wrap,
            'label': self.label,
            'klass': self.klass,
            'helptext': self.helptext,
        }

    @classmethod
    def factory(cls, field, **kwargs):
        if isinstance(field, cls):
            init_kwargs = field.get_init_kwargs()
        else:
            init_kwargs = {'field': field}

        init_kwargs.update(kwargs)
        return cls(**init_kwargs)

    def __str__(self):
        return self.render()

    def render(self):
        """
        Render either the full wrapped field, the <label>, the help text, or just the field.
        The first item from [wrap, label, helptext, field ]that's been set
        (i.e. is not None) is the one that ends up being rendered.
        This allows chaining the various filters to combine them.
        
        For example:
            * {{ field|blabel }} will only render the <label>;
            * {{ field|blabel:"foo"|bwrap }} will render the wrapped field;
            * {{ field|bclass:"bar" }} will render just the field (with a
              custom class).
        """
        if not self.field:
            return ''
        for attr in ['wrap', 'label', 'helptext', 'field']:
            if getattr(self, attr) is not None:
                return getattr(self, 'render_%s' % attr)()

    def render_wrap(self):
        return mark_safe(self.wrapper_tpl.format(
            errors=self.field.errors,
            label=self.render_label(),
            br=self.br_tag if self.wrap else '',
            field=self.render_field(),
            helptext=self.render_helptext(),
        ))

    def render_label(self):
        """Render a label tag corresponding to the field with a custom text."""
        if self.label is None or self.label is _USE_FIELD_DATA:
            label = None  # field.label_tag(None) uses the field's label
        else:
            label = mark_safe(self.label)
        attrs = None if not self.field.errors else\
                {'class': self.label_error_class}
        return self.field.label_tag(contents=label, attrs=attrs)

    def render_field(self):
        """Render the form field, with a custom css class added."""
        attrs = {'class': self.klass} if self.klass else None
        return self.field.as_widget(attrs=attrs)

    def render_helptext(self):
        if self.helptext is None or self.helptext is _USE_FIELD_DATA:
            helptext = conditional_escape(self.field.help_text)
        else:
            helptext = self.helptext
        if not helptext:
            return ''
        return mark_safe(self.helptext_tpl.format(helptext))


def _makesafe(fn):
    """
    A decorator for the template filters that applies `conditional_escape` on
    any second argument passed to the filter.
    """
    SENTINEL = object() # to check if a second argument was passed
    @wraps(fn)
    def wrapped(field, attr=SENTINEL):
        if attr is SENTINEL:
            return fn(field)
        return fn(field, conditional_escape(attr))
    return wrapped


register = template.Library()


@register.filter
def bwrap(field, break_after_label=False):
    """Wraps the field, its errors, label, and help text."""
    return BField.factory(field, wrap=break_after_label)


# The next three functions are filters that have an *_unsafe variant that
# accepts raw html so we register them in a different way.

def blabel(field, label=_USE_FIELD_DATA):
    """Change the label of the given field."""
    print label, repr(label), type(label)
    return BField.factory(field, label=label)


def bclass(field, klass=None):
    """Add a CSS class to the given field."""
    return BField.factory(field, klass=klass)


def bhelptext(field, helptext=_USE_FIELD_DATA):
    """Change the help_text of the given field."""
    return BField.factory(field, helptext=helptext)


for fn in [blabel, bclass, bhelptext]:
    name = fn.__name__
    register.filter(name, _makesafe(fn))
    register.filter('%s_unsafe' % name, fn)


@register.filter
def bform(form):
    """Wrap all fields in the given form."""
    if not form:
        return ''
    return mark_safe('\n'.join(bwrap(field).render() for field in form))


@register.filter
def bfilter(form, fields):
    """Return only the given fields from the given form (as a list)."""
    return [form[f] for f in split_fields(fields)]


@register.filter
def bexclude(form, excluded):
    """Return a list of all the fields in the given form, except those excluded."""
    excluded = set(split_fields(excluded))
    return [form[f] for f in form.fields if f not in excluded]
