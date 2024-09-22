#!/bin/bash

if [ ! -d "m2m100_418M" ]; then
    mkdir m2m100_418M
    cd m2m100_418M
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/config.json
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/generation_config.json
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/sentencepiece.bpe.model
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/special_tokens_map.json
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/tokenizer_config.json
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/vocab.json
    curl -LO https://huggingface.co/facebook/m2m100_418M/resolve/main/pytorch_model.bin
    cd ../
fi

if [ ! -d "m2m100_1.2B" ]; then
    mkdir m2m100_1.2B
    cd m2m100_1.2B
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/config.json
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/generation_config.json
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/sentencepiece.bpe.model
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/special_tokens_map.json
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/tokenizer_config.json
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/vocab.json
    curl -LO https://huggingface.co/facebook/m2m100_1.2B/resolve/main/pytorch_model.bin
    cd ../
fi

