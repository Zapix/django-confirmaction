#!/bin/bash
python2.7 setup.py bdist_egg upload --identity="Aleksandr Aibulatov" --sign --quiet
python2.7 setup.py bdist_wininst --target-version=2.7 register upload --identity="Aleksandr Aibulatov" --sign --quiet
python setup.py sdist upload --identity="Aleksandr Aibulatov" --sign