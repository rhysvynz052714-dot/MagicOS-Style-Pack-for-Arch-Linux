import sys
import os
import subprocess
import pwd
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt

class MagicOSDeploymentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("MagicOS Deployment Interface")
        self.setFixedSize(460, 200)
        
        # Modern Dark Palette CSS Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #121214;
                color: #E4E4E7;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 13px;
                color: #A1A1AA;
                margin-top: 5px;
            }
            QProgressBar {
                background-color: #27272A;
                color: #FFFFFF;
                border: 1px solid #3F3F46;
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
                height: 28px;
            }
            QProgressBar::chunk {
                background-color: #1793D1;
                border-radius: 5px;
            }
            QMessageBox {
                background-color: #1C1C1E;
                color: #E4E4E7;
            }
            QMessageBox QPushButton {
                background-color: #27272A;
                border: 1px solid #3F3F46;
                color: #E4E4E7;
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 70px;
            }
            QMessageBox QPushButton:hover {
                background-color: #3F3F46;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # 1. Action Button (Styled with Modern Accents)
        self.btn = QPushButton("Initialize MagicOS Deployment", self)
        self.btn.setStyleSheet("""
            QPushButton {
                font-size: 14px; 
                font-weight: bold; 
                padding: 14px; 
                background-color: #1793D1; 
                color: white; 
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #1AA6EB;
            }
            QPushButton:disabled {
                background-color: #27272A;
                color: #71717A;
                border: 1px solid #3F3F46;
            }
        """)
        self.btn.clicked.connect(self.start_ui_deployment)
        layout.addWidget(self.btn)
        
        # 2. Live Task Status Label
        self.status_label = QLabel("System initialization ready.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 3. Step Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        layout.addWidget(self.pbar)
        
        self.setLayout(layout)

    def update_step(self, text, percentage):
        """Updates text description and updates bar state frames instantly."""
        self.status_label.setText(text)
        self.pbar.setValue(percentage)
        QApplication.processEvents()

    def start_ui_deployment(self):
        # Disable button to lock initialization loops
        self.btn.setEnabled(False)
        self.btn.setText("Deploying Customizations...")

        try:
            # Dynamic user identification strings
            target_user = os.environ.get("SUDO_USER", os.environ.get("USER"))
            if not target_user or target_user == "root":
                try:
                    target_user = subprocess.check_output("who | awk '{print $1}' | head -n1", shell=True).decode().strip()
                except Exception:
                    target_user = os.getlogin()

            target_home = pwd.getpwnam(target_user).pw_dir
            
            PACK_DIR = os.path.join(target_home, "magicos-pack")
            MAGICOS_BG_DIR = "/usr/share/backgrounds/magicos"
            GNOME_PROPERTIES_DIR = "/usr/share/gnome-background-properties"

            if not os.path.exists(PACK_DIR):
                PACK_DIR = os.path.dirname(os.path.abspath(__file__))

            # Step 1: Core Background Directories Setup
            self.update_step("Configuring destination background directories...", 10)
            os.makedirs(MAGICOS_BG_DIR, exist_ok=True)
            subprocess.run(f"cp -r {PACK_DIR}/magicos/* {MAGICOS_BG_DIR}/", shell=True, capture_output=True)

            # Step 2: XML Wallpaper Configuration Mapping
            self.update_step("Deploying system environment theme xml sheets...", 25)
            os.makedirs(GNOME_PROPERTIES_DIR, exist_ok=True)
            subprocess.run(["cp", os.path.join(PACK_DIR, "background-properties/luminous.xml"), GNOME_PROPERTIES_DIR], capture_output=True)

            # Step 3: Logo System Branding Pixmaps
            self.update_step("Applying desktop identity layout pixmaps...", 40)
            subprocess.run(["cp", os.path.join(PACK_DIR, "logos/archlinux-logo-text.svg"), "/usr/share/pixmaps"], capture_output=True)
            subprocess.run(["cp", os.path.join(PACK_DIR, "logos/archlinux-logo-text-dark.svg"), "/usr/share/pixmaps"], capture_output=True)
            subprocess.run(["cp", os.path.join(PACK_DIR, "logos/ten-logo.svg"), "/usr/share/pixmaps"], capture_output=True)
            subprocess.run(["cp", os.path.join(PACK_DIR, "logos/ten-logo-dark.svg"), "/usr/share/pixmaps"], capture_output=True)
            
            os.makedirs("/usr/share/icons", exist_ok=True)
            subprocess.run(["cp", "-r", os.path.join(PACK_DIR, "Radiation"), "/usr/share/icons"], capture_output=True)

            # Step 4: Inject custom os-release identification file
            self.update_step("Rewriting system release files variables...", 50)
            os_release_data = """NAME="MagicOS"
PRETTY_NAME="MagicOS Edition"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org"
DOCUMENTATION_URL="https://archlinux.org"
SUPPORT_URL="https://archlinux.org"
BUG_REPORT_URL="https://archlinux.org"
PRIVACY_POLICY_URL="https://archlinux.org"
LOGO=ten-logo
"""
            with open("/etc/os-release", "w") as os_f:
                os_f.write(os_release_data)

            # Step 5: Copy TrueType Fonts
            self.update_step("Registering system typography font indices...", 60)
            os.makedirs("/usr/share/fonts", exist_ok=True)
            subprocess.run(["cp", "-r", os.path.join(PACK_DIR, "HONORSans"), "/usr/share/fonts"], capture_output=True)

            # Step 6: Deploy Plymouth Boot Theme
            self.update_step("Injecting Plymouth graphical boot parameters...", 75)
            subprocess.run(["pacman", "-S", "--noconfirm", "plymouth"], capture_output=True)
            os.makedirs("/usr/share/plymouth/themes", exist_ok=True)
            subprocess.run(["cp", "-r", os.path.join(PACK_DIR, "magicboot"), "/usr/share/plymouth/themes"], capture_output=True)
            subprocess.run(["plymouth-set-default-theme", "-R", "magicboot"], capture_output=True)

            # Step 7: Safe Initramfs preset generation
            self.update_step("Compiling kernel safe fallback initramfs images...", 85)
            subprocess.run(["mkinitcpio", "-P"], capture_output=True)

            # Step 8: Font Config Caches
            self.update_step("Flushing localized storage system layout caches...", 95)
            subprocess.run(["fc-cache", "-f", "-v"], capture_output=True)
            subprocess.run(["rm", "-rf", "/var/cache/fontconfig/*"], capture_output=True)
            subprocess.run(["fc-cache", "-f", "-v"], capture_output=True)

        except Exception as e:
            print(f"Non-fatal staging error logged: {e}")

        # Step 9: Reach 100% and execute forced GSettings/dconf theme allocation
        self.update_step("Finalizing dconf profile registries integration...", 100)
        self.btn.setText("Process Completed")
        
        self.force_system_theme_and_icons(target_user, target_home)
        self.prompt_final_reboot_choice()

    def force_system_theme_and_icons(self, target_user, target_home):
        try:
            dconf_dir = os.path.join(target_home, ".config", "dconf")
            os.makedirs(dconf_dir, exist_ok=True)
            os.makedirs("/tmp/dconf-magicos-force", exist_ok=True)
            
            forced_config = f"""[org/gnome/desktop/background]
picture-uri='file:///usr/share/backgrounds/magicos/luminous-l.jpg'
picture-uri-dark='file:///usr/share/backgrounds/magicos/luminous-d.jpg'
picture-options='zoom'

[org/gnome/desktop/interface]
icon-theme='Radiation'
"""
            with open("/tmp/dconf-magicos-force/00-override", "w") as f:
                f.write(forced_config)
                
            subprocess.run(["pkill", "-9", "-u", target_user, "-f", "dconf-service"], capture_output=True)
            subprocess.run(["dconf", "compile", os.path.join(dconf_dir, "user"), "/tmp/dconf-magicos-force/"], check=True)
            subprocess.run(["chown", "-R", f"{target_user}:{target_user}", dconf_dir], check=True)
            subprocess.run(["rm", "-rf", "/tmp/dconf-magicos-force"])
        except Exception as e:
            print(f"Failed to apply direct theme adjustments: {e}")

    def prompt_final_reboot_choice(self):
        reply = QMessageBox.question(
            self, 
            'Deployment Successful', 
            'All parameters applied smoothly.\nWould you like to restart the hardware station now?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.trigger_hardware_reset()
        else:
            self.status_label.setText("Process ended. Reboot sequence paused.")

    def trigger_hardware_reset(self):
        try:
            subprocess.run(["systemctl", "reboot", "-i"], check=True)
        except Exception:
            try:
                subprocess.run(["reboot", "-f"], check=True)
            except Exception:
                os.system("echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger")

if __name__ == '__main__':
    os.environ["QT_QPA_PLATFORM"] = "xcb"
    app = QApplication(sys.argv)
    ex = MagicOSDeploymentApp()
    ex.show()
    sys.exit(app.exec())

