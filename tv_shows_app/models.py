from django.db import models
from datetime import datetime
# Create your models here.
class ShowManager(models.Manager):
    def basic_validation(self,post_data):
        errors={}
        #if title less than 2 give error massage
        if len(post_data['title'])<2:
            errors['title']='Title should be at least 2 characters'
        
        #if title exist give error massage. first at the create page, we check if the title exists in db (we can see btn's value to know which page)
        # or if it is edit page, we check if the title exist and if its exist we check if the object we are editing is in the filtered list or not( if both ture it means there is similar title other than the edited one its self )
        filtered_list=Show.objects.filter(title=post_data['title'])
        if (filtered_list.exists() and post_data['btn']=='Create') or filtered_list.exists() and Show.objects.get(id=post_data['show.id']) not in filtered_list:# post_data['show.id'] the id of the object we are editing 
            errors['title2']='Title already exist'
            
        if len(post_data['nw'])<3:
            errors['nw']='Network should be at least 3 characters'
        
        #if threre is a description check if length less than 3, if there is no desc it will not return error
        if post_data['desc']:
            if len(post_data['desc'])<3:
                errors['desc']='Description should be at least 10 characters'
        
        # if date is empty when create new show
        if post_data['date' ]==''  and post_data['btn']=='Create':
            errors['date2']='You should enter Release Date'
        
        # if the entered date is in the future 
        if post_data['date']>str(datetime.today()):
            errors['date']='Release Date should be in the past'
        return errors

class Show(models.Model):
    title=models.CharField(max_length=45)
    network=models.CharField(max_length=45)
    date=models.DateField(blank=True, null=True)
    desc=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ShowManager()