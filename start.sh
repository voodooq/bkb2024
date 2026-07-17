#!/bin/bash
docker-compose -f bkb2024.yml down
docker-compose -f bkb2024.yml up -d
