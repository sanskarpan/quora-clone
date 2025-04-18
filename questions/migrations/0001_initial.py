# Generated by Django 5.0.5 on 2025-04-07 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Question",
                "verbose_name_plural": "Questions",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="questions.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Answer",
                "verbose_name_plural": "Answers",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "answer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to="questions.answer",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="likes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Like",
                "verbose_name_plural": "Likes",
                "indexes": [
                    models.Index(
                        fields=["answer"], name="questions_l_answer__9aa75f_idx"
                    ),
                    models.Index(
                        fields=["user"], name="questions_l_user_id_915f01_idx"
                    ),
                ],
                "unique_together": {("answer", "user")},
            },
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["-created_at"], name="questions_q_created_7d8295_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="question",
            index=models.Index(
                fields=["author"], name="questions_q_author__0c91b6_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(
                fields=["-created_at"], name="questions_a_created_0b9f16_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(
                fields=["question"], name="questions_a_questio_fe80e9_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="answer",
            index=models.Index(
                fields=["author"], name="questions_a_author__057c19_idx"
            ),
        ),
    ]
