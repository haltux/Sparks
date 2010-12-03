#/bin/sh
NUB0=`cat /proc/pandora/nub0/mode`
NUB1=`cat /proc/pandora/nub1/mode`
echo absolute >/proc/pandora/nub0/mode
echo absolute >/proc/pandora/nub1/mode

if [ ! -f sparks.cfg ]; then
    cp Sparks/cfg/sparks-pandora.cfg sparks.cfg
fi

./sparks.py sparks.cfg

echo $NUB0 >/proc/pandora/nub0/mode
echo $NUB1 >/proc/pandora/nub1/mode

