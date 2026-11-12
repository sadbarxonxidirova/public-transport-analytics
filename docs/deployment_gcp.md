# Google Cloud Run deployment — bosqichma-bosqich

## 1. Tayyorlash
- Google Cloud Console'da yangi project yarating.
- Billing account ulang (xarajatlarni nazorat qiling).
- Google Cloud SDK (`gcloud`) o‘rnating.
- Terminalda `gcloud auth login` bajaring.

## 2. Kerakli API'larni yoqish
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## 3. Loyihani deploy qilish
Loyiha ildiz papkasida:
```bash
gcloud run deploy public-transport-analytics --source . --region us-central1 --allow-unauthenticated --port 8080 --memory 1Gi --cpu 1 --min 0 --max 2
```
Deploy yakunida ko‘rsatilgan Service URL'ni oching.

## 4. Cloud Storage (ixtiyoriy)
Agar xom CSV fayllarni konteynerdan tashqarida saqlash talab qilinsa, Cloud Storage bucket yarating, CSV fayllarni yuklang va Cloud Run service account'iga faqat kerakli bucket uchun Storage Object Viewer ruxsatini bering. Keyin ilovaning loader qatlamini bucket'dan o‘qiydigan qilib sozlash kerak. Hozirgi versiya CSV'larni image/container ichidagi `data/raw/` papkasidan o‘qiydi.

## 5. Xarajat va xavfsizlik
- Cloud Run min instances = 0 qilib qoldiring.
- Max instances limitini kichik qiymatda saqlang.
- Billing budget va alert yarating.
- Ish tugagach Cloud Run service va keraksiz resurslarni o‘chiring.
- Service'ni ommaga ochish (`--allow-unauthenticated`) faqat dashboard ommaviy ko‘rilishi kerak bo‘lsa tanlanadi; aks holda autentifikatsiyani yoqing.

## 6. Muhim texnik izoh
Cloud Run konteyner fayl tizimi vaqtinchalik. SQLite faylini Cloud Run ichida doimiy ma'lumotlar ombori sifatida ishlatish tavsiya etilmaydi. Hozirgi demo ilova CSV'larni o‘qib, tahlil qiladi; SQLite skripti lokal schema va DB namunasini yaratadi. Production holatida Cloud SQL yoki tashqi boshqariladigan DB tanlash kerak bo‘lishi mumkin.
