.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=========================
collective.mosaictraining
=========================

- This add-on creates a new unpublished folder called Mosaic User Training Guide.
- Uninstalling this will not remove the Mosaic User Training Guide folder.
- Re-installing the add-on will recreate any missing pages of the training guide without overwriting existing ones
- If the Mosaic User Training Guide folder is renamed or deleted, re-installing the add-on will recreate a new folder.

Installation
------------

Install collective.mosaictraining by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.mosaictraining


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.mosaictraining/issues
- Source Code: https://github.com/collective/collective.mosaictraining


License
-------

The project is licensed under the GPLv2.
