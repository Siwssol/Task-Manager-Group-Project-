from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(name='Board',
                               fields=[
                                   ('board_name', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                                   ('board_type', models.CharField(max_length=7)),
                                   ('created_at', models.DateTimeField(auto_now_add=True)),
                                   ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                                   ('team_emails',models.CharField(max_length=1000))
                                ],
                                options={
                                    'ordering': ['-created_at'],
                                }
                            ),
        ]
    
