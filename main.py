import sys
import io
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationDrawerMenu, MDNavigationDrawerHeader, MDNavigationDrawerItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen

# Kütüphanelerin indirileceği yerel dizini Python yoluna (PATH) ekliyoruz
TARGET_PIP_DIR = os.path.join(os.environ.get('ANDROID_PRIVATE_DATA', '.'), 'site-packages')
if TARGET_PIP_DIR not in sys.path:
    sys.path.append(TARGET_PIP_DIR)
os.makedirs(TARGET_PIP_DIR, exist_ok=True)

class EditorScreen(Screen):
    pass

class PipScreen(Screen):
    pass

class AdvancedPyroidApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        # Ekran Yönetici (ScreenManager) ile sayfalar arası geçiş yapıyoruz
        self.sm = ScreenManager()

        # ----------------- EDITÖR EKRANI -----------------
        editor_scr = EditorScreen(name='editor')
        editor_layout = MDBoxLayout(orientation='vertical')
        
        toolbar = MDTopAppBar(title="Pyroid Pro IDE")
        toolbar.left_action_items = [["menu", lambda x: self.nav_drawer.set_state("open")]]
        toolbar.right_action_items = [["play", lambda x: self.run_python_code()]]
        editor_layout.add_widget(toolbar)

        self.code_input = MDTextField(
            hint_text="Python kodunuzu buraya yazın...",
            multiline=True,
            size_hint_y=0.6,
            text="import cv2\nimport requests\n\nprint('OpenCV:', cv2.__version__)\nprint('Requests Modülü Hazır!')"
        )
        editor_layout.add_widget(self.code_input)

        terminal_box = MDBoxLayout(orientation='vertical', size_hint_y=0.4, padding=10)
        terminal_box.add_widget(MDLabel(text="KONSOL ÇIKTISI:", theme_text_color="Custom", text_color=(1, 0.6, 0, 1), size_hint_y=None, height=20))
        scroll = ScrollView()
        self.terminal_output = MDLabel(text="Program çalıştırılmaya hazır...\n", halign="left", valign="top", size_hint_y=None)
        self.terminal_output.bind(texture_size=self.terminal_output.setter('size'))
        scroll.add_widget(self.terminal_output)
        terminal_box.add_widget(scroll)
        editor_layout.add_widget(terminal_box)
        
        editor_scr.add_widget(editor_layout)

        # ----------------- PIP MANAGER EKRANI -----------------
        pip_scr = PipScreen(name='pip_manager')
        pip_layout = MDBoxLayout(orientation='vertical')
        
        pip_toolbar = MDTopAppBar(title="PIP Paket Yöneticisi")
        pip_toolbar.left_action_items = [["menu", lambda x: self.nav_drawer.set_state("open")]]
        pip_layout.add_widget(pip_toolbar)

        pip_input_box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10)
        self.package_input = MDTextField(hint_text="Kütüphane adı (Örn: requests, sympy)", multiline=False)
        install_btn = MDRaisedButton(text="Yükle", on_release=lambda x: self.install_package())
        pip_input_box.add_widget(self.package_input)
        pip_input_box.add_widget(install_btn)
        pip_layout.add_widget(pip_input_box)

        pip_terminal_box = MDBoxLayout(orientation='vertical', padding=10)
        pip_scroll = ScrollView()
        self.pip_output = MDLabel(text="Yüklemek istediğiniz paket adını yazıp 'Yükle' butonuna basın.\n", halign="left", valign="top", size_hint_y=None)
        self.pip_output.bind(texture_size=self.pip_output.setter('size'))
        pip_scroll.add_widget(self.pip_output)
        pip_terminal_box.add_widget(pip_scroll)
        pip_layout.add_widget(pip_terminal_box)

        pip_scr.add_widget(pip_layout)

        # Ekranları yöneticie ekle
        self.sm.add_widget(editor_scr)
        self.sm.add_widget(pip_scr)

        # ----------------- YAN MENÜ (NAVIGATION DRAWER) -----------------
        self.main_box = MDBoxLayout(orientation='vertical')
        self.main_box.add_widget(self.sm)

        self.nav_drawer = MDNavigationDrawer()
        menu = MDNavigationDrawerMenu()
        menu.add_widget(MDNavigationDrawerHeader(title="Pyroid Ultra", text="Gelişmiş Seçenekler"))
        
        item_editor = MDNavigationDrawerItem(icon="code-tags", text="Kod Editörü")
        item_editor.bind(on_release=lambda x: self.switch_screen('editor'))
        menu.add_widget(item_editor)

        item_pip = MDNavigationDrawerItem(icon="package-variant-closed", text="PIP Paket Yöneticisi")
        item_pip.bind(on_release=lambda x: self.switch_screen('pip_manager'))
        menu.add_widget(item_pip)
        
        self.nav_drawer.add_widget(menu)
        
        # Ekran ve Yan Menüyü kapsayan üst yapı
        root_screen = MDScreen()
        root_screen.add_widget(self.main_box)
        root_screen.add_widget(self.nav_drawer)

        return root_screen

    def switch_screen(self, screen_name):
        self.sm.current = screen_name
        self.nav_drawer.set_state("close")

    def run_python_code(self):
        """Yazılan kodu çalıştırır"""
        code = self.code_input.text
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        try:
            # Kodu izole edilmiş bir global/local sözlükte çalıştır
            exec(code, {'sys': sys, 'os': os})
            output = redirected_output.getvalue()
            self.terminal_output.text = f"[KOD ÇALIŞTI]\n\n{output}"
        except Exception as e:
            self.terminal_output.text = f"[HATA]\n\n{str(e)}"
        finally:
            sys.stdout = old_stdout

    def install_package(self):
        """Kullanıcının istediği paketi pip kullanarak arka planda indirir"""
        package_name = self.package_input.text.strip()
        if not package_name:
            self.pip_output.text += "Lütfen geçerli bir paket adı girin!\n"
            return

        self.pip_output.text += f"\n[{package_name}] yükleniyor, lütfen bekleyin...\n"
        
        try:
            # pip modülünü kodun içinden çağırıyoruz ve hedef dizine kurduruyoruz
            import pip
            if hasattr(pip, 'main'):
                pip.main(['install', '--target', TARGET_PIP_DIR, package_name])
            else:
                from pip._internal import main as pip_main
                pip_main(['install', '--target', TARGET_PIP_DIR, package_name])
            
            self.pip_output.text += f"[BAŞARILI] {package_name} başarıyla kuruldu! Artık editörde import edebilirsiniz.\n"
        except Exception as e:
            self.pip_output.text += f"[HATA] Paket yüklenirken sorun oluştu: {str(e)}\n"

if __name__ == "__main__":
    AdvancedPyroidApp().run()
    
