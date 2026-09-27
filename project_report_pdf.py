from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.units import inch

OUTPUT = 'WholeSync_Project_Documentation.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='DocTitleCustom', fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name='DocSubtitleCustom', fontName='Helvetica', fontSize=12, leading=18, textColor=colors.HexColor('#334155'), alignment=1, spaceAfter=18))
styles.add(ParagraphStyle(name='SectionTitleCustom', fontName='Helvetica-Bold', fontSize=16, leading=22, textColor=colors.HexColor('#0F172A'), spaceBefore=18, spaceAfter=10))
styles.add(ParagraphStyle(name='SubTitleCustom', fontName='Helvetica-Bold', fontSize=12.5, leading=18, textColor=colors.HexColor('#1F2937'), spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name='BodyTextCustom', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#111827'), spaceAfter=6))
styles.add(ParagraphStyle(name='CodeTextCustom', fontName='Courier', fontSize=8.2, leading=11, textColor=colors.HexColor('#111827'), backColor=colors.HexColor('#F8FAFC'), borderPadding=8, borderColor=colors.HexColor('#CBD5E1'), borderWidth=0.5, spaceBefore=8, spaceAfter=10))

story = []

def add_paragraph(text, style='BodyTextCustom'):
    story.append(Paragraph(text, styles[style]))


def add_code(code):
    story.append(Preformatted(code, styles['CodeTextCustom']))

# cover page
story.append(Spacer(1, 0.35 * inch))
story.append(Paragraph('WholeSync', styles['DocTitleCustom']))
story.append(Paragraph('A B2B Wholesale Marketplace for Retailers and Wholesalers', styles['DocSubtitleCustom']))
story.append(Paragraph('Project Documentation', styles['DocSubtitleCustom']))
story.append(Spacer(1, 0.7 * inch))
teams = [
    ['Team Members', 'Role'],
    ['Aswin I.', 'Developer'],
    ['Karthikeyan S.', 'Developer'],
    ['Naveen Kumar P.', 'Developer'],
    ['Saravanan P.', 'Developer'],
    ['Sivadurai R.', 'Developer'],
    ['Dr. T. Mahendran', 'Project Guide'],
]
team_table = Table(teams, colWidths=[3.4 * inch, 2.2 * inch])
team_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#CBD5E1')),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
]))
story.append(team_table)
story.append(PageBreak())

# certificate
add_paragraph('Certificate', 'SectionTitleCustom')
add_paragraph('This project is submitted in partial fulfillment of the requirements for the academic programme in Computer Science and Engineering.', 'BodyTextCustom')
add_paragraph('Project Title: WholeSync', 'BodyTextCustom')
add_paragraph('Student Team:', 'SubTitleCustom')
add_paragraph('• Aswin I.<br/>• Karthikeyan S.<br/>• Naveen Kumar P.<br/>• Saravanan P.<br/>• Sivadurai R.', 'BodyTextCustom')
add_paragraph('Project Guide: Dr. T. Mahendran', 'BodyTextCustom')
add_paragraph('Date: ______________________', 'BodyTextCustom')
add_paragraph('Signature of Guide: ______________________', 'BodyTextCustom')
story.append(PageBreak())

# declaration
add_paragraph('Declaration', 'SectionTitleCustom')
add_paragraph('We, the undersigned students, declare that the project work titled “WholeSync” is our original work and has not been submitted elsewhere for academic credit.', 'BodyTextCustom')
add_paragraph('Acknowledgement', 'SectionTitleCustom')
add_paragraph('We sincerely thank our project guide, Dr. T. Mahendran, for constant guidance, encouragement, and support throughout the project work.', 'BodyTextCustom')
story.append(PageBreak())

# TOC
add_paragraph('Table of Contents', 'SectionTitleCustom')
for item in [
    '1. Abstract', '2. Introduction', '3. Problem Statement', '4. Objectives', '5. Scope and Features',
    '6. Database Schema', '7. Modules and Functional Description', '8. System Design and Architecture',
    '9. Implementation Details', '10. Core Code Snippets', '11. Screenshot Section', '12. Testing and Validation',
    '13. Deployment and Run Guide', '14. Future Enhancements', '15. Conclusion', '16. References',
]:
    add_paragraph(item, 'BodyTextCustom')
story.append(PageBreak())

# abstract intro
add_paragraph('Abstract', 'SectionTitleCustom')
add_paragraph('WholeSync is a web-based B2B marketplace platform designed to connect wholesalers and retailers across Tamil Nadu. The application enables wholesalers to manage inventory and maintain business profiles, while retailers can search, compare, bookmark, and contact sellers easily. The system is developed using Django and SQLite and is designed to be scalable, secure, and practical for local trade.', 'BodyTextCustom')
story.append(PageBreak())

add_paragraph('Introduction', 'SectionTitleCustom')
add_paragraph('The project addresses the common problem of fragmented trade communication between wholesalers and retailers. Many local businesses rely on informal communication and lack a digital marketplace that is easy to use. WholeSync provides a structured platform that improves product visibility, trust, and regional business efficiency.', 'BodyTextCustom')
add_paragraph('Problem Statement', 'SectionTitleCustom')
add_paragraph('Retailers often face difficulty locating reliable sellers and comparing prices. Wholesalers also need a digital presence to publish inventory and reach more buyers. WholeSync fills this gap by providing a role-based B2B marketplace with inventory management, compare features, and seller location visibility.', 'BodyTextCustom')
add_paragraph('Objectives', 'SectionTitleCustom')
for obj in [
    'To build a digital marketplace connecting wholesalers and retailers.',
    'To provide secure and role-based registration and login.',
    'To enable wholesaler stock management and business profile maintenance.',
    'To allow retailers to search, filter, compare, and bookmark products.',
    'To provide map-based shop location view for trusted seller discovery.',
    'To develop a functional and professional academic project application.',
]:
    add_paragraph('• ' + obj, 'BodyTextCustom')
story.append(PageBreak())

# features
add_paragraph('Scope and Features', 'SectionTitleCustom')
add_paragraph('The application is designed for Tamil Nadu-based wholesale and retail trade. It includes seller inventory management, retailer search, bookmark system, price comparison, map-based location visibility, and a responsive web interface. The system can also be extended to include payment integration, messaging, and analytics in the future.', 'BodyTextCustom')
add_paragraph('Core Features', 'SubTitleCustom')
for feature in [
    'Role-based registration for sellers and retailers',
    'Email verification for account authenticity',
    'Seller dashboard for managing stock',
    'Bulk stock upload support',
    'Retailer search with district and category filters',
    'Bookmarking and comparison functionality',
    'Map-based seller location selection and viewing',
    'Responsive design for desktop and mobile use',
]:
    add_paragraph('• ' + feature, 'BodyTextCustom')
story.append(PageBreak())

# database section
add_paragraph('Database Schema', 'SectionTitleCustom')
add_paragraph('The database is implemented using Django ORM, with SQLite used in the development environment. The schema is designed to support user roles, seller profiles, stock items, bookmarks, and email verification tokens.', 'BodyTextCustom')
summary = Table([
    ['Table Name', 'Purpose', 'Key Fields'],
    ['CustomUser', 'Stores user login and role information', 'id, username, email, role, email_verified'],
    ['EmailVerificationToken', 'Stores email verification tokens', 'id, user_id, token, created_at'],
    ['SellerProfile', 'Stores seller profile data and location', 'id, user_id, business_name, address, district, latitude, longitude'],
    ['StockItem', 'Stores seller product records', 'id, seller_id, name, category, price, quantity, description'],
    ['Bookmark', 'Stores retailer favorites', 'id, user_id, item_id, created_at'],
], colWidths=[1.6 * inch, 2.2 * inch, 2.4 * inch])
summary.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
    ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#94A3B8')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
story.append(summary)
add_paragraph('Relationship Summary:', 'SubTitleCustom')
add_paragraph('• CustomUser to SellerProfile: One-to-One<br/>• CustomUser to EmailVerificationToken: One-to-Many<br/>• CustomUser to StockItem: One-to-Many<br/>• CustomUser to Bookmark: One-to-Many<br/>• StockItem to Bookmark: One-to-Many', 'BodyTextCustom')
story.append(PageBreak())

add_paragraph('Database Model Code', 'SectionTitleCustom')
add_code("""# marketplace/models.py
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('seller', 'Wholesale Seller'),
        ('retailer', 'Retailer'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=200)
    address = models.TextField()
    district = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class StockItem(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='stock_items')
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
""")
story.append(PageBreak())

# modules
add_paragraph('Modules and Functional Description', 'SectionTitleCustom')
for module_name, description in [
    ('Authentication Module', 'Handles registration, login, logout, and email verification.'),
    ('Seller Management Module', 'Allows wholesalers to add, update, and delete stock entries.'),
    ('Retailer Search Module', 'Provides product search, district filtering, and comparison features.'),
    ('Bookmark Module', 'Stores retailers’ favourite product lists.'),
    ('Map Location Module', 'Lets sellers pin their location and lets retailers view the location on a map.'),
    ('Admin Module', 'Provides backend data management through Django admin.'),
]:
    add_paragraph(module_name, 'SubTitleCustom')
    add_paragraph(description, 'BodyTextCustom')
story.append(PageBreak())

# architecture
add_paragraph('System Design and Architecture', 'SectionTitleCustom')
add_paragraph('The application follows a standard Django three-tier model: frontend, application logic, and database layer. HTML pages are rendered using Django templates, requests are handled in view files, and all persistent data is stored in SQLite tables generated from models.', 'BodyTextCustom')
add_paragraph('Technology Stack', 'SubTitleCustom')
for tech in [
    'Frontend: HTML, CSS, JavaScript',
    'Backend: Django 5.2, Python 3.11+',
    'Database: SQLite for development',
    'Mapping: Leaflet.js and OpenStreetMap',
    'Security: Role validation, email verification, rate limiting',
]:
    add_paragraph('• ' + tech, 'BodyTextCustom')
story.append(PageBreak())

# implementation details
add_paragraph('Implementation Details', 'SectionTitleCustom')
add_paragraph('The project was implemented in logical phases: authentication, seller dashboard, retailer features, and map integration. Each phase was tested and refined to improve usability and professionalism.', 'BodyTextCustom')
add_paragraph('Main Code Snippets', 'SubTitleCustom')
add_code("""# marketplace/urls.py
urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('search/', search, name='search'),
    path('bookmarks/', bookmarks_view, name='bookmarks'),
    path('compare/', compare_view, name='compare'),
    path('seller/location/<int:user_id>/', seller_location, name='seller_location'),
    path('seller/profile/', seller_profile, name='seller_profile'),
]
""")
add_code("""# marketplace/settings.py
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', str(BASE_DIR / 'db.sqlite3')),
    }
}
""")
story.append(PageBreak())

# screenshot placeholders
add_paragraph('Project Screenshots', 'SectionTitleCustom')
add_paragraph('This section is reserved for the actual project screenshots to be inserted in the final printed copy of the documentation.', 'BodyTextCustom')
for idx in range(1, 5):
    add_paragraph(f'Screenshot {idx}: Project Interface', 'SubTitleCustom')
    add_paragraph('______________________________________________________________<br/>Home page / Registration page / Seller dashboard / Map view', 'BodyTextCustom')
    story.append(Spacer(1, 0.12 * inch))
story.append(PageBreak())

# testing and validation
add_paragraph('Testing and Validation', 'SectionTitleCustom')
add_paragraph('The application was validated by testing the major project flows and ensuring that core operations behave correctly. The checks include registration, login, stock management, search, comparison, bookmark usage, and seller location mapping.', 'BodyTextCustom')
for item in [
    'User registration and login work correctly.',
    'Sellers can add and edit stock items.',
    'Retailers can search and compare products.',
    'Bookmarks save and display properly.',
    'Seller location is stored and displayed on the map.',
    'Password visibility toggle works on login and registration forms.',
]:
    add_paragraph('• ' + item, 'BodyTextCustom')
story.append(PageBreak())

# deployment guide
add_paragraph('Deployment and Run Guide', 'SectionTitleCustom')
add_paragraph('The project can be run locally through the Django development server. The commands below are used for setup and execution.', 'BodyTextCustom')
add_code("""cd \"d:\\whole-sync\\pocket-santhai\"
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
""")
story.append(PageBreak())

# future enhancements and conclusion
add_paragraph('Future Enhancements', 'SectionTitleCustom')
for item in [
    'Secure order placement and payment gateway integration.',
    'Real-time chat between sellers and retailers.',
    'Analytics dashboards for sales and stock trends.',
    'Multi-language support for Tamil and English.',
    'Expanded logistics and delivery integration.',
]:
    add_paragraph('• ' + item, 'BodyTextCustom')
add_paragraph('Conclusion', 'SectionTitleCustom')
add_paragraph('WholeSync is a practical and meaningful B2B marketplace application that connects wholesalers and retailers while improving transparency, convenience, and efficiency in local trading. It demonstrates the use of Django framework, database design, authentication, and responsive web development in a real-world scenario. The project is suitable for academic evaluation, further enhancement, and practical deployment.', 'BodyTextCustom')
add_paragraph('References', 'SectionTitleCustom')
add_paragraph('1. Django Documentation<br/>2. SQLite Documentation<br/>3. OpenStreetMap and Leaflet JS Documentation<br/>4. Python Official Documentation', 'BodyTextCustom')
add_paragraph('Submitted by:', 'SubTitleCustom')
add_paragraph('Aswin I., Karthikeyan S., Naveen Kumar P., Saravanan P., Sivadurai R.', 'BodyTextCustom')
add_paragraph('Guided by: Dr. T. Mahendran', 'BodyTextCustom')

pdf = SimpleDocTemplate(OUTPUT, pagesize=A4, rightMargin=0.6 * inch, leftMargin=0.6 * inch, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
pdf.build(story)
print('Created PDF:', OUTPUT)
