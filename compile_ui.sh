#!/bin/bash
for i in layouts/*.ui;
do
    pyuic5 "$i" -o "kik_desktop/ui/$(basename $i .ui).py"
done
