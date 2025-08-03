import flask
from flask import request, redirect, url_for, render_template, flash, abort

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    # ล้างการแคช session เพื่อให้ได้ข้อมูลล่าสุดจากฐานข้อมูล
    db.session.expire_all()
    
    # ดึงข้อมูล Note พร้อมกับ Tag ที่เกี่ยวข้อง
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.updated_date.desc())
    ).scalars()
    
    return flask.render_template(
        "index.html",
        notes=notes,
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("error", form.errors)
        return flask.render_template(
            "notes-create.html",
            form=form,
        )
    note = models.Note()
    form.populate_obj(note)
    note.tags = []

    db = models.db
    for tag_name in form.tags.data:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )

        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)

        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    try:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )
        
        if not tag:
            flash("Tag ไม่พบ", "error")
            return redirect(url_for("index"))
            
        notes = db.session.execute(
            db.select(models.Note).where(models.Note.tags.any(id=tag.id))
        ).scalars()
    except Exception as e:
        app.logger.error(f"Error in tags_view: {str(e)}")
        flash(f"เกิดข้อผิดพลาด: {str(e)}", "error")
        return redirect(url_for("index"))

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
    )


@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flash("โน้ตไม่พบ", "error")
        return redirect(url_for("index"))

    form = forms.EditNoteForm(obj=note)
    form.note_id.data = note_id
    
    # ดึงข้อมูล tags ที่มีอยู่แล้ว
    tag_names = [tag.name for tag in note.tags]
    form.tags.data = tag_names
    
    if form.validate_on_submit():
        # เก็บข้อมูล tags ไว้ก่อน
        tag_data = form.tags.data
        
        # ลบฟิลด์ tags ชั่วคราวเพื่อไม่ให้ populate_obj พยายามตั้งค่า
        form_tags = form.tags
        delattr(form, 'tags')
        
        # อัปเดตข้อมูลจากฟอร์ม (ยกเว้น tags)
        form.populate_obj(note)
        
        # เพิ่มฟิลด์ tags กลับไป
        form.tags = form_tags
        
        # ล้าง tags ปัจจุบันและเพิ่ม tags ใหม่
        note.tags = []
        
        # อัปเดต tags
        for tag_name in tag_data:
            tag = db.session.execute(
                db.select(models.Tag).where(models.Tag.name == tag_name)
            ).scalars().first()
            
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            
            note.tags.append(tag)
        
        db.session.commit()
        flash("อัปเดตโน้ตเรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))
    
    return render_template("notes-edit.html", form=form, note=note)


@app.route("/notes/delete/<int:note_id>", methods=["GET", "POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flash("โน้ตไม่พบ", "error")
        return redirect(url_for("index"))

    form = forms.DeleteNoteForm()
    form.note_id.data = note_id  # ตั้งค่า note_id ในฟอร์ม
    
    if request.method == "POST" and form.validate_on_submit():
        db.session.delete(note)
        db.session.commit()
        flash("ลบโน้ตเรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))
    
    return render_template("notes-delete.html", form=form, note=note)


@app.route("/tags/create", methods=["GET", "POST"])
def tags_create():
    form = forms.TagForm()
    if form.validate_on_submit():
        db = models.db
        tag = models.Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash("สร้าง Tag เรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))
    
    return render_template("tags-create.html", form=form)


@app.route("/tags/edit/<tag_name>", methods=["GET", "POST"])
def tags_edit(tag_name):
    db = models.db
    try:
        tag = db.session.execute(
            db.select(models.Tag).where(models.Tag.name == tag_name)
        ).scalars().first()
        
        if not tag:
            flash("Tag ไม่พบ", "error")
            return redirect(url_for("index"))

        form = forms.EditTagForm()
        form.original_name.data = tag_name
        
        if request.method == "GET":
            form.name.data = tag.name
        
        if form.validate_on_submit():
            # เก็บชื่อใหม่
            new_name = form.name.data
            
            # พิมพ์ข้อมูลเพื่อตรวจสอบ
            print(f"กำลังแก้ไข Tag: {tag_name} -> {new_name}")
            
            # ตรวจสอบว่าชื่อใหม่มีอยู่แล้วหรือไม่ (ยกเว้นตัวมันเอง)
            if new_name != tag_name:
                existing_tag = db.session.execute(
                    db.select(models.Tag).where(models.Tag.name == new_name)
                ).scalars().first()
                
                if existing_tag:
                    flash(f"Tag ชื่อ '{new_name}' มีอยู่แล้ว", "error")
                    return render_template("tags-edit.html", form=form, tag=tag)
            
            # ค้นหา Note ที่มี Tag นี้เพื่อให้แน่ใจว่าความสัมพันธ์ยังคงอยู่
            notes_with_tag = db.session.execute(
                db.select(models.Note).where(models.Note.tags.any(id=tag.id))
            ).scalars().all()
            
            # อัปเดตชื่อ Tag
            tag.name = new_name
            
            # บันทึกการเปลี่ยนแปลง
            db.session.add(tag)  # เพิ่มบรรทัดนี้เพื่อให้แน่ใจว่า session รู้ว่าต้องอัปเดตวัตถุนี้
            db.session.commit()
            
            # รีเฟรชทั้ง Tag และ Note ที่เกี่ยวข้อง
            db.session.refresh(tag)  # รีเฟรชวัตถุจากฐานข้อมูล
            for note in notes_with_tag:
                db.session.refresh(note)  # รีเฟรช Note ที่มี Tag นี้
                
            # ล้างการแคชทั้งหมด
            db.session.expire_all()
            
            flash(f"อัปเดต Tag จาก '{tag_name}' เป็น '{new_name}' เรียบร้อยแล้ว", "success")
            # กลับไปที่หน้าแรกแทนเพื่อให้เห็นการเปลี่ยนแปลงทั้งหมด
            return redirect(url_for("index"))
        
        return render_template("tags-edit.html", form=form, tag=tag)
    
    except Exception as e:
        db.session.rollback()
        flash(f"เกิดข้อผิดพลาด: {str(e)}", "error")
        print(f"Error in tags_edit: {str(e)}")
        return redirect(url_for("index"))


@app.route("/tags/delete/<tag_name>", methods=["GET", "POST"])
def tags_delete(tag_name):
    db = models.db
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.name == tag_name)
    ).scalars().first()
    
    if not tag:
        flash("Tag ไม่พบ", "error")
        return redirect(url_for("index"))

    form = forms.DeleteTagForm()
    form.tag_name.data = tag_name
    
    if request.method == "POST" and form.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash("ลบ Tag เรียบร้อยแล้ว", "success")
        return redirect(url_for("index"))
    
    return render_template("tags-delete.html", form=form, tag=tag)


if __name__ == "__main__":
    app.run(debug=True)
