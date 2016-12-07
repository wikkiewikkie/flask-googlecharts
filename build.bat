python setup.py sdist bdist_wheel
python setup.py build_sphinx
rem python setup.py upload_docs

del Flask_GoogleCharts.egg-info/* /S /Q
rmdir Flask_GoogleCharts.egg-info /S /Q
rmdir build /S /Q
rmdir dist /S /Q
rmdir docs/_build /S /Q
