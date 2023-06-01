from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username =  StringField("이름", 
                            validators=[DataRequired(), Length(min=2, max=5)])
    id =  StringField("아이디", 
                            validators=[DataRequired(), Length(min=4, max=10)])
    password = PasswordField("비밀번호", 
                            validators=[DataRequired(), Length(min=4, max=10)])
    confirm_password = PasswordField("비밀번호 확인", 
                            validators=[DataRequired(), EqualTo("password")] )
    submit = SubmitField("가입")