def get_xpath_for_option(option):
    # List of dropdown options
    dropdown_options = ["الرجاء الاختيار","التجارة", "المقاولات", "التشغيل والصيانة والنظافة للمنشآت",
                        "العقارات والأراضي","الصناعة والتعدين والتدوير","الغاز والمياه والطاقة",
                        "المناجم والبترول والمحاجر","الإعلام والنشر والتوزيع","الاتصالات وتقنية المعلومات",
                        "الزراعة والصيد","الرعاية الصحية والنقاهة","التعليم والتدريب",
                        "التوظيف والاستقدام","الأمن والسلامة","النقل والبريد والتخزين",
                        "المهن الاستشارية","السياحة والمطاعم والفنادق وتنظيم المعارض",
                        "المالية والتمويل والتأمين","الخدمات الأخرى"]

    # Check if the option exists in the list
    if option in dropdown_options:
        # Find the index of the option and create the XPath with index+1 for li[]
        index = dropdown_options.index(option)
        xpath = f'//*[@id="basicInfo"]/div/div[4]/div/div/div/ul/li[{index + 1}]/a'
        return xpath
    else:
        return "Option not found in the dropdown list."