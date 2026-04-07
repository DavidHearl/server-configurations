from django.core.management.base import BaseCommand
from server_deployments.models import DashboardLink


class Command(BaseCommand):
    help = 'Populate dashboard with links from HTML file'

    def handle(self, *args, **options):
        # Clear existing links
        DashboardLink.objects.all().delete()
        
        links = [
            # Network - Internal
            {'name': 'Virgin Router', 'url': 'http://192.168.0.1', 'icon': 'icons/virgin.png', 
             'category': 'network', 'tab': 'network', 'description': '192.168.0.1', 'order': 1},
            {'name': 'Dream Machine Pro', 'url': 'http://192.168.1.1', 'icon': 'icons/unifi.png', 
             'category': 'network', 'tab': 'network', 'description': '192.168.1.1', 'order': 2},
            {'name': '48 Port Network Switch', 'url': 'http://192.168.1.28', 'icon': 'icons/network.png', 
             'category': 'network', 'tab': 'network', 'description': '192.168.1.28', 'order': 3},
            {'name': 'Proxmox', 'url': 'http://192.168.1.43', 'icon': 'icons/proxmox.png', 
             'category': 'network', 'tab': 'network', 'description': '192.168.1.43', 'order': 4},
            
            # Apps - UNRAID (Internal)
            {'name': 'UNRAID', 'url': 'http://192.168.1.44', 'icon': 'icons/unraid.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44', 'order': 1},
            {'name': 'Plex', 'url': 'http://192.168.1.44:32400', 'icon': 'icons/plex.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:32400', 'order': 2},
            {'name': 'Overseerr', 'url': 'http://192.168.1.44:5055', 'icon': 'icons/overseerr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:5055', 'order': 3},
            {'name': 'Cleanarr', 'url': 'http://192.168.1.44:5000', 'icon': 'icons/cleanarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:5000', 'order': 4},
            {'name': 'Disk Speed', 'url': 'http://192.168.1.44:8888', 'icon': 'icons/diskspeed.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:8888', 'order': 5},
            {'name': 'Nextcloud', 'url': 'http://192.168.1.44:444', 'icon': 'icons/nextcloud.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:444', 'order': 6},
            {'name': 'Prowlarr', 'url': 'http://192.168.1.44:9696', 'icon': 'icons/prowlarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:9696', 'order': 7},
            {'name': 'Radarr', 'url': 'http://192.168.1.44:7878', 'icon': 'icons/radarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:7878', 'order': 8},
            {'name': 'SABNZB', 'url': 'http://192.168.1.44:8080', 'icon': 'icons/sab.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:8080', 'order': 9},
            {'name': 'Sonarr', 'url': 'http://192.168.1.44:8989', 'icon': 'icons/sonarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:8989', 'order': 10},
            {'name': 'Tautulli', 'url': 'http://192.168.1.44:8181', 'icon': 'icons/tautulli.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:8181', 'order': 11},
            {'name': 'Tdarr', 'url': 'http://192.168.1.44:8264', 'icon': 'icons/tdarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '192.168.1.44:8264', 'order': 12},
            
            # Apps - Dell C2100 VMs (Internal)
            {'name': 'Predictions', 'url': 'http://192.168.1.9', 'icon': 'icons/premier-league.png', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.9', 'order': 1},
            {'name': 'Say it Again', 'url': 'http://192.168.1.34', 'icon': 'icons/language.png', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.34', 'order': 2, 'active': False},
            {'name': 'Quiz Site', 'url': 'http://192.168.1.93', 'icon': 'icons/quiz.jpg', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.93', 'order': 3, 'active': False},
            {'name': 'Investments', 'url': 'http://192.168.1.178', 'icon': 'icons/investments.jpg', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.178', 'order': 4, 'active': False},
            {'name': 'Server Configurations', 'url': 'http://192.168.1.105', 'icon': 'icons/servers.jpg', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.105', 'order': 5, 'active': False},
            {'name': 'Property Finances', 'url': 'http://192.168.1.70', 'icon': 'icons/house.jpg', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.70', 'order': 6, 'active': False},
            {'name': 'Workouts', 'url': 'http://192.168.1.53', 'icon': 'icons/dumbbell.jpg', 
             'category': 'servers', 'tab': 'apps', 'description': '192.168.1.53', 'order': 7, 'active': False},
            
            # Apps - UNRAID (Tailscale)
            {'name': 'UNRAID (Tailscale)', 'url': 'http://100.74.250.48', 'icon': 'icons/unraid.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48', 'order': 13},
            {'name': 'Plex (Tailscale)', 'url': 'http://100.74.250.48:32400', 'icon': 'icons/plex.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:32400', 'order': 14},
            {'name': 'Overseerr (Tailscale)', 'url': 'http://100.74.250.48:5055', 'icon': 'icons/overseerr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:5055', 'order': 15},
            {'name': 'Cleanarr (Tailscale)', 'url': 'http://100.74.250.48:5000', 'icon': 'icons/cleanarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:5000', 'order': 16},
            {'name': 'Disk Speed (Tailscale)', 'url': 'http://100.74.250.48:8888', 'icon': 'icons/diskspeed.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:8888', 'order': 17},
            {'name': 'Nextcloud (Tailscale)', 'url': 'http://100.74.250.48:444', 'icon': 'icons/nextcloud.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:444', 'order': 18},
            {'name': 'Prowlarr (Tailscale)', 'url': 'http://100.74.250.48:9696', 'icon': 'icons/prowlarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:9696', 'order': 19},
            {'name': 'Radarr (Tailscale)', 'url': 'http://100.74.250.48:7878', 'icon': 'icons/radarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:7878', 'order': 20},
            {'name': 'SABNZB (Tailscale)', 'url': 'http://100.74.250.48:8080', 'icon': 'icons/sab.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:8080', 'order': 21},
            {'name': 'Sonarr (Tailscale)', 'url': 'http://100.74.250.48:8989', 'icon': 'icons/sonarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:8989', 'order': 22},
            {'name': 'Tautulli (Tailscale)', 'url': 'http://100.74.250.48:8181', 'icon': 'icons/tautulli.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:8181', 'order': 23},
            {'name': 'Tdarr (Tailscale)', 'url': 'http://100.74.250.48:8264', 'icon': 'icons/tdarr.png', 
             'category': 'unraid', 'tab': 'apps', 'description': '100.74.250.48:8264', 'order': 24},
            
            # Network - Tailscale
            {'name': 'Proxmox (Tailscale)', 'url': 'http://100.113.235.116:8006', 'icon': 'icons/proxmox.png', 
             'category': 'network', 'tab': 'network', 'description': '100.113.235.116:8006', 'order': 5},
            
            # Apps - Dell C2100 VMs (Tailscale)
            {'name': 'Predictions (Tailscale)', 'url': 'http://100.119.207.7', 'icon': 'icons/premier-league.png', 
             'category': 'servers', 'tab': 'apps', 'description': '100.119.207.7', 'order': 8},
            
            # Public - Django Applications
            {'name': 'Predictions', 'url': 'https://predictions.mediaservers.co.uk', 'icon': 'icons/premier-league.png', 
             'category': 'services', 'tab': 'public', 'description': 'predictions.mediaservers.co.uk', 'order': 1},
            {'name': 'Quiz Site', 'url': 'https://quiz.mediaservers.co.uk', 'icon': 'icons/quiz.jpg', 
             'category': 'services', 'tab': 'public', 'description': 'quiz.mediaservers.co.uk', 'order': 2, 'active': False},
            {'name': 'Scene Automation', 'url': 'https://scene-automation-e08fb55351d3.herokuapp.com/ships_and_areas/', 'icon': 'icons/ship.jpg', 
             'category': 'services', 'tab': 'public', 'description': 'Heroku', 'order': 3, 'active': False},
            {'name': 'Sweet Shop', 'url': 'https://the-sweet-shop-davidhearl.herokuapp.com/', 'icon': 'icons/sweet.png', 
             'category': 'services', 'tab': 'public', 'description': 'Heroku', 'order': 4},
            {'name': 'Investments', 'url': 'https://investments.mediaservers.co.uk', 'icon': 'icons/investments.jpg', 
             'category': 'services', 'tab': 'public', 'description': 'investments.mediaservers.co.uk', 'order': 5, 'active': False},
            {'name': 'Say it Again', 'url': 'https://sayitagain.mediaservers.co.uk', 'icon': 'icons/language.png', 
             'category': 'services', 'tab': 'public', 'description': 'sayitagain.mediaservers.co.uk', 'order': 6, 'active': False},
            {'name': 'Golf Statistics', 'url': 'https://golf.mediaservers.co.uk', 'icon': 'icons/golf.png', 
             'category': 'services', 'tab': 'public', 'description': 'golf.mediaservers.co.uk', 'order': 7, 'active': False},
            {'name': 'Connect Four', 'url': 'https://connect-four.mediaservers.co.uk', 'icon': 'icons/connectfour.jpg', 
             'category': 'services', 'tab': 'public', 'description': 'connectfour.mediaservers.co.uk', 'order': 8, 'active': False},
            
            # Public - Static Applications
            {'name': 'Mortgage Calculator', 'url': 'https://davidhearl.github.io/finances/', 'icon': 'icons/mortgage.png', 
             'category': 'other', 'tab': 'public', 'description': 'GitHub Pages', 'order': 1},
            {'name': 'Fun with Flags', 'url': 'https://davidhearl.github.io/flag-game/', 'icon': 'icons/flag.jpg', 
             'category': 'other', 'tab': 'public', 'description': 'GitHub Pages', 'order': 2},
            {'name': 'Chiropractic Website', 'url': 'https://davidhearl.github.io/chiropractic-website/', 'icon': 'icons/body.png', 
             'category': 'other', 'tab': 'public', 'description': 'GitHub Pages', 'order': 3},
            {'name': 'My Portfolio', 'url': 'https://davidhearl.com', 'icon': 'icons/person.png', 
             'category': 'other', 'tab': 'public', 'description': 'davidhearl.com', 'order': 4},
            {'name': 'Django Cheatsheet', 'url': 'https://davidhearl.github.io/django-cheatsheet/', 'icon': 'icons/document.png', 
             'category': 'other', 'tab': 'public', 'description': 'GitHub Pages', 'order': 5},
        ]
        
        created_count = 0
        for link_data in links:
            DashboardLink.objects.create(**link_data)
            created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} dashboard links')
        )
