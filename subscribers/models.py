from django.db import models


class Subscribers(models.Model):
    email = models.EmailField(
        max_length=32,
        help_text="Email Address"
    )
    full_name = models.CharField(
        max_length=100,
        help_text="First and Last Name"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ('created_at',)
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"
        db_table = "subscribers"
