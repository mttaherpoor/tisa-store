from django.db import models
from django.urls import reverse


class LearningPath(models.Model):
    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    title = models.CharField(
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(
        unique=True,
    )

    short_description = models.CharField(
        max_length=300,
        blank=True,
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="learning_paths/",
        blank=True,
        null=True,
    )

    difficulty = models.CharField(
        max_length=20,
        choices=Difficulty.choices,
        default=Difficulty.BEGINNER,
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Learning Path"
        verbose_name_plural = "Learning Paths"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "learning_path_detail",
            kwargs={"slug": self.slug},
        )

    @property
    def total_steps(self):
        return self.steps.count()

    @property
    def total_projects(self):
        return self.steps.filter(
            is_project=True
        ).count()

    @property
    def total_hours(self):
        return sum(
            step.estimated_hours
            for step in self.steps.all()
        )


class LearningStep(models.Model):
    path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="steps",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
        db_index=True,
    )

    course = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    is_project = models.BooleanField(
        default=False,
        help_text="Marks this step as a practical project.",
    )

    is_optional = models.BooleanField(
        default=False,
        help_text="Optional step in the learning path.",
    )

    estimated_hours = models.PositiveIntegerField(
        default=0,
    )

    resource_url = models.URLField(
        blank=True,
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Learning Step"
        verbose_name_plural = "Learning Steps"

    def __str__(self):
        return f"{self.path.title} | Step {self.order}: {self.title}"