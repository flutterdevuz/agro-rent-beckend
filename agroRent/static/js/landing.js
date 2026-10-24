/**
 * AgroRent Landing Page Interactive Script
 */

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Lucide icons if available
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // Mobile Navigation Menu Toggle
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const closeMobileMenuBtn = document.getElementById('close-mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      mobileMenu.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    });

    const closeMenu = () => {
      mobileMenu.classList.add('hidden');
      document.body.style.overflow = '';
    };

    if (closeMobileMenuBtn) {
      closeMobileMenuBtn.addEventListener('click', closeMenu);
    }

    // Close when clicking on any mobile nav link
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', closeMenu);
    });
  }

  // Sticky Header Shadow on Scroll
  const header = document.querySelector('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      header.classList.add('shadow-md');
    } else {
      header.classList.remove('shadow-md');
    }
  });

  // Phone Number Input Masking (+998 XX XXX XX XX)
  const phoneInputs = document.querySelectorAll('input[type="tel"]');
  phoneInputs.forEach(input => {
    input.addEventListener('focus', () => {
      if (!input.value.trim()) {
        input.value = '+998 ';
      }
    });

    input.addEventListener('input', (e) => {
      let val = input.value.replace(/\D/g, '');
      if (val.startsWith('998')) {
        val = val.substring(3);
      }
      
      let formatted = '+998';
      if (val.length > 0) formatted += ' ' + val.substring(0, 2);
      if (val.length >= 3) formatted += ' ' + val.substring(2, 5);
      if (val.length >= 6) formatted += ' ' + val.substring(5, 7);
      if (val.length >= 8) formatted += ' ' + val.substring(7, 9);
      
      input.value = formatted;
    });
  });

  // Number Counter Animation
  const animateCounters = () => {
    const counterElements = document.querySelectorAll('[data-target]');
    counterElements.forEach(counter => {
      const target = parseFloat(counter.getAttribute('data-target'));
      const prefix = counter.getAttribute('data-prefix') || '';
      const suffix = counter.getAttribute('data-suffix') || '';
      const isDecimal = target % 1 !== 0;
      
      let count = 0;
      const duration = 2000;
      const stepTime = 30;
      const steps = duration / stepTime;
      const increment = target / steps;

      const updateCount = () => {
        count += increment;
        if (count < target) {
          counter.innerText = prefix + (isDecimal ? count.toFixed(1) : Math.floor(count).toLocaleString()) + suffix;
          setTimeout(updateCount, stepTime);
        } else {
          counter.innerText = prefix + (isDecimal ? target.toFixed(1) : target.toLocaleString()) + suffix;
        }
      };

      updateCount();
    });
  };

  // Intersection Observer for Counters
  const statsSection = document.getElementById('stats-section') || document.getElementById('quick-stats');
  if (statsSection) {
    let counted = false;
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !counted) {
          animateCounters();
          counted = true;
        }
      });
    }, { threshold: 0.3 });
    observer.observe(statsSection);
  } else {
    animateCounters();
  }

  // How It Works Steps Interaction
  const stepItems = document.querySelectorAll('.step-item');
  stepItems.forEach((item, index) => {
    item.addEventListener('click', () => {
      stepItems.forEach(s => s.classList.remove('active'));
      item.classList.add('active');
    });
  });

  // Services Data for Modal and Fast Booking
  const servicesData = {
    'tractor': {
      title: 'Traktor ijarasi',
      desc: 'Zamonaviy Claas, John Deere va Case traktorlari. Turli quvvatdagi texnikalar har qanday dala ishlari uchun tayyor.',
      rate: '150 000 - 300 000 so\'m / soat',
      features: ['Tajribali mexanizator bilan', 'Yoqilg\'i xizmati ichida', 'GPS orqali aniq hisob-kitob'],
      img: 'assets/images/service-tractor-hd.png'
    },
    'combine': {
      title: 'Kombayn xizmati',
      desc: 'Bug\'doy, makkajo\'xori va boshqa donli ekinlarni sifatli, nobudgarchiliksiz o\'rib-yig\'ib olish xizmati.',
      rate: '400 000 - 650 000 so\'m / gektar',
      features: ['Tezkor yetib borish', 'Yuqori unumdorlik', 'Don tozaligi kafolatlangan'],
      img: 'assets/images/service-combine-hd.png'
    },
    'plow': {
      title: 'Yer haydash',
      desc: 'Kuzgi va bahorgi sifatli chuqur haydash, yerni tekislash va ekishga to\'liq tayyorlash xizmatlari.',
      rate: '250 000 - 350 000 so\'m / gektar',
      features: ['Chuqur haydash (30-40 sm)', 'Chizellash va kultivatsiya', 'Yer unumdorligini oshirish'],
      img: 'assets/images/service-plow-hd.png'
    },
    'seeder': {
      title: 'Ekish xizmati',
      desc: 'Zamonaviy pnevmatik va mexanik seyalkalar bilan urug\'larni bir xil chuqurlikda va me\'yorda ekish.',
      rate: '200 000 - 300 000 so\'m / gektar',
      features: ['Aniq me\'yorli ekish', 'O\'g\'it bilan birga ekish', 'Urug\' sarfini tejash'],
      img: 'assets/images/service-seeder-hd.png'
    },
    'drone': {
      title: 'Dron orqali purkash',
      desc: 'Agrodronlar (DJI Agras T40 / T30) orqali kimyoviy vositalar va suspenziyalarni o\'ta aniqlikda purkash.',
      rate: '60 000 - 90 000 so\'m / gektar',
      features: ['90% gacha suv tejash', 'O\'simlikni ezmaslik', 'Kuniga 60-80 gektar maydon'],
      img: 'assets/images/service-drone-hd.png'
    },
    'truck': {
      title: 'Yuk tashish',
      desc: 'Qishloq xo\'jaligi mahsulotlarini, o\'g\'it va texnikalarni daladan omborga yoki bozorga yetkazish.',
      rate: 'Masofaga va hajmga qarab kelishilgan',
      features: ['Katta sig\'imli yuk mashinalari', 'Xavfsiz va tezkor tashish', 'Fermadan to\'g\'ridan-to\'g\'ri olib ketish'],
      img: 'assets/images/service-truck-hd.png'
    },
    'seeds': {
      title: 'Urug\' va ko\'chatlar',
      desc: 'Sertifikatlangan, serhosil va iqlimga mos navli urug\'lar hamda baquvvat ko\'chatlar ta\'minoti.',
      rate: 'Urug\' naviga qarab',
      features: ['100% unuvchanlik kafolati', 'Kasalikka chidamli navlar', 'Agronom maslahati bepul'],
      img: 'assets/images/service-seeds-hd.png'
    },
    'fertilizer': {
      title: 'O\'g\'it va vositalar',
      desc: 'Mineral va organik o\'g\'itlar, gerbitsidlar, insektitsidlar hamda o\'simliklarni himoya vositalari.',
      rate: 'Ulgurji va arzon narxlar',
      features: ['Sertifikatlangan mahsulotlar', 'Dala bo\'yicha tahlil asosida', 'To\'g\'ridan-to\'g\'ri yetkazib berish'],
      img: 'assets/images/service-fertilizer-hd.png'
    }
  };

  // Service Modal Elements
  const serviceModal = document.getElementById('service-modal');
  const closeModalBtn = document.getElementById('close-service-modal');
  const modalTitle = document.getElementById('modal-service-title');
  const modalDesc = document.getElementById('modal-service-desc');
  const modalRate = document.getElementById('modal-service-rate');
  const modalImg = document.getElementById('modal-service-img');
  const modalFeatures = document.getElementById('modal-service-features');
  const modalSelectServiceBtn = document.getElementById('modal-select-service-btn');

  let currentSelectedKey = 'tractor';

  // Open Service Modal
  window.openServiceModal = (key) => {
    const data = servicesData[key];
    if (!data || !serviceModal) return;

    currentSelectedKey = key;
    if (modalTitle) modalTitle.innerText = data.title;
    if (modalDesc) modalDesc.innerText = data.desc;
    if (modalRate) modalRate.innerText = data.rate;
    if (modalImg) modalImg.src = data.img;

    if (modalFeatures) {
      modalFeatures.innerHTML = data.features.map(f => `
        <li class="flex items-center gap-2 text-sm text-gray-700">
          <span class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
            ✓
          </span>
          <span>${f}</span>
        </li>
      `).join('');
    }

    serviceModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  };

  // Close Service Modal
  if (closeModalBtn && serviceModal) {
    const closeModal = () => {
      serviceModal.classList.add('hidden');
      document.body.style.overflow = '';
    };

    closeModalBtn.addEventListener('click', closeModal);
    serviceModal.addEventListener('click', (e) => {
      if (e.target === serviceModal) closeModal();
    });
  }

  // Pre-select service in form when modal CTA is clicked
  if (modalSelectServiceBtn) {
    modalSelectServiceBtn.addEventListener('click', () => {
      const data = servicesData[currentSelectedKey];
      if (serviceModal) serviceModal.classList.add('hidden');
      document.body.style.overflow = '';

      const serviceSelect = document.getElementById('service-select');
      if (serviceSelect && data) {
        serviceSelect.value = data.title;
      }

      const formSection = document.getElementById('boglanish');
      if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Form Submission Handling
  const contactForm = document.getElementById('contact-form');
  const toastNotification = document.getElementById('toast-notification');
  const toastMessage = document.getElementById('toast-message');

  const showToast = (message) => {
    if (!toastNotification) return;
    if (toastMessage) toastMessage.innerText = message;
    toastNotification.classList.remove('hidden');

    setTimeout(() => {
      toastNotification.classList.add('hidden');
    }, 4500);
  };

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();

      const name = contactForm.querySelector('input[name="name"]')?.value;
      const phone = contactForm.querySelector('input[name="phone"]')?.value;
      const service = contactForm.querySelector('select[name="service"], input[name="service"]')?.value;

      if (!phone || phone.length < 13) {
        alert('Iltimos, to\'liq telefon raqamingizni kiriting!');
        return;
      }

      // Simulate successful request
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg> Yuborilmoqda...
      `;
      submitBtn.disabled = true;

      setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        contactForm.reset();
        showToast(`Rahmat, ${name || 'hurmatli fermer'}! Buyurtmangiz qabul qilindi. 15 daqiqada bog'lanamiz.`);
      }, 1000);
    });
  }

  // Language Dropdown Switcher
  const langSelector = document.getElementById('lang-selector');
  const langMenu = document.getElementById('lang-menu');
  const currentLangLabel = document.getElementById('current-lang-label');

  if (langSelector && langMenu) {
    langSelector.addEventListener('click', (e) => {
      e.stopPropagation();
      langMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', () => {
      langMenu.classList.add('hidden');
    });

    const langOptions = langMenu.querySelectorAll('[data-lang]');
    langOptions.forEach(opt => {
      opt.addEventListener('click', (e) => {
        const lang = opt.getAttribute('data-lang');
        if (currentLangLabel) currentLangLabel.innerText = lang.toUpperCase();
        langMenu.classList.add('hidden');
        switchLanguage(lang);
      });
    });
  }

  // Multi-language strings
  const translations = {
    'uz': {
      'nav_services': 'Xizmatlar',
      'nav_how': 'Qanday ishlaydi',
      'nav_benefits': 'Afzalliklar',
      'nav_partners': 'Hamkorlar',
      'nav_contact': 'Bog\'lanish',
      'nav_start': 'Boshlash',
      'hero_badge': 'QIShLOQ XO\'JALIGI UChUN ZAMONAVIY YECHIM',
      'hero_title': 'Qishloq xo\'jaligi texnikalari va agroxizmatlarni <span class="text-amber-500">bir platformada</span> toping.',
      'hero_desc': 'Traktor, kombayn, seyalka, purkagich, suv nasoslari va boshqa texnikalarni ijaraga oling, shuningdek agroxizmatlarga buyurtma bering. Dehqonlar uchun tez, qulay va ishonchli platforma.',
      'hero_cta': 'Xizmatni boshlash',
      'hero_how': 'Qanday ishlaydi?',
      'stat_users': 'FOYDALANUVChI',
      'stat_services': 'XIZMAT TURI',
      'stat_region': 'PILOT HUDUD',
      'stat_orders': 'BUYURTMA QABUL QILISh'
    },
    'ru': {
      'nav_services': 'Услуги',
      'nav_how': 'Как это работает',
      'nav_benefits': 'Преимущества',
      'nav_partners': 'Партнеры',
      'nav_contact': 'Контакты',
      'nav_start': 'Начать',
      'hero_badge': 'СОВРЕМЕННОЕ РЕШЕНИЕ ДЛЯ СЕЛЬСКОГО ХОЗЯЙСТВА',
      'hero_title': 'Сельскохозяйственная техника и агроуслуги <span class="text-amber-500">на одной платформе</span>.',
      'hero_desc': 'Арендуйте тракторы, комбайны, сеялки, опрыскиватели и насосы, заказывайте агроуслуги онлайн. Быстро, удобно и надежно для фермеров.',
      'hero_cta': 'Начать работу',
      'hero_how': 'Как это работает?',
      'stat_users': 'ПОЛЬЗОВАТЕЛЕЙ',
      'stat_services': 'ВИДОВ УСЛУГ',
      'stat_region': 'ПИЛОТНЫЙ РЕГИОН',
      'stat_orders': 'ПРИЕМ ЗАЯВОК 24/7'
    },
    'en': {
      'nav_services': 'Services',
      'nav_how': 'How It Works',
      'nav_benefits': 'Benefits',
      'nav_partners': 'Partners',
      'nav_contact': 'Contact',
      'nav_start': 'Get Started',
      'hero_badge': 'MODERN SOLUTION FOR AGRICULTURE',
      'hero_title': 'Find agricultural machinery and agriservices <span class="text-amber-500">on one platform</span>.',
      'hero_desc': 'Rent tractors, combine harvesters, seeders, sprayers, and pumps. Order agricultural services online with verified partners.',
      'hero_cta': 'Get Started',
      'hero_how': 'How It Works?',
      'stat_users': 'ACTIVE USERS',
      'stat_services': 'SERVICE TYPES',
      'stat_region': 'PILOT REGION',
      'stat_orders': 'ORDER ACCEPTANCE'
    }
  };

  const switchLanguage = (lang) => {
    const dict = translations[lang] || translations['uz'];
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.innerHTML = dict[key];
      }
    });
  };
});
