#!/bin/bash
script test.log -q -c "ls"
cat test.log | aha |  html2text -width 999 > output.txt