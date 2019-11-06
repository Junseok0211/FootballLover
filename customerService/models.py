from django.db import models
from account.models import FNSUser

# Create your models here.
class CS(models.Model):
    title = models.CharField(null=False, max_length=50, blank=False)
    content = models.TextField(null=False, max_length=1000, blank=False)
    email = models.EmailField(null=False)
    user = models.ForeignKey(FNSUser, on_delete=models.CASCADE, related_name='csPost')
    created = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    updated = models.DateTimeField(auto_now=True, verbose_name='수정시간')
    
    def __str__(self):
        return self.title

    def summary(self):
        return self.content[:20]
