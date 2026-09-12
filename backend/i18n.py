"""CLA / سیلا — bilingual UI strings (spec 00: Full Persian + English support).

``t(key, lang)`` returns the Persian (fa) or English (en) string.
GHS hazard statements (H-codes) are translated for display; the database
stores only the codes (spec 06: ``ghs_hazards`` = JSON list).

Persian GHS texts are concise working translations of the official hazard
statements — for regulatory use always consult the supplier SDS.
"""

from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    # --- app shell / navigation -------------------------------------------
    "app.title": {"fa": "سیلا — دستیار آزمایشگاه شیمی", "en": "CLA — Chemistry Lab Assistant"},
    "app.subtitle": {"fa": "شیمیدان مجازی — فاز ۱: مدیریت مواد اولیه",
                     "en": "Virtual Chemist — Phase 1: Starting Materials Manager"},
    "nav.library": {"fa": "📚 کتابخانه مواد", "en": "📚 Materials Library"},
    "nav.add_edit": {"fa": "➕ افزودن / ویرایش ماده", "en": "➕ Add / Edit Material"},
    "nav.search": {"fa": "🔍 جستجوی پیشرفته", "en": "🔍 Advanced Search"},
    "nav.transfer": {"fa": "📦 ورود / خروج داده", "en": "📦 Import / Export"},
    "nav.settings": {"fa": "⚙️ تنظیمات", "en": "⚙️ Settings"},
    "sidebar.language": {"fa": "🌐 زبان / Language", "en": "🌐 Language / زبان"},
    "sidebar.offline": {"fa": "🔌 حالت آفلاین — بدون اتصال به اینترنت",
                        "en": "🔌 Offline mode — no internet connection"},
    "sidebar.version": {"fa": "نسخه", "en": "Version"},
    "sidebar.db": {"fa": "پایگاه‌داده", "en": "Database"},

    # --- library page ------------------------------------------------------
    "library.title": {"fa": "کتابخانه مواد اولیه", "en": "Starting Materials Library"},
    "library.filter_status": {"fa": "فیلتر وضعیت", "en": "Filter by status"},
    "library.quick_search": {"fa": "جستجوی سریع (نام، CAS، SMILES…)",
                             "en": "Quick search (name, CAS, SMILES…)"},
    "library.count": {"fa": "ماده", "en": "material(s)"},
    "library.select_hint": {"fa": "یک ردیف را از جدول انتخاب کنید تا جزئیات و کنترل‌ها نمایش داده شود.",
                            "en": "Select a row in the table to see details and controls."},
    "library.details": {"fa": "جزئیات ماده", "en": "Material details"},
    "library.structure": {"fa": "ساختار دوبعدی", "en": "2D structure"},
    "library.no_structure": {"fa": "ساختاری برای نمایش وجود ندارد (RDKit لازم است).",
                             "en": "No structure to display (RDKit required)."},
    "library.stock_control": {"fa": "کنترل موجودی", "en": "Stock control"},
    "library.adjust_delta": {"fa": "تغییر مقدار (+ / −)", "en": "Adjust amount (+ / −)"},
    "library.apply_delta": {"fa": "اعمال تغییر", "en": "Apply adjustment"},
    "library.set_quantity": {"fa": "تنظیم دقیق مقدار", "en": "Set exact quantity"},
    "library.enable": {"fa": "✅ فعال کردن", "en": "✅ Enable (Active)"},
    "library.disable": {"fa": "⛔ غیرفعال کردن کامل", "en": "⛔ Disable completely (Inactive)"},
    "library.status_note_disabled": {
        "fa": "این ماده غیرفعال است و در سنتز استفاده نخواهد شد.",
        "en": "This material is disabled and will NOT be used in synthesis."},
    "library.edit": {"fa": "✏️ ویرایش این ماده", "en": "✏️ Edit this material"},
    "library.delete": {"fa": "🗑️ حذف ماده", "en": "🗑️ Delete material"},
    "library.delete_confirm": {"fa": "حذف را تأیید می‌کنم (غیرقابل بازگشت)",
                               "en": "I confirm deletion (cannot be undone)"},
    "library.deleted": {"fa": "ماده «{name}» حذف شد.", "en": "Material “{name}” deleted."},
    "library.history": {"fa": "تاریخچه تغییرات", "en": "Change history"},
    "library.ghs": {"fa": "خطرات GHS", "en": "GHS hazards"},
    "library.properties": {"fa": "خواص فیزیکی", "en": "Physical properties"},
    "library.notes": {"fa": "یادداشت‌ها", "en": "Notes"},
    "library.saved_qty": {"fa": "مقدار به‌روزرسانی شد.", "en": "Quantity updated."},
    "library.saved_status": {"fa": "وضعیت به‌روزرسانی شد.", "en": "Status updated."},

    # --- table columns ------------------------------------------------------
    "col.name": {"fa": "نام", "en": "Name"},
    "col.name_en": {"fa": "نام انگلیسی", "en": "English name"},
    "col.name_fa": {"fa": "نام فارسی", "en": "Persian name"},
    "col.smiles": {"fa": "SMILES", "en": "SMILES"},
    "col.cas": {"fa": "CAS", "en": "CAS"},
    "col.formula": {"fa": "فرمول", "en": "Formula"},
    "col.mw": {"fa": "جرم مولکولی", "en": "Mol. weight"},
    "col.quantity": {"fa": "مقدار", "en": "Quantity"},
    "col.unit": {"fa": "واحد", "en": "Unit"},
    "col.min_stock": {"fa": "حداقل موجودی", "en": "Min stock"},
    "col.status": {"fa": "وضعیت", "en": "Status"},
    "col.inchikey": {"fa": "InChIKey", "en": "InChIKey"},
    "col.synonyms": {"fa": "مترادف‌ها", "en": "Synonyms"},
    "col.created_at": {"fa": "تاریخ افزودن", "en": "Date added"},
    "col.updated_at": {"fa": "آخرین تغییر", "en": "Last modified"},
    "col.similarity": {"fa": "شباهت", "en": "Similarity"},

    # --- statuses ------------------------------------------------------------
    "status.Active": {"fa": "🟢 فعال", "en": "🟢 Active"},
    "status.Inactive": {"fa": "⛔ غیرفعال", "en": "⛔ Inactive"},
    "status.OutOfStock": {"fa": "⚪ ناموجود", "en": "⚪ Out of stock"},
    "status.LowStock": {"fa": "🟡 موجودی کم", "en": "🟡 Low stock"},
    "status.All": {"fa": "همه", "en": "All"},

    # --- add / edit page ------------------------------------------------------
    "addedit.title_new": {"fa": "افزودن ماده جدید", "en": "Add a new material"},
    "addedit.title_edit": {"fa": "ویرایش ماده: {name}", "en": "Edit material: {name}"},
    "addedit.input_method": {"fa": "روش ورود ساختار", "en": "Structure input method"},
    "addedit.method_draw": {"fa": "🖊️ رسم ساختار (JSME)", "en": "🖊️ Draw structure (JSME)"},
    "addedit.method_smiles": {"fa": "⌨️ وارد کردن SMILES", "en": "⌨️ Enter SMILES"},
    "addedit.method_lookup": {"fa": "📖 جستجو با نام / CAS در کتابخانه محلی",
                              "en": "📖 Look up by name / CAS in local library"},
    "addedit.jsme_hint": {
        "fa": "ساختار را رسم کنید و روی Apply کلیک کنید؛ SMILES به‌طور خودکار در فرم ثبت می‌شود.",
        "en": "Draw the structure and click Apply — the SMILES is filled into the form automatically."},
    "addedit.editor_unavailable": {
        "fa": "ویرایشگر ساختار در این محیط در دسترس نیست — لطفاً SMILES را مستقیماً وارد کنید.",
        "en": "The structure editor is unavailable in this environment — please enter SMILES directly."},
    "addedit.smiles_label": {"fa": "SMILES", "en": "SMILES"},
    "addedit.validate": {"fa": "اعتبارسنجی و محاسبه شناسه‌ها",
                         "en": "Validate & compute identifiers"},
    "addedit.valid": {"fa": "✅ SMILES معتبر است.", "en": "✅ SMILES is valid."},
    "addedit.invalid": {"fa": "❌ SMILES نامعتبر است — ساختار را بررسی کنید.",
                        "en": "❌ Invalid SMILES — please check the structure."},
    "addedit.no_rdkit": {
        "fa": "⚠️ RDKit نصب نیست: شناسه‌ها محاسبه نمی‌شوند و اعتبارسنجی ساختار ممکن نیست.",
        "en": "⚠️ RDKit is not installed: identifiers cannot be computed and structures cannot be validated."},
    "addedit.computed": {"fa": "شناسه‌های محاسبه‌شده", "en": "Computed identifiers"},
    "addedit.duplicate_warn": {
        "fa": "⚠️ ماده‌ای با همین InChIKey از قبل در کتابخانه وجود دارد (شناسه {id}: {name}).",
        "en": "⚠️ A material with this InChIKey already exists (id {id}: {name})."},
    "addedit.lookup_hint": {
        "fa": "نام یا CAS را وارد کنید؛ فقط در پایگاه‌داده محلی جستجو می‌شود (بدون اینترنت).",
        "en": "Type a name or CAS; searched only in the local database (no internet)."},
    "addedit.lookup_none": {"fa": "موردی یافت نشد.", "en": "Nothing found."},
    "addedit.lookup_use": {"fa": "انتخاب و انتقال به فرم", "en": "Select & fill into form"},
    "addedit.section_identity": {"fa": "مشخصات", "en": "Identity"},
    "addedit.section_stock": {"fa": "موجودی", "en": "Stock"},
    "addedit.section_safety": {"fa": "ایمنی", "en": "Safety"},
    "addedit.section_props": {"fa": "خواص فیزیکی (اختیاری)", "en": "Physical properties (optional)"},
    "addedit.ghs_select": {"fa": "کدهای خطر GHS", "en": "GHS hazard codes"},
    "addedit.ghs_custom": {"fa": "کدهای اضافی (با ویرگول جدا کنید)",
                           "en": "Additional codes (comma-separated)"},
    "addedit.mp": {"fa": "نقطه ذوب (°C)", "en": "Melting point (°C)"},
    "addedit.bp": {"fa": "نقطه جوش (°C)", "en": "Boiling point (°C)"},
    "addedit.density": {"fa": "چگالی (g/mL)", "en": "Density (g/mL)"},
    "addedit.appearance": {"fa": "ظاهر", "en": "Appearance"},
    "addedit.solubility": {"fa": "حلالیت", "en": "Solubility"},
    "addedit.save": {"fa": "💾 ذخیره ماده", "en": "💾 Save material"},
    "addedit.saved_new": {"fa": "✅ ماده «{name}» اضافه شد.", "en": "✅ Material “{name}” added."},
    "addedit.saved_edit": {"fa": "✅ ماده «{name}» به‌روزرسانی شد.", "en": "✅ Material “{name}” updated."},
    "addedit.name_required": {"fa": "نام انگلیسی الزامی است.", "en": "English name is required."},
    "addedit.cancel_edit": {"fa": "پایان ویرایش", "en": "Cancel editing"},

    # --- search page ----------------------------------------------------------
    "search.title": {"fa": "جستجوی پیشرفته", "en": "Advanced Search"},
    "search.mode": {"fa": "نوع جستجو", "en": "Search mode"},
    "search.mode_text": {"fa": "متنی (نام / مترادف / CAS / SMILES / InChIKey)",
                         "en": "Text (name / synonym / CAS / SMILES / InChIKey)"},
    "search.mode_exact": {"fa": "تطابق دقیق (InChIKey)", "en": "Exact match (InChIKey)"},
    "search.mode_sub": {"fa": "جستجوی زیرساختار", "en": "Substructure search"},
    "search.mode_sim": {"fa": "جستجوی شباهت", "en": "Similarity search"},
    "search.query": {"fa": "عبارت جستجو", "en": "Search query"},
    "search.query_structure": {"fa": "ساختار پرس‌وجو (SMILES/SMARTS یا رسم)",
                               "en": "Query structure (SMILES/SMARTS or draw)"},
    "search.threshold": {"fa": "آستانه شباهت", "en": "Similarity threshold"},
    "search.run": {"fa": "🔍 اجرای جستجو", "en": "🔍 Run search"},
    "search.results": {"fa": "نتیجه", "en": "result(s)"},
    "search.needs_rdkit": {
        "fa": "⚠️ این نوع جستجو به RDKit نیاز دارد که نصب نیست.",
        "en": "⚠️ This search mode requires RDKit, which is not installed."},
    "search.use_query": {"fa": "انتخاب به‌عنوان ساختار پرس‌وجو",
                         "en": "Use as query structure"},

    # --- import / export -------------------------------------------------------
    "transfer.title": {"fa": "ورود و خروج داده", "en": "Import / Export"},
    "transfer.export_all": {"fa": "خروجی از کل کتابخانه", "en": "Export whole library"},
    "transfer.export_csv": {"fa": "⬇️ خروجی CSV", "en": "⬇️ Export CSV"},
    "transfer.export_json": {"fa": "⬇️ خروجی JSON", "en": "⬇️ Export JSON"},
    "transfer.export_sdf": {"fa": "⬇️ خروجی SDF", "en": "⬇️ Export SDF"},
    "transfer.import": {"fa": "وارد کردن مواد", "en": "Import materials"},
    "transfer.import_hint": {
        "fa": "فایل CSV / JSON / SDF را انتخاب کنید. ابتدا پیش‌نمایش را بررسی و سپس ورود را تأیید کنید. موارد تکراری (InChIKey یکسان) رد می‌شوند.",
        "en": "Choose a CSV / JSON / SDF file. Review the preview, then confirm. Duplicates (same InChIKey) are skipped."},
    "transfer.upload": {"fa": "فایل", "en": "File"},
    "transfer.preview": {"fa": "پیش‌نمایش", "en": "Preview"},
    "transfer.confirm": {"fa": "✅ تأیید و ورود اطلاعات", "en": "✅ Confirm import"},
    "transfer.imported": {"fa": "{n} ماده وارد شد؛ {s} مورد تکراری رد شد؛ {e} خطا.",
                          "en": "Imported {n} material(s); skipped {s} duplicate(s); {e} error(s)."},
    "transfer.sdf_needs_rdkit": {
        "fa": "⚠️ ورود/خروج SDF بدون RDKit ممکن نیست.",
        "en": "⚠️ SDF import/export requires RDKit."},
    "transfer.backup_note": {
        "fa": "نکته: برای پشتیبان‌گیری کامل می‌توانید پوشه data/ را کپی کنید (spec 06).",
        "en": "Tip: for a full backup simply copy the data/ folder (spec 06)."},

    # --- settings page ----------------------------------------------------------
    "settings.title": {"fa": "تنظیمات", "en": "Settings"},
    "settings.language": {"fa": "زبان رابط کاربری", "en": "Interface language"},
    "settings.db_info": {"fa": "اطلاعات پایگاه‌داده", "en": "Database info"},
    "settings.db_path": {"fa": "مسیر", "en": "Path"},
    "settings.db_size": {"fa": "اندازه", "en": "Size"},
    "settings.counts": {"fa": "فعال", "en": "Active"},
    "settings.reseed": {"fa": "بازافزودن مواد پیش‌فرضِ ناموجود",
                        "en": "Re-add missing default materials"},
    "settings.reseed_done": {"fa": "{n} ماده پیش‌فرض اضافه شد.",
                             "en": "Added {n} default material(s)."},
    "settings.reseed_none": {"fa": "همه مواد پیش‌فرض از قبل موجود هستند.",
                             "en": "All default materials are already present."},
    "settings.future": {
        "fa": "تنظیمات زیر برای فازهای بعدی ذخیره می‌شوند (spec 06): عمق جستجو، زمان محاسبه، مدل AI محلی، سطح نمایش ایمنی.",
        "en": "These settings are stored for later phases (spec 06): search depth, computation time, local AI model, safety display level."},
    "settings.about": {"fa": "درباره سیلا", "en": "About سیلا (CLA)"},
    "settings.about_text": {
        "fa": "سیلا یک شیمیدان مجازی آفلاین و دوزبانه است. فاز ۱: مدیریت مواد اولیه. "
              "این ابزار جایگزین شیمیدان انسان نیست؛ همیشه پیش از کار عملی، SDS و منابع معتبر را بررسی کنید.",
        "en": "CLA (سیلا) is an offline, bilingual Virtual Chemist. Phase 1: Starting Materials Manager. "
              "It is not a replacement for a human chemist — always verify SDS and authoritative sources before practical work."},

    # --- misc -------------------------------------------------------------------
    "common.none": {"fa": "—", "en": "—"},
    "common.close": {"fa": "بستن", "en": "Close"},
    "error.generic": {"fa": "خطا: {msg}", "en": "Error: {msg}"},
}

# ---------------------------------------------------------------------------
# GHS hazard statements (H-codes) — concise bilingual working translations.
# For regulatory purposes consult the official SDS.
# ---------------------------------------------------------------------------
GHS_H_STATEMENTS: dict[str, dict[str, str]] = {
    "H224": {"en": "Extremely flammable liquid and vapour",
             "fa": "مایع و بخار بسیار اشتعال‌پذیر"},
    "H225": {"en": "Highly flammable liquid and vapour",
             "fa": "مایع و بخار بسیار اشتعال‌پذیر"},
    "H226": {"en": "Flammable liquid and vapour",
             "fa": "مایع و بخار اشتعال‌پذیر"},
    "H227": {"en": "Combustible liquid", "fa": "مایع قابل اشتعال"},
    "H228": {"en": "Flammable solid", "fa": "جامد اشتعال‌پذیر"},
    "H260": {"en": "In contact with water releases flammable gases which may ignite spontaneously",
             "fa": "در تماس با آب، گازهای اشتعال‌پذیری آزاد می‌کند که ممکن است خودبه‌خود مشتعل شوند"},
    "H261": {"en": "In contact with water releases flammable gas",
             "fa": "در تماس با آب، گاز اشتعال‌پذیر آزاد می‌کند"},
    "H271": {"en": "May cause fire or explosion; strong oxidiser",
             "fa": "ممکن است باعث آتش‌سوزی یا انفجار شود؛ اکسیدکننده قوی"},
    "H272": {"en": "May intensify fire; oxidiser",
             "fa": "ممکن است آتش را تشدید کند؛ اکسیدکننده"},
    "H290": {"en": "May be corrosive to metals", "fa": "ممکن است برای فلزات خورنده باشد"},
    "H301": {"en": "Toxic if swallowed", "fa": "در صورت بلع سمی است"},
    "H302": {"en": "Harmful if swallowed", "fa": "در صورت بلع مضر است"},
    "H304": {"en": "May be fatal if swallowed and enters airways",
             "fa": "در صورت بلع و ورود به مجاری تنفسی ممکن است کشنده باشد"},
    "H311": {"en": "Toxic in contact with skin", "fa": "در تماس با پوست سمی است"},
    "H312": {"en": "Harmful in contact with skin", "fa": "در تماس با پوست مضر است"},
    "H314": {"en": "Causes severe skin burns and eye damage",
             "fa": "باعث سوختگی شدید پوست و آسیب جدی چشم می‌شود"},
    "H315": {"en": "Causes skin irritation", "fa": "باعث تحریک پوست می‌شود"},
    "H317": {"en": "May cause an allergic skin reaction",
             "fa": "ممکن است باعث واکنش آلرژیک پوستی شود"},
    "H318": {"en": "Causes serious eye damage", "fa": "باعث آسیب جدی چشم می‌شود"},
    "H319": {"en": "Causes serious eye irritation", "fa": "باعث تحریک جدی چشم می‌شود"},
    "H330": {"en": "Fatal if inhaled", "fa": "در صورت استنشاق کشنده است"},
    "H331": {"en": "Toxic if inhaled", "fa": "در صورت استنشاق سمی است"},
    "H332": {"en": "Harmful if inhaled", "fa": "در صورت استنشاق مضر است"},
    "H334": {"en": "May cause allergy or asthma symptoms or breathing difficulties if inhaled",
             "fa": "در صورت استنشاق ممکن است باعث آلرژی، علائم آسم یا دشواری تنفس شود"},
    "H335": {"en": "May cause respiratory irritation",
             "fa": "ممکن است باعث تحریک دستگاه تنفسی شود"},
    "H336": {"en": "May cause drowsiness or dizziness",
             "fa": "ممکن است باعث خواب‌آلودگی یا سرگیجه شود"},
    "H340": {"en": "May cause genetic defects", "fa": "ممکن است باعث نقایص ژنتیکی شود"},
    "H341": {"en": "Suspected of causing genetic defects",
             "fa": "مشکوک به ایجاد نقایص ژنتیکی"},
    "H350": {"en": "May cause cancer", "fa": "ممکن است باعث سرطان شود"},
    "H351": {"en": "Suspected of causing cancer", "fa": "مشکوک به سرطان‌زایی"},
    "H360": {"en": "May damage fertility or the unborn child",
             "fa": "ممکن است به باروری یا جنین آسیب برساند"},
    "H360D": {"en": "May damage the unborn child",
              "fa": "ممکن است به جنین آسیب برساند"},
    "H361": {"en": "Suspected of damaging fertility or the unborn child",
             "fa": "مشکوک به آسیب به باروری یا جنین"},
    "H361d": {"en": "Suspected of damaging the unborn child",
              "fa": "مشکوک به آسیب به جنین"},
    "H370": {"en": "Causes damage to organs", "fa": "به اندام‌ها آسیب می‌رساند"},
    "H372": {"en": "Causes damage to organs through prolonged or repeated exposure",
             "fa": "در اثر مواجهه طولانی یا مکرر به اندام‌ها آسیب می‌رساند"},
    "H373": {"en": "May cause damage to organs through prolonged or repeated exposure",
             "fa": "ممکن است در اثر مواجهه طولانی یا مکرر به اندام‌ها آسیب برساند"},
    "H400": {"en": "Very toxic to aquatic life", "fa": "بسیار سمی برای آبزیان"},
    "H410": {"en": "Very toxic to aquatic life with long lasting effects",
             "fa": "بسیار سمی برای آبزیان با اثرات طولانی‌مدت"},
    "H412": {"en": "Harmful to aquatic life with long lasting effects",
             "fa": "مضر برای آبزیان با اثرات طولانی‌مدت"},
}


def t(key: str, lang: str, **kwargs) -> str:
    """Translate ``key`` into ``lang`` ('fa'|'en'), with optional formatting."""
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get("en") or key
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text


def ghs_label(code: str, lang: str) -> str:
    """Human-readable GHS statement for an H-code, e.g. 'H225 — …'."""
    entry = GHS_H_STATEMENTS.get(code.strip())
    if entry is None:
        return code
    return f"{code} — {entry.get(lang) or entry['en']}"


def known_ghs_codes() -> list[str]:
    return sorted(GHS_H_STATEMENTS.keys())
