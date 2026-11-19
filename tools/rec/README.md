# Velké nahrávky ze hry (víc než ~100 MB) – jak je dostat do cloudu

1. Na PC nahrávku binárně rozdělit (Claude Code): kousky po 50 331 648 B do
   `VOID_SURVIVORS_v0_6_3D_UNIVERSE\nahravky_casti\<název>.partNNN`.
2. V cloudu stáhnout (device_stage_files) **jeden kousek na jedno volání** – nejdřív první a poslední dva (ftyp + moov).
3. `assemble_parts.py` zapíše stažené kousky do řídké (sparse) kopie v plné velikosti.
4. `ffprobe -show_entries packet=pts_time,size,pos,flags` → `vpk.csv`; `keyframes_from_stss.py` přečte všechny keyframy z moov.
5. `keyframe_sheet.py` / `dense_sheet.py` = náhledové listy z kousků, které už jsou stažené; `check_shots.py spec.json` ověří, že má každý záběr svoje kousky.
Cesty ve skriptech jsou pro REC D (`/root/build/rec1118`); pro další nahrávku je stačí přepsat.
