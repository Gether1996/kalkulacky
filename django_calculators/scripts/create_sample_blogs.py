"""
Create sample blog posts for testing

Run with: docker compose exec backend python manage.py shell < create_sample_blogs.py
"""

from calculators.models import BlogCategory, BlogPost
from datetime import datetime

# Create categories
categories_data = [
    {
        'name': 'Dane 2026',
        'slug': 'dane-2026',
        'description': 'Zmeny v daňovej legislatíve pre rok 2026',
        'color': '#DC2626',
        'icon': '📊',
        'order': 1
    },
    {
        'name': 'Kalkulačky návody',
        'slug': 'kalkulacky-navody',
        'description': 'Ako používať naše kalkulačky',
        'color': '#2563EB',
        'icon': '🧮',
        'order': 2
    },
    {
        'name': 'Slovenské financie',
        'slug': 'slovenske-financie',
        'description': 'Tipy a triky pre vaše peniaze',
        'color': '#16A34A',
        'icon': '💰',
        'order': 3
    }
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = BlogCategory.objects.get_or_create(
        slug=cat_data['slug'],
        defaults=cat_data
    )
    if created:
        print(f"✅ Created category: {category.name}")
    else:
        print(f"ℹ️  Category already exists: {category.name}")

# Get category instances
dane_cat = BlogCategory.objects.get(slug='dane-2026')
kalkulacky_cat = BlogCategory.objects.get(slug='kalkulacky-navody')
financie_cat = BlogCategory.objects.get(slug='slovenske-financie')

# Create blog posts
posts_data = [
    {
        'title': 'Progresívne zdanenie 2026: Ako ovplyvní vašu mzdu?',
        'slug': 'progresivne-zdanenie-2026',
        'category': dane_cat,
        'excerpt': 'Od roku 2026 sa na Slovensku zavádza progresívne zdanenie so 4 sadzbami. Zistite, koľko zaplatíte na daniach a ako sa to odrazí vo vašej čistej mzde.',
        'content_html': '''
<h2>Nové sadzby dane z príjmu</h2>
<p>Od 1. januára 2026 sa na Slovensku mení systém zdaňovania príjmov fyzických osôb. Prechádza sa z dvojstupňového na štvorstupňové progresívne zdanenie.</p>

<h3>Aktuálne sadzby pre rok 2026:</h3>
<table>
    <thead>
        <tr>
            <th>Sadzba</th>
            <th>Základ dane (ročne)</th>
            <th>Základ dane (mesačne)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>19%</strong></td>
            <td>do 43 983,32 EUR</td>
            <td>do 3 665,28 EUR</td>
        </tr>
        <tr>
            <td><strong>25%</strong></td>
            <td>43 983,33 - 60 349,21 EUR</td>
            <td>3 665,29 - 5 029,10 EUR</td>
        </tr>
        <tr>
            <td><strong>30%</strong></td>
            <td>60 349,22 - 75 010,32 EUR</td>
            <td>5 029,11 - 6 250,86 EUR</td>
        </tr>
        <tr>
            <td><strong>35%</strong></td>
            <td>nad 75 010,32 EUR</td>
            <td>nad 6 250,86 EUR</td>
        </tr>
    </tbody>
</table>

<h3>Čo to znamená pre vás?</h3>
<p>Pri hrubej mzde <strong>1 500 EUR</strong> mesačne:</p>
<ul>
    <li>Sociálne poistenie: <strong>201 EUR</strong> (13,4%)</li>
    <li>Zdravotné poistenie: <strong>97,50 EUR</strong> (6,5%)</li>
    <li>Daňový základ: <strong>1 201,50 EUR</strong></li>
    <li>Nezdaniteľná časť (NČZD): <strong>-381,61 EUR</strong></li>
    <li>Zdaniteľný základ: <strong>819,89 EUR</strong></li>
    <li>Daň (19%): <strong>155,78 EUR</strong></li>
    <li><strong>Čistá mzda: 1 045,72 EUR</strong> (69,7%)</li>
</ul>

<h3>Nezdaniteľná časť základu dane (NČZD)</h3>
<p>Každý zamestnanec má nárok na nezdaniteľnú časť základu dane vo výške <strong>4 579,26 EUR ročne</strong> (381,61 EUR mesačne). Táto suma sa odpočítava od daňového základu PRED výpočtom dane.</p>

<h3>Daňový bonus na deti</h3>
<p>Rodičia s vyživovanými deťmi majú nárok na daňový bonus:</p>
<ul>
    <li><strong>50 EUR mesačne</strong> na jedno dieťa (zjednodušene)</li>
    <li>Bonus sa odpočítava od vypočítanej dane</li>
    <li>Daň sa nemôže stať zápornou</li>
</ul>

<h2>Vyskúšajte si výpočet</h2>
<p>Použite našu <a href="/calculator/salary">kalkulačku čistej mzdy</a>, kde môžete zadať svoju hrubú mzdu a počet vyživovaných detí. Kalkulačka vám presne vypočíta čistú mzdu podľa nových pravidiel 2026.</p>
        ''',
        'meta_keywords': 'progresívne zdanenie, dane 2026, čistá mzda, NČZD, daňový bonus',
        'related_calculator': 'salary',
        'tags': 'dane, 2026, progresívne zdanenie, mzda',
        'status': 'published',
        'published_at': datetime.now()
    },
    {
        'title': 'Ako používať kalkulačku čistej mzdy',
        'slug': 'ako-pouzivat-kalkulacku-cistej-mzdy',
        'category': kalkulacky_cat,
        'excerpt': 'Naučte sa správne používať našu kalkulačku čistej mzdy a pochopte všetky položky vo výpočte.',
        'content_html': '''
<h2>Krok za krokom</h2>
<p>Kalkulačka čistej mzdy vám pomôže zistiť, koľko peňazí skutočne dostanete na účet po odpočítaní všetkých odvodov a daní.</p>

<h3>1. Zadajte hrubú mzdu</h3>
<p>Do prvého poľa zadajte vašu <strong>hrubú mesačnú mzdu</strong> v eurách. To je suma uvedená vo vašej pracovnej zmluve.</p>

<h3>2. Zadajte počet detí (voliteľné)</h3>
<p>Ak máte vyživované deti, zadajte ich počet. Za každé dieťa získate daňový bonus <strong>50 EUR mesačne</strong>.</p>

<h3>3. Interpretácia výsledkov</h3>
<p>Kalkulačka vám zobrazí:</p>
<ul>
    <li><strong>Sociálne poistenie (13,4%):</strong> Odvod na dôchodkové, nemocenské a úrazové poistenie</li>
    <li><strong>Zdravotné poistenie (6,5%):</strong> Odvod do zdravotnej poisťovne</li>
    <li><strong>Daňový základ:</strong> Hrubá mzda mínus odvody</li>
    <li><strong>NČZD:</strong> Nezdaniteľná časť, ktorá sa odpočíta pred zdanením</li>
    <li><strong>Zdaniteľný základ:</strong> Suma, z ktorej sa počíta daň</li>
    <li><strong>Daň z príjmu:</strong> Vypočítaná podľa progresívnych sadzieb</li>
    <li><strong>Daňový bonus:</strong> Zľava na dani za deti</li>
    <li><strong>Čistá mzda:</strong> Konečná suma na vašom účte</li>
</ul>

<h2>Praktický príklad</h2>
<p>Pri hrubej mzde <strong>2 000 EUR</strong> a <strong>2 deťoch</strong>:</p>
<pre>
Hrubá mzda:           2 000,00 EUR
- Sociálne:            -268,00 EUR
- Zdravotné:           -130,00 EUR
= Daňový základ:      1 602,00 EUR
- NČZD:                -381,61 EUR
= Zdaniteľný základ:  1 220,39 EUR
- Daň (19%):           -231,87 EUR
+ Bonus (2 deti):      +100,00 EUR
= Daň po bonuse:       -131,87 EUR
────────────────────────────────
ČISTÁ MZDA:          1 470,13 EUR (73,5%)
</pre>

<h2>Tipy</h2>
<ul>
    <li>Používajte posuvník pre rýchle porovnanie rôznych miezd</li>
    <li>Benchmark tlačidlá vám ponúknu typické mzdové úrovne na Slovensku</li>
    <li>Efektívna miera zdanenia ukazuje, koľko % z hrubej mzdy idete skutočne na odvody a dane</li>
</ul>

<a href="/calculator/salary" style="display: inline-block; padding: 12px 24px; background: #3B82F6; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; margin-top: 20px;">Otvoriť kalkulačku →</a>
        ''',
        'meta_keywords': 'kalkulačka mzdy, návod, čistá mzda, hrubá mzda',
        'related_calculator': 'salary',
        'tags': 'návod, kalkulačka, mzda, tutoriál',
        'status': 'published',
        'published_at': datetime.now()
    },
    {
        'title': 'Ako ušetriť na daniach v roku 2026',
        'slug': 'ako-usetrit-na-daniach-2026',
        'category': financie_cat,
        'excerpt': 'Praktické tipy ako legálne znížiť svoju daňovú záťaž a získať späť viac peňazí.',
        'content_html': '''
<h2>Legálne spôsoby ako platiť menej na daniach</h2>
<p>V tomto článku sa dozviete, ako môžete legálne optimalizovať svoju daňovú záťaž a ušetriť peniaze.</p>

<h3>1. Využite daňový bonus na deti</h3>
<p>Ak máte vyživované deti, máte nárok na daňový bonus:</p>
<ul>
    <li>Do 6 rokov: približne <strong>70 EUR mesačne</strong></li>
    <li>Od 6 do 15 rokov: približne <strong>50 EUR mesačne</strong></li>
    <li>Nad 15 rokov: približne <strong>25 EUR mesačne</strong></li>
</ul>
<p><em>Poznámka: Naša kalkulačka používa zjednodušenú sadzbu 50 EUR/mesiac</em></p>

<h3>2. Príspevky na doplnkové dôchodkové sporenie (DDS)</h3>
<p>Príspevky na DDS si môžete odpočítať od základu dane až do výšky <strong>180 EUR ročne</strong>. Štát vám navyše prispeje bonusom až <strong>66 EUR ročne</strong>.</p>

<h3>3. Daňovo uznateľné výdavky pre SZČO</h3>
<p>Ak ste podnikateľ, môžete si uplatniť:</p>
<ul>
    <li>Paušálne výdavky (40-60% z príjmov)</li>
    <li>Reálne výdavky spojené s podnikaním</li>
    <li>Odpisy majetku</li>
</ul>

<h3>4. Nehnuteľnosti a hypotéky</h3>
<p>Ak vlastníte nehnuteľnosť:</p>
<ul>
    <li>Úroky z hypotéky na vlastné bývanie nie sú daňovo uznateľné pre zamestnancov</li>
    <li>Prenájom nehnuteľnosti je zdanený samostatne</li>
</ul>

<h2>Kalkulátory, ktoré vám pomôžu</h2>
<p>Využite naše kalkulačky pre lepšie plánovanie:</p>
<ul>
    <li><a href="/calculator/salary">Kalkulačka čistej mzdy</a> - Zistite, koľko zarobíte netto</li>
    <li><a href="/calculator/mortgage">Kalkulačka hypotéky</a> - Vypočítajte splátky úveru</li>
</ul>

<blockquote>
    <strong>Dôležité:</strong> Vždy konzultujte konkrétne daňové otázky s daňovým poradcom. Tento článok poskytuje len všeobecné informácie.
</blockquote>
        ''',
        'meta_keywords': 'ušetriť na daniach, daňové tipy, DDS, daňový bonus, optimalizácia daní',
        'related_calculator': '',
        'tags': 'dane, úspory, tipy, slovensko, DDS',
        'status': 'published',
        'published_at': datetime.now()
    }
]

print("\nCreating blog posts...")
for post_data in posts_data:
    post, created = BlogPost.objects.get_or_create(
        slug=post_data['slug'],
        defaults=post_data
    )
    if created:
        print(f"✅ Created post: {post.title}")
    else:
        print(f"ℹ️  Post already exists: {post.title}")

print("\n✅ Sample blog data created successfully!")
print("\nYou can now:")
print("1. Visit http://localhost:4200/blog to see the blog list")
print("2. Click on any post to read the full content")
print("3. Navigate to calculators from blog posts")
