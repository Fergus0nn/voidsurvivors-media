# Virální shorty – playbook VOID SURVIVORS

Sepsáno 15. 11. 2026 z rozboru, jak dělají shorty podobné hry a indie vývojáři (zdroje dole), a z našich vlastních čísel (stats/learnings.md).
Platí pro TikTok, Instagram Reels i YouTube Shorts. Každé nové video projde tímhle checklistem.

## 1. Háček – první vteřina rozhoduje
- Divák se rozhodne zhruba za 1 s. Video začíná **nejsilnějším momentem** (největší chaos, boss, skoro smrt) – nikdy logem ani úvodem.
- **Jeden háček na video**: buď velké číslo / tvrzení („90 enemies. ONE TAP.“), nebo výzva („Can YOU survive this?“), nebo kontrast („Minute 1 vs minute 20“).
  - Naše data: háček s číslem (EP 5) porazil EP 4 na TikToku (průměrné sledování 3,1 s vs 2,3 s) i na Instagramu (přeskočení 61 % vs 88 %). „Can you survive 20 minutes?“ měl nejrychlejší start na TikToku.
- Háček je **pozvánka pro diváka** („can YOU…“, „which minute gets YOU?“), ne odmítnutí.
- První snímek: velký gameplay přes celou šířku (čtverec nebo celá výška), velký text a Kai hned vidět. Žádný malý pruh hry s rozmazanými okraji.

## 2. Délka a smyčka
- Bojový / mechanický klip **10–15 s**, devlog **15–30 s**. Kratší = víc lidí dokouká.
- Konec navazuje na začátek (**smyčka**) – opakovaná zhlédnutí se počítají.

## 3. Formáty, které u survivor-like her fungují
- **Minute 1 vs minute 20** – eskalace, tvrdé střihy, začni tím nejextrémnějším. (REEL 5)
- **Before / after** – stará vs nová grafika, tvrdý střih, nejdramatičtější změna první.
- **Výzva s číslem** – „Can YOU beat combo 20,000?“
- **Bugy a faily** – vtipné, sdílené, polidšťují vývojáře.
- **Číslovaná série** („EP 8“, „Day 30“) – lidi pak hledají starší díly; chce pravidelné vydávání.
- **Uspokojivé smyčky** – řetězové výbuchy, magnet stahuje 500 krystalů.
- **Příběh vývojáře** – „solo dev z Česka“, „dělám to po nocích“ – storytelling táhne.
- **Přímá výzva komunitě** – „Gamers, help me name this boss“ → komentáře.

## 4. Mluvené slovo (Kai)
- Vypravěč přes záznam hry je ověřený indie formát (případová studie: 571 tis. zhlédnutí, 2 900 wishlistů z jednoho videa s TTS hlasem).
- Kai mluví **krátké věty (max. ~7 slov)** každé 2–4 s, vždy k tomu, co je zrovna vidět. Před velkým výbuchem nech 1 s bez řeči.
- Hlas: Kokoro `am_michael` (Daniel vybral „hlas 2“) – `tools/reel/kai_voice.py`. Hudba a efekty se pod hlasem ztiší (`clean_audio.py`, `voice`).
- Nejvíc zapojení mají videa, kde mluví sám vývojář – kdyby Daniel někdy chtěl, stačí nahrát pár vět do mobilu.
- Obecný TTS hlas, který nenapodobuje skutečného člověka, podle návodů k pravidlům TikToku označení „AI-generated“ nevyžaduje. AI nikdy nezmiňujeme v textu.

## 5. Text na obrazovce
- Max. 2 řádky, 3–6 slov, jedno zvýrazněné slovo. Ne v horních ~150 px (lišta TikToku), ne ve spodních 20 %, ne u pravého okraje (tlačítka).
- Počítej s tím, že divák hru nikdy neviděl – žádný vnitřní kontext.

## 6. Konec a výzva
- Velká jasná výzva ~3 s. Steam stránka zatím není → „FOLLOW FOR MORE“ nebo otázka do komentářů („WHICH MINUTE ENDS YOU?“).
- **Nikdy nekončit „How long would you survive?“** (Daniel 15. 11. – už bylo moc často). Konec pokaždé jiný: „FOLLOW FOR MORE CHAOS“, otázka k obsahu videa („Run or fight?“, „Which minute ends you?“), cliffhanger.
- Nikdy „play / download / demo / free“.
- Na komentáře odpovídat během první hodiny po zveřejnění.

## 7. Náhledovka (cover)
- Na TikToku v hlavním feedu skoro nerozhoduje, ale po hitu si lidi prohlíží profil – mřížka musí vypadat dobře. Na Instagramu (mřížka) a YouTube (police Shorts) rozhoduje víc.
- Nejsilnější záběr + **2–3 slova velkým písmem uprostřed** (přežijí ořez 1:1 / 4:5) + štítek VOID SURVIVORS. Formát before/after funguje i jako náhledovka.
- `tools/reel/make_cover.py`; v Metricoolu `videoThumbnailUrl` (Instagram ano; TikTok jen u firemního účtu; YouTube jen u ověřeného kanálu).

## 8. Po hitu
- Když video udělá aspoň 3× průměr, další týden udělej 2–3 videa ve stejném stylu; formáty, které nefungují, rychle opusť.
- Po hitu je dobré znovu nahrát starší dobrá videa s novým háčkem.

## 9. Co už máme a držíme
- Zvuk jen ze souborů hry (hudba + efekty + Kai), nikdy zvuk nahrávky (Spotify).
- Popisek: 1 věta + otázka, ~5 hashtagů (#voidsurvivors první); YouTube: hledaná slova v názvu.
- 1 video denně v 18:00, všechno se zveřejňuje automaticky.

## 10. Co dělají velké survivor-like hry (podrobně: stats/konkurence_socialni_site.md)
- Hity (Vampire Survivors, Halls of Torment, Brotato, Megabonk) nakopli **streameři a YouTubeři**, ne vlastní TikTok. Shorty budují komunitu a viditelnost.
- Všechno se láme na **Steamu**: stránka → wishlisty → demo → Next Fest. Jakmile bude Steam stránka, konec videí = „WISHLIST ON STEAM“.
- Nejlepší shorty po čase **nahrát znovu** s novým háčkem – stejné video může jednou udělat 10 tis. a podruhé miliony zhlédnutí.
- Ptát se diváků na nápady („help me name this boss“) – komentáře + nápady zdarma.

## Zdroje
- How To Market A Game – Seven great tips for marketing your indie game on TikTok: https://howtomarketagame.com/2022/02/07/seven-great-tips-for-marketing-your-indie-game-on-tiktok/
- presskit.gg – TikTok indie game marketing field guide: https://presskit.gg/field-guides/tiktok-indie-game-marketing
- GameDiscoverCo – Everything you want to know about shortform video & games: https://newsletter.gamediscover.co/p/everything-you-want-to-know-about
- HypeHype – How to use video hooks to promote your game: https://learn.hypehype.com/game-promotion/how-to-use-video-hooks-to-promote-your-game
- Outlook Respawn – How viral indies of 2025 succeeded (Megabonk, CloverPit): https://respawn.outlookindia.com/gaming/gaming-news/creativity-over-cost-how-viral-indies-of-2025-succeeded
- Kompozy – TikTok AI disclosure policy guide: https://kompozy.io/guides/tiktok-ai-disclosure-policy
