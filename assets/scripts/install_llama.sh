#!/data/data/com.termux/files/usr/bin/sh

pkg update && pkg upgrade -y
pkg install git cmake make clang wget -y

git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

make

mkdir -p models/GGUF

wget -o model.gguf https://huggingface.co/innermost47/cbt-french-model/resolve/main/unsloth.Q4_K_M.gguf?download=true -P models/GGUF/

chmod +x ./main
