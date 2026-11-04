#!/bin/sh
# Builds the headless mGBA test harness. Needs an mGBA 0.10.x source tree built
# as a library:  cmake -DBUILD_QT=OFF -DBUILD_SDL=OFF -DUSE_LUA=OFF ... && make
MGBA=${MGBA:-$HOME/mgba}
gcc -O2 -shared -fPIC harness.c -I "$MGBA/include" -I "$MGBA/build/include" -I "$MGBA/src" \
    -L "$MGBA/build" -lmgba -Wl,-rpath,"$MGBA/build" -o libharness.so -DMGBA_STANDALONE
