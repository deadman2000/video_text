#!/bin/bash

export PATH="/opt/venv/bin:$PATH"

#pip install -U -r requirements.txt
pip install -U yt-dlp

echo "Run processor"
python3 -u ./processor.py