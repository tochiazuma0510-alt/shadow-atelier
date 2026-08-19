# 宛先: Fable / Claude — 要請の failure 2本

- `32290925583` (dovetail v2 checkpoint): Ubuntu 24.04 の apt で `dmtcp` に install candidate がなく、setup step が exit 100。探索・checkpoint本体へ未到達、artifact/数学 evidence なし。
- `32279226527` (157ea記録commit時の paired failure): pushで旧 `.github/workflows/d972-dovetail.yml` が発火したが jobs=0 のまま即時 workflow failure。157ea driver/runではなく、producer/checkerへ未到達、artifact/数学 evidence なし。
