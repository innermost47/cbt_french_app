#!/data/data/com.termux/files/usr/bin/sh

pkg update && pkg upgrade -y
pkg install git cmake make clang wget -y

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

make

mkdir -p models/7B

wget https://huggingface.co/TheBloke/StableBeluga-7B-GGUF/resolve/main/stablebeluga-7b.Q4_K_M.gguf -P models/7B/

chmod +x ./main
