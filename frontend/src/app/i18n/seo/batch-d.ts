import { SeoContentMap } from "./types";

// Filled by the SEO-coverage pass (calculators that previously had no SEO).
export const SEO_BATCH_D: SeoContentMap = {
  vat: {
    sk: {
      title: "Kalkulačka DPH 2026 – výpočet DPH z ceny",
      description:
        "Vypočítajte DPH z ceny bez dane alebo si oddeľte DPH z ceny s daňou. Kalkulačka pracuje so základnou aj zníženou sadzbou DPH pre rok 2026.",
      keywords:
        "kalkulačka DPH, výpočet DPH, DPH z ceny, základ dane a DPH, sadzba DPH 2026",
      faq: [
        {
          question: "Ako pripočítam DPH k cene bez dane?",
          answer:
            "Cenu bez DPH vynásobíte sadzbou DPH a výsledok pripočítate k základu. Napríklad pri sadzbe 23 % je cena s DPH rovná základu vynásobenému hodnotou 1,23. Kalkulačka to spočíta automaticky.",
        },
        {
          question: "Ako oddelím DPH z ceny s daňou?",
          answer:
            "Cenu s DPH vydelíte hodnotou 1 plus sadzba (napr. 1,23 pri 23 %), čím získate základ dane. Rozdiel medzi cenou s daňou a základom je samotná DPH.",
        },
      ],
    },
    cs: {
      title: "Kalkulačka DPH 2026 – výpočet DPH z ceny",
      description:
        "Spočítejte DPH z ceny bez daně nebo oddělte DPH z ceny s daní. Kalkulačka pracuje se základní i sníženou sazbou DPH pro rok 2026.",
      keywords:
        "kalkulačka DPH, výpočet DPH, DPH z ceny, základ daně a DPH, sazba DPH 2026",
      faq: [
        {
          question: "Jak připočtu DPH k ceně bez daně?",
          answer:
            "Cenu bez DPH vynásobíte sazbou DPH a výsledek připočtete k základu. Například při sazbě 21 % je cena s DPH rovna základu vynásobenému hodnotou 1,21. Kalkulačka to spočítá automaticky.",
        },
        {
          question: "Jak oddělím DPH z ceny s daní?",
          answer:
            "Cenu s DPH vydělíte hodnotou 1 plus sazba (např. 1,21 při 21 %), čímž získáte základ daně. Rozdíl mezi cenou s daní a základem je samotná DPH.",
        },
      ],
    },
    en: {
      title: "VAT Calculator 2026 – Add or Remove VAT from a Price",
      description:
        "Add VAT to a net price or extract VAT from a gross price. The calculator works with both the standard and reduced VAT rates for 2026.",
      keywords:
        "VAT calculator, VAT calculation, add VAT, remove VAT, VAT rate 2026",
      faq: [
        {
          question: "How do I add VAT to a net price?",
          answer:
            "Multiply the net price by the VAT rate and add the result to the base. For example, at a 23% rate the gross price equals the base multiplied by 1.23. The calculator does this automatically.",
        },
        {
          question: "How do I remove VAT from a gross price?",
          answer:
            "Divide the gross price by 1 plus the rate (e.g. 1.23 for 23%) to get the net base. The difference between the gross price and the base is the VAT itself.",
        },
      ],
    },
    pl: {
      title: "Kalkulator VAT 2026 – obliczenie VAT od ceny",
      description:
        "Dolicz VAT do ceny netto lub wydziel VAT z ceny brutto. Kalkulator obsługuje stawkę podstawową i obniżoną VAT na rok 2026.",
      keywords:
        "kalkulator VAT, obliczenie VAT, doliczanie VAT, wydzielanie VAT, stawka VAT 2026",
      faq: [
        {
          question: "Jak doliczyć VAT do ceny netto?",
          answer:
            "Cenę netto mnożysz przez stawkę VAT i wynik dodajesz do podstawy. Na przykład przy stawce 23% cena brutto równa się podstawie pomnożonej przez 1,23. Kalkulator liczy to automatycznie.",
        },
        {
          question: "Jak wydzielić VAT z ceny brutto?",
          answer:
            "Cenę brutto dzielisz przez 1 plus stawka (np. 1,23 przy 23%), aby uzyskać podstawę netto. Różnica między ceną brutto a podstawą to sam VAT.",
        },
      ],
    },
    hu: {
      title: "ÁFA-kalkulátor 2026 – ÁFA számítása az árból",
      description:
        "Számítsa ki az ÁFA-t a nettó árból, vagy fejtse vissza az ÁFA-t a bruttó árból. A kalkulátor a 2026-os általános és kedvezményes ÁFA-kulccsal is működik.",
      keywords:
        "ÁFA kalkulátor, ÁFA számítás, ÁFA hozzáadása, ÁFA visszafejtése, ÁFA kulcs 2026",
      faq: [
        {
          question: "Hogyan adom hozzá az ÁFA-t a nettó árhoz?",
          answer:
            "A nettó árat megszorozza az ÁFA-kulccsal, és az eredményt hozzáadja az alaphoz. Például 27%-os kulcs esetén a bruttó ár az alap 1,27-tel szorzott értéke. A kalkulátor ezt automatikusan elvégzi.",
        },
        {
          question: "Hogyan fejtem vissza az ÁFA-t a bruttó árból?",
          answer:
            "A bruttó árat elosztja 1 plusz a kulccsal (pl. 1,27 a 27%-nál), így megkapja a nettó alapot. A bruttó ár és az alap különbsége maga az ÁFA.",
        },
      ],
    },
  },

  vacation: {
    sk: {
      title: "Kalkulačka dovolenky 2026 – nárok na dni dovolenky",
      description:
        "Vypočítajte si nárok na dovolenku za rok 2026 podľa veku a odpracovaného času. Zohľadní čerpané dni aj zostatok z minulého roka (orientačne).",
      keywords:
        "kalkulačka dovolenky, nárok na dovolenku 2026, výpočet dovolenky, dni dovolenky, zostatok dovolenky",
      faq: [
        {
          question: "Koľko dní dovolenky mám nárok za rok?",
          answer:
            "Základná výmera je 20 dní za rok, zamestnanec starší ako 33 rokov alebo s trvalou starostlivosťou o dieťa má nárok na 25 dní. Kalkulačka zohľadní pomernú časť podľa odpracovaného obdobia (orientačne).",
        },
        {
          question: "Prepadne mi nevyčerpaná dovolenka?",
          answer:
            "Nevyčerpanú dovolenku zamestnávateľ spravidla prevádza do nasledujúceho roka. Kalkulačka umožňuje zadať zostatok z minulého roka aj plánované čerpanie, aby ste videli aktuálny zostatok.",
        },
      ],
    },
    cs: {
      title: "Kalkulačka dovolené 2026 – nárok na dny dovolené",
      description:
        "Spočítejte si nárok na dovolenou za rok 2026 podle věku a odpracované doby. Zohlední čerpané dny i zůstatek z minulého roku (orientačně).",
      keywords:
        "kalkulačka dovolené, nárok na dovolenou 2026, výpočet dovolené, dny dovolené, zůstatek dovolené",
      faq: [
        {
          question: "Kolik dní dovolené mám nárok za rok?",
          answer:
            "Základní výměra je zpravidla 20 dní za rok, řada zaměstnavatelů poskytuje 25 dní. Kalkulačka zohlední poměrnou část podle odpracovaného období (orientačně).",
        },
        {
          question: "Propadne mi nevyčerpaná dovolená?",
          answer:
            "Nevyčerpanou dovolenou zaměstnavatel zpravidla převádí do následujícího roku. Kalkulačka umožňuje zadat zůstatek z minulého roku i plánované čerpání, abyste viděli aktuální zůstatek.",
        },
      ],
    },
    en: {
      title: "Vacation Calculator 2026 – Annual Leave Entitlement",
      description:
        "Calculate your 2026 annual leave entitlement based on age and time worked. It factors in days taken and any balance carried over (indicative).",
      keywords:
        "vacation calculator, annual leave entitlement 2026, holiday calculation, leave days, leave balance",
      faq: [
        {
          question: "How many vacation days am I entitled to per year?",
          answer:
            "The basic entitlement in Slovakia is 20 days per year; employees over 33 or caring for a child are entitled to 25 days. The calculator applies the pro-rata share based on time worked (indicative).",
        },
        {
          question: "Do I lose unused vacation days?",
          answer:
            "Unused leave is usually carried over to the following year by the employer. The calculator lets you enter last year's balance and planned days so you can see your current balance.",
        },
      ],
    },
    pl: {
      title: "Kalkulator urlopu 2026 – wymiar dni urlopu",
      description:
        "Oblicz wymiar urlopu na rok 2026 według wieku i przepracowanego czasu. Uwzględnia dni wykorzystane oraz saldo z poprzedniego roku (orientacyjnie).",
      keywords:
        "kalkulator urlopu, wymiar urlopu 2026, obliczenie urlopu, dni urlopu, saldo urlopu",
      faq: [
        {
          question: "Ile dni urlopu przysługuje mi na rok?",
          answer:
            "Na Słowacji podstawowy wymiar to 20 dni w roku, a pracownikom powyżej 33 lat lub sprawującym opiekę nad dzieckiem przysługuje 25 dni. Kalkulator uwzględnia część proporcjonalną według przepracowanego okresu (orientacyjnie).",
        },
        {
          question: "Czy niewykorzystany urlop przepada?",
          answer:
            "Niewykorzystany urlop pracodawca zwykle przenosi na kolejny rok. Kalkulator pozwala wpisać saldo z poprzedniego roku i planowane wykorzystanie, abyś widział aktualne saldo.",
        },
      ],
    },
    hu: {
      title: "Szabadságkalkulátor 2026 – éves szabadságkeret",
      description:
        "Számítsa ki a 2026-os éves szabadságkeretét életkor és ledolgozott idő alapján. Figyelembe veszi a kivett napokat és az átvitt egyenleget (tájékoztató jelleggel).",
      keywords:
        "szabadságkalkulátor, éves szabadságkeret 2026, szabadság számítás, szabadságnapok, szabadságegyenleg",
      faq: [
        {
          question: "Hány nap szabadság jár egy évre?",
          answer:
            "Szlovákiában az alapkeret évi 20 nap, a 33 év feletti vagy gyermeket gondozó munkavállalók 25 napra jogosultak. A kalkulátor a ledolgozott idő alapján az arányos részt is figyelembe veszi (tájékoztató jelleggel).",
        },
        {
          question: "Elvész a fel nem használt szabadság?",
          answer:
            "A fel nem használt szabadságot a munkáltató általában átviszi a következő évre. A kalkulátorban megadhatja az előző évi egyenleget és a tervezett kivételt, hogy lássa az aktuális egyenleget.",
        },
      ],
    },
  },

  "sick-leave": {
    sk: {
      title: "Kalkulačka PN 2026 – výpočet nemocenskej dávky",
      description:
        "Vypočítajte si výšku náhrady príjmu a nemocenskej dávky počas PN v roku 2026. Prvých 10 dní platí zamestnávateľ, potom Sociálna poisťovňa (orientačne).",
      keywords:
        "kalkulačka PN, výpočet nemocenskej, náhrada príjmu, dávka PN 2026, práceneschopnosť",
      faq: [
        {
          question: "Kto platí prvých 10 dní PN?",
          answer:
            "Prvých 10 kalendárnych dní práceneschopnosti vypláca náhradu príjmu zamestnávateľ, od 11. dňa preberá výplatu nemocenskej dávky Sociálna poisťovňa (orientačne).",
        },
        {
          question: "Koľko percent príjmu dostanem počas PN?",
          answer:
            "Prvé 3 dni je náhrada 25 % denného vymeriavacieho základu, od 4. dňa 55 %. Kalkulačka z hrubej mzdy odhadne dennú aj celkovú sumu (orientačne).",
        },
      ],
    },
    cs: {
      title: "Kalkulačka nemocenské 2026 – výpočet dávky během PN",
      description:
        "Spočítejte si náhradu mzdy a nemocenskou dávku během pracovní neschopnosti v roce 2026 podle slovenských pravidel (orientačně).",
      keywords:
        "kalkulačka nemocenské, výpočet nemocenské, náhrada mzdy, dávka PN 2026, pracovní neschopnost",
      faq: [
        {
          question: "Kdo platí prvních 10 dní PN?",
          answer:
            "Podle slovenských pravidel vyplácí prvních 10 kalendářních dní pracovní neschopnosti náhradu příjmu zaměstnavatel, od 11. dne přebírá výplatu nemocenské dávky Sociální pojišťovna (orientačně).",
        },
        {
          question: "Kolik procent příjmu dostanu během PN?",
          answer:
            "První 3 dny je náhrada 25 % denního vyměřovacího základu, od 4. dne 55 %. Kalkulačka z hrubé mzdy odhadne denní i celkovou částku (orientačně).",
        },
      ],
    },
    en: {
      title: "Sick Leave Calculator 2026 – Sickness Benefit Estimate",
      description:
        "Estimate your income compensation and sickness benefit during sick leave in 2026. The first 10 days are paid by the employer, then the Social Insurance (indicative).",
      keywords:
        "sick leave calculator, sickness benefit calculation, income compensation, sick pay 2026, incapacity for work",
      faq: [
        {
          question: "Who pays the first 10 days of sick leave?",
          answer:
            "Under Slovak rules, the employer pays income compensation for the first 10 calendar days of incapacity; from day 11 the Social Insurance Agency pays the sickness benefit (indicative).",
        },
        {
          question: "What percentage of income do I get on sick leave?",
          answer:
            "For the first 3 days the compensation is 25% of the daily assessment base, and from day 4 it is 55%. The calculator estimates the daily and total amount from your gross salary (indicative).",
        },
      ],
    },
    pl: {
      title: "Kalkulator zwolnienia lekarskiego 2026 – zasiłek chorobowy",
      description:
        "Oszacuj wysokość świadczenia i zasiłku chorobowego podczas zwolnienia lekarskiego w 2026 roku według słowackich zasad (orientacyjnie).",
      keywords:
        "kalkulator zwolnienia lekarskiego, obliczenie zasiłku chorobowego, świadczenie chorobowe, zasiłek 2026, niezdolność do pracy",
      faq: [
        {
          question: "Kto płaci za pierwsze 10 dni zwolnienia?",
          answer:
            "Według słowackich zasad przez pierwsze 10 dni kalendarzowych niezdolności do pracy świadczenie wypłaca pracodawca, a od 11. dnia zasiłek chorobowy przejmuje Zakład Ubezpieczeń Społecznych (orientacyjnie).",
        },
        {
          question: "Ile procent dochodu otrzymam na zwolnieniu?",
          answer:
            "Przez pierwsze 3 dni świadczenie wynosi 25% dziennej podstawy wymiaru, a od 4. dnia 55%. Kalkulator na podstawie wynagrodzenia brutto szacuje kwotę dzienną i łączną (orientacyjnie).",
        },
      ],
    },
    hu: {
      title: "Táppénz-kalkulátor 2026 – táppénz becslése",
      description:
        "Becsülje meg a keresetpótlást és a táppénzt betegállomány idején 2026-ban, a szlovák szabályok szerint (tájékoztató jelleggel).",
      keywords:
        "táppénz kalkulátor, táppénz számítás, keresetpótlás, táppénz 2026, keresőképtelenség",
      faq: [
        {
          question: "Ki fizeti a betegállomány első 10 napját?",
          answer:
            "A szlovák szabályok szerint a keresőképtelenség első 10 naptári napjára a munkáltató fizet keresetpótlást, a 11. naptól a táppénzt a Társadalombiztosítási Intézet folyósítja (tájékoztató jelleggel).",
        },
        {
          question: "A jövedelem hány százalékát kapom táppénzen?",
          answer:
            "Az első 3 napon a pótlás a napi számítási alap 25%-a, a 4. naptól 55%-a. A kalkulátor a bruttó bérből becsüli a napi és a teljes összeget (tájékoztató jelleggel).",
        },
      ],
    },
  },

  "parental-benefit": {
    sk: {
      title: "Kalkulačka rodičovského príspevku 2026",
      description:
        "Vypočítajte si výšku rodičovského príspevku a materskej v roku 2026 podľa dátumu narodenia dieťaťa a príjmu. Základná aj zvýšená sadzba (orientačne).",
      keywords:
        "rodičovský príspevok 2026, kalkulačka materskej, rodičovská dávka, príspevok na dieťa, materská 2026",
      faq: [
        {
          question: "Aká je výška rodičovského príspevku v roku 2026?",
          answer:
            "Rodičovský príspevok má základnú sadzbu pre rodičov bez predchádzajúcej materskej a vyššiu sadzbu pre tých, ktorí poberali materské. Kalkulačka určí, ktorá sadzba sa na vás vzťahuje (orientačne).",
        },
        {
          question: "Môžem popri rodičovskom príspevku pracovať?",
          answer:
            "Áno, počas poberania rodičovského príspevku môžete pracovať bez straty nároku na dávku. Kalkulačka umožňuje zadať plánovaný príjem a zohľadní ho v prehľade (orientačne).",
        },
      ],
    },
    cs: {
      title: "Kalkulačka rodičovského příspěvku 2026",
      description:
        "Spočítejte si výši rodičovského příspěvku a mateřské v roce 2026 podle data narození dítěte a příjmu, dle slovenských pravidel (orientačně).",
      keywords:
        "rodičovský příspěvek 2026, kalkulačka mateřské, rodičovská dávka, příspěvek na dítě, mateřská 2026",
      faq: [
        {
          question: "Jaká je výše rodičovského příspěvku v roce 2026?",
          answer:
            "Rodičovský příspěvek má podle slovenských pravidel základní sazbu pro rodiče bez předchozí mateřské a vyšší sazbu pro ty, kteří pobírali mateřskou. Kalkulačka určí, která sazba se na vás vztahuje (orientačně).",
        },
        {
          question: "Mohu při rodičovském příspěvku pracovat?",
          answer:
            "Ano, během pobírání rodičovského příspěvku můžete pracovat bez ztráty nároku na dávku. Kalkulačka umožňuje zadat plánovaný příjem a zohlední jej v přehledu (orientačně).",
        },
      ],
    },
    en: {
      title: "Parental Benefit Calculator 2026 – Parental Allowance",
      description:
        "Estimate your parental allowance and maternity benefit in 2026 based on the child's birth date and income. Basic and higher rate (indicative).",
      keywords:
        "parental benefit 2026, maternity benefit calculator, parental allowance, child allowance, maternity 2026",
      faq: [
        {
          question: "How much is the parental allowance in 2026?",
          answer:
            "Under Slovak rules the parental allowance has a basic rate for parents without prior maternity benefit and a higher rate for those who received it. The calculator determines which rate applies to you (indicative).",
        },
        {
          question: "Can I work while receiving parental allowance?",
          answer:
            "Yes, you can work while receiving the parental allowance without losing the entitlement. The calculator lets you enter planned income and factors it into the overview (indicative).",
        },
      ],
    },
    pl: {
      title: "Kalkulator świadczenia rodzicielskiego 2026",
      description:
        "Oszacuj wysokość świadczenia rodzicielskiego i zasiłku macierzyńskiego w 2026 roku według daty urodzenia dziecka i dochodu, wg słowackich zasad (orientacyjnie).",
      keywords:
        "świadczenie rodzicielskie 2026, kalkulator macierzyńskiego, zasiłek rodzicielski, świadczenie na dziecko, macierzyński 2026",
      faq: [
        {
          question: "Ile wynosi świadczenie rodzicielskie w 2026 roku?",
          answer:
            "Według słowackich zasad świadczenie rodzicielskie ma stawkę podstawową dla rodziców bez wcześniejszego zasiłku macierzyńskiego oraz stawkę wyższą dla tych, którzy go pobierali. Kalkulator ustala, która stawka Cię dotyczy (orientacyjnie).",
        },
        {
          question: "Czy mogę pracować podczas świadczenia rodzicielskiego?",
          answer:
            "Tak, podczas pobierania świadczenia rodzicielskiego można pracować bez utraty prawa do świadczenia. Kalkulator pozwala wpisać planowany dochód i uwzględnia go w zestawieniu (orientacyjnie).",
        },
      ],
    },
    hu: {
      title: "Szülői támogatás kalkulátor 2026",
      description:
        "Becsülje meg a szülői támogatás és a gyermekgondozási díj összegét 2026-ban a gyermek születési dátuma és a jövedelem alapján, a szlovák szabályok szerint (tájékoztató jelleggel).",
      keywords:
        "szülői támogatás 2026, gyermekgondozási díj kalkulátor, szülői ellátás, gyermektámogatás, anyasági 2026",
      faq: [
        {
          question: "Mennyi a szülői támogatás összege 2026-ban?",
          answer:
            "A szlovák szabályok szerint a szülői támogatásnak van egy alapösszege az anyasági ellátás nélküli szülőknek, és egy magasabb összege azoknak, akik anyasági ellátásban részesültek. A kalkulátor meghatározza, melyik összeg vonatkozik Önre (tájékoztató jelleggel).",
        },
        {
          question: "Dolgozhatok a szülői támogatás mellett?",
          answer:
            "Igen, a szülői támogatás folyósítása alatt dolgozhat az ellátásra való jogosultság elvesztése nélkül. A kalkulátorban megadhatja a tervezett jövedelmet, amelyet figyelembe vesz az áttekintésben (tájékoztató jelleggel).",
        },
      ],
    },
  },

  pregnancy: {
    sk: {
      title: "Tehotenská kalkulačka – termín pôrodu a týždne tehotenstva",
      description:
        "Vypočítajte si predpokladaný termín pôrodu, aktuálny týždeň tehotenstva a trimester podľa poslednej menštruácie alebo dátumu počatia.",
      keywords:
        "tehotenská kalkulačka, termín pôrodu, výpočet týždňa tehotenstva, trimester, dátum počatia",
      faq: [
        {
          question: "Ako sa počíta termín pôrodu?",
          answer:
            "Termín pôrodu sa štandardne určuje ako 280 dní (40 týždňov) od prvého dňa poslednej menštruácie, prípadne 266 dní od počatia. Ide o odhad, skutočný pôrod môže nastať o 1-2 týždne skôr či neskôr.",
        },
        {
          question: "V ktorom trimestri sa práve nachádzam?",
          answer:
            "Prvý trimester trvá 1.-12. týždeň, druhý 13.-26. týždeň a tretí 27.-40. týždeň. Kalkulačka podľa zadaného dátumu určí aktuálny týždeň aj trimester tehotenstva.",
        },
      ],
    },
    cs: {
      title: "Těhotenská kalkulačka – termín porodu a týdny těhotenství",
      description:
        "Spočítejte si předpokládaný termín porodu, aktuální týden těhotenství a trimestr podle poslední menstruace nebo data početí.",
      keywords:
        "těhotenská kalkulačka, termín porodu, výpočet týdne těhotenství, trimestr, datum početí",
      faq: [
        {
          question: "Jak se počítá termín porodu?",
          answer:
            "Termín porodu se standardně určuje jako 280 dní (40 týdnů) od prvního dne poslední menstruace, případně 266 dní od početí. Jde o odhad, skutečný porod může nastat o 1-2 týdny dříve či později.",
        },
        {
          question: "Ve kterém trimestru se právě nacházím?",
          answer:
            "První trimestr trvá 1.-12. týden, druhý 13.-26. týden a třetí 27.-40. týden. Kalkulačka podle zadaného data určí aktuální týden i trimestr těhotenství.",
        },
      ],
    },
    en: {
      title: "Pregnancy Calculator – Due Date and Pregnancy Weeks",
      description:
        "Calculate your estimated due date, current pregnancy week and trimester based on your last menstrual period or conception date.",
      keywords:
        "pregnancy calculator, due date, pregnancy week calculation, trimester, conception date",
      faq: [
        {
          question: "How is the due date calculated?",
          answer:
            "The due date is usually set at 280 days (40 weeks) from the first day of the last menstrual period, or 266 days from conception. It is an estimate; actual birth may occur 1-2 weeks earlier or later.",
        },
        {
          question: "Which trimester am I in?",
          answer:
            "The first trimester runs from weeks 1-12, the second from 13-26 and the third from 27-40. Based on the date you enter, the calculator determines your current week and trimester.",
        },
      ],
    },
    pl: {
      title: "Kalkulator ciąży – termin porodu i tygodnie ciąży",
      description:
        "Oblicz przewidywany termin porodu, aktualny tydzień ciąży i trymestr na podstawie ostatniej miesiączki lub daty poczęcia.",
      keywords:
        "kalkulator ciąży, termin porodu, obliczenie tygodnia ciąży, trymestr, data poczęcia",
      faq: [
        {
          question: "Jak oblicza się termin porodu?",
          answer:
            "Termin porodu ustala się standardowo jako 280 dni (40 tygodni) od pierwszego dnia ostatniej miesiączki lub 266 dni od poczęcia. To szacunek, rzeczywisty poród może nastąpić 1-2 tygodnie wcześniej lub później.",
        },
        {
          question: "W którym trymestrze się znajduję?",
          answer:
            "Pierwszy trymestr trwa od 1. do 12. tygodnia, drugi od 13. do 26., a trzeci od 27. do 40. Na podstawie podanej daty kalkulator określa aktualny tydzień i trymestr ciąży.",
        },
      ],
    },
    hu: {
      title: "Terhességi kalkulátor – szülési időpont és terhességi hetek",
      description:
        "Számítsa ki a várható szülési időpontot, az aktuális terhességi hetet és a trimesztert az utolsó menstruáció vagy a fogamzás dátuma alapján.",
      keywords:
        "terhességi kalkulátor, szülési időpont, terhességi hét számítás, trimeszter, fogamzás dátuma",
      faq: [
        {
          question: "Hogyan számítják ki a szülési időpontot?",
          answer:
            "A szülési időpontot általában az utolsó menstruáció első napjától számított 280 nap (40 hét), illetve a fogamzástól számított 266 nap alapján határozzák meg. Ez becslés, a tényleges szülés 1-2 héttel korábban vagy később is bekövetkezhet.",
        },
        {
          question: "Melyik trimeszterben vagyok?",
          answer:
            "Az első trimeszter az 1-12. hét, a második a 13-26. hét, a harmadik a 27-40. hét. A megadott dátum alapján a kalkulátor meghatározza az aktuális hetet és trimesztert.",
        },
      ],
    },
  },

  inflation: {
    sk: {
      title: "Kalkulačka inflácie – vývoj kúpnej sily peňazí",
      description:
        "Zistite, ako inflácia znižuje kúpnu silu vašich peňazí v čase. Vypočítajte reálnu hodnotu sumy o niekoľko rokov pri zadanej miere inflácie.",
      keywords:
        "kalkulačka inflácie, kúpna sila peňazí, výpočet inflácie, reálna hodnota peňazí, miera inflácie",
      faq: [
        {
          question: "Ako inflácia ovplyvňuje hodnotu peňazí?",
          answer:
            "Inflácia postupne znižuje kúpnu silu peňazí, takže za rovnakú sumu si o niekoľko rokov kúpite menej. Kalkulačka ukáže, akú reálnu hodnotu bude mať vaša suma po zadanom počte rokov.",
        },
        {
          question: "Ako sa počíta budúca kúpna sila?",
          answer:
            "Súčasná suma sa každý rok znižuje o mieru inflácie zloženým spôsobom, teda suma sa delí hodnotou (1 + inflácia) umocnenou na počet rokov. Kalkulačka to spočíta automaticky.",
        },
      ],
    },
    cs: {
      title: "Kalkulačka inflace – vývoj kupní síly peněz",
      description:
        "Zjistěte, jak inflace snižuje kupní sílu vašich peněz v čase. Spočítejte reálnou hodnotu částky za několik let při zadané míře inflace.",
      keywords:
        "kalkulačka inflace, kupní síla peněz, výpočet inflace, reálná hodnota peněz, míra inflace",
      faq: [
        {
          question: "Jak inflace ovlivňuje hodnotu peněz?",
          answer:
            "Inflace postupně snižuje kupní sílu peněz, takže za stejnou částku si za několik let koupíte méně. Kalkulačka ukáže, jakou reálnou hodnotu bude mít vaše částka po zadaném počtu let.",
        },
        {
          question: "Jak se počítá budoucí kupní síla?",
          answer:
            "Současná částka se každý rok snižuje o míru inflace složeným způsobem, tedy částka se dělí hodnotou (1 + inflace) umocněnou na počet let. Kalkulačka to spočítá automaticky.",
        },
      ],
    },
    en: {
      title: "Inflation Calculator – Purchasing Power of Money Over Time",
      description:
        "See how inflation erodes the purchasing power of your money over time. Calculate the real value of an amount in a few years at a given inflation rate.",
      keywords:
        "inflation calculator, purchasing power of money, inflation calculation, real value of money, inflation rate",
      faq: [
        {
          question: "How does inflation affect the value of money?",
          answer:
            "Inflation gradually reduces the purchasing power of money, so the same amount buys less after a few years. The calculator shows what real value your amount will have after the number of years you enter.",
        },
        {
          question: "How is future purchasing power calculated?",
          answer:
            "The present amount is reduced each year by the inflation rate on a compound basis, meaning the amount is divided by (1 + inflation) raised to the number of years. The calculator does this automatically.",
        },
      ],
    },
    pl: {
      title: "Kalkulator inflacji – siła nabywcza pieniądza w czasie",
      description:
        "Sprawdź, jak inflacja obniża siłę nabywczą Twoich pieniędzy w czasie. Oblicz realną wartość kwoty za kilka lat przy podanej stopie inflacji.",
      keywords:
        "kalkulator inflacji, siła nabywcza pieniądza, obliczenie inflacji, realna wartość pieniądza, stopa inflacji",
      faq: [
        {
          question: "Jak inflacja wpływa na wartość pieniądza?",
          answer:
            "Inflacja stopniowo obniża siłę nabywczą pieniądza, więc za tę samą kwotę po kilku latach kupisz mniej. Kalkulator pokazuje, jaką realną wartość będzie miała Twoja kwota po podanej liczbie lat.",
        },
        {
          question: "Jak oblicza się przyszłą siłę nabywczą?",
          answer:
            "Obecna kwota jest co roku pomniejszana o stopę inflacji w sposób złożony, czyli kwotę dzieli się przez (1 + inflacja) podniesione do potęgi liczby lat. Kalkulator liczy to automatycznie.",
        },
      ],
    },
    hu: {
      title: "Inflációs kalkulátor – a pénz vásárlóereje az idő során",
      description:
        "Nézze meg, hogyan csökkenti az infláció a pénze vásárlóerejét az idő során. Számítsa ki egy összeg reálértékét néhány év múlva adott inflációs ráta mellett.",
      keywords:
        "inflációs kalkulátor, pénz vásárlóereje, infláció számítás, pénz reálértéke, inflációs ráta",
      faq: [
        {
          question: "Hogyan befolyásolja az infláció a pénz értékét?",
          answer:
            "Az infláció fokozatosan csökkenti a pénz vásárlóerejét, így ugyanazért az összegért néhány év múlva kevesebbet kap. A kalkulátor megmutatja, mekkora reálértéke lesz az összegének a megadott évek után.",
        },
        {
          question: "Hogyan számítják ki a jövőbeli vásárlóerőt?",
          answer:
            "A jelenlegi összeget évente az inflációs rátával csökkentik kamatos módon, azaz az összeget elosztják (1 + infláció) értékkel az évek számának hatványára emelve. A kalkulátor ezt automatikusan elvégzi.",
        },
      ],
    },
  },
};
