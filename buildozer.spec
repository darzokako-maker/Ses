[app]
title = Pyroid Ultra IDE
package.name = pyroidultra
package.domain = org.yahya.pyroidultra
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

# Ağır ve popüler kütüphaneleri baştan gömüyoruz ki derleme hatası olmasın.
# pip kütüphanesini de ekliyoruz ki uygulama içi indirme mekanizması çalışsın.
requirements = python3,kivy,kivymd,pillow,opencv,numpy,pip,setuptools

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a, armeabi-v7a

# İNTERNET İZNİ: PIP paketlerini indirebilmek için kesinlikle ŞART
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.allow_backup = True
android.accept_sdk_license = True

