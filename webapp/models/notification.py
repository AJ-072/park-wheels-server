from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=50,)
    message = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    # image = models.CharField(null=True,max_length=)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.message
