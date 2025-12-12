#!/bin/bash

paths=(
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06417/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06418/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06419/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06421/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06422/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06423/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06424/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06425/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06426/uubar/mdst
/belle/MC/release-08-00-08/DB00003307/MC16rd_proc16/prod00045483/s00/e0012/4S/r06427/uubar/mdst
)

for p in "${paths[@]}"; do
    echo "Running for: $p"
    gbasf2 \
        -p nbar_cocktail_12122025 \
        -s release-08-01-05 \
        -i "$p" \
        ~zanusso/work_nbar/m_macro/grid/grid_head.py
done