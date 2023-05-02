from django.db import models


class Notifications(models.Model):
    message = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    # image = models.CharField(null=True,max_length=)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)
    updated_at = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.message
