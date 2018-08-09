from django.core.management.base import BaseCommand
from smartad.settings import Images_Folder,Image_Types

class Command(BaseCommand):
    help = 'Start the editor to create banner templates'

    def handle(self, *a, **k):
        from adsgen.designer import design
        design(Images_Folder,Image_Types)
        pass
