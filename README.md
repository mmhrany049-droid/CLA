# CLA / سیلا — Chemistry Lab Assistant / دستیار آزمایشگاه شیمی

> **فاز ۱ پیاده‌سازی شده: مدیر مواد اولیه (Starting Materials Manager)**
> Phase 1 implemented: Starting Materials Manager — per `CLA_Prompts/07_Development_Roadmap_and_Priorities.md`

---

## فارسی

**سیلا** یک «شیمیدان مجازی» آفلاین و دوزبانه (فارسی/انگلیسی) است — نه یک دستیار ساده.
نقشه راه پروژه در پوشه `CLA_Prompts/` قرار دارد (۹ فایل مشخصات).

### ویژگی‌های فاز ۱
- 📚 کتابخانه مواد اولیه با **۷۰ ماده پیش‌بارگذاری‌شده** (حلال‌ها، اسیدها و بازها، معرف‌های رایج، بلوک‌های ساختمانی) — همه با نام فارسی، CAS، خطرات GHS و خواص فیزیکی
- ➕ افزودن ماده با **SMILES، نام/CAS (جستجوی محلی) یا رسم ساختار** (ویرایشگر JSME — کاملاً آفلاین)
- 🧮 محاسبه خودکار شناسه‌ها با RDKit: SMILES کانونیکال، InChI، InChIKey، فرمول و جرم مولکولی
- 📦 **کنترل کامل موجودی**: افزایش/کاهش مقدار، تنظیم دقیق، واحد (g/mL/mol/…)، حداقل موجودی
- 🟢🟡⚪⛔ **وضعیت**: فعال / غیرفعال (غیرفعال = هرگز در سنتز استفاده نمی‌شود) / ناموجود / موجودی کم — به‌همراه تاریخچه کامل تغییرات
- 🔍 جستجو: متنی (فارسی/انگلیسی/CAS/مترادف)، تطابق دقیق InChIKey، **زیرساختار** و **شباهت** (Tanimoto)
- ⚠️ **ایمنی**: کدهای GHS با ترجمه فارسی و انگلیسی روی هر ماده؛ هشدارهای پیش‌سازهای regulated در یادداشت‌ها
- 🌐 **دوزبانه کامل** با چیدمان راست‌به‌چپ برای فارسی و سوئیچ زبان در نوار کناری
- 📤 ورود/خروج: CSV، JSON، SDF
- 🔌 **کاملاً آفلاین** — هیچ درخواست اینترنتی خودکاری وجود ندارد (تله‌متری Streamlit هم غیرفعال است)

### نصب و اجرا
```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt      # ویندوز: .venv\Scripts\pip
.venv/bin/streamlit run app.py                  # سپس مرورگر: http://localhost:8501
```
نصب وابستگی‌ها یک‌بار و با اینترنت انجام می‌شود؛ **اجرای برنامه کاملاً آفلاین است.**
پایگاه‌داده در اولین اجرا به‌طور خودکار ساخته و با مواد پیش‌فرض پر می‌شود
(`data/starting_materials/compounds.db`). برای ساخت دستی: `python scripts/init_db.py`.

### تست‌ها
```bash
python -m pytest tests/ -v        # ۲۲ تست: پایگاه‌داده، CRUD، جستجو، seed، IO، UI
```

### نکته ایمنی
سیلا جایگزین شیمیدان انسان نیست. اطلاعات GHS و خواص، curated و آموزشی هستند —
پیش از هر کار عملی، SDS تامین‌کننده و منابع معتبر را بررسی کنید.

---

## English

**CLA (سیلا)** is an offline-first, bilingual (Persian/English) **Virtual Chemist** — not a simple assistant.
The full specifications live in `CLA_Prompts/` (9 files). This repo currently implements **Phase 1: the Starting Materials Manager** (Streamlit, per the agreed stack decision), the foundation the synthesis engine will consume in Phase 2.

### Phase 1 features
- 📚 Materials library **pre-loaded with 70 common chemicals** (the 12 spec-mandated solvents, acids & bases, common reagents, simple building blocks) — each with Persian name, CAS, GHS hazards and physical properties
- ➕ Add materials **by SMILES, by name/CAS (local lookup only), or by drawing** (JSME editor, fully offline — assets bundled locally)
- 🧮 Automatic identifier computation via RDKit: canonical SMILES, InChI, InChIKey, formula, MW
- 📦 **Full stock control**: increase/decrease, exact set, units (g/mL/mol/…), minimum stock level, complete change history
- 🟢🟡⚪⛔ **Status**: Active / Inactive (never usable in synthesis) / OutOfStock / LowStock — derived honestly from quantity
- 🔍 Search: text (fa/en/CAS/synonyms), exact InChIKey, **substructure**, **similarity** (Morgan + Tanimoto)
- ⚠️ **Safety**: GHS H-codes with bilingual statements on every material; regulated-precursor warnings in notes
- 🌐 **Full bilingual UI** with RTL layout for Persian and instant language switching (persisted)
- 📤 Import/Export: CSV, JSON, SDF
- 🔌 **Completely offline** — zero automatic network requests (Streamlit telemetry disabled)

### Install & run
```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt      # Windows: .venv\Scripts\pip
.venv/bin/streamlit run app.py                  # then open http://localhost:8501
```
Dependency installation needs internet **once**; the application itself runs **fully offline**.
The SQLite database is created and seeded automatically on first launch
(`data/starting_materials/compounds.db`), or manually: `python scripts/init_db.py`.
Linux note: 2D rendering needs `libxrender1` (present on normal desktops); without it the app degrades gracefully.

### Tests
```bash
python -m pytest tests/ -v        # 22 tests: db, CRUD, search, seed, IO, UI-level add flow
```

### Project layout
```
CLA/
├── app.py                  # Streamlit entry point
├── backend/                # DB (SQLite), materials repo, RDKit chemistry, i18n, seed data, IO
├── frontend/               # Streamlit UI (pages: library, add/edit, search, transfer, settings)
├── modules/                # synthesis / properties / design / safety — Phase 2+ placeholders
├── local_ai/               # Ollama integration — Phase 3 placeholder
├── data/                   # runtime data (local-only, gitignored; copyable to another machine)
│   ├── starting_materials/compounds.db
│   └── user_settings/settings.json
├── scripts/init_db.py      # manual DB init + seed
├── tests/                  # pytest suite (backend + UI smoke/e2e)
├── docs/                   # architecture & Phase-1 decisions
├── third_party/            # attribution & licensing notes
└── CLA_Prompts/            # the 9 specification files (master documents)
```

### Safety disclaimer
CLA is not a replacement for a human chemist. GHS data and physical properties are curated for planning support — always verify against supplier SDS and authoritative sources before practical work.
