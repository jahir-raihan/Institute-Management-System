# Generated by Django 3.2.9 on 2022-01-24 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collegeSystem', '0004_auto_20220124_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='grade_file',
        ),
        migrations.RemoveField(
            model_name='gradefile',
            name='up_result_sheet',
        ),
        migrations.DeleteModel(
            name='TestSubChoice',
        ),
        migrations.AddField(
            model_name='uploadresult',
            name='department',
            field=models.CharField(choices=[('computer_science_technology', 'Computer Science Technology'), ('civil_technology', 'Civil Technology'), ('architecture_technology', 'Architecture Technology'), ('textile_technology', 'TextTile Technology'), ('electrical_engineering', 'Electrical Engineering')], default='CST', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uploadresult',
            name='session_year',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='uploadresult',
            name='which_semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='collegeSystem.semester'),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
        migrations.DeleteModel(
            name='GradeFile',
        ),
    ]
