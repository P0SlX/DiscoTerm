#!/bin/bash
script test.log -q -c touch test
cat test.log | aha |  html2text -width 999 > output.txt