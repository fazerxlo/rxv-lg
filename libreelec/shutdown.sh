case "$1" in
  halt)
    # your commands here
    ;;
  poweroff)
    # your commands here
    ;;
  reboot)
    # your commands here
    ;;
  *)
    # your commands here
    echo "RXVLG shutting down"
    kill $(pgrep -f 'python /storage/rxvlg/rxvlg.py')
    ;;
esac
