while true; do
  git pull
  sudo pip3 install -r requirements.txt --upgrade
  python3 FireFighter.py
  echo "Shut down"
  sleep 10
done