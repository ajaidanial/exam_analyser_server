# Generated by Django 3.0.10 on 2020-11-02 12:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("examination", "0004_questioncategory"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionPaper",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_question_papers",
                        to="examination.Exam",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_question_papers",
                        to="examination.Subject",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_related_name": "related_question_papers",
                "unique_together": {("exam", "subject")},
            },
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.TextField()),
                ("description", models.TextField(default=None, null=True)),
                (
                    "question_categories",
                    models.ManyToManyField(
                        related_name="related_questions",
                        to="examination.QuestionCategory",
                    ),
                ),
                (
                    "question_paper",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="related_questions",
                        to="examination.QuestionPaper",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "default_related_name": "related_questions",
                "unique_together": {("name", "question_paper")},
            },
        ),
    ]
