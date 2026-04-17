from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from ..models import Diary, db
from ..services.diary_service import (
    apply_diary_data,
    build_diary_query,
    validate_diary_form,
)

diary_bp = Blueprint("diary", __name__)


@diary_bp.route("/")
def home():
    recent_diaries = (
        Diary.query.order_by(Diary.entry_date.desc(), Diary.created_at.desc())
        .limit(5)
        .all()
    )
    return render_template("index.html", recent_diaries=recent_diaries)


@diary_bp.route("/diaries")
def list_diaries():
    q = request.args.get("q", "").strip()
    entry_date = request.args.get("entry_date", "").strip()
    tag = request.args.get("tag", "").strip()

    diaries = build_diary_query(q, entry_date, tag).all()

    return render_template(
        "diary_list.html",
        diaries=diaries,
        q=q,
        entry_date=entry_date,
        tag=tag,
    )


@diary_bp.route("/diaries/new", methods=["GET", "POST"])
def create_diary():
    if request.method == "POST":
        data, errors = validate_diary_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "diary_form.html",
                page_title="日記を作成",
                submit_label="保存する",
                diary=None,
                form_data=request.form,
            )

        diary = Diary()
        apply_diary_data(diary, data)
        db.session.add(diary)
        db.session.commit()

        flash("日記を保存しました。", "success")
        return redirect(url_for("diary.diary_detail", diary_id=diary.id))

    return render_template(
        "diary_form.html",
        page_title="日記を作成",
        submit_label="保存する",
        diary=None,
        form_data={},
    )


@diary_bp.route("/diaries/<int:diary_id>")
def diary_detail(diary_id: int):
    diary = Diary.query.get_or_404(diary_id)
    return render_template("diary_detail.html", diary=diary)


@diary_bp.route("/diaries/<int:diary_id>/edit", methods=["GET", "POST"])
def edit_diary(diary_id: int):
    diary = Diary.query.get_or_404(diary_id)

    if request.method == "POST":
        data, errors = validate_diary_form(request.form)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "diary_form.html",
                page_title="日記を編集",
                submit_label="更新する",
                diary=diary,
                form_data=request.form,
            )

        apply_diary_data(diary, data)
        db.session.commit()

        flash("日記を更新しました。", "success")
        return redirect(url_for("diary.diary_detail", diary_id=diary.id))

    return render_template(
        "diary_form.html",
        page_title="日記を編集",
        submit_label="更新する",
        diary=diary,
        form_data={},
    )


@diary_bp.route("/diaries/<int:diary_id>/delete", methods=["POST"])
def delete_diary(diary_id: int):
    diary = Diary.query.get_or_404(diary_id)

    db.session.delete(diary)
    db.session.commit()

    flash("日記を削除しました。", "success")
    return redirect(url_for("diary.list_diaries"))