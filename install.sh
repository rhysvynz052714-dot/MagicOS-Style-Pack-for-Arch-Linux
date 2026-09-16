#!/bin/bash

pkill -u "$USER" -f dconf-service 2>/dev/null

# 2. Re-initialize DBUS connection variables aggressively
export $(dbus-launch)
export DBUS_SESSION_BUS_ADDRESS
export DBUS_SESSION_BUS_PID
# Define the file you want to check
FILE="/usr/share/backgrounds"
FILEPROPERTIESDOSBACKGROUNDS="/usr/share/gnome-background-properties"

while true; do
    clear
    echo "======================="
    echo "  MAGICOS PACK SETUP   "
    echo "======================="
    sleep 2
    echo "Installing and may break"
    read -p "Do you want to continue? (y/n): " -n 1 -r choice
    echo "" # Moves to a new line

    case "$choice" in
        [Yy]* ) 
            echo "Installing"
            
            # --- IF/ELSE FILE CHECK INSIDE YES ---
            if [ -f "$FILE" ]; then
               cp -r magicos /usr/share/backgrounds               
            else
                echo "missing backgrounds creating new file..."
                mkdir /usr/share/backgrounds
                cp -r magicos /usr/share/backgrounds 

                # Add your actions for when the file is missing here
            fi
            # -------------------------------------
	    # --- IF/ELSE FILE CHECK INSIDE YES ---
            if [ -f "$FILEPROPERTIESDOSBACKGROUNDS" ]; then
               cp background-properties/luminous.xml/ /usr/share/gnome-background-properties
            else
                echo "missing backgrounds creating new file..."
                mkdir /usr/share/gnome-background-properties
                cp background-properties/luminous.xml /usr/share/gnome-background-properties

                # Add your actions for when the file is missing here
            fi
            # -------------------------------------
	    cp logos/archlinux-logo-text.svg logos/archlinux-logo-text-dark.svg /usr/share/pixmaps
            cp logos/ten-logo.svg logos/ten-logo-dark.svg /usr/share/pixmaps
            cp -r Radiation /usr/share/icons
sudo tee /etc/os-release << 'EOF'
NAME="MagicOS"
PRETTY_NAME="MagicOS Edition"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://archlinux.org"
PRIVACY_POLICY_URL="https://archlinux.org"
LOGO=ten-logo
EOF
            cp -r HONORSans /usr/share/fonts
	    sudo pacman -S plymouth
	    sudo cp -r magicboot /usr/share/plymouth/themes
	    sudo plymouth-set-default-theme -R magicboot
            echo "Mkinitcpio first"
	    sudo mkinitcpio -P
	    echo "Generaring initramfs it will won't boot or fail"
	    sudo mkinitcpio -p linux
	    fc-cache -f -v	    sudo rm -rf /var/cache/fontconfig/*
	    sudo fc-cache -f -v
	    
echo "Setting wallpaper..."
gsettings set org.gnome.desktop.background picture-uri "file:///usr/share/backgrounds/magicos/luminous-l.jpg"
gsettings set org.gnome.desktop.background picture-uri-dark "file:///usr/share/backgrounds/magicos/luminous-d.jpg"

# (Optional) Adjust how the background image is rendered (e.g., 'zoom', 'scaled', 'centered')
gsettings set org.gnome.desktop.background picture-options "zoom"

# 3. Set the Icon Theme
echo "Setting icon theme to ${ICON_THEME_NAME}..."
gsettings set org.gnome.desktop.interface icon-theme "Radiation"

# 6. Clean up the spawned DBus process safely
if [ -n "$DBUS_SESSION_BUS_PID" ]; then
    kill "$DBUS_SESSION_BUS_PID" 2>/dev/null
fi

echo "Theme customization complete!"

	    sleep 3
	    clear
	    echo installation successfully
# --- INNER SYSTEM REBOOT PROMPT ---
                read -p "Would you like to reboot the entire system now? (y/n): " -n 1 -r system_choice
                echo ""

                case "$system_choice" in
                    [Yy]* )
                        echo "WARNING: System is rebooting NOW..."
                        reboot # Executes immediate hardware restart
                        ;;
                    [Nn]* )
                        echo "Reboot later"
                        exit 0 # Loops back to the primary file check question
                        ;;
                    * )
                        echo "Invalid input."
                        exit 0
                        ;;
                esac
	    
            break
            ;;
        [Nn]* ) 
            echo "Abort."
            exit 0
            ;;
        * ) 
            echo "Abort."
	    exit 0
            ;;
    esac
done
