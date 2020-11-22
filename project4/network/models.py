from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	#followercnt=models.IntegerField(default=0)
	#followingcnt=models.IntegerField(default=0)
	likes=models.ManyToManyField('Posts',related_name='fans')
	follows=models.ManyToManyField('self',symmetrical=False,related_name="followers")
	#pass

class Posts(models.Model):
	author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted")
	content=models.CharField(max_length=300)
	date=models.DateTimeField()
	totallikes=models.IntegerField(default=0)
	def __str__(self):
		return f"[user:{self.author}]-{self.content}(likes-{self.totallikes})"