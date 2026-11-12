# Public Transport Passenger Analytics System

**Jamoat transporti yo‘lovchilarini tahlil qilish tizimi** — to‘rtta AQSh jamoat transporti agentligining yo‘nalish kesimidagi yo‘lovchilar va qatnov ko‘rsatkichlarini taqqoslash uchun o‘quv-tahliliy web-ilova.

## Dataset

Berrebi, S., Joshi, S. & Watkins, K. E. *Route-Level Ridership and Frequency Data in Four Transit Agencies (STRIDE project A2)*. Zenodo, 2020. DOI: [10.5281/zenodo.3758777](https://doi.org/10.5281/zenodo.3758777).

Manba fayllari `data/raw/` papkasida saqlanadi:
- `MARTA_Route.csv`
- `TRIMET_Route.csv`
- `MIAMI_DADE_Route.csv`
- `METRO_TRANSIT_Route.csv`

Dataset tavsifiga ko‘ra, ma’lumotlar TriMet, Metro Transit, Miami-Dade Transit va MARTA agentliklarida 2012–2018 oralig‘idagi weekday (ish kuni) yo‘lovchi boardings va vehicle-trips ko‘rsatkichlarini route darajasida jamlaydi. CSV ustunlaridagi `12` va `17` qo‘shimchalari manbaning davr belgilari; ularni barcha agentliklar uchun aynan 2012 va 2017 kalendar yili deb talqin qilish mumkin emas. Masalan, MARTA faylida markup sanalari `May-14` va `Apr-18` ko‘rinishida.

## Funksiyalar

- 4 agentlik ma’lumotlarini yagona standart long formatga o‘tkazish.
- Agentlik, davr va ko‘rsatkich bo‘yicha interaktiv filtrlash.
- `SUMons`, `AVGons`, `AVGtrips`, `AVGonPERtrip`, bekatlar sonini ko‘rish.
- Agentliklar va davrlar kesimida taqqoslash.
- Yo‘nalishlar reytingi va taqsimot grafiklari.
- Boshlang‘ich (`12`) va taqqoslash (`17`) davrlari orasidagi farqni hisoblash.
- Filtrlangan ma’lumotlarni CSV formatida yuklab olish.
- Dataset sifati bo‘yicha qisqa hisobot.

## Texnologiyalar

Python 3.11, Pandas, Streamlit, Plotly, SQLite, Docker, PlantUML, Pytest, Google Cloud Run va ixtiyoriy Cloud Storage.

## Papka tuzilmasi

```text
public_transport_passenger_analytics/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── data/raw/                 # 4 ta original CSV
├── src/data_processing.py   # yuklash va normalizatsiya
├── database/schema.sql      # SQLite sxemasi
├── database/build_db.py     # DB yaratish skripti
├── diagrams/                # PlantUML diagrammalar
├── docs/                    # hisobot va deploy qo‘llanmasi
├── scripts/                 # GCP deploy skripti
└── tests/                   # avtomatik testlar
```

## Lokal ishga tushirish (Windows)

1. Python 3.11 o‘rnating.
2. ZIP arxivni oching va loyiha papkasini VS Code yoki terminalda oching.
3. Virtual muhit yarating:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Kutubxonalarni o‘rnating:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Dashboardni ishga tushiring:

```powershell
streamlit run app.py
```

Brauzerda odatda `http://localhost:8501` ochiladi.

## SQLite bazasini yaratish

```powershell
python database/build_db.py
```

Natijada `database/transport_analytics.db` yaratiladi. Dashboard SQLite bazasidan o‘qiydi. Agar DB mavjud bo‘lmasa, ilova ishga tushganda `database/build_db.py` orqali CSV manbalaridan avtomatik yaratadi.

## Testlar

```powershell
pytest -q
```

## Docker orqali ishga tushirish

```powershell
docker compose up --build
```

Brauzer: `http://localhost:8501`.

## Google Cloud Run deployment

Talablar: Google Cloud akkaunti, billing yoqilgan loyiha, `gcloud` CLI va Docker. Cloud Run ishlatilishiga qarab xarajat bo‘lishi mumkin; billing budjeti va limitlarini sozlang.

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
gcloud run deploy public-transport-analytics \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --min 0 \
  --max 2
```

Deploy yakunida terminal bergan HTTPS URL ni ochib tekshiring. Bu loyiha hozircha CSV fayllarni konteyner ichidan o‘qiydi. Cloud Run konteyner fayl tizimi doimiy saqlash uchun mo‘ljallanmagan; production holatida CSV fayllarni Cloud Storage bucket'dan o‘qish yoki boshqariladigan DB ishlatish tavsiya etiladi. Ushbu topshiriqning kichik, o‘quviy versiyasi uchun Cloud SQL/BigQuery majburiy emas.

## GitHub'ga joylash

```bash
git init
git add .
git commit -m "Initial Public Transport Passenger Analytics System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/public-transport-passenger-analytics-system.git
git push -u origin main
```

GitHub repository Settings → Collaborators → Add people orqali `Supervisor` username'ini qidirib, o‘qituvchini taklif qiling. Email bo‘yicha taklif qilish faqat GitHub akkauntiga bog‘langan email mos bo‘lsa ishlaydi. Repository URL'ni topshiriqda ko‘rsating.

## Muhim metodologik cheklovlar

- Bu dataset kunlik vaqt qatori yoki real-time GPS oqimi emas; route-level davr agregatlari.
- Dataset tavsifida weekday total daily passenger boardings va vehicle-trips ko‘rsatkichlari jamlangani aytiladi.
- `SUMons` va `AVGons` kabi source nomlari saqlangan; ularning birlik va hisoblash talqini manba tadqiqotidagi metodologiya bilan birga tushuntirilishi kerak.
- Turli agentliklarning qamrovi, markup sanasi va yo‘nalish soni farq qiladi. Ularning xom yig‘indilarini aholi soni yoki bozor ulushi kabi talqin qilmang.
- Bu loyiha transport yo‘lovchilari tahlili bo‘lib, chipta narxi yoki real-time marshrut kuzatuvini o‘z ichiga olmaydi.

## Diagrammalar

`diagrams/` ichidagi `.puml` fayllarni PlantUML serveri, VS Code PlantUML kengaytmasi yoki PlantUML desktop vositasi bilan render qiling.
