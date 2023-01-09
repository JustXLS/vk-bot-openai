until python main.py; do
    echo "Bot crashed with exit code $?.  Respawning.." >&2
    sleep 1
done