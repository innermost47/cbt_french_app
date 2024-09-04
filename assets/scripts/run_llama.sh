#!/data/data/com.termux/files/usr/bin/sh

output=$(./main --seed -1 --threads 4 --n_predict 30 --model ./models/GGUF/model.gguf -p "$1")

echo "$output"
