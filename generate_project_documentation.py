from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from reportlab.lib import colors
from reportlab.lib.units import inch

OUTPUT = 'WholeSync_Project_Documentation.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='ProjectTitle', fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.HexColor('#0F172A'), alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name='ProjectSubtitle', fontName='Helvetica', fontSize=12, leading=18, textColor=colors.HexColor('#334155'), alignment=1, spaceAfter=20))
styles.add(ParagraphStyle(name='Section', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#0F172A'), spaceBefore=18, spaceAfter=10))
styles.add(ParagraphStyle(name='SubSection', fontName='Helvetica-Bold', fontSize=13, leading=18, textColor=colors.HexColor('#1F2937'), spaceBefore=10, spaceAfter=6))
styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor('#111827'), spaceAfter=6))
styles.add(ParagraphStyle(name='Compact', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#111827'), spaceAfter=4))
styles.add(ParagraphStyle(name='Code', fontName='Courier', fontSize=8.5, leading=11, textColor=colors.HexColor('#111827'), backColor=colors.HexColor('#F8FAFC'), borderPadding=8, borderColor=colors.HexColor('#CBD5E1'), borderWidth=0.5, spaceBefore=8, spaceAfter=10))

body = []

def add_code(code):
    body.append(Preformatted(code, styles['Code']))

body.append(Spacer(1, 0.4 * inch))
body.append(Paragraph('WholeSync', styles['ProjectTitle']))
body.append(Paragraph('A B2B Wholesale Marketplace for Retailers and Wholesalers', styles['ProjectSubtitle']))
body.append(Paragraph('Project Documentation', styles['ProjectSubtitle']))
body.append(Spacer(1, 0.8 * inch))
team = [
    ['Team Members', 'Role'],
    ['Aswin I.', 'Developer'],
    ['Karthikeyan S.', 'Developer'],
    ['Naveen Kumar P.', 'Developer'],
    ['Saravanan P.', 'Developer'],
    ['Sivadurai R.', 'Developer'],
    ['Dr. T. Mahendran', 'Project Guide'],
]
team_table = Table(team, colWidths=[3.5 * inch, 2.1 * inch])
team_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#CBD5E1')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8FAFC'), colors.white]),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
]))
body.append(team_table)
body.append(PageBreak())

body.append(Paragraph('Certificate', styles['Section']))
body.append(Paragraph('This project is submitted in partial fulfilment of the requirements for the academic course in Computer Science and Engineering.', styles['Body']))
body.append(Paragraph('Project Title: WholeSync', styles['Body']))
body.append(Paragraph('Student Team:', styles['SubSection']))
body.append(Paragraph('• Aswin I.<br/>• Karthikeyan S.<br/>• Naveen Kumar P.<br/>• Saravanan P.<br/>• Sivadurai R.', styles['Body']))
body.append(Paragraph('Project Guide: Dr. T. Mahendran', styles['Body']))
body.append(Paragraph('Date: ____________________', styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Declaration', styles['Section']))
body.append(Paragraph('We, the undersigned students, declare that the project work titled WholeSync is our original work and has not been submitted elsewhere for academic credit.', styles['Body']))
body.append(Paragraph('Acknowledgement', styles['Section']))
body.append(Paragraph('We express our sincere gratitude to our guide, Dr. T. Mahendran, and the faculty members for their continuous support, encouragement, and guidance throughout the project.', styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Table of Contents', styles['Section']))
for item in [
    '1. Abstract',
    '2. Introduction',
    '3. Problem Statement',
    '4. Objectives',
    '5. Scope and Features',
    '6. Database Schema',
    '7. Modules and Functional Description',
    '8. System Design and Architecture',
    '9. Implementation Details',
    '10. Core Code Snippets',
    '11. Screenshot Section',
    '12. Testing and Validation',
    '13. Deployment and Run Guide',
    '14. Future Enhancements',
    '15. Conclusion',
    '16. References',
]:
    body.append(Paragraph(item, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Abstract', styles['Section']))
body.append(Paragraph('WholeSync is a web-based B2B marketplace that connects wholesalers and retailers in Tamil Nadu. The system allows wholesalers to list products, manage stock, and share their shop location. Retailers can search products, compare offers, bookmark items, and contact sellers efficiently. The application is built with Django and uses SQLite for development, providing a secure and practical digital marketplace.', styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Introduction', styles['Section']))
body.append(Paragraph('Modern business operations require efficient digital channels for buying and selling. Retailers face difficulty in discovering reliable wholesalers and comparing product prices. WholeSync solves this by creating a centralized marketplace where sellers and buyers can interact transparently. The system supports role-based accounts, district-wise product discovery, stock management, and map-enabled supplier location.', styles['Body']))
body.append(Paragraph('Problem Statement', styles['Section']))
body.append(Paragraph('Retailers often depend on informal communication and scattered sources to find suppliers. This causes slow decision-making, inconsistent pricing, and poor visibility of stock. WholeSync provides a structured digital environment for local B2B trade by connecting sellers and retailers in one platform.', styles['Body']))
body.append(Paragraph('Objectives', styles['Section']))
for obj in [
    'To build a digital marketplace connecting wholesalers and retailers.',
    'To provide a secure user registration and login system.',
    'To enable stock management and seller profile maintenance.',
    'To support product search, filtering, bookmarking, and comparison.',
    'To allow wholesalers to display their shop location using a map.',
    'To create a user-friendly and scalable academic project application.',
]:
    body.append(Paragraph('• ' + obj, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Scope and Features', styles['Section']))
body.append(Paragraph('The project includes user authentication, inventory management, retailer search, bookmarking, comparison, profile settings, and merchant location mapping. It is designed for local Tamil Nadu markets and can be expanded into a larger e-commerce platform in the future.', styles['Body']))
body.append(Paragraph('Core Features', styles['SubSection']))
for feature in [
    'Role-based registration for sellers and retailers',
    'Email verification for user security',
    'Seller dashboard for stock addition and updates',
    'Bulk stock upload support',
    'Retailer search with keyword, category, and district filters',
    'Bookmarking and compare features',
    'Map-based shop location selection and viewing',
    'Responsive web interface',
]:
    body.append(Paragraph('• ' + feature, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Database Schema', styles['Section']))
body.append(Paragraph('The database is implemented using Django ORM with SQLite in the development environment. The schema stores user details, seller profiles, stock items, bookmarks, and email verification tokens.', styles['Body']))
body.append(Paragraph('Schema Summary', styles['SubSection']))
summary = Table([
    ['Table Name', 'Purpose', 'Key Fields'],
    ['CustomUser', 'Stores user login and role information', 'id, username, email, role, email_verified'],
    ['EmailVerificationToken', 'Tracks email verification tokens', 'id, user_id, token, created_at'],
    ['SellerProfile', 'Stores business information and location', 'id, user_id, business_name, address, district, latitude, longitude'],
    ['StockItem', 'Stores seller products', 'id, seller_id, name, category, price, quantity, description'],
    ['Bookmark', 'Stores retailer saved products', 'id, user_id, item_id, created_at'],
], colWidths=[1.5 * inch, 2.2 * inch, 2.6 * inch])
summary.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
    ('GRID', (0, 0), (-1, -1), 0.7, colors.HexColor('#94A3B8')),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
body.append(summary)
body.append(Spacer(1, 0.2 * inch))
body.append(Paragraph('Relationships', styles['SubSection']))
body.append(Paragraph('• CustomUser to SellerProfile: One-to-One<br/>• CustomUser to EmailVerificationToken: One-to-Many<br/>• CustomUser to StockItem: One-to-Many<br/>• CustomUser to Bookmark: One-to-Many<br/>• StockItem to Bookmark: One-to-Many', styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Database Schema (Model Logic)', styles['Section']))
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
body.append(PageBreak())

body.append(Paragraph('Modules and Functional Description', styles['Section']))
for name, desc in [
    ('Authentication Module', 'Controls registration, login, logout, and email verification flows.'),
    ('Seller Management Module', 'Allows sellers to update profile information, add stock, and upload inventory.'),
    ('Retailer Module', 'Enables search, filtering, bookmarking, and product comparison.'),
    ('Location Module', 'Allows sellers to mark shop location and lets retailers view it on a map.'),
    ('Admin Module', 'Provides backend management of the application data.'),
]:
    body.append(Paragraph(name, styles['SubSection']))
    body.append(Paragraph(desc, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('System Design and Architecture', styles['Section']))
body.append(Paragraph('The application follows a typical Django three-tier architecture. The frontend layer uses HTML, CSS, and JavaScript templates. The application layer contains Django views, forms, and business logic. The data layer uses SQLite database tables generated via models and migrations.', styles['Body']))
body.append(Paragraph('Technology Stack', styles['SubSection']))
for tech in [
    'Frontend: HTML, CSS, JavaScript',
    'Backend: Django 5.2, Python 3.11+',
    'Database: SQLite for development',
    'Mapping: Leaflet.js and OpenStreetMap',
    'Security: Django auth, email verification, rate limiting',
]:
    body.append(Paragraph('• ' + tech, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Implementation Details', styles['Section']))
body.append(Paragraph('The project was developed in modules and integrated progressively. Authentication and user roles were implemented first, followed by seller inventory management and retailer features. Finally, location mapping and UI refinements were added to improve user trust and business utility.', styles['Body']))
body.append(Paragraph('Main Code Excerpts', styles['SubSection']))
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
body.append(PageBreak())

body.append(Paragraph('Project Screenshots', styles['Section']))
body.append(Paragraph('The following section provides the required screenshot placeholders for the final submission. These areas can be replaced with actual project screenshots during printing or report binding.', styles['Body']))
for idx in range(1, 5):
    body.append(Paragraph(f'Screenshot {idx}: Project Interface', styles['SubSection']))
    body.append(Paragraph('________________________________________________________________________________<br/>Home page / Registration page / Seller dashboard / Map view', styles['Compact']))
    body.append(Spacer(1, 0.15 * inch))
body.append(PageBreak())

body.append(Paragraph('Testing and Validation', styles['Section']))
body.append(Paragraph('The system was validated through functional checks and Django-based testing. Core flows such as user registration, retailer search, seller stock management, and map location functionality were verified to work successfully.', styles['Body']))
for check in [
    'Registration and login flow works correctly.',
    'Retailers can search and compare products.',
    'Sellers can add, update, and delete stock items.',
    'Seller location is saved and displayed correctly.',
    'Password visibility toggle works on login and registration forms.',
]:
    body.append(Paragraph('• ' + check, styles['Body']))
body.append(PageBreak())

body.append(Paragraph('Deployment and Run Guide', styles['Section']))
body.append(Paragraph('The project runs in a local Django environment and can be deployed to hosting platforms such as Render.', styles['Body']))
add_code(r'''cd "d:\whole-sync\pocket-santhai"
python -m venv .venv
.
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
''')
body.append(PageBreak())

body.append(Paragraph('Future Enhancements', styles['Section']))
for item in [
    'Order management and payment integration',
    'Real-time chat between buyers and sellers',
    'Seller analytics dashboard',
    'Multi-language support',
    'Expanded location services and delivery integration',
]:
    body.append(Paragraph('• ' + item, styles['Body']))
body.append(Paragraph('Conclusion', styles['Section']))
body.append(Paragraph('WholeSync is a practical and modern B2B marketplace application that addresses the needs of local wholesalers and retailers. It combines secure authentication, digital inventory management, information visibility, and map-based seller location into a single unified system. The project demonstrates the application of Django framework principles, database design, and full-stack development in a real-world business scenario.', styles['Body']))
body.append(Paragraph('References', styles['Section']))
body.append(Paragraph('1. Django Official Documentation<br/>2. SQLite Documentation<br/>3. OpenStreetMap and Leaflet JS Documentation<br/>4. Python Official Documentation', styles['Body']))
body.append(Paragraph('Submitted by:', styles['SubSection']))
body.append(Paragraph('Aswin I., Karthikeyan S., Naveen Kumar P., Saravanan P., Sivadurai R.', styles['Body']))
body.append(Paragraph('Project Guide: Dr. T. Mahendran', styles['Body']))

pdf = SimpleDocTemplate(OUTPUT, pagesize=A4, rightMargin=0.6 * inch, leftMargin=0.6 * inch, topMargin=0.5 * inch, bottomMargin=0.5 * inch)
pdf.build(body)
print('Created PDF:', OUTPUT)
