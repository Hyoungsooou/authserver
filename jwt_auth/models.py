# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    created_time = models.DateTimeField(blank=True, null=True)
    updated_time = models.DateTimeField(blank=True, null=True)
    # This field type is a guess.
    user_type = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    sns_type = models.TextField(blank=True, null=True)
    sns_uid = models.TextField(blank=True, null=True)
    email = models.TextField()
    hashed_password = models.TextField(blank=True, null=True)
    name = models.TextField()
    profile_image = models.TextField(blank=True, null=True)
    point = models.IntegerField(blank=True, null=True)
    bpm = models.IntegerField(blank=True, null=True)
    favorite_users = models.BinaryField(blank=True, null=True)
    interest_items = models.BinaryField(blank=True, null=True)
    is_agree_push_chat = models.BooleanField(blank=True, null=True)
    is_agree_push_keyword = models.BooleanField(blank=True, null=True)
    is_agree_push_system = models.BooleanField(blank=True, null=True)
    is_agree_push_ad = models.BooleanField(blank=True, null=True)
    hashed_bank_password = models.TextField(blank=True, null=True)
    block_users = models.BinaryField(blank=True, null=True)
    blocked_by = models.BinaryField(blank=True, null=True)
    bank_password_changed_at = models.DateTimeField(blank=True, null=True)
    is_agent = models.BooleanField(blank=True, null=True)
    followed_by = models.BinaryField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    quit_at = models.DateField(blank=True, null=True)
    email_backup = models.TextField(blank=True, null=True)
    keyword_list = models.BinaryField(blank=True, null=True)
    apple_refresh_token = models.TextField(blank=True, null=True)
    # This field type is a guess.
    grade = models.TextField(blank=True, null=True)
    pampam_name = models.TextField(blank=True, null=True)
    pampam_position = models.TextField(blank=True, null=True)
    kg_name = models.TextField(blank=True, null=True)
    kg_no = models.TextField(blank=True, null=True)
    kg_commid = models.TextField(blank=True, null=True)
    kg_socialno = models.TextField(blank=True, null=True)
    kg_sex = models.TextField(blank=True, null=True)
    kg_foreigner = models.TextField(blank=True, null=True)
    kg_ci = models.TextField(blank=True, null=True)
    kg_di = models.TextField(blank=True, null=True)
    is_restricted = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    PASSWORD_FIELD = 'hashed_password'

    class Meta:
        managed = False
        db_table = 'user'
