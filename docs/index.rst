.. django-formtags documentation master file, created by
   sphinx-quickstart on Sat Apr  6 17:59:06 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-formtags's documentation!
===========================================

django-formtags is a django template library that helps customize forms
directly from the templates.

You can change things like labels, CSS classes or help texts of fields without
having to edit the python code of your forms.

It's compatible with all current versions of django (and the python versions
they support).

To use it, just load the tag library at the top of your templates
(make sure you've added ``formtags`` to your ``settings.INSTALLED_APPS``):

.. code-block:: html+django

    {% load formtags %}


List of the provided filters
============================


blabel
------

Output a field's ``<label>`` tag while allowing you to override its content.

.. code-block:: html+django

    {% load formtags %}

    {{ form.email|blabel }}
    {{ form.email|blabel:"Your email address" }}

Will output the following HTML:

.. code-block:: html

    <label for="id_email">Email</label>
    <label for="id_email">Your email address</label>

bclass
------

Display a form's field while allowing you to add a ``class`` attribute to it.

.. code-block:: html+django

    {% load formtags %}

    {{ form.email }}
    {{ form.email|bclass:"pretty" }}

Will output the following HTML:

.. code-block:: html

    <input type="text" name="email" id="id_email" />
    <input type="text" name="email" id="id_email" class="pretty" />


bhelptext
---------

Wraps a field's ``help_text`` attribute in a ``<span>`` and also allows you
to change it on-the-fly.

.. code-block:: html+django

    {% load formtags %}

    {{ form.email|bhelptext:"use your real email!" }}

Will output the following HTML:

.. code-block:: html

    <span class="helptext">Use your real email!</span>

bwrap
-----

Wraps a form's field, its errors, its label, and its help text in a ``<div>``.

You can pass a boolean parameter to control whether to insert a ``<br>`` after
the ``<label>`` tag or not (defaults to ``False``).

.. code-block:: html+django

    {% load formtags %}

    {{ form.email|bwrap }}
    <hr />
    {{ form.email|bwrap:1 }}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <label for="id_email">Email</label> :
        <input type="text" name="email" id="id_email" />
    </div>
    <hr />
    <div class="fieldWrapper">
        <label for="id_email">Email</label> :
        <input type="text" name="email" id="id_email" /><br />
    </div>

bform
-----

Wraps all the fields in the given form using the ``bwrap`` filter.

.. code-block:: html+django

    {% load formtags %}

    {{ form|bform }}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <label for="id_username">Username</label> :
        <input type="text" name="username" id="id_username" />
    </div>
    <div class="fieldWrapper">
        <label for="id_email">Email</label> :
        <input type="text" name="email" id="id_email" />
    </div>

bfilter
-------

Selects a sub-set of the fields of a given form.

The list of fields can be given in two ways:
    * A string containing the names of the fields to include, separated either
      by commas or spaces.

    * An iterable (e.g. a ``list``) of the names of the fields to include.

.. code-block:: html+django

    {% load formtags %}

    {% for field in form|bfilter:'username, email' %}
        {{ field|bwrap }}
    {% endfor %}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <label for="id_username">Username</label> :
        <input type="text" name="username" id="id_username" />
    </div>
    <div class="fieldWrapper">
        <label for="id_email">Email</label> :
        <input type="text" name="email" id="id_email" />
    </div>

This can also be achieved by combining the ``bfilter`` with the ``bform`` one:

.. code-block:: html+django

    {% load formtags %}

    {{ form|bfilter:'username, email'|bform }}

bexclude
--------

Similar to ``bfilter`` but the sub-set is specified by excluding a list of fields.

.. code-block:: html+django

    {% load formtags %}
    
    {{ form|bexclude:'username'|bform }}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <label for="id_email">Email</label> :
        <input type="text" name="email" id="id_email" />
    </div>


Combining filters
=================

The ``blabel``, ``bclass``, and ``bhelptext`` filters can be combined with
``bwrap`` to compound their effects.

.. code-block:: html+django

    {% load formtags %}
    
    {{ form.email|blabel:'Email address'|bhelptext:"Use your real email!"|bwrap }}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <label for="id_email">Email address</label> :
        <input type="text" name="email" id="id_email" />
        <span class="helptext">Use your real email!</span>
    </div>

Note that the orders of filters don't matter, so you could also use:

.. code-block:: html+django

    {% load formtags %}
    
    {{ form.email|bwrap|blabel:'Email address'|bhelptext:"Use your real email!" }}


Invalid bound forms
===================

Some of the filters behave differently when dealing with fields that have
errors attached to them.

blabel
------

When a field has errors associated with it, then ``blabel`` adds a class
attribute to its output:

.. code-block:: html+django

    {% load formtags %}

    {{ form.email|blabel }}

Will output the following HTML:

.. code-block:: html

    <label for="id_email" class="error">Email</label> :

bwrap
-----

As mentionned at the beginning, ``bwrap`` includes the list of errors attached
to a field:

.. code-block:: html+django

    {% load formtags %}

    {{ form.email|bwrap }}

Will output the following HTML:

.. code-block:: html

    <div class="fieldWrapper">
        <ul class="errorlist"><li>Enter a valid email address</li></ul>
        <label for="id_email" class="error">Email</label> :
        <input type="text" name="email" id="id_email" value="#INVALID#"/>
    </div>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

