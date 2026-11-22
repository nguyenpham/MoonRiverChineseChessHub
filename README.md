# MoonRiver Chinese Chess Hub

Free data for **xiangqi (Chinese chess)**: game databases and opening books for
MoonRiver, Banksia, OOBS, OCGDB and any program that reads them.
Everything is published as **GitHub releases** of this repository (see the *Releases* page); the
repository itself holds only this description.

| release (tag) | file | what | size | download (`.7z`) |
|---|---|---|---:|---:|
| `moonrivermasters-db` | `moonrivermasters.ocgdb.db3` | game database, OCGDB (SQLite) | 31.3 MB | 14.8 MB |
| `moonrivermasters-mrbk` | `moonrivermasters.mrbk` | opening book, MoonRiver `.mrbk` | 880 KB | 415 KB |
| `moonrivermasters-obs` | `moonrivermasters.obs.db3` | opening book, OOBS (SQLite, with win/draw/loss) | 9.8 MB | 1.1 MB |

All files are compressed with 7-Zip (LZMA2). Unpack them with 7-Zip, `7z x <file>.7z`, or the
Windows 11 Explorer.

---

## 1. MoonRiver Masters database: `moonrivermasters.ocgdb.db3`

**135,030 xiangqi games between human players**, 1905–2026, duplicates removed.

### 1.1 Which games

- **Rated online games** (the games that carry Elo ratings): kept when **both players are rated
  2500 or more** — 2,496 games.
- **All other games** (over-the-board championships, leagues, opens, team events…): kept when
  **both players are humans**. Games of engines (computer tournaments, engine matches, test runs),
  players named after a program, placeholder names (empty, `NA`, `Red`, `Black`…) and opening
  lines stored as games (a "player" named after an opening) are left out. A player shown only by
  his team or region (`SiChuan`, `ZheJiang`) is kept: those are league games whose player name was
  lost.

### 1.2 Contents

| | count |
|---|---:|
| games | 135,030 |
| players | 16,272 |
| events / sites | 3,402 / 90 |
| comments | 1,051 |
| average length | 81.6 plies |
| games of ≥ 40 plies | 127,554 |
| results: red wins / draws / black wins / none | 50,876 / 46,125 / 38,017 / 12 |
| games from a set-up position (`FEN`) | 57 |

Player names are as the games wrote them: Chinese characters, pinyin (often with the province or
club first, `GuangDong Xu YinChuan`), nicknames of online players. The same player may appear
under several spellings.

### 1.3 Using it

It is a normal OCGDB file (SQLite): MoonRiver opens it in its database viewer, `ocgdb` and `oobs`
read it, and any SQLite tool can query it (tables `Games`, `Players`, `Events`, `Sites`,
`Comments`, `Info`; `Info.Variant` = `xiangqi`). Moves are stored in `Games.Moves2`, encoded; to get
the games as PGN, export them from MoonRiver's database viewer.

```bash
sqlite3 moonrivermasters.ocgdb.db3 "SELECT p.Name, count(*) n FROM Games g JOIN Players p
  ON p.ID IN (g.WhiteID, g.BlackID) GROUP BY p.ID ORDER BY n DESC LIMIT 10"
```

SHA-256 `e3cd923efff1a4fd6fe92d1076cb8e713077465c43200d740ed87b88b331f512`.

---

## 2. MoonRiver Masters opening books

Two books from the database above, made the same way, only the format differs.

### 2.1 How they were made

With **OOBS 4** (https://github.com/nguyenpham/oobs, the xiangqi binary `oobs-xq`), from the games
of the database exported to PGN:

```
oobs-xq -create -in moonrivermasters.pgn -out moonrivermasters.mrbk    -plytake 15 -plycount 40 -hit 3
oobs-xq -create -in moonrivermasters.pgn -out moonrivermasters.obs.db3 -plytake 15 -plycount 40 -hit 3
```

| option | meaning |
|---|---|
| `-plycount 40` | only games of **40 plies or more** |
| `-plytake 15` | each game is read for its **first 15 plies** (lines can reach the position after ply 15) |
| `-hit 3` | a move is kept only if it was played in **at least 3 games** from that position |
| (default) | games without a result, and games from a set-up position, are skipped |

127,551 games passed the filters. OOBS is deterministic: the same games and options give the same
books, byte for byte.

### 2.2 `moonrivermasters.mrbk` — MoonRiver book

The book format of MoonRiver, Banksia and Banksia GUI (xiangqi): a 128-byte header (with the
description), then 16-byte records sorted by key (64-bit key, move, 32-bit weight).

- 55,015 entries.
- Weight of a move = 2 × wins + draws for the side that plays it (OOBS default
  `win=2,draw=1,loss=0`), not scaled. A move with weight 0 (only losses) is not written, which is
  why it has fewer entries than the OOBS book.
- SHA-256 `b207d7a561d78e5c885909ba1d0cc7639e6ef5502fe299586c7a4c27dd8d03ae`.

### 2.3 `moonrivermasters.obs.db3` — OOBS book

An SQLite database that keeps the full statistics, so other books can be made from it later.

- Table `Book(ID, EPD, Move, Active, Win, Draw, Loss, Comment)`, index on `EPD`; `Win/Draw/Loss`
  are for the side that plays the move. Table `Info` holds the description, `Variant` = xiangqi,
  `ItemCount`.
- 56,581 rows (moves) in 38,174 positions; every row has at least 3 games.
- SHA-256 `715adf3ba19ceccd546fde01044ae664598a379a7ca38650a011930b456f6c0e`.

The first moves of red, from the book:

| move | games | red wins | draws | black wins |
|---|---:|---:|---:|---:|
| h2e2 (central cannon, 炮二平五) | 61,752 | 22,663 | 19,346 | 19,743 |
| c3c4 (pawn opening, 兵七进一) | 27,036 | 11,677 | 9,181 | 6,178 |
| g0e2 (elephant opening, 相三进五) | 14,864 | 5,057 | 6,327 | 3,480 |
| b0c2 (horse opening, 马八进七) | 5,473 | 1,967 | 2,010 | 1,496 |
| h2d2 (cannon to the palace corner, 炮二平六) | 4,478 | 1,721 | 1,508 | 1,249 |
| g3g4 (pawn opening, 兵三进一) | 4,239 | 1,835 | 1,158 | 1,246 |

### 2.4 Using them

In MoonRiver or Banksia GUI, add the file as an opening book. From the command line:

```bash
# look the start position up in both books
oobs-xq -in moonrivermasters.obs.db3 -in moonrivermasters.mrbk \
        -fen "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1" -o printall

# plain SQL on the OOBS book
sqlite3 moonrivermasters.obs.db3 "SELECT Move, Win, Draw, Loss FROM Book
  WHERE EPD = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - -' ORDER BY 2*Win+Draw DESC"

# make other books from the OOBS one (same depth: 15 plies)
oobs-xq -export -in moonrivermasters.obs.db3 -out mm-hit10.mrbk -hit 10
oobs-xq -export -in moonrivermasters.obs.db3 -out mm-start.epd -plytake 12 -plydelta 0 -hit 100
```

### 2.5 Limits

- The books end after ply 16 (`-plytake 15` + 1): from a later position they have no moves.
- `-hit 3` counts games per move, so a rare but sound move with only 1–2 games is missing.
- Players are told apart by name only; an engine game recorded under human names could not be
  recognised.

---

## 3. SHA-256 of the downloads

| file | SHA-256 |
|---|---|
| `moonrivermasters.ocgdb.db3.7z` | `38c39bcec6c553eca4cade5a6f4445c54e1d244263815f780c8c50c7fbaa138d` |
| `moonrivermasters.mrbk.7z` | `9c35e4fb585fcf0dd24957f3a25211db4c15355912a40a6c85958939fccb5302` |
| `moonrivermasters.obs.db3.7z` | `f0d892d6f2a20f734961dfe92c62e7c8563e053fc21925b93451bee2ca7b3206` |

## 4. Licence

The data is free to use. The repository is under the MIT licence ([LICENSE](LICENSE)).
