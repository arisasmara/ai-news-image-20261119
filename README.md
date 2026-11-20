# One image of 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/arisasmara/ai-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/arisasmara/ai-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for the make.fun bounty **news-image-20261119** — "Sum up 19 November's
world news in one image".

## The image

`entry.png` is a single 1024 x 1024 editorial poster. Deep indigo/purple
background, warm amber accents, white bold labels. A banner across the top
names the day in large letters: **19 NOVEMBER 2026**. Below it, one wide
hero panel and a 2 x 3 grid of six panels sum up the day's news.

The seven stories, all events of Thursday 19 November 2026, verified against
Reuters, BBC, CNN, Al Jazeera and other outlets on the day:

1. **TRUMP · XI · PUTIN MEET** — First trilateral, 4-point pact, no Ukraine
   deal. The three leaders met for about 90 minutes at Kylin Villa,
   Shenzhen, and issued a four-point joint declaration (UN reform, more
   refined-oil supply, ICC jurisdiction limits, dialogue on reducing
   nuclear risks). No breakthrough on Ukraine, Iran or nuclear arms.
2. **BRIDGE HIT AGAIN** — 3rd attack in 3 days, rail halted. The Crimean
   Bridge was attacked again; traffic was closed and damage assessed,
   the third attack in three days after the 17 November strike collapsed
   the road arch.
3. **BIGGEST IPO EVER** — Anthropic debuts on Nasdaq. Claude-maker
   Anthropic raised $81.3bn in the biggest IPO of all time; shares began
   trading on Nasdaq as ANT on 19 November, valuing the company at more
   than $1.4tn.
4. **MISSILE HITS RIYADH TOWER** — Houthis claim strike, PIF tower hit.
   A missile hit the PIF Tower (80 storeys, 385 m) in Riyadh's King
   Abdullah Financial District; the Houthis claimed the strike
   themselves. Windows blown out across 7–8 floors, no injuries.
5. **BANGLADESH BURNS** — Lockdown violence, Yunus home torched. A
   banned party's nationwide lockdown turned violent: ruling-party
   members killed, Muhammad Yunus's ancestral home in Chattogram set
   ablaze, Grameen Bank branches torched, border guards deployed.
6. **ISRAEL PUSHES PAST LINE** — Rare ground move in Gaza. Israeli tanks
   advanced across the Gaza ceasefire line in a rare ground incursion
   beyond the Yellow Line.
7. **MYANMAR GUILTY OF GENOCIDE** — ICJ rules 9–6, historic first. The
   International Court of Justice found Myanmar responsible for genocide
   against the Rohingya, the first time in the court's 80-year history
   it has held a state accountable for genocide. Final and binding.

The picture is a flat, stylised illustration — no photographs, no
photorealistic faces, no company logos. It was drawn by `draw_image.py`
in this repository (Pillow), from the verified story list above.

## The program

`main.py` (Python 3.13, standard library only) does one thing: it copies
the `entry.png` shipped in this repository, byte for byte, to the output
directory as `entry.png`. It uses no network, no clock and no randomness,
so both runs write identical bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The image lands at `out/entry.png`.

To re-render the poster from scratch:

```sh
python3 draw_image.py
```

## License

MIT — see `LICENSE`.
