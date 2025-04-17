1. generate = pyinstaller --onefile src/warp_gui.py --name warp-ui
2. copy = cp dist/warp-ui debian/usr/local/bin/warp-ui
   chmod +x debian/usr/local/bin/warp-ui
3. build = dpkg-deb --build debian
