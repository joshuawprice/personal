#!/usr/bin/env sh

# Mostly just copied from papermc's start script generator.
# https://docs.papermc.io/misc/tools/start-script-gen/

exec java -Xms64M -Xmx256M -XX:+AlwaysPreTouch -XX:+ParallelRefProcEnabled -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=4M -XX:MaxInlineLevel=15 -jar velocity.jar
