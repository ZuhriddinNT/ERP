from django.core.management.base import BaseCommand
from accounts.models import User


class Command ( BaseCommand ) :
    help = 'Create an admin user'

    def handle(self, *args, **kwargs) :
        if not User.objects.filter ( username='admin' ).exists () :
            User.objects.create_superuser (
                username='admin',
                email='admin@edurate.com',
                password='admin123',
                user_type='admin',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write ( self.style.SUCCESS ( 'Admin user created successfully!' ) )
            self.stdout.write ( 'Username: admin' )
            self.stdout.write ( 'Password: admin123' )
        else :
            self.stdout.write ( self.style.WARNING ( 'Admin user already exists' ) )