# Legislatíva 2026 — stav (finálny)

## ✅ OVERENÉ z oficiálnych zdrojov + implementované/opravené

**SK — dane a mzdy**
- Životné minimum 284,13 € · **4-pásmová daň 19/25/30/35 %** (154,8×/212,4×/264× ŽM) — implementovaná
- NČZD 5966,73 € (497,23 €/mes); mesačne sa nekráti (rieši ročné zúčtovanie — správne)
- Priemerná mzda 2024 = 1524 € · max. soc. vymeriavací základ 16 764 €/mes
- Minimálna mzda 915 € / 5,259 € · **DPH 23/19/5/0 %**
- **Refundovateľný daňový bonus:** % z hrubá−odvody (1=29 %…6+=64 %), krátenie od mes. základu 2 286 € (−1/10 na dieťa), vyplácaný nad rámec dane

**SK — odvody a dávky**
- Max. DVZ nemocenské 100,21 €/deň · dôchodková hodnota (ADH) 19,7633 €
- Priemerný dôchodok ~701 € · min. dôchodok 411,90 €
- SZČO min. zdrav./soc. základ 914,40 € · materské 75 %
- Rodičovský 364,80 € (bez materského) / 500,10 € (s materským); **bez príjmového testu**

**SK — dotácie**
- Solár Zelená domácnostiam: 500 €/kW, max 7 kW, 3 500 € (základ)
- Tepelné čerpadlo: 380 €/kW, **max 3 800 €** (opravené) · Obnov dom: **75 %, 15 000/19 000 €** (opravené)

**CZ** ✅ potvrdené: sleva 30 840 Kč · daň 15/23 % nad 1 762 812 Kč · min. soc. záloha 5 720 Kč · min. zdrav. základ 24 483,50 Kč / záloha 3 306 Kč · detský kredit 1267/1860/2320 · **refundovateľný bonus** (od 11 200 Kč) · DPH 21/12 %

**PL** ✅ potvrdené: kwota wolna 30 000 zł (300/mes) · 12/32 % nad 120 000 zł · ZUS 13,71 % · KUP 250 zł · zdrav. 9 %

**HU** ✅ opravené: SZJA 15 % · TB 18,5 % · **rodinná úľava PER DIEŤA × počet** (1=133 340, 2=266 660/dieťa, 3+=440 000/dieťa) + **családi járulékkedvezmény** (nevyužitá časť z odvodov)

Zdroje: Sociálna poisťovňa, Finančná správa SR, ŠÚ SR, podnikajte.sk, finsider.sk, officina.hu, e15.cz, infakt.pl, plan-obnovy-dotacie.sk, enerta.sk.

---

## ⚠️ TREBA 100 % POTVRDIŤ / ROZHODNÚŤ (zvyšok — nízky dopad)

1. **Rodičovský — model výberu:** sumy a príjmový test opravené, ale kalkulačka stále ponúka „osnova (3 r.) / alternatíva (6 r.)". Reálne: rozdiel je „mal/nemal materské" a 6 rokov len pri chorom dieťati. **Prepísať aj tento výber + frontend?** (dizajnové rozhodnutie)
2. **NON_TAXABLE_AMOUNT_DISABILITY** (vyššia NČZD pre ZŤP) — som si takmer istý, že pri dani z príjmu **neexistuje** (mŕtvy kód). **Potvrď odstránenie.**
3. **Dôchodkový vek** — nechal som 64 pre oboch; reálne závisí od ročníka (63–64+2 mes., −6 mes./dieťa). **Prepracovať na tabuľku podľa ročníka?** (dizajnové rozhodnutie)
4. **Solár — zvýhodnená sadzba 575 €/kW / 4 370 €** (znečistené ovzdušie / koniec tuhého paliva) — pridať ako druhú vetvu? A **nové kolo SIEA na jeseň 2026** môže sumy zmeniť.
5. **HU zamestnávateľské szocho 13 %** a **CZ hlbšie sub-hodnoty** (dôchodkové redukčné hranice) — štrukturálne OK, ale explicitne som ich neoveril na 100 %.

## ⛔ LEN TY
- **Legal:** obchodné meno, IČO, sídlo → `[DOPLŇTE]` v privacy/terms.
- **og:image** (1200×630) + **PWA ikony** (192/512/maskable).

---

---

## 🌍 POKRYTIE KRAJÍN — teraz PLNÉ (SK/CZ/PL/HU pre všetky kalkulačky)

Doplnené **PL a HU enginy** pre freelancer, dôchodok, dovolenku, PN, rodičovský a solár
(predtým len mzda + DPH; zvyšok padal na SK pravidlá). Sú **INDIKATÍVNE** (ako CZ) — model je
správny, ale tieto čísla treba časom potvrdiť:

**PL (`pl_2026.json`)** — freelancer paušál 20 % (placeholder; PL skala paušál nemá — zvážiť ryčzałt),
ZUS základ 5 652,60 zł (60 % z prognóz. mzdy 9 420), zdrav. min. 432,54 zł, dôchodok NDC aproximácia
(÷220,8), min. dôchodok 1 978,49 zł, PN predpoklad vek < 50 (33 dní zamestnávateľ), materská 20 týž.
100 % + 41 týž. 70 %, solár Mój Prąd 6.0 (PV max 7 000 + batéria 16 000 zł).

**HU (`hu_2026.json`)** — freelancer átalány 40 % (môže stúpnuť na 45 %), min. mzda 322 800 Ft,
dôchodok násobková tabuľka + valorizácia (aproximácia), min. dôchodok / GYES 28 500 Ft, GYED max
451 920 Ft, CSED 24 týž. 100 %, táppénz 60 % / betegszabadság 70 % (15 dní), solár Napenergia Plusz
(batéria strop 2,5 mil. Ft, cena 350 000 Ft/kWp).

CZ ostáva potvrdené správne (hlavné hodnoty), okrem hlbších dôchodkových redukčných hraníc.

---

**Zhrnutie:** ~20 SK hodnôt overených/opravených + plné PL/HU enginy (indikatívne). Zvyšok (⚠️) sú 2 dizajnové
rozhodnutia (rodičovský model, dôchodkový vek), 1 potvrdenie na odstránenie (ZŤP NČZD) a
dotačné detaily podľa aktuálneho kola — všetko nízky dopad. Assety/legal sú na tebe.
