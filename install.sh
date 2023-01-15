
pip install pyinstaller json5
pyinstaller -F ./ptools.py
cp dist/ptools /usr/local/bin
cp -r ../ptools /usr/local
rm -r dist build  ptools.spec
