# PUBLIC TRANSPORT PASSENGER ANALYTICS SYSTEM
## Jamoat transporti yo‘lovchilarini tahlil qilish tizimi

### 1. Loyiha haqida umumiy ma’lumot

Ushbu loyiha to‘rtta jamoat transporti agentligining yo‘nalish darajasidagi yo‘lovchi oqimi va transport qatnovlari ko‘rsatkichlarini qayta ishlash, taqqoslash hamda vizual ko‘rinishda taqdim etish uchun ishlab chiqiladi. Tizim foydalanuvchiga agentlik, yo‘nalish va manba davri bo‘yicha ma’lumotlarni filtrlash, statistik ko‘rsatkichlarni ko‘rish va CSV hisobotni yuklab olish imkonini beradi.

### 2. Muammoning qo‘yilishi

Transportni rejalashtirishda qaysi yo‘nalishlarda yo‘lovchi oqimi yuqoriroq ekanini, xizmat chastotasi bilan yo‘lovchilar ko‘rsatkichi qanday bog‘liqligini va vaqt o‘tishi bilan ko‘rsatkichlar qanday o‘zgarganini tahlil qilish muhim. Turli agentliklarning ma’lumotlari alohida CSV fayllarda berilganligi sababli ularni yagona formatga keltirish va taqqoslash zarur.

### 3. Maqsad va vazifalar

**Maqsad:** route-level yo‘lovchilar va qatnov ma’lumotlarini yagona analitik tizimda jamlash va interaktiv dashboard orqali tahlil qilish.

**Vazifalar:**
- to‘rtta CSV faylni yuklash va tekshirish;
- agentlik va yo‘nalish identifikatorlarini standartlashtirish;
- 12 va 17 manba davrlarini long formatga o‘tkazish;
- ko‘rsatkichlarni agentlik, davr va yo‘nalish bo‘yicha guruhlash;
- interaktiv grafik va jadvallar yaratish;
- SQLite ma’lumotlar bazasi sxemasini yaratish;
- testlash va bulutga joylashtirishga tayyorlash.

### 4. Dataset tavsifi

Manba: Berrebi, Simon; Joshi, Sanskruti; Watkins, Kari E. (2020). *Route-Level Ridership and Frequency Data in Four Transit Agencies (STRIDE project A2)*. Zenodo. DOI: 10.5281/zenodo.3758777.

Fayllar: MARTA_Route.csv, TRIMET_Route.csv, MIAMI_DADE_Route.csv, METRO_TRANSIT_Route.csv. Tekshiruvda fayllarda mos ravishda 87, 80, 74 va 117 qator, jami 358 ta yo‘nalish yozuvi bor. Har bir faylda 13 ta ustun mavjud. Tekshiruvda bo‘sh katak va to‘liq takroriy qator aniqlanmadi. Har bir agentlik faylida yo‘nalish identifikatori ustuni o‘z nomiga ega: `route_id`, `route_number`, `QSTOPROUTE`, `line_id`.

Muhim izoh: ustunlardagi `12` va `17` qo‘shimchalari manba davr kodlari sifatida saqlanadi. Agentliklarning haqiqiy markup sanalari bir xil emas. Masalan, MARTA faylida `May-14` va `Apr-18`, TriMet faylida `1-Apr-12` va `1-Apr-17` ko‘rsatilgan. Shu sababli barcha agentliklar uchun bu davrlarni aynan 2012 va 2017 kalendar yillari deb ko‘rsatish noto‘g‘ri.

### 5. Ko‘rsatkichlar talqini

Manba tadqiqotida `Rid` yo‘lovchi boardings va alightings jami, `Freq` esa transport qatnovlari bilan bog‘langan. CSV dagi `SUMons` route-level jami yo‘lovchi ko‘rsatkichini ifodalaydi. Fayllar bo‘yicha `AVGons` qiymati `SUMons / Stops` nisbatiga, `AVGonPERtrip` esa `AVGons / AVGtrips` nisbatiga mos kelishi tekshirildi (kichik tafovutlar yaxlitlash sababli). Dashboard source ustun nomlarini saqlaydi va hisoblangan farqlarni ko‘rsatishda manba davrlarini (`12`, `17`) alohida belgilaydi.

### 6. Texnologiyalar

- Python 3.11 — dasturlash tili.
- Pandas — CSV ma’lumotlarni o‘qish, tozalash va standartlashtirish.
- Streamlit — web-dashboard.
- Plotly — interaktiv grafiklar.
- SQLite — relational ma’lumotlar bazasi.
- PlantUML — UML va ER diagrammalar.
- Docker — konteynerlash.
- Pytest — avtomatik testlar.
- Google Cloud Run — bulutli joylashtirish platformasi.

### 7. Dasturiy arxitektura

Tizim qatlamli arxitekturaga ega: ma’lumotlar manbasi, yuklash va normalizatsiya qatlami, ma’lumotlar bazasi, analitika qatlami va foydalanuvchi interfeysi. CSV fayllar `data/raw/` papkasida saqlanadi. `src/data_processing.py` turli nomdagi route identifikatorlarini `route_id` ga keltiradi va davr suffixlarini alohida yozuvlarga aylantiradi. Normallashtirilgan yozuvlar SQLite bazasiga saqlanadi. Streamlit foydalanuvchi filtrlarini qabul qiladi, SQLite orqali ma’lumotlarni o‘qib, Pandas yordamida agregatsiya qiladi va Plotly grafiklarini ko‘rsatadi.

### 8. UML diagrammalar

Loyiha tarkibida quyidagi PlantUML diagrammalari mavjud:
- `system_architecture.puml` — umumiy tizim arxitekturasi;
- `component_diagram.puml` — komponentlar va ularning bog‘lanishi;
- `use_case.puml` — foydalanuvchi imkoniyatlari;
- `activity_diagram.puml` — ma’lumotni yuklashdan natijani ko‘rsatishgacha bo‘lgan jarayon;
- `er_diagram.puml` — ma’lumotlar bazasi jadvallari va munosabatlari.

### 9. Ma’lumotlar bazasi

Ma’lumotlar bazasi uchta asosiy jadvaldan iborat:

**agency** — transport agentligi: `agency_id` (PK), `agency_code`, `agency_name`, `city_region`.

**route** — agentlikka tegishli yo‘nalish: `route_pk` (PK), `agency_id` (FK), `source_route_id`. `agency_id + source_route_id` kombinatsiyasi noyob.

**route_period** — muayyan yo‘nalishning manba davridagi ko‘rsatkichlari: `route_period_id` (PK), `route_pk` (FK), `period_code`, `summary_begin_date`, `stops`, `avg_on_per_trip`, `avg_trips`, `sum_ons`, `avg_ons`, `source_file`. `route_pk + period_code` kombinatsiyasi noyob.

Bog‘lanish: bitta agentlikda ko‘plab yo‘nalishlar bo‘lishi mumkin; bitta yo‘nalishda esa ikki manba davri bo‘yicha ko‘rsatkichlar saqlanadi.

### 10. Tizim funksiyalari

- agentlik va davr filtrlari;
- umumiy KPI ko‘rsatkichlari;
- agentliklar bo‘yicha taqqoslash;
- yo‘nalishlar reytingi;
- `SUMons`, `AVGons`, `AVGtrips`, `AVGonPERtrip`, bekatlar soni bo‘yicha grafiklar;
- boshlang‘ich va taqqoslash davrlari o‘rtasidagi mutlaq va foizli farq;
- ma’lumotlar sifati jadvali;
- filtrlangan natijani CSV shaklida yuklab olish.

### 11. Cheklovlar va to‘g‘ri talqin

Dataset kunlik yoki soatlik alohida vaqt qatorini bermaydi; u route-level markup/davr agregatlaridan iborat. Shu sababli dashboard kunlik/soatlik trend yoki real-time monitoring deb taqdim etilmaydi. Turli agentliklarning hududi, yo‘nalishlar qamrovi va kuzatuv davri farq qiladi. Xom yig‘indilarni bevosita bozor ulushi yoki aholi jon boshiga ko‘rsatkich deb talqin qilish mumkin emas. `SUMons` va `AVGons` source ustun nomlari saqlanadi; ularning aniq metodologik ta’rifi datasetni qo‘llab-quvvatlagan tadqiqot bilan izohlanadi.

### 12. GitHub va Google Cloud Platform

Loyiha GitHub repository sifatida `public-transport-passenger-analytics-system` nomi bilan joylashtirilishi mumkin. Repository yaratilgach, `git init`, `git add`, `git commit`, `git remote add` va `git push` buyruqlari bajariladi. O‘qituvchiga kirish berish uchun GitHub repository Settings → Collaborators orqali `Supervisor` foydalanuvchisi taklif qilinadi.

Bulutli joylashtirish uchun Cloud Run konteynerli web-ilovani ishga tushiradi. Cloud Build/Artifact Registry build jarayonida yordam beradi. Cloud Storage xom CSV fayllarni alohida saqlash uchun ixtiyoriy. Kichik o‘quv loyihasida BigQuery yoki Cloud SQL majburiy emas. Cloud xizmatlari uchun billing talab qilinishi va foydalanishga qarab xarajat yuzaga kelishi mumkin.

### 13. Ishga tushirish

```bash
python -m venv .venv
pip install -r requirements.txt
streamlit run app.py
```

Brauzerda `http://localhost:8501` manzili ochiladi. SQLite bazasini yaratish: `python database/build_db.py`. Testlar: `pytest -q`.

### 14. Xulosa

Loyiha to‘rtta transport agentligi bo‘yicha yo‘nalish darajasidagi yo‘lovchi va qatnov ko‘rsatkichlarini yagona formatda tahlil qilish imkonini beradi. Dashboard ma’lumotlarni filtrlash, taqqoslash, vizual ko‘rish va CSV hisobot olishni ta’minlaydi. Tizimning asosiy afzalligi — haqiqiy ochiq datasetdan foydalanishi va manba ma’lumotlarining cheklovlarini yashirmasdan ko‘rsatishidir.
