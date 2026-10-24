from home.models import (
    WebsiteSettings, WebsiteService, WebsitePartner, WebsiteStep, WebsiteBenefit
)

def seed_website_data():
    """
    Seed initial landing page data if not already present.
    """
    # 1. Settings
    settings, created = WebsiteSettings.objects.get_or_create(id=1)
    if created:
        settings.hero_badge = "QIShLOQ XO'JALIGI UChUN ZAMONAVIY YECHIM"
        settings.hero_title = "Qishloq xo'jaligi texnikalari va agroxizmatlarni bir platformada toping."
        settings.hero_description = "Traktor, kombayn, seyalka, purkagich, suv nasoslari va boshqa texnikalarni ijaraga oling, shuningdek agroxizmatlarga buyurtma bering. Dehqonlar uchun tez, qulay va ishonchli platforma."
        settings.hero_primary_cta_text = "Xizmatni boshlash"
        settings.hero_primary_cta_link = "#boglanish"
        settings.hero_secondary_cta_text = "Qanday ishlaydi?"
        settings.hero_secondary_cta_link = "#qanday-ishlaydi"
        settings.google_play_url = "https://play.google.com/store/apps/details?id=uz.agrorent"
        settings.app_store_url = "https://apps.apple.com/app/agrorent/id123456789"
        settings.phone_number = "+998 90 123 45 67"
        settings.email = "info@agrorent.uz"
        settings.address = "Andijon viloyati, Andijon shahri"
        settings.telegram_url = "https://t.me/agrorent_uz"
        settings.instagram_url = "https://instagram.com/agrorent_uz"
        settings.facebook_url = "https://facebook.com/agrorent.uz"
        settings.youtube_url = "https://youtube.com/@agrorent"
        settings.stats_users = "600+"
        settings.stats_services = "8 ta"
        settings.stats_region = "Andijon"
        settings.stats_orders_support = "24/7"
        settings.stat_total_orders = "10 000+"
        settings.stat_total_farmers = "1 200+"
        settings.stat_total_companies = "150+"
        settings.stat_rating = "4.9"
        settings.cta_title = "Bugun AgroRent bilan yangi imkoniyatlarga qadam qo'ying!"
        settings.cta_subtitle = "Zamonaviy qishloq xo'jaligi uchun ishonchli raqamli hamkor."
        settings.save()

    # 2. Services
    services_data = [
        {
            "slug": "tractor",
            "title": "Traktor ijarasi",
            "description": "Zamonaviy Claas, John Deere va Case traktorlari. Turli quvvatdagi texnikalar har qanday dala ishlari uchun tayyor.",
            "price_estimate": "150 000 - 300 000 so'm / soat",
            "features": "Tajribali mexanizator bilan\nYoqilg'i xizmati ichida\nGPS orqali aniq hisob-kitob",
            "image_url": "/api/static/images/service-tractor-hd.png",
            "order": 1
        },
        {
            "slug": "combine",
            "title": "Kombayn xizmati",
            "description": "Bug'doy, makkajo'xori va boshqa donli ekinlarni sifatli, nobudgarchiliksiz o'rib-yig'ib olish xizmati.",
            "price_estimate": "400 000 - 650 000 so'm / gektar",
            "features": "Tezkor yetib borish\nYuqori unumdorlik\nDon tozaligi kafolatlangan",
            "image_url": "/api/static/images/service-combine-hd.png",
            "order": 2
        },
        {
            "slug": "plow",
            "title": "Yer haydash",
            "description": "Kuzgi va bahorgi sifatli chuqur haydash, yerni tekislash va ekishga to'liq tayyorlash xizmatlari.",
            "price_estimate": "250 000 - 350 000 so'm / gektar",
            "features": "Chuqur haydash (30-40 sm)\nChizellash va kultivatsiya\nYer unumdorligini oshirish",
            "image_url": "/api/static/images/service-plow-hd.png",
            "order": 3
        },
        {
            "slug": "seeder",
            "title": "Ekish xizmati",
            "description": "Zamonaviy pnevmatik va mexanik seyalkalar bilan urug'larni bir xil chuqurlikda va me'yorda ekish.",
            "price_estimate": "200 000 - 300 000 so'm / gektar",
            "features": "Aniq me'yorli ekish\nO'g'it bilan birga ekish\nUrug' sarfini tejash",
            "image_url": "/api/static/images/service-seeder-hd.png",
            "order": 4
        },
        {
            "slug": "drone",
            "title": "Dron orqali purkash",
            "description": "Agrodronlar (DJI Agras T40 / T30) orqali kimyoviy vositalar va suspenziyalarni o'ta aniqlikda purkash.",
            "price_estimate": "60 000 - 90 000 so'm / gektar",
            "features": "90% gacha suv tejash\nO'simlikni ezmaslik\nKuniga 60-80 gektar maydon",
            "image_url": "/api/static/images/service-drone-hd.png",
            "order": 5
        },
        {
            "slug": "truck",
            "title": "Yuk tashish",
            "description": "Qishloq xo'jaligi mahsulotlarini, o'g'it va texnikalarni daladan omborga yoki bozorga yetkazish.",
            "price_estimate": "Masofaga va hajmga qarab kelishilgan",
            "features": "Katta sig'imli yuk mashinalari\nXavfsiz va tezkor tashish\nFermadan to'g'ridan-to'g'ri olib ketish",
            "image_url": "/api/static/images/service-truck-hd.png",
            "order": 6
        },
        {
            "slug": "seeds",
            "title": "Urug' va ko'chatlar",
            "description": "Sertifikatlangan, serhosil va iqlimga mos navli urug'lar hamda baquvvat ko'chatlar ta'minoti.",
            "price_estimate": "Urug' naviga qarab",
            "features": "100% unuvchanlik kafolati\nKasalikka chidamli navlar\nAgronom maslahati bepul",
            "image_url": "/api/static/images/service-seeds-hd.png",
            "order": 7
        },
        {
            "slug": "fertilizer",
            "title": "O'g'it va vositalar",
            "description": "Mineral va organik o'g'itlar, gerbitsidlar, insektitsidlar hamda o'simliklarni himoya vositalari.",
            "price_estimate": "Ulgurji va arzon narxlar",
            "features": "Sertifikatlangan mahsulotlar\nDala bo'yicha tahlil asosida\nTo'g'ridan-to'g'ri yetkazib berish",
            "image_url": "/api/static/images/service-fertilizer-hd.png",
            "order": 8
        }
    ]

    for s in services_data:
        WebsiteService.objects.get_or_create(
            slug=s["slug"],
            defaults=s
        )

    # 3. Partners & Team
    partners_data = [
        {"name": '"AgroServis" MChJ', "role": "Qishloq xo'jaligi xizmatlari", "photo_url": "/api/static/images/partner-1-hd.png", "member_type": "partner", "order": 1},
        {"name": '"Farg\'ona Agro"', "role": "Texnika ijarasi", "photo_url": "/api/static/images/partner-2-hd.png", "member_type": "partner", "order": 2},
        {"name": '"Samarqand Don"', "role": "Don yetishtirish", "photo_url": "/api/static/images/partner-3-hd.png", "member_type": "partner", "order": 3},
        {"name": '"Namangan Agrotech"', "role": "Purkash xizmatlari", "photo_url": "/api/static/images/partner-4-hd.png", "member_type": "partner", "order": 4},
        {"name": '"Qishloq Fayz"', "role": "Urug' va ko'chatlar", "photo_url": "/api/static/images/partner-5-hd.png", "member_type": "partner", "order": 5},
        {"name": '"AgroLogistic"', "role": "Yuk tashish", "photo_url": "/api/static/images/partner-6-hd.png", "member_type": "partner", "order": 6},
    ]

    for p in partners_data:
        WebsitePartner.objects.get_or_create(
            name=p["name"],
            defaults=p
        )

    # 4. Steps
    steps_data = [
        {"step_number": "01", "title": "Xizmatni tanlang", "description": "Kerakli texnika yoki agroxizmatni tanlang.", "order": 1},
        {"step_number": "02", "title": "Buyurtma bering", "description": "Manzil, sana va boshqa ma'lumotlarni kiriting.", "order": 2},
        {"step_number": "03", "title": "Xizmat ko'rsatuvchi bilan bog'laning", "description": "Platforma orqali tasdiqlangan hamkor bilan aloqa qiling.", "order": 3},
        {"step_number": "04", "title": "Xizmatni oling va baholang", "description": "Ish tugagach, xizmat sifatini baholang.", "order": 4},
    ]

    for st in steps_data:
        WebsiteStep.objects.get_or_create(
            step_number=st["step_number"],
            defaults=st
        )

    # 5. Benefits
    benefits_data = [
        {"title": "Tez va qulay kirish", "description": "Bir necha daqiqada xizmat toping va buyurtma bering.", "icon": "zap", "order": 1},
        {"title": "Ishonchli hamkorlar", "description": "Tekshirilgan va tajribali xizmat ko'rsatuvchilar bilan ishlang.", "icon": "shield-check", "order": 2},
        {"title": "Shaffof narxlar", "description": "Narxlar ochiq va haqiqiy, hech qanday yashirin to'lovlar yo'q.", "icon": "receipt", "order": 3},
        {"title": "Barcha agroehtiyojlar bir platformada", "description": "Texnika, xizmat, urug', o'g'it va boshqa resurslar.", "icon": "sprout", "order": 4},
    ]

    for b in benefits_data:
        WebsiteBenefit.objects.get_or_create(
            title=b["title"],
            defaults=b
        )
