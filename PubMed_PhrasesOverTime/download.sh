#!/bin/bash
for i in $(seq -f "%04g" 1 1015)
do
  wget --continue ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed20n$i.xml.gz
done
