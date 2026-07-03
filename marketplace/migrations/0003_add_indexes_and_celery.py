from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_customuser_email_verified_emailverificationtoken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockitem',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='stockitem',
            name='category',
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='bookmarks', to='marketplace.customuser'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, db_index=True, max_length=254, verbose_name='email address'),
        ),
    ]
