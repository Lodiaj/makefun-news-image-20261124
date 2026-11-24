# makefun-news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Lodiaj/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Lodiaj/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper poster summing up Tuesday 24 November 2026: the war spilling into Poland, Huang's return to Nvidia, the COP31 climate talks collapsing, Lagarde resigning from the ECB, the O'Hare ground stop, and Norway's court voiding oil licences. The poster is drawn by `gen_image.py` (Pillow, flat shapes, no network); `main.ts` validates the PNG — magic, IHDR size, and every chunk's CRC32 — and copies it to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Check it with `python3 verify.py`: it runs `main.ts` twice and proves both outputs are byte-identical to the 1024x1024 `entry.png` in this repo.

---

<sub>Entered on [make.fun](https://make.fun/?ref=v7bcp4ry&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
