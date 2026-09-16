import sys
import os
import subprocess
import pwd
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt

class MagicOSUninstallerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("MagicOS System Uninstaller")
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
                background-color: #d9534f;
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
        
        # 1. Action Button (Styled with Warning Accent Red)
        self.btn = QPushButton("Remove MagicOS Customizations", self)
        self.btn.setStyleSheet("""
            QPushButton {
                font-size: 14px; 
                font-weight: bold; 
                padding: 14px; 
                background-color: #d9534f; 
                color: white; 
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e5635e;
            }
            QPushButton:disabled {
                background-color: #27272A;
                color: #71717A;
                border: 1px solid #3F3F46;
            }
        """)
        self.btn.clicked.connect(self.start_ui_uninstallation)
        layout.addWidget(self.btn)
        
        # 2. Live Task Status Label
        self.status_label = QLabel("Uninstaller initialization ready.", self)
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

    def start_ui_uninstallation(self):
        self.btn.setEnabled(False)
        self.btn.setText("Purging Customizations...")

        try:
            # Dynamic user identification strings
            target_user = os.environ.get("SUDO_USER", os.environ.get("USER"))
            if not target_user or target_user == "root":
                try:
                    target_user = subprocess.check_output("who | awk '{print $1}' | head -n1", shell=True).decode().strip()
                except Exception:
                    target_user = os.getlogin()

            target_home = pwd.getpwnam(target_user).pw_dir

            # Step 1: Remove Background Graphics Assets Folder
            self.update_step("Removing background layouts directories...", 15)
            subprocess.run(["rm", "-rf", "/usr/share/backgrounds/magicos"], capture_output=True)

            # Step 2: Remove Custom Pixmap Branding Logos
            self.update_step("Cleaning up branding identity layout pixmaps...", 30)
            subprocess.run([
                "rm", "-rf", 
                "/usr/share/pixmaps/archlinux-logo-text.svg", 
                "/usr/share/pixmaps/archlinux-logo-text-dark.svg", 
                "/usr/share/pixmaps/ten-logo.svg", 
                "/usr/share/pixmaps/ten-logo-dark.svg"
            ], capture_output=True)

            # Step 3: Inject custom Generic/Unknown OS Release Identification
            self.update_step("Reverting /etc/os-release core properties...", 45)
            os_release_data = """NAME="Unknown"
PRETTY_NAME="Unknown OS"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://archlinux.org"
PRIVACY_POLICY_URL="https://archlinux.org"
"""
            with open("/etc/os-release", "w") as os_f:
                os_f.write(os_release_data)

            # Step 4: Remove XML Background Property Configuration References
            self.update_step("Purging environment theme XML descriptors...", 55)
            subprocess.run(["rm", "-rf", "/usr/share/gnome-background-properties/luminous.xml"], capture_output=True)

            # Step 5: Remove Custom Environment System Icon Frameworks
            self.update_step("Wiping desktop icon pack paths...", 65)
            subprocess.run(["rm", "-rf", "/usr/share/icons/Radiation"], capture_output=True)

            # Step 6: Remove Typography Font Subdirectories
            self.update_step("Cleaning up system-wide typography directories...", 75)
            subprocess.run(["rm", "-rf", "/usr/share/fonts/HONORSans"], capture_output=True)

            # Step 7: Purge Plymouth Boot Themes
            self.update_step("Uninstalling boot animation resources...", 80)
            subprocess.run(["rm", "-rf", "/usr/share/plymouth/themes/magicboot"], capture_output=True)

            # Step 8: Safe Initramfs presets image compilation
            self.update_step("Compiling kernel safe fallback initramfs images...", 90)
            subprocess.run(["mkinitcpio", "-P"], capture_output=True)

            # Step 9: Flush and update local system font configuration cache blocks
            self.update_step("Flushing system layout font cache indexes...", 95)
            subprocess.run(["fc-cache", "-f", "-v"], capture_output=True)
            subprocess.run(["rm", "-rf", "/var/cache/fontconfig/*"], capture_output=True)
            subprocess.run(["fc-cache", "-f", "-v"], capture_output=True)

        except Exception as e:
            print(f"Non-fatal uninstallation trace caught: {e}")

        # Step 10: Finalizing registry drops
        self.update_step("Reverting desktop configuration registries...", 100)
        self.btn.setText("Purge Completed")
        
        self.revert_system_theme_and_icons(target_user, target_home)
        self.prompt_final_reboot_choice()

    def revert_system_theme_and_icons(self, target_user, target_home):
        """Forces default desktop environment values back into the user binary dconf database"""
        try:
            dconf_dir = os.path.join(target_home, ".config", "dconf")
            if os.path.exists(dconf_dir):
                os.makedirs("/tmp/dconf-uninstall-force", exist_ok=True)
                
                default_config = f"""[org/gnome/desktop/background]
picture-uri='file:///usr/share/backgrounds/gnome/adwaita-l.jpg'
picture-uri-dark='file:///usr/share/backgrounds/gnome/adwaita-d.jpg'
picture-options='zoom'

[org/gnome/desktop/interface]
icon-theme='Adwaita'
"""
                with open("/tmp/dconf-uninstall-force/00-default", "w") as f:
                    f.write(default_config)
                    
                subprocess.run(["pkill", "-9", "-u", target_user, "-f", "dconf-service"], capture_output=True)
                subprocess.run(["dconf", "compile", os.path.join(dconf_dir, "user"), "/tmp/dconf-uninstall-force/"], check=True)
                subprocess.run(["chown", "-R", f"{target_user}:{target_user}", dconf_dir], check=True)
                subprocess.run(["rm", "-rf", "/tmp/dconf-uninstall-force"])
        except Exception as e:
            print(f"Failed to reset user theme choices: {e}")

    def prompt_final_reboot_choice(self):
        reply = QMessageBox.question(
            self, 
            'System Restored', 
            'MagicOS profile has been removed successfully.\nWould you like to restart the machine now to finalize adjustments?',
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
    ex = MagicOSUninstallerApp()
    ex.show()
    sys.exit(app.exec())
