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
}


SKILL_NAME: dict[str, str] = {
    # Jobvision skill name
    
}


SKILL_LEVEL: dict[str, str] = {
    # Jobvision level
    'مقدماتی': 'Basic',
    'متوسط': 'Intermediate',
    'پیشرفته': 'Advanced',
}
