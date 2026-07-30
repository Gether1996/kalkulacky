import { SeoContentMap } from "./types";

// Filled by the SEO-coverage pass (calculators that previously had no SEO).
export const SEO_BATCH_F: SeoContentMap = {
  percentage: {
    sk: {
      title: "Percentuálna kalkulačka – výpočet percent online",
      description:
        "Vypočítajte percentá jednoducho: koľko je X % z Y, koľko percent je jedno číslo z druhého, percentuálnu zmenu, pripočítanie či odpočítanie percent.",
      keywords:
        "percentuálna kalkulačka, výpočet percent, koľko je percento z čísla, percentuálna zmena, pripočítať percentá",
      faq: [
        {
          question: "Ako vypočítam, koľko je X % z čísla?",
          answer:
            "Číslo vynásobte percentom a vydeľte 100. Napríklad 20 % z 200 je 200 × 20 ÷ 100 = 40. Kalkulačka to spraví automaticky po zadaní hodnôt.",
        },
        {
          question: "Ako sa počíta percentuálna zmena?",
          answer:
            "Od novej hodnoty odpočítajte pôvodnú, výsledok vydeľte pôvodnou hodnotou a vynásobte 100. Kladné číslo znamená nárast, záporné pokles.",
        },
      ],
    },
    cs: {
      title: "Procentuální kalkulačka – výpočet procent online",
      description:
        "Spočítejte procenta jednoduše: kolik je X % z Y, kolik procent je jedno číslo z druhého, procentuální změnu, přičtení či odečtení procent.",
      keywords:
        "procentuální kalkulačka, výpočet procent, kolik je procento z čísla, procentuální změna, přičíst procenta",
      faq: [
        {
          question: "Jak vypočítám, kolik je X % z čísla?",
          answer:
            "Číslo vynásobte procentem a vydělte 100. Například 20 % z 200 je 200 × 20 ÷ 100 = 40. Kalkulačka to udělá automaticky po zadání hodnot.",
        },
        {
          question: "Jak se počítá procentuální změna?",
          answer:
            "Od nové hodnoty odečtěte původní, výsledek vydělte původní hodnotou a vynásobte 100. Kladné číslo znamená nárůst, záporné pokles.",
        },
      ],
    },
    en: {
      title: "Percentage Calculator – Calculate Percentages Online",
      description:
        "Work out percentages easily: what is X% of Y, what percent one number is of another, percentage change, and adding or subtracting a percentage.",
      keywords:
        "percentage calculator, calculate percentages, what is percent of a number, percentage change, add percentage",
      faq: [
        {
          question: "How do I calculate X% of a number?",
          answer:
            "Multiply the number by the percentage and divide by 100. For example, 20% of 200 is 200 × 20 ÷ 100 = 40. The calculator does this automatically once you enter the values.",
        },
        {
          question: "How is percentage change calculated?",
          answer:
            "Subtract the original value from the new value, divide the result by the original value and multiply by 100. A positive number is an increase, a negative one a decrease.",
        },
      ],
    },
    pl: {
      title: "Kalkulator procentowy – obliczanie procentów online",
      description:
        "Obliczaj procenty łatwo: ile to X% z Y, jakim procentem jest jedna liczba drugiej, zmiana procentowa oraz dodawanie i odejmowanie procentów.",
      keywords:
        "kalkulator procentowy, obliczanie procentów, ile to procent z liczby, zmiana procentowa, dodać procenty",
      faq: [
        {
          question: "Jak obliczyć, ile to X% z liczby?",
          answer:
            "Pomnóż liczbę przez procent i podziel przez 100. Na przykład 20% z 200 to 200 × 20 ÷ 100 = 40. Kalkulator zrobi to automatycznie po wpisaniu wartości.",
        },
        {
          question: "Jak oblicza się zmianę procentową?",
          answer:
            "Od nowej wartości odejmij pierwotną, wynik podziel przez wartość pierwotną i pomnóż przez 100. Liczba dodatnia oznacza wzrost, ujemna spadek.",
        },
      ],
    },
    hu: {
      title: "Százalékkalkulátor – százalékszámítás online",
      description:
        "Számoljon százalékot egyszerűen: mennyi X%-a Y-nak, hány százaléka egy szám a másiknak, százalékos változás, valamint százalék hozzáadása és levonása.",
      keywords:
        "százalékkalkulátor, százalékszámítás, mennyi egy szám százaléka, százalékos változás, százalék hozzáadása",
      faq: [
        {
          question: "Hogyan számítom ki egy szám X%-át?",
          answer:
            "Szorozza meg a számot a százalékkal, és ossza el 100-zal. Például 200 20%-a: 200 × 20 ÷ 100 = 40. A kalkulátor ezt automatikusan elvégzi az értékek megadása után.",
        },
        {
          question: "Hogyan számítják a százalékos változást?",
          answer:
            "Az új értékből vonja ki az eredetit, az eredményt ossza el az eredeti értékkel, majd szorozza meg 100-zal. A pozitív szám növekedést, a negatív csökkenést jelent.",
        },
      ],
    },
  },

  "split-bill": {
    sk: {
      title: "Rozdelenie účtu – kalkulačka na delenie účtu a prepitné",
      description:
        "Rozdeľte účet medzi viacerých ľudí rovnomerne, podľa položiek alebo vlastných súm. Kalkulačka pripočíta prepitné a vypočíta sumu na osobu.",
      keywords:
        "rozdelenie účtu, delenie účtu kalkulačka, účet na osobu, prepitné kalkulačka, koľko platí každý",
      faq: [
        {
          question: "Ako rozdelím účet medzi viac ľudí?",
          answer:
            "Zadajte celkovú sumu a počet osôb. Kalkulačka vydelí sumu rovnomerne, prípadne podľa položiek alebo vlastných súm, a zobrazí, koľko platí každý.",
        },
        {
          question: "Ako sa počíta prepitné?",
          answer:
            "Prepitné sa počíta ako percento z celkovej sumy účtu. Bežne sa dáva 10 – 15 %. Kalkulačka ho pripočíta k účtu a rozdelí medzi všetkých.",
        },
      ],
    },
    cs: {
      title: "Rozdělení účtu – kalkulačka na dělení účtu a spropitné",
      description:
        "Rozdělte účet mezi více lidí rovnoměrně, podle položek nebo vlastních částek. Kalkulačka přičte spropitné a spočítá částku na osobu.",
      keywords:
        "rozdělení účtu, dělení účtu kalkulačka, účet na osobu, spropitné kalkulačka, kolik platí každý",
      faq: [
        {
          question: "Jak rozdělím účet mezi více lidí?",
          answer:
            "Zadejte celkovou částku a počet osob. Kalkulačka částku rozdělí rovnoměrně, případně podle položek nebo vlastních částek, a zobrazí, kolik platí každý.",
        },
        {
          question: "Jak se počítá spropitné?",
          answer:
            "Spropitné se počítá jako procento z celkové částky účtu. Běžně se dává 10 – 15 %. Kalkulačka jej přičte k účtu a rozdělí mezi všechny.",
        },
      ],
    },
    en: {
      title: "Split the Bill – Bill Splitter and Tip Calculator",
      description:
        "Split a bill among several people equally, by items or by custom amounts. The calculator adds the tip and works out how much each person pays.",
      keywords:
        "split the bill, bill splitter calculator, cost per person, tip calculator, how much each person pays",
      faq: [
        {
          question: "How do I split a bill between several people?",
          answer:
            "Enter the total amount and the number of people. The calculator divides the amount equally, or by items or custom amounts, and shows how much each person pays.",
        },
        {
          question: "How is the tip calculated?",
          answer:
            "The tip is calculated as a percentage of the total bill. A common amount is 10 – 15%. The calculator adds it to the bill and splits it among everyone.",
        },
      ],
    },
    pl: {
      title: "Podział rachunku – kalkulator dzielenia rachunku i napiwku",
      description:
        "Podziel rachunek między kilka osób równo, według pozycji lub własnych kwot. Kalkulator dolicza napiwek i oblicza kwotę na osobę.",
      keywords:
        "podział rachunku, kalkulator dzielenia rachunku, koszt na osobę, kalkulator napiwku, ile płaci każdy",
      faq: [
        {
          question: "Jak podzielić rachunek między kilka osób?",
          answer:
            "Wpisz całkowitą kwotę i liczbę osób. Kalkulator dzieli kwotę równo, ewentualnie według pozycji lub własnych kwot, i pokazuje, ile płaci każdy.",
        },
        {
          question: "Jak oblicza się napiwek?",
          answer:
            "Napiwek oblicza się jako procent całkowitej kwoty rachunku. Zwykle daje się 10 – 15%. Kalkulator dolicza go do rachunku i dzieli między wszystkich.",
        },
      ],
    },
    hu: {
      title: "Számla felosztása – számlaosztó és borravaló-kalkulátor",
      description:
        "Ossza fel a számlát több ember között egyenlően, tételek vagy egyedi összegek szerint. A kalkulátor hozzáadja a borravalót és kiszámítja a fejenkénti összeget.",
      keywords:
        "számla felosztása, számlaosztó kalkulátor, fejenkénti összeg, borravaló kalkulátor, ki mennyit fizet",
      faq: [
        {
          question: "Hogyan osszam fel a számlát több ember között?",
          answer:
            "Adja meg a teljes összeget és a személyek számát. A kalkulátor egyenlően osztja el az összeget, vagy tételek, illetve egyedi összegek szerint, és megmutatja, ki mennyit fizet.",
        },
        {
          question: "Hogyan számítják a borravalót?",
          answer:
            "A borravalót a teljes számla százalékában számítják. Általában 10 – 15% szokásos. A kalkulátor hozzáadja a számlához és felosztja mindenki között.",
        },
      ],
    },
  },

  "area-volume": {
    sk: {
      title: "Výpočet obsahu a objemu – kalkulačka plôch a telies",
      description:
        "Vypočítajte obsah a obvod 2D útvarov aj objem a povrch 3D telies. Štvorec, obdĺžnik, kruh, trojuholník, kocka, valec, guľa a ďalšie tvary.",
      keywords:
        "výpočet obsahu, výpočet objemu, plocha útvaru, objem telesa, geometrická kalkulačka",
      faq: [
        {
          question: "Aké tvary kalkulačka podporuje?",
          answer:
            "Podporuje bežné 2D útvary (štvorec, obdĺžnik, kruh, trojuholník a ďalšie) aj 3D telesá (kocka, kváder, valec, guľa, kužeľ). Stačí vybrať tvar a zadať rozmery.",
        },
        {
          question: "V akých jednotkách sú výsledky?",
          answer:
            "Výsledky sú v tých istých jednotkách ako zadané rozmery: obsah v druhej mocnine (napr. m²), objem v tretej mocnine (napr. m³). Používajte rovnaké jednotky pre všetky rozmery.",
        },
      ],
    },
    cs: {
      title: "Výpočet obsahu a objemu – kalkulačka ploch a těles",
      description:
        "Spočítejte obsah a obvod 2D útvarů i objem a povrch 3D těles. Čtverec, obdélník, kruh, trojúhelník, krychle, válec, koule a další tvary.",
      keywords:
        "výpočet obsahu, výpočet objemu, plocha útvaru, objem tělesa, geometrická kalkulačka",
      faq: [
        {
          question: "Jaké tvary kalkulačka podporuje?",
          answer:
            "Podporuje běžné 2D útvary (čtverec, obdélník, kruh, trojúhelník a další) i 3D tělesa (krychle, kvádr, válec, koule, kužel). Stačí vybrat tvar a zadat rozměry.",
        },
        {
          question: "V jakých jednotkách jsou výsledky?",
          answer:
            "Výsledky jsou ve stejných jednotkách jako zadané rozměry: obsah ve druhé mocnině (např. m²), objem ve třetí mocnině (např. m³). Používejte stejné jednotky pro všechny rozměry.",
        },
      ],
    },
    en: {
      title: "Area and Volume Calculator – Shapes and Solids",
      description:
        "Calculate the area and perimeter of 2D shapes and the volume and surface of 3D solids: square, rectangle, circle, triangle, cube, cylinder, sphere and more.",
      keywords:
        "area calculator, volume calculator, shape area, solid volume, geometry calculator",
      faq: [
        {
          question: "Which shapes does the calculator support?",
          answer:
            "It supports common 2D shapes (square, rectangle, circle, triangle and more) and 3D solids (cube, cuboid, cylinder, sphere, cone). Just pick a shape and enter the dimensions.",
        },
        {
          question: "What units are the results in?",
          answer:
            "Results are in the same units as the dimensions you enter: area is squared (e.g. m²) and volume is cubed (e.g. m³). Use the same unit for all dimensions.",
        },
      ],
    },
    pl: {
      title: "Pole i objętość – kalkulator figur i brył",
      description:
        "Oblicz pole i obwód figur 2D oraz objętość i powierzchnię brył 3D: kwadrat, prostokąt, koło, trójkąt, sześcian, walec, kula i inne.",
      keywords:
        "kalkulator pola, kalkulator objętości, pole figury, objętość bryły, kalkulator geometryczny",
      faq: [
        {
          question: "Jakie figury obsługuje kalkulator?",
          answer:
            "Obsługuje popularne figury 2D (kwadrat, prostokąt, koło, trójkąt i inne) oraz bryły 3D (sześcian, prostopadłościan, walec, kula, stożek). Wystarczy wybrać figurę i podać wymiary.",
        },
        {
          question: "W jakich jednostkach są wyniki?",
          answer:
            "Wyniki są w tych samych jednostkach co podane wymiary: pole w kwadracie (np. m²), objętość w sześcianie (np. m³). Używaj tych samych jednostek dla wszystkich wymiarów.",
        },
      ],
    },
    hu: {
      title: "Terület- és térfogatszámítás – síkidomok és testek",
      description:
        "Számítsa ki a 2D síkidomok területét és kerületét, valamint a 3D testek térfogatát és felszínét: négyzet, téglalap, kör, háromszög, kocka, henger, gömb és több.",
      keywords:
        "területszámítás, térfogatszámítás, síkidom területe, test térfogata, geometriai kalkulátor",
      faq: [
        {
          question: "Milyen alakzatokat támogat a kalkulátor?",
          answer:
            "Támogatja a gyakori 2D síkidomokat (négyzet, téglalap, kör, háromszög és több) és a 3D testeket (kocka, téglatest, henger, gömb, kúp). Csak válassza ki az alakzatot és adja meg a méreteket.",
        },
        {
          question: "Milyen mértékegységben vannak az eredmények?",
          answer:
            "Az eredmények ugyanolyan egységben vannak, mint a megadott méretek: a terület négyzeten (pl. m²), a térfogat köbön (pl. m³). Használjon azonos egységet minden mérethez.",
        },
      ],
    },
  },

  "unit-converter": {
    sk: {
      title: "Prevodník jednotiek – dĺžka, hmotnosť, objem, teplota",
      description:
        "Prevádzajte jednotky dĺžky, hmotnosti, objemu, plochy a teploty. Metre na míle, kilogramy na libry, litre na galóny, Celzius na Fahrenheit a ďalšie.",
      keywords:
        "prevodník jednotiek, prevod jednotiek, km na míle, kg na libry, Celzius na Fahrenheit",
      faq: [
        {
          question: "Aké jednotky viem previesť?",
          answer:
            "Prevediete dĺžku, hmotnosť, objem, plochu a teplotu. Vyberte kategóriu, zvoľte zdrojovú a cieľovú jednotku a zadajte hodnotu — prevod prebehne automaticky.",
        },
        {
          question: "Ako prevediem Celzius na Fahrenheit?",
          answer:
            "V kategórii teplota vyberte °C ako zdrojovú a °F ako cieľovú jednotku. Vzorec je °F = °C × 9/5 + 32. Kalkulačka výsledok vypočíta okamžite.",
        },
      ],
    },
    cs: {
      title: "Převodník jednotek – délka, hmotnost, objem, teplota",
      description:
        "Převádějte jednotky délky, hmotnosti, objemu, plochy a teploty. Metry na míle, kilogramy na libry, litry na galony, Celsius na Fahrenheit a další.",
      keywords:
        "převodník jednotek, převod jednotek, km na míle, kg na libry, Celsius na Fahrenheit",
      faq: [
        {
          question: "Jaké jednotky mohu převést?",
          answer:
            "Převedete délku, hmotnost, objem, plochu a teplotu. Vyberte kategorii, zvolte zdrojovou a cílovou jednotku a zadejte hodnotu — převod proběhne automaticky.",
        },
        {
          question: "Jak převedu Celsius na Fahrenheit?",
          answer:
            "V kategorii teplota vyberte °C jako zdrojovou a °F jako cílovou jednotku. Vzorec je °F = °C × 9/5 + 32. Kalkulačka výsledek spočítá okamžitě.",
        },
      ],
    },
    en: {
      title: "Unit Converter – Length, Weight, Volume, Temperature",
      description:
        "Convert units of length, weight, volume, area and temperature. Metres to miles, kilograms to pounds, litres to gallons, Celsius to Fahrenheit and more.",
      keywords:
        "unit converter, convert units, km to miles, kg to pounds, Celsius to Fahrenheit",
      faq: [
        {
          question: "Which units can I convert?",
          answer:
            "You can convert length, weight, volume, area and temperature. Pick a category, choose the source and target unit and enter a value — the conversion happens automatically.",
        },
        {
          question: "How do I convert Celsius to Fahrenheit?",
          answer:
            "In the temperature category, select °C as the source and °F as the target unit. The formula is °F = °C × 9/5 + 32. The calculator computes the result instantly.",
        },
      ],
    },
    pl: {
      title: "Przelicznik jednostek – długość, masa, objętość, temperatura",
      description:
        "Przeliczaj jednostki długości, masy, objętości, powierzchni i temperatury. Metry na mile, kilogramy na funty, litry na galony, Celsjusz na Fahrenheita i więcej.",
      keywords:
        "przelicznik jednostek, przeliczanie jednostek, km na mile, kg na funty, Celsjusz na Fahrenheita",
      faq: [
        {
          question: "Jakie jednostki mogę przeliczyć?",
          answer:
            "Przeliczysz długość, masę, objętość, powierzchnię i temperaturę. Wybierz kategorię, źródłową i docelową jednostkę oraz wpisz wartość — przeliczenie nastąpi automatycznie.",
        },
        {
          question: "Jak przeliczyć Celsjusza na Fahrenheita?",
          answer:
            "W kategorii temperatura wybierz °C jako źródłową i °F jako docelową jednostkę. Wzór to °F = °C × 9/5 + 32. Kalkulator obliczy wynik natychmiast.",
        },
      ],
    },
    hu: {
      title: "Mértékegység-átváltó – hossz, tömeg, térfogat, hőmérséklet",
      description:
        "Váltson át hossz-, tömeg-, térfogat-, terület- és hőmérséklet-egységeket. Méter mérföldre, kilogramm fontra, liter gallonra, Celsius Fahrenheitre és több.",
      keywords:
        "mértékegység átváltó, egységátváltás, km mérföldre, kg fontra, Celsius Fahrenheitre",
      faq: [
        {
          question: "Milyen egységeket válthatok át?",
          answer:
            "Átválthat hosszt, tömeget, térfogatot, területet és hőmérsékletet. Válasszon kategóriát, forrás- és célegységet, majd adjon meg egy értéket — az átváltás automatikusan megtörténik.",
        },
        {
          question: "Hogyan váltok Celsiust Fahrenheitre?",
          answer:
            "A hőmérséklet kategóriában válassza a °C-ot forrásként és a °F-ot célként. A képlet: °F = °C × 9/5 + 32. A kalkulátor azonnal kiszámítja az eredményt.",
        },
      ],
    },
  },

  basic: {
    sk: {
      title: "Online kalkulačka – základné počítanie a pamäť",
      description:
        "Jednoduchá online kalkulačka na sčítanie, odčítanie, násobenie a delenie. Percentá, odmocnina, druhá mocnina, pamäť a história výpočtov.",
      keywords:
        "online kalkulačka, základná kalkulačka, kalkulačka na počítanie, kalkulačka s pamäťou, kalkulačka percent",
      faq: [
        {
          question: "Čo všetko kalkulačka dokáže?",
          answer:
            "Zvláda štyri základné operácie, percentá, odmocninu, druhú mocninu a prevrátenú hodnotu. Má aj pamäť (M+, M-, MR) a ukladá históriu výpočtov.",
        },
        {
          question: "Dá sa ovládať klávesnicou?",
          answer:
            "Áno. Číslice a operátory (+, -, *, /) zadávate priamo z klávesnice, Enter alebo = vypočíta výsledok a Escape kalkulačku vynuluje.",
        },
      ],
    },
    cs: {
      title: "Online kalkulačka – základní počítání a paměť",
      description:
        "Jednoduchá online kalkulačka na sčítání, odčítání, násobení a dělení. Procenta, odmocnina, druhá mocnina, paměť a historie výpočtů.",
      keywords:
        "online kalkulačka, základní kalkulačka, kalkulačka na počítání, kalkulačka s pamětí, kalkulačka procent",
      faq: [
        {
          question: "Co všechno kalkulačka umí?",
          answer:
            "Zvládá čtyři základní operace, procenta, odmocninu, druhou mocninu a převrácenou hodnotu. Má i paměť (M+, M-, MR) a ukládá historii výpočtů.",
        },
        {
          question: "Lze ji ovládat klávesnicí?",
          answer:
            "Ano. Číslice a operátory (+, -, *, /) zadáváte přímo z klávesnice, Enter nebo = spočítá výsledek a Escape kalkulačku vynuluje.",
        },
      ],
    },
    en: {
      title: "Online Calculator – Basic Math and Memory",
      description:
        "A simple online calculator for addition, subtraction, multiplication and division. Percentages, square root, square, memory and calculation history.",
      keywords:
        "online calculator, basic calculator, simple calculator, calculator with memory, percentage calculator",
      faq: [
        {
          question: "What can the calculator do?",
          answer:
            "It handles the four basic operations, percentages, square root, square and reciprocal. It also has memory (M+, M-, MR) and keeps a history of your calculations.",
        },
        {
          question: "Can I use the keyboard?",
          answer:
            "Yes. Type digits and operators (+, -, *, /) directly on the keyboard, press Enter or = to get the result and Escape to clear the calculator.",
        },
      ],
    },
    pl: {
      title: "Kalkulator online – podstawowe obliczenia i pamięć",
      description:
        "Prosty kalkulator online do dodawania, odejmowania, mnożenia i dzielenia. Procenty, pierwiastek, kwadrat, pamięć i historia obliczeń.",
      keywords:
        "kalkulator online, podstawowy kalkulator, prosty kalkulator, kalkulator z pamięcią, kalkulator procentów",
      faq: [
        {
          question: "Co potrafi kalkulator?",
          answer:
            "Obsługuje cztery podstawowe działania, procenty, pierwiastek kwadratowy, kwadrat i odwrotność. Ma też pamięć (M+, M-, MR) i zapisuje historię obliczeń.",
        },
        {
          question: "Czy można obsługiwać go klawiaturą?",
          answer:
            "Tak. Cyfry i operatory (+, -, *, /) wpisujesz bezpośrednio z klawiatury, Enter lub = oblicza wynik, a Escape zeruje kalkulator.",
        },
      ],
    },
    hu: {
      title: "Online számológép – alapműveletek és memória",
      description:
        "Egyszerű online számológép összeadáshoz, kivonáshoz, szorzáshoz és osztáshoz. Százalék, négyzetgyök, négyzet, memória és számítási előzmények.",
      keywords:
        "online számológép, alap számológép, egyszerű számológép, memóriás számológép, százalék számológép",
      faq: [
        {
          question: "Mit tud a számológép?",
          answer:
            "Kezeli a négy alapműveletet, a százalékot, a négyzetgyököt, a négyzetre emelést és a reciprokot. Van memóriája is (M+, M-, MR) és menti a számítási előzményeket.",
        },
        {
          question: "Használható billentyűzettel?",
          answer:
            "Igen. A számjegyeket és a műveleti jeleket (+, -, *, /) közvetlenül a billentyűzetről adhatja meg, az Enter vagy = kiszámítja az eredményt, az Escape pedig lenullázza a számológépet.",
        },
      ],
    },
  },
};
