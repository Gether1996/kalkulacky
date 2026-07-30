# Legislatíva 2026 — stav

## ✅ VYRIEŠENÉ (dohľadal som z oficiálnych zdrojov a zapísal do `sk_2026.json`)

Zdroje: Sociálna poisťovňa, Finančná správa SR, ŠÚ SR, podnikajte.sk, finsider.sk, socpoist.sk.

| Hodnota | Bolo | Teraz (2026) | Zdroj |
|---|---|---|---|
| Životné minimum | (nekonzistentné) | **284,13 €/mes** (od 1.7.2025) | MPSVR/Finsider |
| **Daň z príjmu — pásma** | „len 19/25 %" | **4 pásma 19/25/30/35 %** (154,8× / 212,4× / 264× ŽM) — REÁLNE od 2026! | podnikajte.sk, wellbens.sk |
| → hranice | 43983,32 / 60349,21 / 75010,32 | **potvrdené správne** + implementované do výpočtu | Finančná správa |
| NČZD ročná | 5966,76 | **5966,73 €** (21× ŽM) | Finsider/Podnikajte |
| Priemerná mzda 2024 | 1400 | **1524 €** | ŠÚ SR / Soc. poisťovňa |
| Max. vymeriavací základ soc. | 8862 | **16764 €/mes** (11× priem. mzda) | Sociálna poisťovňa |
| Max. DVZ nemocenské | 241,64 €/deň | **100,2083 €/deň** | Sociálna poisťovňa |
| Dôchodková hodnota (ADH) | 14,50 | **19,7633 €** | Sociálna poisťovňa |
| SZČO min. základ zdravotné | 762 | **914,40 €** (= min. sociálny) | Sociálna poisťovňa |
| Minimálna mzda | 915 / 5,259 | **potvrdené správne** | Podnikajte |
| Daňový bonus na dieťa | 100 / 50 | **potvrdené správne** | Finančná správa |
| Rodičovský príspevok | 381,90 / 270 | **364,80 € (bez materského) / 500,10 € (s materským)** | Peniaze.sk/socpoist |
| Materské — sadzba | 75 % | **potvrdené správne** (max 2 254,70 / 2 329,90 €/mes) | JASPIS/socpoist |
| DPH | 23/19/5 | **potvrdené správne** | — |

---

## 🔶 ZOSTÁVA — doménové rozhodnutia (mám čísla, ale treba tvoje „áno/nie/ako")

1. **NČZD phase-out (krátenie pri vysokých príjmoch)** — mám vzorec: plná NČZD do ročného základu **26 083,13 €**, nula od **43 983,32 €**. Pozn.: pri MESAČNEJ výplate sa NČZD bežne uplatňuje celá (497,23 €) a krátenie rieši ročné zúčtovanie — preto to väčšina mesačných kalkulačiek nekráti. **Chceš to krátiť aj v mesačnom výpočte?** áno / nie
2. **Refundovateľný daňový bonus** — mám krátenie: od ročného základu **27 432 €** sa bonus na každé dieťa znižuje o 1/10 rozdielu. Chýba mi potvrdenie **% stropu z čiastkového základu dane podľa počtu detí** (1 dieťa 20 %, 2 = 27 %, 3 = 34 %…?). **Potvrď % tabuľku 2026** a implementujem.
3. **Model rodičovského** — kalkulačka dnes rozlišuje „osnova (3 roky) / alternatíva (6 rokov)", ale správne rozlíšenie je **„mal / nemal predchádzajúce materské"** (sumy 364,80 / 500,10 už opravené). **Prepísať logiku kalkulačky na tento model?** áno / nie
4. **CZ daňový bonus** — dnes zastropený na 0; v CZ je vyplácaný ako záporná daň. Opraviť? áno / nie

## 🔶 ZOSTÁVA — nižšia istota / netlačí

- **Priemerný dôchodok (650 €) a minimálny dôchodok (370 €) 2026** — nechal som ako odhad; ak máš presné, doplním.
- **Dôchodkový vek** — dnes 64 pre oboch; v realite závisí od ročníka (zjednodušené).
- **Dotácie 2026** (solár €500/kW·7kW·3500€·4025€ · tepelné čerpadlo 380€/kW·3400€ · Obnov dom 60%·14000/19000€) — over podľa **aktuálneho kola výzvy** (SIEA/Obnov dom), tie sa menia každé kolo.
- **CZ/PL/HU** medzinárodné hodnoty — označené „orientačné", neoveril som (netlačí).

## ⛔ ZOSTÁVA — len tvoje (nedá sa dohľadať)

- **Legal:** obchodné meno, IČO, sídlo prevádzkovateľa → `[DOPLŇTE]` v privacy/terms.
- **og:image** (1200×630) + **PWA ikony** (192/512/maskable) — binárne assety.

---

**Zhrnutie:** ~13 kľúčových hodnôt som overil a opravil sám (vrátane veľkej opravy — 4-pásmová daň je reálna od 2026). Zostávajú hlavne 4 doménové rozhodnutia (body 1–4) a assety/legal.
