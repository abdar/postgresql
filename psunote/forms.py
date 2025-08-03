from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from wtforms import Field, widgets, StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length

import models


class TagListField(Field):
    widget = widgets.TextInput()

    def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.data = []

    def process_formdata(self, valuelist):
        data = []
        if valuelist:
            data = [x.strip() for x in valuelist[0].split(",")]

        if not self.remove_duplicates:
            self.data = data
            return

        self.data = []
        for d in data:
            if d not in self.data:
                self.data.append(d)

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""


BaseNoteForm = model_form(

    models.Note, base_class=FlaskForm, exclude=["created_date", "updated_date"], db_session=models.db.session

)


class NoteForm(BaseNoteForm):
    tags = TagListField("Tag")
    submit = SubmitField("บันทึก")


class EditNoteForm(BaseNoteForm):
    tags = TagListField("Tag")
    note_id = HiddenField("Note ID")
    submit = SubmitField("อัปเดต")


class DeleteNoteForm(FlaskForm):
    note_id = HiddenField("Note ID")
    submit = SubmitField("ยืนยันการลบ")


class TagForm(FlaskForm):
    name = StringField("ชื่อ Tag", validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField("บันทึก")


class EditTagForm(FlaskForm):
    name = StringField("ชื่อ Tag", validators=[DataRequired(), Length(min=1, max=50)])
    original_name = HiddenField("Original Tag Name")
    submit = SubmitField("อัปเดต")


class DeleteTagForm(FlaskForm):
    tag_name = HiddenField("Tag Name")
    submit = SubmitField("ยืนยันการลบ")
