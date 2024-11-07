"""In this module we define equivalence of attributes for 'education' and 'skill'."""


EDUCATION_DEGREE: dict[str, str] = {
    # Jobvision degree
    'کاردانی': 'Associate',
    'لیسانس': 'Bachelor',
    'کارشناسی': 'Bachelor',
    'کارشناسی ارشد': 'Master',
    'فوق لیسانس': 'Master',
}


EDUCATION_COURSE: dict[str, str] = {
    # Jobvision course
    'کامپیوتر / فناوری اطلاعات': 'Computer and IT',
    'ریاضی و آمار': 'Math and Statics',
    'مهندسی برق': 'Electrical Engineering',
    'ایمنی/ محیط زیست': 'HSE',
    'مهندسی شیمی / پلیمر': 'Chemical Engineering/Polymer',
    'مهندسی صنایع': 'Industrial Engineering',
    'مدیریت / بازرگانی / کسب و کار': 'Business/Management/Commerce',
    'زبان و ادبیات': 'Literature',
    'مهندسی مکانیک': 'Mechanical Engineering',
    'مهندسی معدن / زمین شناسی': 'Mining Engineering/Geology',
    'مالی و حسابداری': 'Finance and Accounting',
    'اقتصاد': 'Economy',
    'مهندسی پزشکی': 'Medical Engineering',
    'مهندسی نفت / مهندسی انرژی': 'Petroleum Engineering/Energy Engineering',
    'مهندسی نساجی': 'Textile engineering',
    'مهندسی مواد و متالورژی': 'Materials engineering',
    'فیزیک': 'Physics',
}


SKILL_NAME: dict[str, str] = {
    # Jobvision skill name
}


SKILL_LEVEL: dict[str, str] = {
    # Jobvision skill level
    'مقدماتی': 'Basic',
    'متوسط': 'Intermediate',
    'پیشرفته': 'Advanced',
}



def equivalence_education_degree(degree: str) -> str:
    """Equivalence education degree to a standard value."""
    try:
        if degree in EDUCATION_DEGREE.keys():
            degree = EDUCATION_DEGREE[degree]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_education_degree"')
    
    return degree



def equivalence_education_course(course: str) -> str:
    """Equivalence education course to a standard value."""
    try:
        if course in EDUCATION_COURSE.keys():
            course = EDUCATION_COURSE[course]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_education_course"')
    
    return course



def equivalence_skill_name(skill_name: str) -> str:
    """Equivalence skill name to a standard value."""
    try:
        if skill_name in SKILL_NAME.keys():
            skill_name = SKILL_NAME[skill_name]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_skill_name"')
    
    return skill_name



def equivalence_skill_level(skill_level: str) -> str:
    """Equivalence skill level to a standard value."""
    try:
        if skill_level in SKILL_LEVEL.keys():
            skill_level = SKILL_LEVEL[skill_level]
    
    except Exception as e:
        print('Error in "joblisings.jobvision_ir.equivalence_skill_level"')
    
    return skill_level
