#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}ACTIVATING ENVIRONMENT...${NC}"
source ~/envs/test_deploy/bin/activate

echo -e "${GREEN}RUNNING SPIDER...${NC}"
cd ./
scrapy crawl douban_spider &> log.log