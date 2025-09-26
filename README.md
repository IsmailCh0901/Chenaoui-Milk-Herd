ELEVAGE LAITIER CHENAOUI – Herd Manager

A small, self-hosted herd management web app built with Django and Django REST Framework.
Track animals (ear tag, name, sex, breed, DOB), parents & children, pedigree up to any depth, and milk yield over time. Includes a simple JSON API, a modern UI with table/cards views, search & filters, dark mode, and charts.

Built for Chenaoui’s milk project. Runs locally with SQLite by default.

✨ Features

Animal registry – ear tag, name, sex (F/M/U), breed, DOB, alive

Parents / Children – cross-linked detail pages; children list shows birth year

Pedigree viewer – tidy tree with adjustable depth and contribution %

Milk records – daily liters per animal + trend chart
(hidden for males)

List views – search, filter by sex, sort by ear tag / name / breed / DOB, pagination

Two layouts – table or cards

Dashboard widgets – 7-day milk trend, sex ratio, top breeds

Dark mode – automatic toggle

Admin – manage everything through Django Admin

API – read/write endpoints for animals & milk records (DRF)

🖼 Screenshots

Add your images to /docs/ and link them here.

Animals list (table & cards)

Animal detail (parents, children, pedigree)

Dashboard charts (milk/sex/breeds)

🧱 Tech Stack

Backend – Django 5, Django REST Framework

Database – SQLite (default); any Django DB works

Frontend – Django templates, utility classes, Chart.js

Auth/Admin – Django admin

🚀 Quick Start
# 1) Clone
git clone https://github.com/<you>/<repo>.git
cd <repo>

# 2) Create & activate a virtualenv
# Windows
py -m venv .venv
.venv\Scripts\activate
# macOS/Linux
# python3 -m venv .venv
# source .venv/bin/activate

# 3) Install requirements
pip install -r requirements.txt  # or: pip install django djangorestframework

# 4) Migrate DB & create an admin user
python manage.py migrate
python manage.py createsuperuser

# 5) Run the dev server
python manage.py runserver


Open: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

API root: http://127.0.0.1:8000/api/

Animals list: http://127.0.0.1:8000/

📦 Project Structure
herd/                         # Django project
  settings.py / urls.py / wsgi.py
herdapp/                      # Main app
  models.py                   # Animal, MilkRecord
  views.py                    # list/detail + dashboard
  serializers.py              # DRF serializers
  templates/herdapp/
    base.html
    animal_list.html          # dashboard + list
    animal_detail.html        # detail + pedigree + milk
    _pedigree_node.html       # (if using server-rendered tree nodes)
  static/ (optional)          # put local JS/CSS if not using CDNs

🗃 Data Model (simplified)

Animal

ear_tag (unique), name, sex (F/M/U), breed, date_of_birth, is_alive

sire (FK→Animal, null), dam (FK→Animal, null)

MilkRecord

animal (FK→Animal)

date (date)

liters (decimal/float)

🔌 API (DRF)
Endpoint	Methods	Notes
/api/animals/	GET, POST	List / create animals
/api/animals/<id>/	GET, PUT, PATCH, DELETE	Single animal
/api/milk-records/	GET, POST	List / create milk entries
/api/milk-records/<id>/	GET, PUT, PATCH, DELETE	Single entry

Example (create milk record):

curl -X POST http://127.0.0.1:8000/api/milk-records/ \
  -H "Content-Type: application/json" \
  -d '{"animal": 1, "date": "2025-08-18", "liters": 18.75}'

🧭 Usage Tips

Add animals via Admin or “+ Add animal” on the list page.

Set sire and dam to enable the pedigree tree.

Use the Level control on detail pages to adjust pedigree depth.

Add milk records to populate the milk trend chart
(the chart is suppressed for males automatically).

The list page supports search, sex filter, sorting, and table/cards toggle.

⚙️ Configuration

Default DB: SQLite. For Postgres/MySQL, edit DATABASES in herd/settings.py.

Static files: for production, run python manage.py collectstatic and serve via your web server.

Chart.js is loaded from the CDN by default. If you prefer a local file, put it under herdapp/static/vendor/chartjs/ and include it with {% static %}.

🧪 Development

Code style: standard Django

Tests: (optional) place them in herdapp/tests.py

Useful commands:

python manage.py shell
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

🛣 Roadmap

CSV/Excel import/export

Lactation periods & per-animal stats

User roles/permissions

Mobile-first quick entry for milk

🤝 Contributing

PRs and issues are welcome.
Please open an issue describing your change before large PRs.

📄 License

MIT — see LICENSE.

🙌 Acknowledgements

Built for ELEVAGE LAITIER CHENAOUI to simplify real-world herd tracking with a friendly, fast UI.
