from django.core.management.base import BaseCommand
from server_deployments.models import DjangoGuide, DjangoStep


class Command(BaseCommand):
    help = 'Migrate Django cheatsheet content to database'

    def handle(self, *args, **options):
        self.stdout.write('Starting migration of Django cheatsheet content...')

        # Create New Project Guide
        new_project, created = DjangoGuide.objects.get_or_create(
            slug='new-project',
            defaults={
                'title': 'New Project',
                'description': 'Complete guide to creating a new Django project from scratch',
                'order': 1
            }
        )

        if created:
            steps = [
                {
                    'title': 'Create the Django Project',
                    'order': 1,
                    'step_type': 'section',
                    'content': '''
<ol>
<li>Open VS Code and open the terminal (View > Terminal).</li>
<li>Navigate to your desired directory:
<ul>
<li class="description">macOS/Linux:</li>
<pre><code>cd '/Users/davidhearl/Documents/08 - Programming/GitHub'</code></pre>
<li>Windows:</li>
<pre><code>cd "C:\\Users\\davidhearl\\iCloudDrive\\Documents\\Programming\\GitHub"</code></pre>
</ul>
</li>
<li>Create the project directory</li>
<pre><code>mkdir myproject
cd myproject</code></pre>
<li>Create a virtual environment:</li>
<pre><code>python -m venv virtual_environment</code></pre>
<li>Activate the virtual environment:</li>
<ul>
<li class="description">Windows:</li>
<pre><code>virtual_environment\\Scripts\\activate</code></pre>
<li class="description">macOS/Linux:</li>
<pre><code>source virtual_environment/bin/activate</code></pre>
</ul>
<li>Optional: Upgrade pip to the latest version:</li>
<pre><code>python -m pip install --upgrade pip</code></pre>
<li>Install Django and save requirements:</li>
<pre><code>pip install Django
pip freeze > requirements.txt</code></pre>
<li>Create a new Django project:</li>
<pre><code>django-admin startproject myproject .</code></pre>
<li>Migrate changes</li>
<pre><code>python3 manage.py migrate</code></pre>
<li>Optional: Open the project in Visual Studio Code:</li>
<pre><code>code .</code></pre>
<li>Run the development server:</li>
<pre><code>python3 manage.py runserver</code></pre>
</ol>
                    '''
                },
                {
                    'title': 'Create a Django App',
                    'order': 2,
                    'step_type': 'section',
                    'content': '''
<ol>
<li>Create the app:</li>
<pre><code>python manage.py startapp myapp</code></pre>
<li>Open <code>settings.py</code></li>
<li>Add <code>'myapp'</code> to <code>INSTALLED_APPS</code>:</li>
<pre><code>INSTALLED_APPS = [
    ...
    'myapp',
]</code></pre>
<li>Create a superuser:</li>
<pre><code>python manage.py createsuperuser</code></pre>
</ol>
                    '''
                },
                {
                    'title': 'Django Settings to Change',
                    'order': 3,
                    'step_type': 'section',
                    'content': '''
<p>Edit <code>myproject/settings.py</code>:</p>
<ul>
<li>Create a <code>.env</code> file:</li>
<pre><code>touch .env
echo "SECRET_KEY=your-very-secret-key" >> .env</code></pre>
<li>Install python-dotenv:</li>
<pre><code>pip install python-dotenv
pip freeze > requirements.txt</code></pre>
<li>Turn off debug in production:</li>
<pre><code>DEBUG = False</code></pre>
<li>Set allowed hosts:</li>
<pre><code>ALLOWED_HOSTS = ['yourdomain.com', 'localhost']</code></pre>
<li>Adjust timezone:</li>
<pre><code>TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-us'</code></pre>
<li>Use environment variable for secret key:</li>
<pre><code>import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')</code></pre>
</ul>
                    '''
                },
                {
                    'title': 'Link to GitHub',
                    'order': 4,
                    'step_type': 'section',
                    'content': '''
<ol>
<li>Initialize a Git repository:</li>
<pre><code>git init</code></pre>
<li>Create a <code>.gitignore</code> file:</li>
<pre><code>touch .gitignore</code></pre>
<li>Add items to .gitignore:</li>
<pre><code>virtual_environment/
__pycache__/
*.pyc
*.sqlite3
.env</code></pre>
<li>Install GitHub CLI (macOS/Linux):</li>
<pre><code>brew install gh</code></pre>
<li>Windows:</li>
<pre><code>winget install --id GitHub.cli</code></pre>
<li>Login to GitHub:</li>
<pre><code>gh auth login</code></pre>
<li>Make the first commit:</li>
<pre><code>git add .
git commit -m "Initial commit"</code></pre>
<li>Create repository and push:</li>
<pre><code>gh repo create your-repo-name --public --source=. --remote=origin --push</code></pre>
</ol>
                    '''
                }
            ]

            for step_data in steps:
                DjangoStep.objects.create(guide=new_project, **step_data)

            self.stdout.write(self.style.SUCCESS(f'Created {len(steps)} steps for New Project guide'))

        # Create Deployment Guide
        deployment, created = DjangoGuide.objects.get_or_create(
            slug='deployment',
            defaults={
                'title': 'Deployment',
                'description': 'Step-by-step guide for deploying Django applications with Docker',
                'order': 2
            }
        )

        if created:
            deploy_steps = [
                {
                    'title': 'Create project folder and clone your app',
                    'order': 1,
                    'step_type': 'command',
                    'content': '''
<pre><code>mkdir -p ~/apps/my-new-app
cd ~/apps/my-new-app
git clone https://github.com/yourusername/yourproject.git .</code></pre>
<p><em>Note: You can create .env and docker-compose.yml first and clone later.</em></p>
                    '''
                },
                {
                    'title': 'Create the .env file',
                    'order': 2,
                    'step_type': 'code',
                    'content': '''
<pre><code>touch .env</code></pre>
<p><strong>Add this content to .env:</strong></p>
<pre><code>DJANGO_SETTINGS_MODULE=myproject.settings
SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_STRING
DEBUG=0

ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0,SERVER_IP,mysite.mediaservers.co.uk
CSRF_TRUSTED_ORIGINS=https://mysite.mediaservers.co.uk

DATABASE_URL=postgres://DB_USER:DB_PASS@DB_HOST:5432/DB_NAME

STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media</code></pre>
                    '''
                },
                {
                    'title': 'Create docker-compose.yml',
                    'order': 3,
                    'step_type': 'code',
                    'content': '''
<pre><code>version: "3.9"
services:
  web:
    build: .
    image: my-new-app-web
    env_file: .env
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8001:8000"
    volumes:
      - staticfiles:/app/staticfiles
      - media:/app/media
    healthcheck:
      test: ["CMD", "python", "-c", "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',8000)); print('ok')"]
      interval: 15s
      timeout: 5s
      retries: 5

volumes:
  staticfiles:
  media:</code></pre>
                    '''
                },
                {
                    'title': 'Build, migrate, and run',
                    'order': 4,
                    'step_type': 'command',
                    'content': '''
<pre><code>docker compose build --no-cache
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py collectstatic --noinput
docker compose up -d
docker compose logs -f</code></pre>
<p>Test locally:</p>
<pre><code>curl -I http://127.0.0.1:8001/</code></pre>
                    '''
                },
                {
                    'title': 'Create superuser',
                    'order': 5,
                    'step_type': 'command',
                    'content': '''
<pre><code>docker compose exec web python manage.py createsuperuser</code></pre>
                    '''
                },
                {
                    'title': 'Publish via Cloudflare Tunnel',
                    'order': 6,
                    'step_type': 'section',
                    'content': '''
<pre><code>sudo apt install cloudflared
cloudflared tunnel login
cloudflared tunnel create mysite-tunnel
cloudflared tunnel route dns mysite-tunnel mysite.mediaservers.co.uk</code></pre>
<p><strong>Example config.yml:</strong></p>
<pre><code>tunnel: mysite-tunnel
credentials-file: /home/user/.cloudflared/TUNNEL.json
ingress:
  - hostname: mysite.mediaservers.co.uk
    service: http://127.0.0.1:8001
  - service: http_status:404</code></pre>
<pre><code>sudo cloudflared service install mysite-tunnel</code></pre>
                    '''
                }
            ]

            for step_data in deploy_steps:
                DjangoStep.objects.create(guide=deployment, **step_data)

            self.stdout.write(self.style.SUCCESS(f'Created {len(deploy_steps)} steps for Deployment guide'))

        # Create Redeployment Guide
        redeploy, created = DjangoGuide.objects.get_or_create(
            slug='redeployment',
            defaults={
                'title': 'Redeployment',
                'description': 'Quick guide for redeploying Django applications with Docker',
                'order': 3
            }
        )

        if created:
            redeploy_steps = [
                {
                    'title': 'Check if application is deployed',
                    'order': 1,
                    'step_type': 'command',
                    'content': '<pre><code>sudo docker ps -a</code></pre>'
                },
                {
                    'title': 'Collect static files',
                    'order': 2,
                    'step_type': 'command',
                    'content': '<pre><code>sudo docker-compose run --rm web python manage.py collectstatic --noinput</code></pre>'
                },
                {
                    'title': 'Rebuild if not running',
                    'order': 3,
                    'step_type': 'command',
                    'content': '<pre><code>docker-compose build --no-cache</code></pre>'
                },
                {
                    'title': 'Start the application',
                    'order': 4,
                    'step_type': 'command',
                    'content': '<pre><code>sudo docker-compose up -d</code></pre>'
                },
                {
                    'title': 'Troubleshooting',
                    'order': 5,
                    'step_type': 'note',
                    'content': '''
<p>If issues occur:</p>
<ol>
<li><code>sudo docker-compose down</code></li>
<li>Go back to step 3 (rebuild)</li>
</ol>
                    '''
                }
            ]

            for step_data in redeploy_steps:
                DjangoStep.objects.create(guide=redeploy, **step_data)

            self.stdout.write(self.style.SUCCESS(f'Created {len(redeploy_steps)} steps for Redeployment guide'))

        self.stdout.write(self.style.SUCCESS('Successfully migrated all Django cheatsheet content!'))
