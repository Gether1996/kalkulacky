# Legislatíva 2026 — stav

## ✅ VYRIEŠENÉ (dohľadané z oficiálnych zdrojov + implementované)

Hodnoty: životné minimum 284,13 € · **4-pásmová daň 19/25/30/35 %** (implementovaná) ·
NČZD 5966,73 € · priemerná mzda 2024 = 1524 € · max. soc. základ 16 764 € ·
max. DVZ nemocenské 100,21 €/deň · dôchodková hodnota 19,7633 € · SZČO min. zdrav. základ 914,40 € ·
priemerný dôchodok 701 € · min. dôchodok 411,90 € · rodičovský 364,80/500,10 € · materské 75 %.

Logika: **refundovateľný daňový bonus SK** (% zo základu 29/36/43/50/57/64 + krátenie) ·
**refundovateľný bonus CZ** (záporná daň od 11 200 Kč) · **rodičovský bez príjmového testu** ·
NČZD mesačne sa nekráti (rieši ročné zúčtovanie — správne).

Zdroje: Sociálna poisťovňa, Finančná správa SR, ŠÚ SR, podnikajte.sk, finsider.sk, peniaze.sk.

---

## ❓ ČOMU SI NIE SOM ISTÝ — potrebujem od teba potvrdiť

### Daňový bonus — 2 detaily
1. **Krátenie bonusu pri vysokých príjmoch** — implementoval som „na každé dieťa −1/10 × (mesačný základ − 2 286 €)". Formulácia zdroja bola trochu nejednoznačná. **Sedí tento vzorec?** (ovplyvňuje rodičov s mesačným základom nad ~2 286 €)
2. **% sa počíta z „čiastkového základu dane"** = hrubá − odvody (pred NČZD). **Je to správny základ?** (predpokladám áno)

### Rodičovský príspevok — model
3. Sumy (364,80/500,10) a zrušenie príjmového testu sú opravené. Ale kalkulačka stále ponúka výber **„osnova (3 r.) / alternatíva (6 r.)"** — v realite je rozdiel „mal/nemal materské" a 6 rokov platí len pri **dlhodobo nepriaznivom zdravotnom stave dieťaťa**. Úplné zladenie si vyžaduje aj zmenu frontendu. **Chceš prepísať aj tento výber, alebo stačí takto?**

### Dotácie — treba aktuálne kolo výzvy (nemenil som, len solár čiastočne potvrdený)
4. **Solár Zelená domácnostiam:** základ **500 €/kW, max 7 kW, 3 500 €** potvrdené. Ale existuje aj **zvýhodnená sadzba 575 €/kW** (znečistené ovzdušie / koniec tuhého paliva) — mám ju pridať? A **nové kolo na jeseň 2026 môže sumy znížiť.**
5. **Tepelné čerpadlo** (dnes 380 €/kW, max 3 400 €) a **Obnov dom** (60 %, 14 000/19 000 €) — **tieto som NEOVERIL**, over podľa aktuálneho kola SIEA/Obnov dom.

### Odhady / zjednodušenia (nízky dopad)
6. **Priemerný dôchodok 701 €** — približná hodnota (zdroje sa mierne líšia).
7. **Dôchodkový vek** — nechal som **64 pre oboch**; reálne závisí od ročníka (63–64+2 mes., znižuje sa za deti). Pri odhadovej kalkulačke je to zjednodušenie — **prepracovať na tabuľku podľa ročníka?**
8. **NON_TAXABLE_AMOUNT_DISABILITY** (vyššia NČZD pre ZŤP) — som si takmer istý, že pri dani z príjmu **neexistuje** (je to mŕtvy kód). **Potvrď, že to môžem odstrániť.**

### Neoverené (netlačí)
9. **CZ / PL / HU medzinárodné hodnoty** — označené „orientačné", neoveril som ich voči oficiálnym zdrojom 2026.
10. **VAT znížené sadzby 19 % a 5 %** — základná 23 % potvrdená; znížené predpokladám správne, ale explicitne som ich neoveril.

---

## ⛔ LEN TY (nedá sa dohľadať)
- **Legal:** obchodné meno, IČO, sídlo prevádzkovateľa → `[DOPLŇTE]` v privacy/terms.
- **og:image** (1200×630) + **PWA ikony** (192/512/maskable).

---

**Zhrnutie:** overil a implementoval som ~15 hodnôt + 4 doménové rozhodnutia. Zostáva potvrdiť
detaily vyššie (hlavne body 1, 3, 4–5) a dodať legal/assety.
