from django.test import TestCase
from django.urls import reverse

from .models import LearningPath


class LearningPathViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.active_path = LearningPath.objects.create(
            title="Active Learning Path",
            slug="active-learning-path",
            description="Active test path",
            is_active=True,
        )

        cls.inactive_path = LearningPath.objects.create(
            title="Inactive Learning Path",
            slug="inactive-learning-path",
            description="Inactive test path",
            is_active=False,
        )

    def test_learning_path_list(self):
        response = self.client.get(
            reverse("learning_path_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Learning Path")
        self.assertNotContains(response, "Inactive Learning Path")

    def test_active_learning_path_detail(self):
        response = self.client.get(
            self.active_path.get_absolute_url()
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Learning Path")

    def test_inactive_learning_path_detail(self):
        response = self.client.get(
            self.inactive_path.get_absolute_url()
        )

        self.assertEqual(response.status_code, 404)

    def test_nonexistent_learning_path(self):
        response = self.client.get(
            reverse(
                "learning_path_detail",
                kwargs={"slug": "does-not-exist"},
            )
        )

        self.assertEqual(response.status_code, 404)


class FeaturedLearningPathTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        for number in range(1, 6):
            LearningPath.objects.create(
                title=f"Learning Path {number}",
                slug=f"learning-path-{number}",
                description="Test learning path",
                order=number,
                is_active=True,
            )

        LearningPath.objects.create(
            title="Hidden Learning Path",
            slug="hidden-learning-path",
            description="Inactive learning path",
            order=0,
            is_active=False,
        )

    def test_home_displays_three_active_learning_paths(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        featured_paths = response.context["featured_learning_paths"]

        self.assertEqual(len(featured_paths), 3)

        self.assertEqual(
            [path.order for path in featured_paths],
            [1, 2, 3],
        )

        self.assertContains(response, "Learning Path 1")
        self.assertContains(response, "Learning Path 2")
        self.assertContains(response, "Learning Path 3")

        self.assertNotContains(response, "Hidden Learning Path")
        self.assertNotContains(response, "Learning Path 4")
