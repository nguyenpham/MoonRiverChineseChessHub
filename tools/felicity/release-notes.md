Felicity endgame tablebases for xiangqi, **one attacker**: every endgame with one Rook, Cannon, Horse or Pawn on one side and any advisors and elephants on both sides, **324 endgames**, distance to mate (DTM) with the perpetual-check and perpetual-chase rules. 55,894,303 bytes.

**One side to move kept:** only the Red-to-move file of each endgame is in the set (`NAME.w.fexq`). The prober answers a Black-to-move position exactly with a one-ply search over its Red-to-move children, so the set answers every probe the full set of both sides (412 MB) answers. The piece order of each file's index was chosen per endgame for size: the set is 0.14 of the full set.

| file | what | endgames | size |
|---|---|---:|---:|
| `felicity-xq-1-0.zip` | folder `felicity-xq/1-0` | 324 | 55.9 MB |
| `SHA256SUMS.txt` | the zip and every file in it | | |

- Unpack it and point the program at `felicity-xq` (the prober searches the sub-folders). The zip is **not compressed** (stored): the files are LZMA-compressed already. No other table is needed.
- **MoonRiver:** *Tools › Download › Felicity* downloads, unpacks and adds it (Settings › Books & EGTBs) in one click.
- Format: signature 556683, LZMA, 4 KB blocks, the piece order in the header. Read by the Felicity prober of 2026-10-19 or later (the one in MoonRiver and Banksia); **older probers refuse these files**, including the one of the public `nguyenpham/FelicityEgtb`.
- Each file carries its own checksum in the header (bytes 112-127), so a file can be checked on its own.

Checked before publishing: every legal position of every file, read back through the prober, equals the source (1,374,503,436 positions, 0 different); getScore of both sides to move, and every move's score, compared with the full set: 0 mismatches; the zip unpacked with Windows' `tar`, all 324 checksums good.

Code and data are freeware / MIT.
