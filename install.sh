#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

type -P python3 >/dev/null 2>&1 && echo Python 3 is installed
echo -e "${GREEN}DOWNLOADING PROJECT FROM GIT...${NC}"
git clone https://github.com/k4iw3i/douban_spider.git

echo -e "${GREEN}DOWNLOADING PIP TOOL...${NC}"
curl https://bootstrap.pypa.io/get-pip.py | python

echo -e "${GREEN}INSTALLING PACKAGES...${NC}"
pip install scrapy
pip install pandas
pip install bs4
pip install fuckit
pip install requests