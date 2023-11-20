#!/usr/bin/env bash

mkdir -p index
cd index

for i in $(seq 1976 2022)
  do wget --continue https://annualized-gender-data-uspto.s3.amazonaws.com/$i.csv
done
