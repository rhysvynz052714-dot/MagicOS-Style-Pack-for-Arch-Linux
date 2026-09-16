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
    echo "Uninstalling and may break & damage & invalid sectors?"
    read -p "Do you want to continue? (y/n): " -n 1 -r choice
    echo "" # Moves to a new line

    case "$choice" in
        [Yy]* ) 
            echo "Uninstalling"
            
         
                rm -rf /usr/share/backgrounds/magicos 
                rm -rf /usr/share/pixmaps/archlinux-logo-text.svg /usr/share/pixmaps/archlinux-logo-text-dark.svg /usr/share/pixmaps/ten-logo.svg /usr/share/pixmaps/ten-logo-dark.svg
                sudo tee /etc/os-release << 'EOF'
NAME="Unknown"
PRETTY_NAME="Unknown OS"
ID=arch
BUILD_ID=rolling
ANSI_COLOR="38;2;23;147;209"
HOME_URL="https://archlinux.org/"
DOCUMENTATION_URL="https://wiki.archlinux.org/"
SUPPORT_URL="https://bbs.archlinux.org/"
BUG_REPORT_URL="https://archlinux.org"
PRIVACY_POLICY_URL="https://archlinux.org"
EOF
                rm -rf /usr/share/gnome-background-properties/luminous.xml 
                
            rm -rf /usr/share/icons/Radiation

            rm -rf /usr/share/fonts/HONORSans
	    rm -rf /usr/share/plymouth/themes/magicboot 
            echo "Mkinitcpio first"
	    sudo mkinitcpio -P
	    echo "Generaring initramfs it will won't boot or fail"
	    sudo mkinitcpio -p linux
	    fc-cache -f -v	    sudo rm -rf /var/cache/fontconfig/*
	    sudo fc-cache -f -v
	    

	    sleep 3
	    clear
	    echo uninstallation successfully
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
