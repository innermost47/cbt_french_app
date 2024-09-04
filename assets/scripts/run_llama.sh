#!/data/data/com.termux/files/usr/bin/sh

output=$(./main --seed -1 --threads 4 --n_predict 30 --model ./models/7B/stablebeluga-7b.Q4_K_M.gguf -p "$1")

echo "$output"
