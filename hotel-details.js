/**
 * ملف: hotel-details.js
 * الوصف: إدارة صفحة تفاصيل الفنادق
 * الوظائف: عرض تفاصيل الفندق، المراجعات، السلايدر، دعم الفنادق المضافة من المستخدمين
 */

// ==================== قاعدة بيانات الفنادق ====================

const hotelsDetailsData = {
    shebara: {
        name: 'Shebara Resort',
        nameAr: 'منتجع شيبارا',
        location: 'جزيرة شبارة، البحر الأحمر',
        rating: 5,
        startPrice: 10300,
        images: ['images/shebara1.jpg', 'images/shebara2.jpg', 'images/shebara3.jpg', 'images/shebara4.jpg', 'images/shebara5.jpg'],
        tagline: 'استمتع بخدمة ذات مستوى عالمي في Shebara Resort',
        about: [
            {
                title: 'إقامة أنيقة',
                icon: 'fas fa-bed',
                text: 'يقدم منتجع شبارة في حنك غرفاً فاخرة مع إطلالات على البحر أو المسبح. تتميز كل غرفة بمكيف هواء وحمام خاص ووسائل راحة عصرية.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يمكن للضيوف الاستمتاع بمرافق السبا ومركز العافية ومسبح مع إطلالة وشرفة شمسية ومطعم وبار وخدمة واي فاي مجانية. تشمل الخدمات الإضافية علاجات التجميل وحصص اليوغا ومرافق اللياقة البدنية.'
            },
            {
                title: 'تجربة تناول الطعام',
                icon: 'fas fa-utensils',
                text: 'يقدم المطعم المناسب للعائلات المأكولات اليابانية والمتوسطية والبيروفية والمأكولات البحرية والسوشي والآسيوية والعالمية. تشمل خيارات الإفطار الوجبات القارية والأطباق حسب الطلب والنباتية والحلال.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبحان' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-utensils', text: '3 مطاعم' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-coffee', text: 'آلة صنع الشاي/القهوة' },
            { icon: 'fas fa-cocktail', text: 'بار' },
            { icon: 'fas fa-egg', text: 'إفطار كونتيننتال' },
            { icon: 'fas fa-water', text: 'إطلالة على البحر' },
            { icon: 'fas fa-table-tennis', text: 'ملعب تنس' }
        ]
    },
    desertrock: {
        name: 'Desert Rock Resort',
        nameAr: 'منتجع ديزرت روك',
        location: 'حانك، العلا، المملكة العربية السعودية',
        rating: 5,
        startPrice: 8500,
        images: ['images/desertrock1.jpg', 'images/desertrock2.jpg', 'images/desertrock3.jpg', 'images/desertrock4.jpg', 'images/desertrock5.jpg'],
        tagline: 'استمتع بخدمة ذات مستوى عالمي في Desert Rock Resort',
        about: [
            {
                title: 'إقامة فريدة بين الصخور',
                icon: 'fas fa-mountain',
                text: 'يقع منتجع ديزرت روك في حانك بالعلا، وهو مصنف بـ 5 نجوم ويوفر شرفات خاصة مع إطلالات خلابة على الجبال. تتميز كل فيلا بتصميم صخري فريد ومدخل خاص.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يوفر المنتجع مطعمين فاخرين ومسبحاً خارجياً بالإضافة إلى ساونا وحوض استحمام ساخن. يتوفر مركز سبا متكامل ومركز للياقة البدنية.'
            },
            {
                title: 'تجربة طعام متنوعة',
                icon: 'fas fa-utensils',
                text: 'يقدم المطعم إفطار كونتيننتال وحلال وخالي من الجلوتين وأسيوي. خدمة الغرف متاحة على مدار الساعة مع آلة صنع الشاي والقهوة في جميع الغرف.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح خارجي' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-utensils', text: 'مطعمان' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-coffee', text: 'آلة صنع الشاي/القهوة' },
            { icon: 'fas fa-egg', text: 'إفطار كونتيننتال' },
            { icon: 'fas fa-mountain', text: 'إطلالة على الجبل' },
            { icon: 'fas fa-hotel', text: 'تراس' },
            { icon: 'fas fa-hot-tub', text: 'حوض استحمام ساخن' }
        ]
    },
    shaden: {
        name: 'Shaden Resort',
        nameAr: 'منتجع شادن',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        startPrice: 4120,
        images: ['images/shaden1.jpg', 'images/shaden2.jpg', 'images/shaden3.jpg', 'images/shaden4.jpg', 'images/shaden5.jpg'],
        tagline: 'استمتع بخدمة ذات مستوى عالمي في Shaden Resort',
        about: [
            {
                title: 'أماكن إقامة مريحة',
                icon: 'fas fa-home',
                text: 'يوفر منتجع شادن في العلا غرفًا عائلية مع إطلالات على الجبال أو الحديقة. تشتمل كل غرفة على تكييف هواء وحمام خاص ووسائل راحة عصرية.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يمكن للضيوف الاستمتاع بمرافق السبا والساونا ومركز اللياقة البدنية والشرفة المشمسة وحمام السباحة الخارجي. تشمل وسائل الراحة الإضافية غرفة بخار وحوض استحمام ساخن وحمام تركي. كما يتوفر واي فاي مجاني في جميع أنحاء مكان الإقامة.'
            },
            {
                title: 'تجربة تناول الطعام',
                icon: 'fas fa-utensils',
                text: 'يقدم المطعم المناسب للعائلات المأكولات الهندية والشرق أوسطية والعالمية. تشمل خيارات الإفطار الوجبات القارية والأمريكية والبوفيه والأطباق المحلية المميزة. تتميز مناطق تناول الطعام بأجواء تقليدية وعصرية ورومانسية.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح خارجي' },
            { icon: 'fas fa-plane', text: 'خدمة نقل المطار' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-wheelchair', text: 'مرافق لذوي الاحتياجات الخاصة' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-coffee', text: 'آلة صنع الشاي/القهوة' },
            { icon: 'fas fa-mountain', text: 'إطلالة على الجبل' },
            { icon: 'fas fa-hot-tub', text: 'حوض استحمام ساخن' },
            { icon: 'fas fa-hiking', text: 'المشي لمسافات طويلة' }
        ]
    },
    chedi: {
        name: 'The Chedi Hegra',
        nameAr: 'ذا تشيدي حجرا',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        startPrice: 5336,
        images: ['images/chedi1.jpg', 'images/chedi2.jpg', 'images/chedi3.jpg', 'images/chedi4.jpg', 'images/chedi5.jpg'],
        tagline: 'استمتع بخدمة ذات مستوى عالمي في The Chedi Hegra',
        about: [
            {
                title: 'إقامة أنيقة',
                icon: 'fas fa-star',
                text: 'يقدم لك ذا تشيدي حجرا في العلا تجربة منتجع من فئة 5 نجوم مع غرف فاخرة تتميز بشرفات وأرواب حمام. تشتمل كل غرفة على خدمة واي فاي مجانية، مما يضمن بقاء الضيوف على اتصال خلال إقامتهم.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يمكن للضيوف الاستمتاع بمرافق السبا ومركز اللياقة البدنية ومسبح خارجي يعمل على مدار العام. تشمل وسائل الراحة الإضافية شرفة ومطعم واستخدام مجاني للدراجات، مما يوفر فرصًا وفيرة للاسترخاء والترفيه.'
            },
            {
                title: 'تجربة تناول الطعام',
                icon: 'fas fa-utensils',
                text: 'يقدم المنتجع وجبات حلال مع إفطار حسب الطلب يتضمن الشمبانيا والعصير والمعجنات الطازجة والبانكيك والجبن والفواكه. تشمل خيارات تناول الطعام وجبة البرانش والغداء والعشاي والشاي، مما يلبي مختلف الأذواق.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح خارجي' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-wheelchair', text: 'مرافق لذوي الاحتياجات الخاصة' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-utensils', text: 'مطعم' },
            { icon: 'fas fa-egg', text: 'إفطار حسب الطلب' },
            { icon: 'fas fa-biking', text: 'استخدام مجاني للدراجات' },
            { icon: 'fas fa-hiking', text: 'المشي لمسافات طويلة' }
        ]
    },
    fairmont: {
        name: 'Fairmont Riyadh',
        location: 'بوابة الأعمال، الرياض',
        startPrice: 950,
        images: ['images/fairmont1.jpg', 'images/fairmont2.jpg', 'images/fairmont3.jpg', 'images/fairmont4.jpg', 'images/fairmont5.jpg'],
        tagline: 'اشعر وكأنك نجم واستمتع بالمعاملة والخدمات الراقية',
        about: [
            {
                title: 'عن الفندق',
                icon: 'fas fa-hotel',
                text: 'يقع Fairmont Riyadh في بوابة الأعمال، ويحتوي على مسبح داخلي ومركز للياقة البدنية، كما تتوفر خدمة الواي فاي مجاناً في جميع أنحاء الفندق. تحتوي الغرف في الفندق على مكتب، وتضم كل غرفة حمّاماً خاصاً، كما تحتوي جميع الغرف على تلفزيون بشاشة مسطحة مع قنوات فضائية.'
            },
            {
                title: 'المرافق والخدمات',
                icon: 'fas fa-concierge-bell',
                text: 'يمكن للضيوف في مكان الإقامة الاستمتاع ببوفيه إفطار متنوع. يمكن لموظفي مكتب الاستقبال تقديم نصائح حول ما يمكن القيام به في المنطقة.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح داخلي' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-tv', text: 'تلفزيون بشاشة مسطحة' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الاستقبال 24 ساعة' },
            { icon: 'fas fa-utensils', text: 'بوفيه إفطار' },
            { icon: 'fas fa-car', text: 'مواقف سيارات' },
            { icon: 'fas fa-info-circle', text: 'خدمة الكونسيرج' },
            { icon: 'fas fa-suitcase', text: 'مركز أعمال' },
            { icon: 'fas fa-map-marked-alt', text: 'قريب من غرناطة مول' },
            { icon: 'fas fa-plane', text: '15 دقيقة من المطار' },
            { icon: 'fas fa-building', text: 'موقع مثالي للأعمال' }
        ]
    },
    ashar: {
        name: 'Ashar Tented Resort',
        location: 'العلا، المملكة العربية السعودية',
        startPrice: 2800,
        images: ['images/ashar1.jpg', 'images/ashar2.jpg', 'images/ashar3.jpg', 'images/ashar4.jpg', 'images/ashar5.jpg'],
        tagline: 'تجربة فريدة في قلب الصحراء مع إطلالات جبلية خلابة',
        about: [
            {
                title: 'إقامة أنيقة',
                icon: 'fas fa-campground',
                text: 'يقدم منتجع أشار للخيم في العلا خيامًا فاخرة مع إطلالات على الجبال وحمامات خاصة ووسائل راحة عصرية. تتميز كل خيمة بمكيف هواء وشرفة ومدخل خاص.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يستمتع الضيوف بمسبح لا نهائي ومرافق سبا ومركز للياقة البدنية وخدمة واي فاي مجانية. تشمل وسائل الراحة الإضافية مطعمًا ومنطقة جلوس خارجية ودراجات مجانية.'
            },
            {
                title: 'تجربة تناول الطعام',
                icon: 'fas fa-utensils',
                text: 'يقدم المطعم المناسب للعائلات المأكولات الشرق أوسطية والتايلاندية مع خيارات حلال ونباتية ونباتية صرفة. تشمل وجبة الإفطار الأطباق المحلية المميزة والمخبوزات الطازجة ومجموعة متنوعة من المشروبات.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح خارجي لا نهائي' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-ban-smoking', text: 'خيام لغير المدخنين' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الخيام' },
            { icon: 'fas fa-utensils', text: '3 مطاعم' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-coffee', text: 'آلة صنع الشاي/القهوة' },
            { icon: 'fas fa-mountain', text: 'إطلالة على الجبال' },
            { icon: 'fas fa-bicycle', text: 'دراجات مجانية' },
            { icon: 'fas fa-egg', text: 'إفطار كونتيننتال' }
        ]
    },
    caravan: {
        name: 'Caravan AlUla by Our Habitas',
        location: 'العلا، المملكة العربية السعودية',
        startPrice: 2831,
        images: ['images/caravan1.jpg', 'images/caravan2.jpg', 'images/caravan3.jpg', 'images/caravan4.jpg', 'images/caravan5.jpg'],
        tagline: 'اشعر وكأنك نجم واستمتع بالمعاملة والخدمات الراقية',
        about: [
            {
                title: 'إقامة أنيقة',
                icon: 'fas fa-home',
                text: 'يقدم مكان إقامة "Caravan AlUla by Our Habitas" في العلا تجربة فندقية من فئة 5 نجوم مع خدمة واي فاي مجانية ومطعم ودراجات مجانية. يستمتع الضيوف بإطلالات على الجبال وقرب الموقع من موقع الحجر الأثري الذي يبعد 25 كم.'
            },
            {
                title: 'وسائل راحة مريحة',
                icon: 'fas fa-couch',
                text: 'يتميز مكان الإقامة بتكييف الهواء وحمامات خاصة مع دش مشي وأثاث خارجي. تشمل وسائل الراحة الإضافية ميني بار وميكروويف ومستلزمات استحمام مجانية.'
            },
            {
                title: 'خيارات تناول الطعام',
                icon: 'fas fa-utensils',
                text: 'يقدم المطعم العصري والملائم للعائلات المأكولات المكسيكية والشرق أوسطية مع خيارات حلال وخالية من الغلوتين. يشمل الإفطار خيارات نباتية ونباتية صرفة وحلال.'
            },
            {
                title: 'أنشطة ترفيهية',
                icon: 'fas fa-running',
                text: 'يمكن للضيوف المشاركة في دروس اليوغا وليالي الأفلام والاستمتاع بمنطقة الجلوس الخارجية. يتوفر موقف سيارات خاص مجاني في الموقع وخدمة نقل بأجر.'
            }
        ],
        amenities: [
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-utensils', text: 'مطعم عصري' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-bicycle', text: 'دراجات مجانية' },
            { icon: 'fas fa-mountain', text: 'إطلالة على الجبال' },
            { icon: 'fas fa-wind', text: 'تكييف هواء' },
            { icon: 'fas fa-shower', text: 'دش مطري' },
            { icon: 'fas fa-couch', text: 'أثاث خارجي' },
            { icon: 'fas fa-glass-martini', text: 'ميني بار' },
            { icon: 'fas fa-spa', text: 'دروس يوغا' },
            { icon: 'fas fa-film', text: 'ليالي أفلام' }
        ]
    },
    mandarin: {
        name: 'Mandarin Oriental Al Faisaliah',
        location: 'الرياض، المملكة العربية السعودية',
        startPrice: 1530,
        images: ['images/mandarin1.jpg', 'images/mandarin2.jpg', 'images/mandarin3.jpg', 'images/mandarin4.jpg', 'images/mandarin5.jpg'],
        tagline: 'اشعر وكأنك نجم واستمتع بالمعاملة والخدمات الراقية',
        about: [
            {
                title: 'عن الفندق',
                icon: 'fas fa-hotel',
                text: 'يُعد ماندارين أورينتال الفيصلية واحداً من أفضل الفنادق المصنفة 5 نجوم في الرياض، ويضم 325 غرفة وجناحاً مجهزة بشكل جميل وخدمة الخادم الشخصي الحصرية على مدار الساعة ومرافق للاجتماعات العصرية و6 مطاعم عالمية ونادياً صحياً عصرياً وسبا The Ladies المخصص بشكل حصري للسيدات.'
            },
            {
                title: 'الأجنحة والغرف',
                icon: 'fas fa-bed',
                text: 'تعكس الأجنحة المجهزة بأناقة الفخامة والرقي لتوفير مكاناً مثالياً للإقامة، فيما يضفي الطراز السكني والمساحة المنسقة بشكل رائع وتفاصيل الأرابيسك المعمارية الرائعة مع الأناقة العصرية والتكنولوجيا الحديثة أجواءً راقية ورائعة بشكل عام. كما تضم جميع الغرف تلفزيون بشاشة مسطحة مع قنوات فضائية وأجهزة تحكم تعمل بتقنية اللمس للإضاءة والستائر والتدفئة.'
            },
            {
                title: 'المطاعم',
                icon: 'fas fa-utensils',
                text: 'يعد مطعم Globe وجهة فاخرة بحد ذاتها حيث توفر القبة الجيوديسية ذات المظهر المذهل مكاناً رائعاً للاستمتاع بالمأكولات الأوروبية الحديثة المبتكرة قبل الاسترخاء في صالة عسير، وهي صالة السيجار الوحيدة المخصصة في المدينة. كما يعتبر مطعم La Brasserie مسرح طعام تفاعلي متنوع حيث يمكن للضيوف الاستمتاع بالأجواء الحماسية والمشاركة من خلال مشاهدة الطهاة يقومون بعملهم.'
            },
            {
                title: 'النادي الصحي والسبا',
                icon: 'fas fa-spa',
                text: 'يوفر النادي الصحي مسبحاً داخلياً بطول 20 متر ومركز لياقة بدنية حديث مزود بأجهزة التمارين العضلية ذات الحركة الكاملة، بالإضافة إلى منطقة للاسترخاء. كما يمكن للضيوف الاستمتاع بمناطق التسوق والترفيه الفاخرة في مود مول المجاور، وتتوفر مواقف خاصة للسيارات مجاناً في الموقع.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح داخلي 20 متر' },
            { icon: 'fas fa-plane-departure', text: 'خدمة نقل المطار' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-wheelchair', text: 'مرافق لذوي الاحتياجات الخاصة' },
            { icon: 'fas fa-utensils', text: '6 مطاعم عالمية' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-user-tie', text: 'خادم شخصي 24 ساعة' },
            { icon: 'fas fa-shopping-bag', text: 'قريب من مود مول' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' }
        ]
    },
    movenpick: {
        name: 'Movenpick Hotel and Residences Riyadh',
        location: 'الرياض، المملكة العربية السعودية',
        startPrice: 1300,
        images: ['images/movenpick1.jpg', 'images/movenpick2.jpg', 'images/movenpick3.jpg', 'images/movenpick4.jpg', 'images/movenpick5.jpg'],
        tagline: 'اشعر وكأنك نجم واستمتع بالمعاملة والخدمات الراقية',
        about: [
            {
                title: 'أماكن إقامة أنيقة',
                icon: 'fas fa-bed',
                text: 'يقدم مكان إقامة "Movenpick Hotel and Residences Riyadh" في الرياض غرفًا فاخرة مع حمامات خاصة وإطلالات على المسبح ووسائل راحة عصرية. تحتوي كل غرفة على مكتب للعمل وتلفزيون وخدمة واي فاي مجانية، مما يضمن لك إقامة مريحة.'
            },
            {
                title: 'مرافق استثنائية',
                icon: 'fas fa-spa',
                text: 'يمكن للضيوف الاستمتاع بمسبح على السطح ومرافق سبا ومركز للياقة البدنية وشرفة للتشمس وحديقة خضراء. تشمل وسائل الراحة الإضافية مطعمًا يقدم المأكولات الإيطالية والمغربية وبارًا وخدمات التدليك.'
            },
            {
                title: 'موقع متميز',
                icon: 'fas fa-map-marker-alt',
                text: 'يقع الفندق على بُعد 24 كم من مطار الملك خالد الدولي، وبالقرب من معالم سياحية مثل الرياض جاليري مول (5 كم) والورود 2 (8 كم). كما يتوفر موقف سيارات خاص مجاني في الموقع.'
            },
            {
                title: 'رضا الضيوف',
                icon: 'fas fa-star',
                text: 'يحظى الفندق بتقييمات عالية لطاقمه المتفاني ونظافة الغرف المثالية وموقعه المناسب، حيث يوفر خدمة ممتازة وراحة لجميع الزوار.'
            }
        ],
        amenities: [
            { icon: 'fas fa-swimming-pool', text: 'مسبح خارجي على السطح' },
            { icon: 'fas fa-plane-departure', text: 'خدمة نقل المطار' },
            { icon: 'fas fa-ban-smoking', text: 'غرف لغير المدخنين' },
            { icon: 'fas fa-dumbbell', text: 'مركز للياقة البدنية' },
            { icon: 'fas fa-spa', text: 'مركز عافية وسبا' },
            { icon: 'fas fa-concierge-bell', text: 'خدمة الغرف' },
            { icon: 'fas fa-wheelchair', text: 'مرافق لذوي الاحتياجات الخاصة' },
            { icon: 'fas fa-utensils', text: '3 مطاعم' },
            { icon: 'fas fa-cocktail', text: 'بار' },
            { icon: 'fas fa-wifi', text: 'واي فاي مجاني' },
            { icon: 'fas fa-tree', text: 'حديقة خضراء' },
            { icon: 'fas fa-parking', text: 'مواقف سيارات مجانية' }
        ]
    }
};

// الحصول على الفندق الحالي من URL
function getCurrentHotelDetails() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    // التحقق من الفنادق الأساسية (fallback)
    // تم إزالة fallback الافتراضي (shebara) لدعم الأماكن الديناميكية
    return hotelsDetailsData[hotelParam];
}

// جلب بيانات الفندق من الـ backend (إذا كان place_id)
async function fetchPlaceFromBackend(placeId) {
    try {
        const data = await PlacesAPI.getById(placeId);
        if (data && data.id) {
            return {
                id: data.id,
                name: data.title || 'مكان',
                nameAr: data.title || '',
                location: `${data.latitude || ''}, ${data.longitude || ''}`,
                rating: 5,
                startPrice: data.price || 0,
                images: (Array.isArray(data.images) && data.images.length > 0) ? data.images : ['images/default-hotel.jpg'],
                tagline: data.description || '',
                about: [{ title: 'عن المكان', icon: 'fas fa-info-circle', text: data.description || '' }],
                amenities: [],
                status: data.status
            };
        }
    } catch (err) {
        console.warn('تعذر جلب المكان من الـ backend:', err);
    }
    return null;
}

// تحديث معلومات الصفحة
function updatePageContent() {
    const hotel = getCurrentHotelDetails();

    // تحديث العنوان
    document.title = `${hotel.name} - نُزل`;

    // تحديث اسم الفندق
    const hotelNameElement = document.querySelector('.hotel-name');
    if (hotelNameElement) hotelNameElement.textContent = hotel.name;

    // تحديث الموقع
    const hotelLocationElement = document.querySelector('.hotel-location span');
    if (hotelLocationElement) hotelLocationElement.textContent = hotel.location;

    // تحديث السعر
    const priceAmountElement = document.querySelector('.price-amount');
    if (priceAmountElement) priceAmountElement.textContent = `${hotel.startPrice.toLocaleString('en-US')} ر.س`;

    // تحديث tagline
    const taglineElement = document.querySelector('.hotel-tagline p');
    if (taglineElement) taglineElement.textContent = hotel.tagline;

    // تحديث قسم "عن الفندق"
    const descriptionElement = document.querySelector('.hotel-description');
    if (descriptionElement && hotel.about) {
        let aboutHTML = '<h2 class="section-title">عن الفندق</h2>';
        hotel.about.forEach(item => {
            aboutHTML += `
                <div class="description-item">
                    <h3><i class="${item.icon}"></i> ${item.title}</h3>
                    <p>${item.text}</p>
                </div>
            `;
        });
        descriptionElement.innerHTML = aboutHTML;
    }

    // تحديث المرافق
    const amenitiesGrid = document.querySelector('.amenities-grid');
    if (amenitiesGrid && hotel.amenities) {
        let amenitiesHTML = '';
        hotel.amenities.forEach(amenity => {
            amenitiesHTML += `
                <div class="amenity-item">
                    <i class="${amenity.icon}"></i>
                    <span>${amenity.text}</span>
                </div>
            `;
        });
        amenitiesGrid.innerHTML = amenitiesHTML;
    }

    // تحديث الصور في السلايدر
    const sliderWrapper = document.querySelector('.slider-wrapper');
    if (sliderWrapper) {
        let slidesHTML = '';
        let dotsHTML = '';

        hotel.images.forEach((img, index) => {
            slidesHTML += `<div class="hotel-slide ${index === 0 ? 'active' : ''}"><img src="${img}" alt="${hotel.name} ${index + 1}"></div>`;
            dotsHTML += `<span class="dot ${index === 0 ? 'active' : ''}" onclick="goToSlide(${index})"></span>`;
        });

        sliderWrapper.innerHTML = `
            ${slidesHTML}
            <button class="slider-arrow prev" onclick="changeSlide(-1)">
                <i class="fas fa-chevron-right"></i>
            </button>
            <button class="slider-arrow next" onclick="changeSlide(1)">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="slider-dots">${dotsHTML}</div>
        `;
    }

    // تحديث الشريط الثابت للحجز
    const bookingBarName = document.querySelector('.booking-hotel-name');
    const bookingBarPrice = document.querySelector('.booking-price');
    const bookingBtn = document.querySelector('.booking-btn');

    if (bookingBarName) bookingBarName.textContent = hotel.name;
    if (bookingBarPrice) bookingBarPrice.textContent = `يبدأ من ${hotel.startPrice.toLocaleString('ar-EG')} ر.س / ليلة`;

    if (bookingBtn) {
        const hotelParam = new URLSearchParams(window.location.search).get('hotel') || 'shebara';
        bookingBtn.setAttribute('onclick', `handleBooking()`);
    }

    // تحديث رابط الحجز القديم (إن وجد)
    const bookButton = document.querySelector('.book-button');
    if (bookButton) {
        const hotelParam = new URLSearchParams(window.location.search).get('hotel') || 'shebara';
        bookButton.setAttribute('onclick', `window.location.href='reservation.html?hotel=${hotelParam}'`);
    }

    // إخفاء قسم الموقع لديزرت روك وشادن وتشيدي وفيرمونت وآشار وكارافان وماندارين
    const locationSection = document.getElementById('locationSection');
    if (locationSection) {
        const hotelParam = new URLSearchParams(window.location.search).get('hotel');
        if (hotelParam === 'desertrock' || hotelParam === 'shaden' || hotelParam === 'chedi' || hotelParam === 'fairmont' || hotelParam === 'ashar' || hotelParam === 'caravan' || hotelParam === 'mandarin' || hotelParam === 'movenpick') {
            locationSection.style.display = 'none';
        } else {
            locationSection.style.display = 'block';
        }
    }

    // تحديث الغرف المتاحة
    updateRoomsDisplay();
}

// تحديث عرض الغرف ديناميكياً
function updateRoomsDisplay() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || 'shebara';

    // الحصول على بيانات الغرف من reservation.js
    if (typeof hotelsData === 'undefined') {
        console.error('hotelsData غير موجود');
        return;
    }

    const hotelData = hotelsData[hotelParam];
    if (!hotelData || !hotelData.rooms) {
        console.error('بيانات الغرف غير موجودة');
        return;
    }

    const roomsContainer = document.getElementById('roomsContainer');
    if (!roomsContainer) return;

    let roomsHTML = '';
    const taxRate = 0.2075;

    hotelData.rooms.forEach(room => {
        const tax = Math.round(room.price * taxRate);
        const featuresHTML = room.features.map(f =>
            `<span class="feature-tag"><i class="fas fa-check"></i> ${f}</span>`
        ).join('');

        roomsHTML += `
            <div class="room-card">
                <div class="room-header">
                    <h3 class="room-title">${room.name}</h3>
                    <div class="room-size">
                        <i class="fas fa-ruler-combined"></i>
                        <span>${room.size} متر مربع</span>
                    </div>
                </div>
                <div class="room-content">
                    <div class="room-features">
                        ${featuresHTML}
                        <span class="feature-tag"><i class="fas fa-snowflake"></i> تكييف</span>
                        <span class="feature-tag"><i class="fas fa-tv"></i> تلفزيون بشاشة مسطحة</span>
                        <span class="feature-tag"><i class="fas fa-wifi"></i> واي فاي مجاني</span>
                    </div>
                    <div class="room-footer">
                        <div class="room-capacity">
                            <i class="fas fa-users"></i>
                            <span>${room.features[room.features.length - 1]}</span>
                        </div>
                        <div class="room-price">
                            <span class="price">${room.price.toLocaleString('en-US')} ر.س</span>
                            <span class="price-note">+ ${tax.toLocaleString('en-US')} ر.س ضرائب</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    roomsContainer.innerHTML = roomsHTML;
}

// سلايدر صور الفندق
let currentSlide = 0;
let slideInterval;

// بدء السلايدر التلقائي
function startSlider() {
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 2000); // كل ثانيتين
}

// إيقاف السلايدر
function stopSlider() {
    clearInterval(slideInterval);
}

// تغيير الصورة
function changeSlide(direction) {
    const slides = document.querySelectorAll('.hotel-slide');
    const dots = document.querySelectorAll('.dot');

    // إخفاء الصورة الحالية
    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');

    // حساب الصورة الجديدة
    currentSlide = currentSlide + direction;

    // التأكد من البقاء ضمن النطاق
    if (currentSlide >= slides.length) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }

    // إظهار الصورة الجديدة
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');
}

// الانتقال لصورة محددة
function goToSlide(slideIndex) {
    const slides = document.querySelectorAll('.hotel-slide');
    const dots = document.querySelectorAll('.dot');

    // إخفاء الصورة الحالية
    slides[currentSlide].classList.remove('active');
    dots[currentSlide].classList.remove('active');

    // تحديث الفهرس
    currentSlide = slideIndex;

    // إظهار الصورة الجديدة
    slides[currentSlide].classList.add('active');
    dots[currentSlide].classList.add('active');

    // إعادة تشغيل السلايدر
    stopSlider();
    startSlider();
}

// معالجة الحجز
function handleBooking() {
    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        if (typeof showNotification === 'function') {
            showNotification('يجب تسجيل الدخول أولاً للحجز', 'error');
        }
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    // الحصول على معامل الفندق من URL
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || 'shebara';

    // الانتقال لصفحة الحجز مع معامل الفندق
    if (typeof showLoadingScreen === 'function') {
        showLoadingScreen(`reservation.html?hotel=${hotelParam}`);
    } else {
        window.location.href = `reservation.html?hotel=${hotelParam}`;
    }
}

// إيقاف السلايدر عند التمرير فوق الصور
// إيقاف السلايدر عند التمرير فوق الصور
document.addEventListener('DOMContentLoaded', async () => {
    // إظهار حالة التحميل (اختياري - يمكن إضافته في HTML)
    // const loadingMsg = document.createElement('div');
    // loadingMsg.id = 'loadingMsg';
    // loadingMsg.innerHTML = '<div style="text-align:center; padding: 50px;"><i class="fas fa-spinner fa-spin fa-2x"></i><p>جاري تحميل التفاصيل...</p></div>';
    // document.querySelector('main').prepend(loadingMsg);

    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    let placeFound = false;

    // 1. التحقق من البيانات المحلية (للفنادق الـ 9 الأصلية)
    if (hotelsDetailsData[hotelParam]) {
        console.log('تم العثور على المكان في البيانات المحلية:', hotelParam);
        placeFound = true;
    }
    // 2. التحقق من الـ backend (للأماكن الجديدة)
    else if (hotelParam) {
        console.log('محاولة جلب المكان من الـ backend:', hotelParam);
        const backendPlace = await fetchPlaceFromBackend(hotelParam);

        if (backendPlace) {
            // حفظ البيانات في الكائن المحلي ليعمل باقي الكود
            hotelsDetailsData[hotelParam] = backendPlace;
            placeFound = true;
            console.log('تم جلب البيانات بنجاح:', backendPlace);
        }
    }

    // إخفاء التحميل
    // const loadingMsgEl = document.getElementById('loadingMsg');
    // if (loadingMsgEl) loadingMsgEl.remove();

    if (placeFound) {
        // تحديث محتوى الصفحة
        updatePageContent();

        // عرض التعليقات
        await displayReviews();

        // إعداد السلايدر
        const sliderWrapper = document.querySelector('.slider-wrapper');
        if (sliderWrapper) {
            sliderWrapper.addEventListener('mouseenter', stopSlider);
            sliderWrapper.addEventListener('mouseleave', startSlider);
            // بدء السلايدر
            startSlider();
        }
    } else {
        // عرض رسالة خطأ إذا لم يتم العثور على المكان
        const mainContent = document.querySelector('main');
        if (mainContent) {
            mainContent.innerHTML = `
                <div class="places-error" style="height: 50vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                    <i class="fas fa-exclamation-circle fa-4x" style="color: #c62828; margin-bottom: 20px;"></i>
                    <h2 style="font-family: 'Amiri', serif; margin-bottom: 10px;">عذراً، الوجهة غير موجودة</h2>
                    <p style="margin-bottom: 20px;">لم نتمكن من العثور على تفاصيل هذه الوجهة.</p>
                    <a href="places.html" class="card-btn" style="text-decoration: none; display: inline-block; width: auto;">العودة للوجهات</a>
                </div>
            `;
        }
    }
});

// إيقاف السلايدر عند مغادرة الصفحة
window.addEventListener('beforeunload', stopSlider);

// بيانات التعليقات لكل فندق
const hotelReviews = {
    shebara: [
        { name: 'أحمد العتيبي', rating: 5, date: '2026-01-15', comment: 'تجربة رائعة! المنتجع فخم جداً والخدمة ممتازة. الفيلا فوق الماء كانت حلم!' },
        { name: 'سارة المطيري', rating: 5, date: '2026-01-10', comment: 'المكان خيالي والإطلالة على البحر الأحمر ساحرة. الطاقم محترف جداً.' },
        { name: 'خالد الغامدي', rating: 5, date: '2025-12-28', comment: 'أفضل منتجع زرته! النظافة والرقي والهدوء، كل شيء مثالي.' },
        { name: 'نورة السبيعي', rating: 4, date: '2025-12-20', comment: 'منتجع جميل جداً، الطعام لذيذ والمرافق حديثة. أنصح بزيارته.' },
        { name: 'فهد القحطاني', rating: 5, date: '2025-12-15', comment: 'قضينا شهر عسل رائع هنا. المسبح اللامتناهي تحفة فنية!' },
        { name: 'ريم الدوسري', rating: 5, date: '2025-12-08', comment: 'تجربة استثنائية! السبا والمساج كانوا رائعين.' },
        { name: 'عبدالله الشمري', rating: 4, date: '2025-11-30', comment: 'مكان هادئ ومريح، مناسب جداً للعائلات.' },
        { name: 'لطيفة الحربي', rating: 5, date: '2025-11-25', comment: 'الموظفون ودودون جداً والغرف نظيفة ومرتبة.' },
        { name: 'محمد العنزي', rating: 5, date: '2025-11-18', comment: 'يستحق كل ريال! المنتجع فاخر والخدمات متكاملة.' }
    ],
    desertrock: [
        { name: 'عبدالرحمن القرني', rating: 5, date: '2026-02-05', comment: 'تجربة فريدة بين الجبال! المنتجع تحفة معمارية وسط الطبيعة الخلابة.' },
        { name: 'هيفاء الزهراني', rating: 5, date: '2026-01-28', comment: 'الإطلالة على جبال العلا لا توصف! المكان ساحر والخدمة ممتازة.' },
        { name: 'سلطان الجهني', rating: 5, date: '2026-01-20', comment: 'أجمل منتجع في العلا! الفيلا الصخرية كانت تجربة مذهلة.' },
        { name: 'منى الشهري', rating: 4, date: '2026-01-12', comment: 'مكان هادئ ومميز، الطعام لذيذ والموظفين متعاونين.' },
        { name: 'بندر العصيمي', rating: 5, date: '2025-12-30', comment: 'العلا جميلة والمنتجع أجمل! حوض الجاكوزي مع إطلالة الجبال رائع.' },
        { name: 'شهد المالكي', rating: 5, date: '2025-12-22', comment: 'تجربة لا تنسى! المنتجع فخم والسبا مريح جداً.' },
        { name: 'راشد الحارثي', rating: 5, date: '2025-12-15', comment: 'مكان مثالي للاسترخاء بعيداً عن ضجيج المدينة.' },
        { name: 'أمل البقمي', rating: 4, date: '2025-12-08', comment: 'منتجع راقي وخدمة متميزة، الإفطار متنوع ولذيذ.' },
        { name: 'عمر الشمراني', rating: 5, date: '2025-11-28', comment: 'أفضل منتجع زرته في العلا! التصميم الصخري فريد من نوعه.' }
    ],
    shaden: [
        { name: 'فاطمة الأحمدي', rating: 5, date: '2026-02-08', comment: 'منتجع رائع ومناسب للعائلات! الغرف واسعة والإطلالة على الجبال خيالية.' },
        { name: 'عبدالعزيز الشهراني', rating: 5, date: '2026-01-30', comment: 'تجربة مميزة! الموقع قريب من الحجر الأثري والخدمة ممتازة.' },
        { name: 'نوف القحطاني', rating: 4, date: '2026-01-22', comment: 'منتجع جميل والإفطار متنوع ولذيذ. الأطفال استمتعوا بالمسبح كثيراً.' },
        { name: 'ماجد العتيبي', rating: 5, date: '2026-01-15', comment: 'السبا والساونا رائعين! مكان مثالي للاسترخاء والاستجمام.' },
        { name: 'أسماء الدوسري', rating: 5, date: '2025-12-29', comment: 'الطاقم محترف والخدمة سريعة. الغرف نظيفة والتصميم فخم.' },
        { name: 'سعد المطيري', rating: 4, date: '2025-12-18', comment: 'موقع ممتاز قريب من المعالم السياحية. المطعم يقدم أكلات متنوعة.' },
        { name: 'جواهر الغامدي', rating: 5, date: '2025-12-10', comment: 'حمام السباحة جميل والحديقة منظمة. تجربة لا تنسى!' },
        { name: 'خالد الحربي', rating: 5, date: '2025-11-28', comment: 'المنتجع يستحق التجربة! مرافق ممتازة وأسعار معقولة.' },
        { name: 'ريما الزهراني', rating: 5, date: '2025-11-20', comment: 'أجمل إجازة قضيناها! الجو هادئ والخدمة راقية جداً.' }
    ],
    chedi: [
        { name: 'يوسف الحكمي', rating: 5, date: '2026-02-09', comment: 'فندق أسطوري! التصميم فاخر والموقع قريب من الحجر التاريخي.' },
        { name: 'لمى العمري', rating: 5, date: '2026-02-02', comment: 'الإفطار من أفضل ما جربت! المنتجع يهتم بأدق التفاصيل.' },
        { name: 'طلال الغامدي', rating: 5, date: '2026-01-25', comment: 'تجربة استثنائية! السبا والمسبح رائعين والخدمة من الطراز الأول.' },
        { name: 'شهد البيشي', rating: 4, date: '2026-01-18', comment: 'منتجع هادئ ومريح. الغرف واسعة والإطلالة على الصحراء خيالية.' },
        { name: 'فيصل المالكي', rating: 5, date: '2026-01-10', comment: 'أفضل مكان للاسترخاء! استخدام الدراجات المجاني إضافة رائعة.' },
        { name: 'نورة القرشي', rating: 5, date: '2025-12-28', comment: 'الموظفون ودودون جداً والطعام الحلال متنوع ولذيذ.' },
        { name: 'عبدالله السهلي', rating: 5, date: '2025-12-20', comment: 'المنتجع يجمع بين الفخامة والأصالة. تجربة لا تنسى!' },
        { name: 'مها الشمراني', rating: 4, date: '2025-12-12', comment: 'مكان رائع للعائلات. المرافق متكاملة والأسعار معقولة.' },
        { name: 'سلمان العتيبي', rating: 5, date: '2025-12-05', comment: 'أجمل منتجع في العلا! الشرفات الخاصة إضافة مميزة جداً.' }
    ],
    fairmont: [
        { name: 'راشد العمري', rating: 5, date: '2026-02-12', comment: 'فندق عالمي المستوى! الموقع ممتاز في قلب الرياض والخدمة لا مثيل لها.' },
        { name: 'ليلى السديري', rating: 5, date: '2026-02-05', comment: 'المطاعم الستة كلها رائعة! تنوع مذهل في المأكولات والخدمة راقية جداً.' },
        { name: 'بدر الرشيد', rating: 5, date: '2026-01-28', comment: 'السبا والمسبح الداخلي من أفضل ما جربت في فنادق الرياض. تجربة فاخرة!' },
        { name: 'غادة المنصور', rating: 4, date: '2026-01-20', comment: 'الجناح التنفيذي واسع ومريح. الإطلالة على المدينة خيالية.' },
        { name: 'عبدالرحمن الدبيان', rating: 5, date: '2026-01-12', comment: 'موقع استراتيجي قريب من كل شيء. الفندق فخم والموظفين محترفين جداً.' },
        { name: 'نوال الفيصل', rating: 5, date: '2025-12-30', comment: 'نادي اللياقة مجهز بأحدث الأجهزة. الفندق يهتم بكل التفاصيل!' },
        { name: 'سعود الخالد', rating: 5, date: '2025-12-22', comment: 'خدمة الغرف ممتازة والطعام لذيذ. أنصح بالجناح الرئاسي للمناسبات الخاصة.' },
        { name: 'هند العنقري', rating: 4, date: '2025-12-15', comment: 'الفندق نظيف والإفطار متنوع. الواي فاي سريع في كل المبنى.' },
        { name: 'فهد السويلم', rating: 5, date: '2025-12-08', comment: 'أفضل فندق في الرياض للرحلات العملية! قاعات الاجتماعات ممتازة والخدمة احترافية.' }
    ],
    ashar: [
        { name: 'خالد الجهني', rating: 5, date: '2026-02-10', comment: 'تجربة فريدة! الخيام فاخرة والإطلالة على الجبال خيالية.' },
        { name: 'عبير الشمري', rating: 5, date: '2026-02-03', comment: 'المسبح اللانهائي رائع! المنتجع يجمع بين الفخامة والطبيعة الساحرة.' },
        { name: 'محمد العتيبي', rating: 5, date: '2026-01-27', comment: 'السبا والمساج من أفضل ما جربت. الخدمة احترافية والموظفين متعاونين.' },
        { name: 'نوف الدوسري', rating: 4, date: '2026-01-20', comment: 'الطعام لذيذ ومتنوع. المطعم التايلاندي تحديداً مميز جداً!' },
        { name: 'فيصل القحطاني', rating: 5, date: '2026-01-13', comment: 'الدراجات المجانية فكرة رائعة لاستكشاف المنطقة. تجربة لا تنسى!' },
        { name: 'ريم الغامدي', rating: 5, date: '2025-12-29', comment: 'الخيمة الملكية فاخرة جداً! الجاكوزي الخاص والمدخل المنفصل رائعين.' },
        { name: 'سعود المالكي', rating: 5, date: '2025-12-21', comment: 'موقع مثالي قريب من الحجر. المنتجع هادئ ومريح للاسترخاء.' },
        { name: 'مها الحربي', rating: 4, date: '2025-12-14', comment: 'الإفطار متنوع والمخبوزات الطازجة لذيذة. الأطفال استمتعوا كثيراً!' },
        { name: 'عمر الزهراني', rating: 5, date: '2025-12-07', comment: 'أجمل منتجع خيمي زرته! التصميم فريد والخدمة من الطراز الأول.' }
    ],
    caravan: [
        { name: 'أحمد السلمي', rating: 5, date: '2026-02-11', comment: 'تجربة لا تُنسى! الكابينة مريحة والإطلالة على الجبال ساحرة.' },
        { name: 'فاطمة الزهراني', rating: 5, date: '2026-02-04', comment: 'المطعم المكسيكي رائع! الطعام لذيذ والأجواء مميزة جداً.' },
        { name: 'خالد القحطاني', rating: 5, date: '2026-01-28', comment: 'دروس اليوغا وليالي الأفلام كانت تجربة مذهلة! المنتجع فريد من نوعه.' },
        { name: 'نورة الدوسري', rating: 4, date: '2026-01-21', comment: 'الدراجات المجانية ممتازة لاستكشاف المنطقة. الموظفين ودودين جداً.' },
        { name: 'عبدالله الشهري', rating: 5, date: '2026-01-14', comment: 'الجناح البريميوم فاخر! الشرفة الخاصة والإطلالة 360 درجة خيالية.' },
        { name: 'ريما الغامدي', rating: 5, date: '2026-01-07', comment: 'قرب الموقع من الحجر الأثري ميزة رائعة. المنتجع هادئ ومريح.' },
        { name: 'سعد العتيبي', rating: 5, date: '2025-12-30', comment: 'الإفطار النباتي والحلال متنوع ولذيذ. خيارات كثيرة للجميع!' },
        { name: 'هند المطيري', rating: 4, date: '2025-12-23', comment: 'الحمام مع الدش المطري فخم. المنتجع نظيف والخدمة ممتازة.' },
        { name: 'ماجد الحربي', rating: 5, date: '2025-12-16', comment: 'أفضل منتجع في العلا! الأثاث الخارجي والميني بار إضافات رائعة.' }
    ],
    mandarin: [
        { name: 'عبدالعزيز السديري', rating: 5, date: '2026-02-10', comment: 'فندق استثنائي! الخادم الشخصي متوفر 24 ساعة والخدمة فوق الممتازة.' },
        { name: 'لطيفة المنصور', rating: 5, date: '2026-02-03', comment: 'مطعم Globe رائع! القبة الجيوديسية مذهلة والطعام الأوروبي لذيذ جداً.' },
        { name: 'فهد الرشيد', rating: 5, date: '2026-01-27', comment: 'المسبح الداخلي 20 متر ممتاز! النادي الصحي مجهز بأحدث المعدات.' },
        { name: 'منال الخالد', rating: 5, date: '2026-01-20', comment: 'الجناح الملكي فاخر بكل المقاييس! التفاصيل المعمارية الأرابيسك تحفة فنية.' },
        { name: 'سلطان الدبيان', rating: 4, date: '2026-01-13', comment: 'موقع ممتاز بجانب مود مول. التحكم باللمس للإضاءة والستائر ذكي جداً.' },
        { name: 'شهد الفيصل', rating: 5, date: '2026-01-06', comment: 'سبا The Ladies مخصص للسيدات فقط وخدماته رائعة! تجربة استرخاء مميزة.' },
        { name: 'راشد العنقري', rating: 5, date: '2025-12-29', comment: 'مطعم La Brasserie تفاعلي ومبتكر! مشاهدة الطهاة أثناء العمل تجربة ممتعة.' },
        { name: 'أمل السويلم', rating: 5, date: '2025-12-22', comment: 'الإفطار استثنائي! التنوع والجودة من أفضل ما جربت في الرياض.' },
        { name: 'خالد الخثلان', rating: 5, date: '2025-12-15', comment: 'أفضل فندق 5 نجوم في الرياض! الفخامة والرقي في كل تفصيلة.' }
    ],
    movenpick: [
        { name: 'محمد العمري', rating: 5, date: '2026-02-11', comment: 'فندق رائع! المسبح على السطح مذهل والإطلالة خيالية.' },
        { name: 'سارة القحطاني', rating: 5, date: '2026-02-04', comment: 'المطعم الإيطالي لذيذ جداً! الطاقم متعاون والخدمة سريعة.' },
        { name: 'عبدالله الشهراني', rating: 5, date: '2026-01-28', comment: 'السبا وخدمات التدليك من أفضل ما جربت. استرخاء حقيقي!' },
        { name: 'نوف الدوسري', rating: 4, date: '2026-01-21', comment: 'الغرف نظيفة والحمام فاخر. قريب من الرياض جاليري مول.' },
        { name: 'فيصل المالكي', rating: 5, date: '2026-01-14', comment: 'الجناح الرئاسي واسع ومريح! المطبخ الكامل إضافة رائعة.' },
        { name: 'ريم الغامدي', rating: 5, date: '2026-01-07', comment: 'الحديقة الخضراء جميلة والشرفة مريحة للجلسات المسائية.' },
        { name: 'سعود الحربي', rating: 5, date: '2025-12-30', comment: 'الإفطار متنوع جداً! المطعم المغربي يقدم أطباق مميزة.' },
        { name: 'هند العتيبي', rating: 4, date: '2025-12-23', comment: 'موقع ممتاز والمواقف مجانية. الواي فاي سريع في كل الفندق.' },
        { name: 'خالد الزهراني', rating: 5, date: '2025-12-16', comment: 'أفضل فندق للعائلات في الرياض! المرافق متكاملة والخدمة راقية.' }
    ]
};

// عرض التعليقات (يجلب من backend + المحلية)
async function displayReviews() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || 'shebara';
    let reviews = hotelReviews[hotelParam] || hotelReviews.shebara || [];

    // محاولة جلب مراجعات من الـ backend
    try {
        const backendReviews = await ReviewsAPI.getAll();
        if (Array.isArray(backendReviews) && backendReviews.length > 0) {
            // تحويل مراجعات backend لصيغة العرض
            const apiReviews = backendReviews
                .filter(r => r.place_id === hotelParam) // حسب المكان
                .map(r => ({
                    name: r.user_id ? r.user_id.substring(0, 8) : 'مستخدم',
                    rating: r.rating,
                    date: r.created_at ? r.created_at.split('T')[0] : new Date().toISOString().split('T')[0],
                    comment: r.comment || '',
                    fromBackend: true
                }));
            // دمج مراجعات backend مع المحلية (backend أولاً)
            reviews = [...apiReviews, ...reviews];
        }
    } catch (err) {
        console.warn('تعذر جلب المراجعات من الـ backend:', err);
    }

    const reviewsList = document.getElementById('reviewsList');
    if (!reviewsList) return;

    // حساب متوسط التقييم
    const avgRating = reviews.length > 0
        ? (reviews.reduce((sum, r) => sum + r.rating, 0) / reviews.length).toFixed(1)
        : '0';
    const avgRatingElement = document.getElementById('averageRating');
    const reviewsCountElement = document.getElementById('reviewsCount');

    if (avgRatingElement) avgRatingElement.textContent = avgRating;
    if (reviewsCountElement) reviewsCountElement.textContent = `${reviews.length} تقييمات`;

    // عرض التعليقات
    let reviewsHTML = '';
    reviews.forEach(review => {
        const initials = review.name.split(' ').map(n => n[0]).join('');
        const starsHTML = Array(review.rating).fill('<i class="fas fa-star"></i>').join('');

        reviewsHTML += `
            <div class="review-card">
                <div class="review-header">
                    <div class="reviewer-info">
                        <div class="reviewer-avatar">${initials}</div>
                        <div class="reviewer-details">
                            <h4>${review.name}</h4>
                            <span class="review-date">${review.date}</span>
                        </div>
                    </div>
                    <div class="review-rating">
                        ${starsHTML}
                    </div>
                </div>
                <p class="review-content">${review.comment}</p>
            </div>
        `;
    });

    reviewsList.innerHTML = reviewsHTML;
}

// اختيار التقييم
let selectedRatingValue = 0;

function setRating(rating) {
    selectedRatingValue = rating;
    document.getElementById('selectedRating').value = rating;

    const stars = document.querySelectorAll('.star-rating i');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.remove('far');
            star.classList.add('fas', 'active');
        } else {
            star.classList.remove('fas', 'active');
            star.classList.add('far');
        }
    });
}

// إرسال تعليق جديد
async function submitReview(event) {
    event.preventDefault();

    // التحقق من تسجيل الدخول
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
    if (!loggedIn) {
        alert('⚠️ أنت لست مسجلاً!\n\nيجب عليك تسجيل الدخول أولاً لإضافة تعليق.\n\nسيتم تحويلك إلى صفحة تسجيل الدخول...');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 500);
        return;
    }

    // الحصول على معلومات المستخدم
    const userFirstName = localStorage.getItem('userFirstName') || '';
    const userLastName = localStorage.getItem('userLastName') || '';
    const userName = `${userFirstName} ${userLastName}`.trim() || 'مستخدم';
    const userId = localStorage.getItem('userId') || '';

    const rating = parseInt(document.getElementById('selectedRating').value);
    const comment = document.getElementById('reviewText').value.trim();

    if (rating === 0) {
        alert('الرجاء اختيار التقييم');
        return;
    }

    if (!comment) {
        alert('الرجاء كتابة تعليقك');
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || 'shebara';

    // محاولة إرسال المراجعة للـ backend
    let savedToBackend = false;
    if (userId && hotelParam.includes('-')) {
        // إذا كان place_id حقيقي (UUID) أرسله للـ backend
        try {
            await ReviewsAPI.create({
                place_id: hotelParam,
                user_id: userId,
                rating: rating,
                comment: comment
            });
            savedToBackend = true;
        } catch (err) {
            console.warn('تعذر حفظ المراجعة في الـ backend:', err);
        }
    }

    // حفظ محلياً أيضاً (للعرض الفوري)
    const newReview = {
        name: userName,
        rating: rating,
        date: new Date().toISOString().split('T')[0],
        comment: comment
    };

    if (!hotelReviews[hotelParam]) {
        hotelReviews[hotelParam] = [];
    }
    hotelReviews[hotelParam].unshift(newReview);
    localStorage.setItem('hotelReviews', JSON.stringify(hotelReviews));

    // إعادة عرض التعليقات
    await displayReviews();

    // إعادة تعيين النموذج
    document.getElementById('reviewForm').reset();
    setRating(0);

    // رسالة نجاح
    const msg = savedToBackend
        ? 'تم إضافة تعليقك بنجاح وحفظه في قاعدة البيانات! شكراً لمشاركتك'
        : 'تم إضافة تعليقك بنجاح! شكراً لمشاركتك';
    alert(msg);

    // التمرير إلى التعليقات
    document.getElementById('reviewsList').scrollIntoView({ behavior: 'smooth' });
}

// تحميل التعليقات المحفوظة من localStorage عند بدء التشغيل
const savedReviews = localStorage.getItem('hotelReviews');
if (savedReviews) {
    const parsed = JSON.parse(savedReviews);
    Object.keys(parsed).forEach(hotel => {
        if (!hotelReviews[hotel]) {
            hotelReviews[hotel] = [];
        }
        // دمج التعليقات المحفوظة مع الافتراضية
        hotelReviews[hotel] = [...parsed[hotel], ...hotelReviews[hotel]];
    });
}
