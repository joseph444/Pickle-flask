from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,FileField,TextAreaField,MultipleFileField
from wtforms.validators import DataRequired,ValidationError,Length
from flask_wtf.file import FileAllowed


class Posts(FlaskForm):
    Title=StringField('Title',validators=[DataRequired()])
    Type=SelectField('Type',validators=[DataRequired()],choices=[('','--Select Post Type--'),('Recipie','Recipie of Your Food'),('Rating','Rating of an Restraunt/Food store'),('Foodie','About A Food')])
    Description=TextAreaField('Description',validators=[DataRequired()])
    Images=MultipleFileField('',validators=[FileAllowed(['jpg','png','jpeg','gif'],"Please select A Image")])
    Ingredients=TextAreaField("Ingredients")
    Steps=TextAreaField("Steps")
    FoodQuality=StringField("Food Quality")
    Services=StringField("Services Quality")
    Cleanliness=StringField("Cleanliness")
    Behaviour=StringField("Behaviour with Customers")
    Rating=StringField("Overall Rating")
    Submit=SubmitField("Create")

    def validate_type(self):
        if self.Type.data=='Recipie':
            if len(self.Ingredients.data)<4:
                raise ValidationError('For Post Type Recipie Ingredients Can\'t Be Empty or less than the word \'An Egg\' ')
            elif len(self.Steps.data)<3:
                 raise ValidationError('For Post Type Recipie Steps Can\'t Be Empty or less than the word \'Fry\' ')
            elif len(self.FoodQuality.data)>0 or len(self.Services.data)>0 or len(self.Cleanliness.data)>0:
                raise ValidationError('Sorry But For Post Type Recipie Can\'t Have Fields Like FoodQuality,Services Or Cleanliness')
        elif self.Type.data=='Rating':
            if len(self.Services.data)<1:
                raise ValidationError("Services Quality Can't be Empty for Post Type Rating")
            elif len(self.FoodQuality.data)<1:
                raise ValidationError("Food Quality Can't be Empty for Post Type Rating")
            elif len(self.Cleanliness.data)<1:
                raise ValidationError("Cleanliness Can't be Empty for Post Type Rating")
            elif len(self.Behaviour.data)<1:
                raise ValidationError("Behaviour with Customers Can't be Empty for Post Type Rating")
            elif len(self.Rating.data)<1:
                raise ValidationError("Rating Can't be Empty for Post Type Rating")
            elif  len(self.Steps.data)>0 or len(self.Ingredients.data)>0 :
                raise ValidationError("Steps or Ingredients Can't Be Filled in Post Type Rating")
        elif self.Type.data=='Foodie':
            if  len(self.Steps.data)>0 or len(self.Ingredients.data)>0 :
                raise ValidationError("Steps or Ingredients Can't Be Filled in Post Type Food Lover")
            if len(self.FoodQuality.data)>0 or len(self.Services.data)>0 or len(self.Cleanliness.data)>0:
                raise ValidationError('Sorry But For Post Type Recipie Can\'t Have Fields Like FoodQuality,Services Or Cleanliness')