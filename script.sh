#!/bin/bash
script test.log -q -c  """ echo noice """
cat test.log | aha |  html2text -width 999 > output.txt