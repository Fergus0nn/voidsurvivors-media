# VOID SURVIVORS – social media learnings

Brand: Metricool brand id 7905334 (TikTok, Instagram, YouTube = void.survivors / VOID SURVIVORS). Timezone Europe/Prague.

## Rules from Daniel (must always hold)
- VISUAL STYLE (from 2026-11-09, replaces stickman): real gameplay from Daniel's recordings in the middle (landscape, full HUD), blurred copy of the same footage above/below, big captions on top, narrator KAI (2D cartoon young space explorer/dev, black high-collar jacket, purple glow, silver hair streak) pops up bottom-left and talks in a typed speech bubble; end card = logo + Kai + one CTA that does NOT lead to playing/downloading (follow / weekly Friday update / comment).
- FOOTAGE VARIETY: pick shots from stats/footage_catalog.md, never reuse the same shots; log used ranges there.
- SOUND + AUTO-POSTING (Daniel, 2026-11-13, replaces the old "no music / autoPublish=false" rule): NEVER use the audio of a recording – Daniel plays Spotify while recording (REC C for sure). Every reel's soundtrack is built only from game files: music bed from assets/audio/music (hra_boj = battle, boss = boss fights, hra = calm, menu = menu) + clean SFX from assets/audio/sfx at key moments (boss arrival, kills, explosions, end card) + a light hit/death layer during action shots; final ≈ -14 LUFS, video stream copied untouched. Tool: tools/reel/clean_audio.py (plan JSON). ALL posts (TikTok, Instagram, YouTube) are scheduled with autoPublish=true – Daniel no longer adds sounds by hand.
- Old stickman EP1–EP3 already published (keep as is).
- Never mention AI. Never say everything is free.
- NO STEAM PAGE YET (Daniel, 2026-11-12): never write "Coming soon to Steam" / "Wishlist" anywhere (end cards, captions) until Daniel says the page is live. Never show the in-game END OF DEMO / "Add to wishlist" screen.
- Captions (from 2026-11-13): TT/IG = hook line + comment question + 5 tags (#voidsurvivors + genre + #fyp); YouTube = no viral tags, only #shorts #voidsurvivors #indiegame #survivorslike.
- English texts, ~30 s, 9:16, music/SFX only from the game.
- 1 post per day at the best hour (default 18:00; 10:00 is the other peak).

## Schedule
| Date | Episode | File |
|---|---|---|
| 2026-11-06 19:00 | EP 1 How my game was born | v/ep01.mp4 |
| 2026-11-07 10:00 | EP 2 The First Heroes | v/ep02.mp4 |
| 2026-11-08 18:00 | EP 3 Sound & Motion | v/ep03.mp4 |
| 2026-11-09 12:00 | REEL Combo 20,000× (Kai) | v/reel01_combo.mp4 |
| 2026-11-09 18:00 | EP 4 Upgrade Trees & Robots (new style) | v/ep04b.mp4 |
| 2026-11-10 18:00 | EP 5 Extreme Effects (new style) | v/ep05b.mp4 |
| 2026-11-11 18:00 | EP 6 A Bigger Universe | v/ep06.mp4 |
| 2026-11-12 18:00 | EP 7 The Mothership | v/ep07.mp4 |
| 2026-11-13 18:00 | REEL Can you survive 20 minutes? (clean sound: hra_boj + game SFX, auto-post) | v/reel02_survive_clean.mp4 |
| 2026-11-14 18:00 | REEL 3 Bosses. 1 Run. (Kai, hook = bold number claim, CTA = comment; clean sound: boss + game SFX, auto-post) | v/reel03_three_bosses_clean.mp4 |
| planned (NOT scheduled yet – needed from 2026-11-15) | EP 8 … EP 14 | – |

## Learnings (updated daily)
### 2026-11-06
- Sample size: 1 post (EP 1, 19:00 Fri), live ~2.7 h; Metricool has not synced post stats yet → **no performance conclusions possible yet**.
- Best-time-to-post (Metricool audience data, Sat 7 + Sun 8 Nov):
  - TikTok: peak 10:00 (Sat 852 / Sun 816) vs 18:00 (709 / 677).
  - Instagram: peak 10:00 (Sat 3409 / Sun 2582) vs 18:00 (2393 / 2253).
  - YouTube: peak 16:00 (Sat 5880 / Sun 5648); 10:00 Sat 5392 > 18:00 4747, Sun 10:00 4402 < 18:00 5189.
  - → Saturday: 10:00 beats 18:00 on all 3 networks → EP 2 moved to 10:00. Sunday is mixed (YT prefers afternoon) → EP 3 kept at 18:00. This gives a first 10:00 vs 18:00 comparison.
- To test next: hook style (EP 2/3 open with a funny confession – "white spaghetti", "roller skates" – vs EP 1's origin story).

### 2026-11-07
- Sample size: 2 posts per network (EP 1 Fri 19:00, EP 2 Sat 10:00); posts have different ages (26.5 h vs 11.6 h) → all comparisons are weak/preliminary.
- TikTok: EP 1 733 views vs EP 2 119. Even adjusting for age, EP 2 is clearly behind (~10 views/h vs ~28 views/h). Confounders: EP 1 = first post of the series (new-account push), EP 2 posted at 10:00. So the **10:00 slot has NOT proven better** than 18/19:00 yet; the audience-based best-time data alone is not enough.
- TikTok retention is the main weakness: avg watch 5.5 s (EP 1) and 3.4 s (EP 2) of 30 s → most viewers swipe in the first ~3–5 s. Hook in the first 2 s (visual + text) is the biggest lever for EP 6+ (e.g. start with the most spectacular gameplay moment, then the stickman).
- Instagram: views flat (127 vs 115, reach 108 both) – IG distribution seems capped by 0 followers; EP 2 kept viewers longer (6.1 s vs 3.7 s) → the "funny confession" hook ("white spaghetti") may hold IG viewers better; TikTok said the opposite → no conclusion yet.
- ~97–99 % of TikTok views come from For You; hashtags/profile contribute ~0 → hashtags are not a growth lever right now, keep them short.
- Engagement is very low (TikTok EP 1: 10 likes / 733 = 1.4 %; EP 2 0.8 %). No comments/shares → captions could end with a concrete question to invite comments (EP 2 and EP 4 already do; compare EP 3/5 vs EP 4).
- YouTube: Metricool has not synced any per-video stats yet (normal ~48 h delay) → no YT conclusions.
- Best-time (Sun 8 – Tue 10): TikTok Mon/Tue 18:00 is the peak (1096 / 1119, ≥ 10:00); IG prefers 10:00 on Mon (5528 vs 4206), roughly equal on Tue; YT peaks 16:00. Sunday: 10:00 slightly ahead on TT/IG, 18:00 ahead on YT. Given the real-data result above (10:00 post underperformed), **kept EP 3–5 at 18:00**.
- Followers: 0 change on all networks after 2 posts.

### 2026-11-08
- Sample size: TikTok 3 posts (EP 1–3), Instagram 2 (EP 3 not synced), YouTube 0 with data (per-video stats still null after ~50 h). Still preliminary.
- TikTok views are not decided in the first hours: EP 2 went 119 → 447 (+328) between hour 12 and 36, EP 1 only +81 in the same period → TikTok tests a video slowly; judge a post after ≥ 48 h, not on day 1.
- TikTok early velocity: EP 3 (Sun 18:05) 188 views in 3.6 h ≈ 52 views/h vs EP 2 (Sat 10:04) ≈ 10 views/h over its first 11.6 h → 18:00 slot again starts faster than 10:00 (n = 1 per slot, weekday differs). Supports keeping 18:00.
- TikTok avg watch keeps falling: EP 1 5.7 s → EP 2 4.1 s → EP 3 3.2 s (of 30 s). Hook in first 2 s remains the #1 problem; the series format (stickman at desk first) does not stop the scroll. For EP 6+: open on the most spectacular gameplay frame + big text, stickman later.
- Instagram: EP 2 ("white spaghetti" confession hook) beats EP 1 on every quality metric – reel view rate 45.8 % vs 32.0 %, avg watch 5.6 s vs 4.2 s, reach 130 vs 113, first share. n = 2, but consistent with 11-07 → on IG the funny-confession hook looks better than the origin-story hook.
- Followers: first gains – IG +1, YouTube +2 (no per-video YT data yet to attribute them). TikTok flat at 206 (profile-view share of views ~1.3 %).
- Engagement still very low (TikTok likes/views 0.5–1.6 %, 1 comment total). Caption questions (EP 2) have not produced comments yet; EP 4 (question) vs EP 5 (no question) test continues – no caption changes made so they stay comparable.
- Best-time (Mon 9 + Tue 10 Nov): TikTok 18:00 is the daily peak (1096 / 1119, ≥ 10:00 1089 / 1136); IG 10:00 peak on Mon (5528 vs 4206), Tue close (4942 vs 4788); YT peaks 16:00 (9351 / 10353) with 18:00 7229 / 7897. TikTok is the network that actually delivers views (≈ 6× IG), and both real data and audience data favour 18:00 there → **EP 4 and EP 5 kept at 18:00.** A 16:00 test could help YT, but only after YT per-video stats start syncing.

### 2026-11-09
- Sample size: old stickman style TikTok 3 / IG 3 posts with data; new Kai/gameplay style: REEL Combo + EP 4 published today, **no usable data yet** (TT reel shows 4 views – almost certainly an early sync snapshot; EP 4 not synced). Style comparison starts tomorrow; judge after ≥ 48 h.
- TikTok lifetime curve: EP 1 and EP 2 got **0 new views** in the last 24 h (814 / 447) → TikTok stops pushing a video after ~2–2.5 days. Each video's views come almost entirely in its first 48 h, so daily posting matters more than any single post.
- TikTok EP 3 (Sun 18:05, "roller skates" confession hook) reached 623 in 27.6 h – faster than EP 1 (733 in 26.5 h ≈ similar) and much faster than EP 2 at 10:00 (447 total). Avg watch recovered to 5.0 s (EP 2 4.1 s). n = 3, but the 18:00 slot has now delivered the 2 best TikTok starts.
- Instagram: EP 3 = best IG reach so far (183 views / 168 reach in 27.6 h) but the lowest view rate (30.2 %) and avg watch 3.6 s → more reach did not mean better hold. EP 2 is still the only IG post with view rate > 45 %. IG growth per post stays small (+1/+2 views/day after day 2).
- Followers: still tiny (+4 total in 4 days: YT +3, IG +1, TT 0). TikTok profile views 14 on 11-07 but 0 follows → profile/bio does not convert; the end card CTA ("coming soon to Steam" + next-episode tease) is the lever to watch with the new style.
- YouTube per-video stats are still null after ~75 h (only channel-level 513 views on 11-06) → YouTube cannot be evaluated; do not move YT posts for testing until stats sync.
- Best-time (Tue 10 – Fri 13): TikTok 10:00 ≈ 18:00 (Wed 1432 vs 1386, Thu 1471 vs 1378, Fri 1379 vs 1222 – margins 3–11 %); IG 10:00 clearly ahead (Wed 6506 vs 4869, Fri 6734 vs 4418); YT peak 16:00. Real results still favour 18:00 on TikTok (the network with ~4× IG views), and TT/IG posts need Daniel to publish by hand → **kept all posts at 18:00**. A Friday 10:00 IG test could be considered once the new-style posts have a 48 h baseline.
- No caption changes: EP 4 (question) vs EP 5 (no question) test stays clean.

### 2026-11-10
- Sample size: first new-style (Kai/gameplay) data – **Instagram only, n = 2** (REEL Combo ~33 h, EP 4 ~27.5 h) vs 3 stickman reels. TikTok per-video stats did not refresh at all since 11-09 (Metricool sync lag) → no TikTok comparison today; YouTube per-video still null after ~100 h.
- **Instagram: the new style loses viewers in the first 3 seconds more than the stickman style.** Skip rate (swipe within 3 s): stickman 54.9 / 68.3 / 70.9 % vs Kai REEL 79.8 % and EP 4 **88.3 %**; avg watch 3.5–5.5 s vs 2.6 s / 2.0 s; views at similar age: EP 3 183 @ 27.6 h vs EP 4 108 @ 27.5 h. Consistent across both new posts, but n = 2, IG-only, and IG is the small network (≈ ¼ of TikTok views) → **warning signal, not a verdict**. Wait for TikTok numbers (the main network) before changing the format.
- Likely cause to check in the video edit (not changeable via scheduling): the first frame – small landscape gameplay strip in the middle with blurred copies + text, and Kai not yet visible – reads as a "reposted gameplay clip" and does not stop the scroll. Ideas for EP 8+: first 1 s full-height/zoomed action (no blur bars) or Kai's face + a bold one-line claim immediately, captions bigger and on the gameplay.
- IG posts keep growing slowly after day 2 (EP 3 +8 views in 24 h), stickman EP 1/2 flat → like TikTok, IG reach is decided in ~48 h.
- Followers flat today (+0; +4 total in 5 days). No follower effect of the new style visible yet.
- Best-time (Wed 11 – Fri 13): unchanged pattern – TikTok 10:00 ≈ 18:00 (+3–13 % for 10:00), IG 10:00 clearly ahead (+28–52 %), YT peak 16:00 (18:00 ≈ 80 % of peak). Real TikTok results still favour 18:00 and there is no YT per-video data → **kept all posts at 18:00, no caption changes** (EP 4 question vs EP 5 no-question test still running).

### 2026-11-11
- Sample size: first TikTok data for the Kai/gameplay style – TikTok n = 3 Kai (REEL Combo, EP 4, EP 5) vs 3 stickman; IG n = 3 vs 3; YouTube per-video still null (~124 h) → no YT conclusions.
- **TikTok: the new style gets the same or more reach, but people leave faster and like less.** Views: Kai 714 / 749 / 779 vs stickman 815 / 451 / 807 – EP 5 reached 779 in ~25 h, the fastest TT start so far. But avg watch 3.1 / 2.3 / 3.1 s vs 5.7 / 4.2 / 5.7 s, and like rate 0.1–0.4 % vs 1.2–1.6 %. Same pattern as IG yesterday (skip rate 80–88 % on REEL/EP 4) → now confirmed on both networks (n = 3+3 each): the gameplay hook gets shown, the first seconds don't hold.
- **Inside the Kai style, EP 5 ("90 enemies. ONE TAP." – one bold number-claim as the hook) beats EP 4 ("my upgrade tree got out of hand")** on both networks: TT avg watch 3.1 s vs 2.3 s, IG skip rate 60.7 % vs 87.5 %, IG view rate 39.3 % vs 12.5 %. n = 1 vs 1, but consistent across 2 networks → for EP 8+ open with one big concrete claim/number on screen in the first second.
- TikTok reach is not limited by follower count (≈ 99 % For You); the bottleneck is hold + engagement, which is what makes TikTok push a video further. Retention fix (first 1–2 s: full-height action + bold claim, Kai visible immediately) remains the #1 lever – it lives in the video edit, not in scheduling.
- Caption test EP 4 (ends with a question) vs EP 5 (no question): 0 comments on both, likes 1 vs 2 → **no evidence that caption questions create comments** (n = 1 vs 1).
- Posting hour: EP 5 went live on TikTok at 20:11 (2 h after the slot, published by hand) and still had the best start → a 18–20 h publish window works; no reason to move posts. Best-time (Thu 12 + Fri 13): TikTok 10:00 vs 18:00 +7 % / +13 %, IG 10:00 clearly ahead (+24 % / +52 %), YT peak 16:00 (18:00 = 76–81 %). Real TT results keep favouring 18:00 → **kept EP 7 and REEL at 18:00.**
- Trending sound (manual TT/IG) vs automatic (YT) cannot be compared – YouTube still has no per-video data.
- Followers: TikTok −1 (206 → 205), total +3 since start; no follower lift from the new style yet.

### 2026-11-12
- Sample size: TikTok 4 Kai (REEL, EP 4–6) vs 3 stickman; IG 4 vs 3; YouTube per-video still null (~148 h, only EP 1–3 listed) → no YT conclusions, trending-sound (TT/IG) vs auto (YT) still not comparable.
- **TikTok has a hard ceiling of ~700–815 views per post.** 6 of 7 TT posts ended at 715–815 (EP 2 at 10:00 = 451), all ≈ 99 % For You, and they stop growing after ~24–48 h. EP 6 hit 744 in its first 24 h, then (like EP 5: 779 → 780) almost nothing. This looks like TikTok's first test pool; no post has been pushed to a 2nd wave because hold/likes are too weak. Style, hook, caption and hour did not change this ceiling (n = 7) → only better retention/engagement in the video itself can break it.
- EP 6 retention is the 2nd-worst so far: TT avg watch 2.6 s (Kai range 2.3–3.1 s vs stickman 4.2–5.7 s), IG skip rate 75.5 %. Confirms the 11-11 conclusion; EP 5's bold-number hook ("90 enemies. ONE TAP.") is still the best Kai-style opener.
- **Late manual publishing seems to hurt Instagram, not TikTok:** EP 6 went live ~21:05 (3 h late). TikTok: 744 in 24 h (normal). IG: 55 views / 48 reach in 24.6 h vs 106–175 reach for every earlier reel (at 18:00–20:11) – the weakest IG start. IG audience at 21:00 is ~⅓ of 18:00 (1440 vs 4418, Metricool best-time). n = 1, but it fits → **try to publish TT/IG between 18:00 and 19:00, at least on Instagram.** Note: EP 6 still got the first IG save + a share, so the content wasn't the problem.
- Best-time (Fri 13): TikTok 10:00 1379 vs 18:00 1222 (+13 %), IG 10:00 6734 vs 18:00 4418 (+52 %), YT peak 16:00 10698 (18:00 = 76 %). Same pattern as all week; real TT results don't favour 10:00 → **REEL kept at 18:00.** For the next batch, an IG-only 10–12 h slot is the most promising untested change (IG is the network where both the audience data and the EP 6 result point to hour sensitivity).
- Caption/hashtag changes: none – no evidence so far that captions affect anything (≈ 99 % For You, 0 comments on all Kai posts).

### 2026-11-13
- Sample size: TikTok 5 Kai (REEL Combo, EP 4–7) + 1 auto-posted reel (3.6 h old) vs 3 stickman; IG 5 Kai vs 3 stickman (today's reel not synced); YouTube per-video still null (~172 h, only EP 1–3 listed) → no YT conclusions.
- **TikTok ceiling confirmed again:** EP 7 = 734 views in ~24 h (8 of 9 TT posts now 715–815, EP 2 at 10:00 = 459). EP 6 stopped at exactly 744 on day 2. Hold stays low: EP 7 avg watch 3.0 s (Kai range 2.3–3.1 s vs stickman 4.1–5.7 s), 1 like. Nothing in scheduling/captions has moved the ceiling (n = 9).
- **"Late publish hurts Instagram" (11-12) is NOT confirmed:** EP 7 went live on IG at 22:04 (4 h late, even later than EP 6) and still reached 108 people in ~24 h – a normal IG start (Kai range 102–115). EP 6 also caught up on day 2 (55 → 81 views). n = 2 late posts, mixed → hour sensitivity on IG is unproven; the 18:00 slot stays. From today all posts auto-publish on time, so this confound disappears.
- **First auto-posted reel** (clean game audio, no trending sound, TT live 18:07 on time): 257 views in ~3.6 h – the fastest 3.6 h TikTok start so far (EP 3 had 188 at the same age), but avg watch 2.3 s (low end of the Kai range). n = 1 and only hours old → re-check after 48 h; this is the first data point for "game audio + auto" vs "trending sound + manual".
- Kai-style IG skip rate stays 73–88 % (EP 7 75.2 %); only EP 5 (bold number hook) was below 61 %. The fix remains in the first 1–2 s of the edit (full-height action + bold claim, Kai immediately), not in scheduling.
- Best-time (Sat 14): TikTok 10:00 852 vs 18:00 709 (+20 %), IG 10:00 3409 vs 18:00 2393 (+42 %), YT peak 16:00 5880 (18:00 = 81 %). But the only real Saturday-10:00 post (EP 2) was the weakest TT post (459) → **REEL "3 Bosses" kept at 18:00 on all networks.** TT and IG share one post entry, so an IG-only morning test needs separate posts in the next batch.
- Followers: no change (TT 205, IG 1, YT 3; +3 total since start).
- No caption/title/hour changes today – the 11-14 captions already follow the 11-13 caption rule.

## Discord – týdenní updaty
- Každý pátek 18:00 (Praha) post do #🚀・updates (oznamovací kanál, publikovat), ping @🔔 Update Ping.
- Zdroj: stats/changelog.md, sekce Unreleased. Každou změnu ve hře hned zapsat do changelogu.
- Update #1 (v1.5.0) vyšel až v sobotu 14. 11. v 01:19 – páteční automatický běh (17:52) selhal na vyčerpaném limitu používání (USAGE_LIMIT_REACHED), poslal se ručně přes vestavěný prohlížeč. Postup, který funguje: text vložit do pole zprávy přes paste událost (kanály jako <#id>: bugs 1567718497579044894, ideas 1567718511344885800), na konec napsat @Update a vybrat roli z nabídky, Enter, pak Publikovat → Potvrdit.
- Role: automaticky přes Onboarding (CZ/SK, English, Update Ping, Shorts Ping) a Arcane levely (1/5/10/20/35/50). Ručně: Day One, Beta Tester, Fan Art, Moderator, Developer.
