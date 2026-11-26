# THE WORLD IN NUMBERS — 25 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b134-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![make.fun reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b134-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper front page summing up Wednesday 25 November 2026 in numbers: **50 stories, 13 illustration panels, one 1024x1024 image**. Every story on the page happened on 25 November 2026 — the DATE CHECK box on the page says so, and lists the four near-miss items that were left out because they happened on 23–24 November.

## The front page

- **Hero trio:** US tariffs cut on 214 goods · Kospi plunges 6.16% · Shenzhou-21 docks with Tiangong station. Each hero carries a WHY IT MATTERS line and a big red number badge in its scene.
- **47 more numbered stories** (04–50) from Bogor to Cape Canaveral, each with its big number on a chip, a place tag, and a `C · R · CL · ALSO:` line.
- **Bogor card (04):** landslide kills 9, traps 17 as rain hits the Java hills.
- **World map** with pins marking the big numbers, and a sources footer (Reuters, AP, AFP, Bloomberg, Antara, Yonhap, Xinhua, dpa).

## DATE CHECK

Every story on the page is dated Wednesday 25 November 2026. Left out on purpose, because they are not 25 November stories: Huawei verdict 24 Nov · PIF Tower strike 24 Nov · Sudan strikes 24 Nov · Nvidia CEO reinstated 23 Nov. The Hamas security chief in card 05 is Col. Mohammad Abuelouf, 47, killed in Shati with his wife and 2 children — a 25 November story, not the 24 November item of a different name.

## Files

- `entry.png` — the finished front page, 1024x1024, under 1 MiB.
- `gen.py` — build-time renderer (PIL). Run `python3 gen.py` to redraw `entry.png`.
- `main.py` — the graded entry point. **Standard library only** (os, shutil, hashlib, struct, sys): it verifies `entry.png` (PNG, 1024x1024, ≤ 1 MiB, SHA-256) and copies it to `MAKEFUN_OUTPUT_DIR` (default `out`). It never imports PIL.
- `LICENSE` — MIT.

## Run it

```sh
python3 gen.py            # redraw entry.png (needs Pillow, build time only)
python3 main.py           # copy entry.png to ./out
MAKEFUN_OUTPUT_DIR=/tmp/o python3 main.py   # copy elsewhere
```

## Verify it (grader style)

```sh
python3 -m venv /tmp/stdlib-venv
/tmp/stdlib-venv/bin/python main.py   # no Pillow in the venv: exit 0, SHA-256 matches
```
