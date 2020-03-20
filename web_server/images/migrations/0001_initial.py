# Generated by Django 2.2.10 on 2020-02-05 01:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_tag', models.CharField(default='name', max_length=100)),
                ('name', models.CharField(default='name', max_length=100)),
                ('description', models.CharField(default='ASKAP image', max_length=100)),
                ('ra', models.DecimalField(decimal_places=7, max_digits=10)),
                ('dec', models.DecimalField(decimal_places=7, max_digits=10)),
                ('runtime', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField(max_length=300)),
                ('url_2', models.URLField(default='N/A', max_length=300)),
                ('matched_to', models.CharField(default='SUMSS', max_length=40)),
                ('runby', models.CharField(default='unknown', max_length=20)),
                ('number_askap_sources', models.IntegerField(default=0)),
                ('number_sumss_sources', models.IntegerField(default=0)),
                ('number_nvss_sources', models.IntegerField(default=0)),
                ('rms', models.DecimalField(decimal_places=17, default=0.0, max_digits=20)),
                ('transients_master_total', models.IntegerField(default=0)),
                ('transients_master_candidates_total', models.IntegerField(default=0)),
                ('transients_master_flagged_total', models.IntegerField(default=0)),
                ('claimed_by', models.CharField(default='Unclaimed', max_length=20)),
                ('number_candidates_checked', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Processingsettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.IntegerField()),
                ('output_dir', models.URLField(max_length=300)),
                ('askap_csv', models.URLField(max_length=300)),
                ('sumss_csv', models.URLField(max_length=300)),
                ('nvss_csv', models.URLField(default='', max_length=300)),
                ('askap_ext_thresh', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('sumss_ext_thresh', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('nvss_ext_thresh', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('max_separation', models.DecimalField(decimal_places=2, max_digits=4)),
                ('aegean_det_sigma', models.DecimalField(decimal_places=2, max_digits=4)),
                ('aegean_fill_sigma', models.DecimalField(decimal_places=2, max_digits=4)),
                ('flux_ratio_image_view', models.CharField(default='plot', max_length=200)),
                ('position_offset', models.CharField(default='plot', max_length=200)),
                ('source_counts', models.CharField(default='plot', max_length=200)),
                ('flux_ratios', models.CharField(default='plot', max_length=200)),
                ('flux_ratios_from_centre', models.CharField(default='plot', max_length=200)),
                ('askap_overlay', models.CharField(default='plot', max_length=200)),
                ('sumss_overlay', models.CharField(default='plot', max_length=200)),
                ('nvss_overlay', models.CharField(default='plot', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transient_type', models.CharField(max_length=50)),
                ('user_tag', models.CharField(max_length=50)),
                ('user', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.IntegerField()),
                ('master_name', models.CharField(default='askap source', max_length=50)),
                ('askap_name', models.CharField(default='catalog source', max_length=50)),
                ('catalog_name', models.CharField(default='catalog source', max_length=50)),
                ('ra', models.DecimalField(decimal_places=7, max_digits=10)),
                ('dec', models.DecimalField(decimal_places=7, max_digits=10)),
                ('catalog_iflux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('catalog_iflux_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('catalog_rms', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('catalog_mosaic', models.CharField(default='catalog mosaic', max_length=50)),
                ('askap_image', models.CharField(default='askap_image', max_length=250)),
                ('askap_image_2', models.CharField(default='askap_image_2', max_length=250)),
                ('askap_iflux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_iflux_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_scale_flux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_scale_flux_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_non_conv_flux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_non_conv_flux_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_non_conv_scaled_flux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_non_conv_scaled_flux_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_non_conv_d2d', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_rms', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('askap_rms_2', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('d2d_askap_centre', models.DecimalField(decimal_places=12, default=0, max_digits=20, verbose_name='Distance to ASKAP Image Centre')),
                ('ratio', models.DecimalField(decimal_places=12, default=0, max_digits=20, verbose_name='Flux Ratio')),
                ('ratio_e', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('ratio_catalog_flux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('ratio_catalog_flux_err', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('ratio_askap_flux', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('ratio_askap_flux_err', models.DecimalField(decimal_places=12, default=0, max_digits=20)),
                ('ploturl', models.CharField(default='plot', max_length=200)),
                ('pipelinetag', models.CharField(default='N/A', max_length=50, verbose_name='Pipeline Tag')),
                ('usertag', models.CharField(default='N/A', max_length=30, verbose_name='User Tag')),
                ('userreason', models.CharField(default='N/A', max_length=30, verbose_name='User Reason')),
                ('checkedby', models.CharField(default='N/A', max_length=20, verbose_name='Checked By')),
                ('survey', models.CharField(default='N/A', max_length=10)),
                ('nearest_sources', models.CharField(default='', max_length=250)),
                ('transient_type', models.CharField(default='', max_length=50)),
                ('aegean_rms_used', models.CharField(default='False', max_length=6)),
                ('inflated_convolved_flux', models.CharField(default='False', max_length=6, verbose_name='Flux Convolved Error')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_query', models.TextField(blank=True, max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
