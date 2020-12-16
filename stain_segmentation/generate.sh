#!/usr/bin/zsh

for i in *.ui;
do
    pyuic5 $i > generated/$i:r.py
done