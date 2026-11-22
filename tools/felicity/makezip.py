"""Pack the Felicity xiangqi tablebases of one attacker (1-0, White-to-move files only) into one stored zip.

usage: python -I makezip.py SRC OUTDIR
SRC is the stamped set (D:/share-phampc/xq/felicity-cut-repack/1-0 on PhamPC: the 324 NAME.w.fexq files made by
FelicityEGTBBK's tbrepack-xq from xq/felicity/1, FelicityEGTBBK docs/XqCutRepack.md). The zip holds
felicity-xq/1-0/NAME.w.fexq, so later sets of other material can unpack into the same felicity-xq folder.
Stored, not compressed: the files are LZMA blocks already (as the chess release, BanksiaChessHub
tools/felicity/makezips.py). Writes OUTDIR/felicity-xq-1-0.zip and OUTDIR/SHA256SUMS.txt (the zip, then every
file inside it).
"""
import hashlib, os, sys, zipfile

src, out = sys.argv[1:3]
ZIP = "felicity-xq-1-0.zip"
TOP, GROUP = "felicity-xq", "1-0"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


names = sorted(n for n in os.listdir(src) if n.endswith(".w.fexq"))
others = sorted(n for n in os.listdir(src) if not n.endswith(".w.fexq"))
if others:
    sys.exit("unexpected files in %s: %s" % (src, others))
os.makedirs(out, exist_ok=True)
zpath = os.path.join(out, ZIP)
sums = []
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_STORED, allowZip64=False) as z:
    for n in names:
        p = os.path.join(src, n)
        sums.append(f"{sha(p)}  {TOP}/{GROUP}/{n}")
        z.write(p, f"{TOP}/{GROUP}/{n}")
with zipfile.ZipFile(zpath) as z:
    t = z.testzip()
    cnt = len(z.namelist())
print(ZIP, cnt, "files", os.path.getsize(zpath), "bytes, testzip:", t or "ok")
with open(os.path.join(out, "SHA256SUMS.txt"), "w", newline="\n") as f:
    f.write("\n".join([f"{sha(zpath)}  {ZIP}"] + sums) + "\n")
