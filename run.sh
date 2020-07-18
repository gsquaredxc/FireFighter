while true; do
  git pull
  sudo pip3 install -r requirements.txt --upgrade
  python3 FireFighter.py
  sleep 10
done