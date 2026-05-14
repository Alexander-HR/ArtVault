from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class NavbarTests(TestCase):
    def test_guest_navbar_links_are_visible(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Home")
        self.assertContains(response, "Artworks")
        self.assertContains(response, "Sellers")
        self.assertContains(response, "Login")
        self.assertContains(response, "Sign Up")

    def test_protected_profile_redirects_guest_to_login(self):
        response = self.client.get(reverse("profile"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_staff_user_sees_admin_dashboard_link(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="admin_test",
            password="testpass123",
            is_staff=True,
        )

        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")
        self.assertContains(response, reverse("admin:index"))