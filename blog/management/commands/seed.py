from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import CategoryParent, Category, Post, Comment, Tag
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seed data for the blog application'

    def handle(self, *args, **kwargs):
        self.seed_users(5)
        self.seed_categories(5)
        self.seed_posts(10)
        self.seed_tags(5)
        self.seed_comments(20)

    def seed_users(self, n):
        """Create n fake users."""
        for _ in range(n):
            username = fake.user_name()
            email = fake.email()
            password = '123'
            User.objects.create_user(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} users.'))

    def seed_categories(self, n):
        """Create n categories and n parent categories."""
        for _ in range(n):
            parent = CategoryParent.objects.create(title=fake.word())
            for _ in range(3):  # each parent will have 3 child categories
                Category.objects.create(title=fake.word(), parent=parent)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} categories.'))

    def seed_posts(self, n):
        """Create n posts."""
        users = User.objects.all()
        categories = Category.objects.all()
        for _ in range(n):
            user = random.choice(users)
            category = random.choice(categories)
            title = fake.sentence(nb_words=6)
            content = fake.paragraph(nb_sentences=5)
            Post.objects.create(user=user, category=category, title=title, content=content)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} posts.'))

    def seed_tags(self, n):
        """Create n tags and randomly assign to posts."""
        posts = Post.objects.all()
        for _ in range(n):
            tag = Tag.objects.create(name=fake.word())
            # Assign tag to random posts
            random_posts = random.sample(list(posts), k=min(3, len(posts)))  # Max 3 posts per tag
            tag.posts.set(random_posts)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} tags.'))

    def seed_comments(self, n):
        """Create n comments for random posts by random users."""
        users = User.objects.all()
        posts = Post.objects.all()
        for _ in range(n):
            user = random.choice(users)
            post = random.choice(posts)
            content = fake.sentence(nb_words=12)
            Comment.objects.create(user=user, post=post, content=content)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {n} comments.'))
