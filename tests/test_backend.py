"""CLA / سیلا — Phase 1 backend tests.

Run with:  python -m pytest tests/ -v
All tests use temporary databases (never the real data/ folder).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend import chemistry, db, io_formats, materials, settings  # noqa: E402
from backend.seed import loader  # noqa: E402
from backend.seed.compounds import SEED_COMPOUNDS  # noqa: E402


@pytest.fixture()
def db_path(tmp_path):
    p = tmp_path / "test_compounds.db"
    db.init_db(p)
    return p


# --------------------------------------------------------------------------
# schema / init
# --------------------------------------------------------------------------

def test_init_db_is_idempotent(db_path):
    db.init_db(db_path)  # second call must not fail
    with db.get_conn(db_path) as conn:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"materials", "properties", "history", "meta"} <= tables


# --------------------------------------------------------------------------
# chemistry (RDKit)
# --------------------------------------------------------------------------

@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_identifiers_ethanol():
    ident = chemistry.compute_identifiers("CCO")
    assert ident["smiles"] == "CCO"
    assert ident["formula"] == "C2H6O"
    assert abs(ident["molecular_weight"] - 46.068) < 0.01
    assert ident["inchikey"] == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert ident["inchi"].startswith("InChI=1S/C2H6O")


@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_invalid_smiles_rejected():
    ok, _ = chemistry.validate_smiles("C(((")
    assert not ok


@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_substructure_and_similarity():
    assert chemistry.has_substructure("Cc1ccccc1", "c1ccccc1")
    assert not chemistry.has_substructure("CCO", "c1ccccc1")
    sim_close = chemistry.tanimoto("CCO", "CO")
    sim_far = chemistry.tanimoto("CCO", "c1ccccc1")
    assert sim_close > sim_far


# --------------------------------------------------------------------------
# CRUD + stock + status
# --------------------------------------------------------------------------

def _add(db_path, **kw):
    data = dict(name_en="Test chemical", name_fa="ماده آزمایشی",
                smiles="CCO", quantity=100, unit="mL", min_stock=10)
    data.update(kw)
    return materials.add_material(data, db_path=db_path)


def test_add_computes_identifiers(db_path):
    m = _add(db_path)
    if chemistry.HAS_RDKIT:
        assert m.inchikey == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
        assert m.formula == "C2H6O"
    assert m.status == materials.STATUS_ACTIVE
    assert m.effective_status == materials.STATUS_ACTIVE


def test_quantity_controls_and_history(db_path):
    m = _add(db_path, quantity=100)
    m = materials.adjust_quantity(m.id, -30, db_path=db_path)
    assert m.quantity == 70
    m = materials.adjust_quantity(m.id, -100, db_path=db_path)  # clamps at 0
    assert m.quantity == 0
    assert m.effective_status == materials.STATUS_OUT_OF_STOCK
    m = materials.set_quantity(m.id, 5, db_path=db_path)
    assert m.quantity == 5
    assert m.effective_status == materials.STATUS_LOW_STOCK  # 5 <= min_stock 10
    hist = materials.get_history(m.id, db_path=db_path)
    actions = {h["action"] for h in hist}
    assert {"created", "quantity_adjusted", "quantity_set"} <= actions


def test_enable_disable_and_synthesis_gate(db_path):
    m = _add(db_path)
    assert m.is_available
    m2 = materials.set_status(m.id, materials.STATUS_INACTIVE, db_path=db_path)
    assert m2.status == materials.STATUS_INACTIVE
    assert not m2.is_available
    avail = materials.available_for_synthesis(db_path=db_path)
    assert m.id not in [x.id for x in avail]
    m3 = materials.set_status(m.id, materials.STATUS_ACTIVE, db_path=db_path)
    assert m3.is_available
    with pytest.raises(ValueError):
        materials.set_status(m.id, "OutOfStock", db_path=db_path)


def test_update_and_delete(db_path):
    m = _add(db_path)
    m2 = materials.update_material(m.id, {"name_en": "Renamed", "cas": "64-17-5"},
                                   db_path=db_path)
    assert m2.name_en == "Renamed"
    assert m2.cas == "64-17-5"
    assert materials.delete_material(m.id, db_path=db_path)
    assert materials.get_material(m.id, db_path=db_path) is None
    assert not materials.delete_material(m.id, db_path=db_path)


# --------------------------------------------------------------------------
# search
# --------------------------------------------------------------------------

def test_search_modes(db_path):
    _add(db_path, name_en="Ethanol", name_fa="اتانول", smiles="CCO",
         cas="64-17-5", synonyms=["EtOH"])
    _add(db_path, name_en="Toluene", smiles="Cc1ccccc1", cas="108-88-3")

    assert materials.text_search("eth", db_path=db_path)
    assert materials.text_search("اتانول", db_path=db_path)          # Persian
    assert materials.text_search("64-17-5", db_path=db_path)         # CAS
    assert materials.text_search("EtOH", db_path=db_path)            # synonym

    if chemistry.HAS_RDKIT:
        assert materials.exact_search("LFQSCWFLJHTTHZ-UHFFFAOYSA-N", db_path=db_path)
        assert materials.exact_search("CCO", db_path=db_path)
        subs = materials.substructure_search("c1ccccc1", db_path=db_path)
        assert [m.name_en for m in subs] == ["Toluene"]
        sims = materials.similarity_search("CCO", threshold=0.3, db_path=db_path)
        assert sims and sims[0][0].name_en == "Ethanol"


# --------------------------------------------------------------------------
# seed data
# --------------------------------------------------------------------------

@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_seed_loads_spec_required_solvents(tmp_path):
    p = tmp_path / "seed.db"
    n = loader.seed_if_empty(db_path=p)
    assert n == len(SEED_COMPOUNDS)
    all_m = materials.list_materials(db_path=p)
    names = {m.name_en.lower() for m in all_m}
    required = ["water", "ethanol", "methanol", "acetone", "dichloromethane",
                "tetrahydrofuran", "diethyl ether", "hexane", "ethyl acetate",
                "acetonitrile", "dimethyl sulfoxide", "dimethylformamide"]
    for req in required:  # spec 01 §4 mandated solvents
        assert any(req in nm for nm in names), f"missing solvent: {req}"
    for req in ["hydrochloric", "sulfuric", "acetic acid", "sodium hydroxide",
                "potassium hydroxide", "triethylamine", "sodium carbonate"]:
        assert any(req in nm for nm in names), f"missing acid/base: {req}"


@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_seed_is_idempotent_and_bilingual(tmp_path):
    p = tmp_path / "seed.db"
    loader.seed_if_empty(db_path=p)
    second = loader.seed_if_empty(db_path=p)
    assert second == 0  # nothing re-inserted
    all_m = materials.list_materials(db_path=p)
    assert all(m.name_fa for m in all_m)          # bilingual names
    with_smiles = [m for m in all_m if m.smiles]
    assert all(m.inchikey for m in with_smiles)   # identifiers computed
    eth = next(m for m in all_m if m.name_en == "Ethanol")
    assert eth.inchikey == "LFQSCWFLJHTTHZ-UHFFFAOYSA-N"
    assert eth.ghs_hazards == ["H225", "H319"]


# --------------------------------------------------------------------------
# import / export round-trip
# --------------------------------------------------------------------------

def test_csv_json_roundtrip(db_path, tmp_path):
    _add(db_path, name_en="Ethanol", smiles="CCO", quantity=500, unit="mL")
    _add(db_path, name_en="Toluene", smiles="Cc1ccccc1")

    other = tmp_path / "other.db"
    db.init_db(other)

    csv_text = io_formats.export_csv(db_path=db_path)
    summary = io_formats.import_rows(io_formats.parse_csv(csv_text), db_path=other)
    assert summary["imported"] == 2 and summary["errors"] == 0

    # re-import into same db -> duplicates skipped
    summary2 = io_formats.import_rows(io_formats.parse_csv(csv_text), db_path=db_path)
    assert summary2["imported"] == 0
    assert summary2["skipped"] == 2 or summary2["imported"] == 0

    json_text = io_formats.export_json(db_path=db_path)
    third = tmp_path / "third.db"
    db.init_db(third)
    s3 = io_formats.import_rows(io_formats.parse_json(json_text), db_path=third)
    assert s3["imported"] == 2


@pytest.mark.skipif(not chemistry.HAS_RDKIT, reason="RDKit not installed")
def test_sdf_roundtrip(db_path, tmp_path):
    _add(db_path, name_en="Ethanol", smiles="CCO", cas="64-17-5")
    sdf = io_formats.export_sdf(db_path=db_path)
    assert "$$$$" in sdf
    other = tmp_path / "sdf.db"
    db.init_db(other)
    rows = io_formats.parse_sdf(sdf)
    summary = io_formats.import_rows(rows, db_path=other)
    assert summary["imported"] == 1
    m = materials.list_materials(db_path=other)[0]
    assert m.cas == "64-17-5"


# --------------------------------------------------------------------------
# settings & i18n
# --------------------------------------------------------------------------

def test_settings_defaults_and_language(tmp_path, monkeypatch):
    from backend import config
    monkeypatch.setattr(config, "SETTINGS_PATH", tmp_path / "settings.json")
    s = settings.load_settings()
    assert s["language"] in ("fa", "en")
    settings.set_language("en")
    assert settings.get_language() == "en"
    settings.set_language("fa")
    assert settings.get_language() == "fa"
    with pytest.raises(ValueError):
        settings.set_language("de")


def test_i18n_both_languages():
    from backend import i18n
    assert i18n.t("nav.library", "fa") != i18n.t("nav.library", "en")
    assert "اشتعالات" in i18n.ghs_label("H225", "fa") or "اشتعال" in i18n.ghs_label("H225", "fa")
    assert "flammable" in i18n.ghs_label("H225", "en").lower()
    assert i18n.t("missing.key", "fa") == "missing.key"
