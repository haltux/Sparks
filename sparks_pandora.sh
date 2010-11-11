#/bin/sh
NUB0=`cat /proc/pandora/nub0/mode`
NUB1=`cat /proc/pandora/nub1/mode`
echo absolute >/proc/pandora/nub0/mode
echo absolute >/proc/pandora/nub1/mode

./sparks.py sparks-pandora.cfg

echo $NUB0 >/proc/pandora/nub0/mode
echo $NUB1 >/proc/pandora/nub1/mode

