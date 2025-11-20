#!/bin/bash

for i in {1..100}; do
    bsub -q l "basf2 isr_gen_bsub.py -n 1000 -o \"../../root_file/isr/channel_std/testaccio/testaccio_${i}.root\""
done