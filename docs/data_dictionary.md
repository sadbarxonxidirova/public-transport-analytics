# Data Dictionary

| Standart nom | Manba ustunlari | Mazmuni / izoh |
|---|---|---|
| `agency` | CSV fayl nomidan | Transport agentligi kodi: MARTA, TRIMET, MIAMI_DADE, METRO_TRANSIT |
| `route_id` | `route_id`, `route_number`, `QSTOPROUTE`, `line_id` | Agentlik ichidagi yo‘nalish identifikatori; agentliklar orasida takrorlanishi mumkin |
| `period_code` | ustun suffix `12` yoki `17` | Manba davri kodi; kalendar yil deb avtomatik qabul qilinmaydi |
| `summary_begin_date` | `summary_begin_date12/17` | Tegishli davr uchun manbada berilgan boshlanish sanasi/markup yorlig‘i |
| `stops` | `Stops12/17` | Davr bo‘yicha yo‘nalish bekatlari soni |
| `avg_on_per_trip` | `AVGonPERtrip12/17` | Manbadagi yo‘lovchi ko‘rsatkichining bir qatnovga nisbatan o‘rtacha metrikasi; qiymatlar `avg_ons / avg_trips` nisbatiga mos keladi |
| `avg_trips` | `AVGtrips12/17` | Manbada berilgan o‘rtacha ish kuni transport qatnovlari ko‘rsatkichi |
| `sum_ons` | `SUMons12/17` | Yo‘nalish bo‘yicha jami kundalik yo‘lovchi boardings/alightings ko‘rsatkichi (tadqiqotdagi Rid mazmuni); source nomi saqlanadi |
| `avg_ons` | `AVGons12/17` | Bir bekatga to‘g‘ri keladigan o‘rtacha yo‘lovchi ko‘rsatkichi; fayllardagi qiymatlar `sum_ons / stops` nisbatiga mos |
| `source_file` | fayl nomi | Ma’lumot kelgan original CSV |

Original CSV ustunlari o‘zgartirilmaydi; analitika uchun standart nomlar qo‘llanadi. Dataset tavsifi weekdays bo‘yicha daily passenger boardings va vehicle-trips ko‘rsatkichlari berilishini bildiradi. Har bir source metrikasining hisoblash tafsilotlari uchun Berrebi, Joshi & Watkins tadqiqotiga murojaat qiling.

## Tekshiruv orqali kuzatilgan metrik munosabatlar

CSV qiymatlarida `AVGons ≈ SUMons / Stops` va `AVGonPERtrip ≈ AVGons / AVGtrips` munosabatlari kuzatildi (kichik farqlar yaxlitlashdan). Bu munosabatlar data validation uchun ishlatilishi mumkin; asl ustun qiymatlari o‘zgartirilmaydi.
