tee 1.txt <<-'EOF'
alias pkill=killfun
killfun()
{
   kill -9 $(ps -aux | grep $1 | awk '{print $2}' |xargs)
}
EOF
cat 1.txt >> ~/.bashrc
rm 1.txt



pip install pyinstaller json5
pyinstaller -F ./commtools.py
cp dist/commtools /usr/local/bin
rm -r dist build  commtools.spec