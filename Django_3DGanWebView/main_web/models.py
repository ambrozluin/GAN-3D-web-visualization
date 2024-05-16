from django.db import models

class GanGeneratedModel(models.Model):
    name = models.CharField(max_length=50, default='name')
    generated_Img = models.ImageField(upload_to='images/', default='default.jpg')

    def __str__(self):
        return self.name

class Voxel(models.Model):
    id = models.AutoField(primary_key=True)  # Explicitly defining primary key
    model = models.CharField(max_length=50, default='model')
    data = models.BinaryField()

    def __str__(self):
        return self.model