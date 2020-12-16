#!/usr/bin/zsh

for i in ui/*.ui;
do
    pyuic5 $i > generated/$i:t:r.py
done
