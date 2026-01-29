# core/fields.py
import os
from django.db.models import FileField
from django.core.files.uploadedfile import UploadedFile
# from core.utils.virus_scan import scan_file  # We'll create this next
import logging

logger = logging.getLogger(__name__)

class SecureFileField(FileField):
    """
    Custom FileField that automatically scans uploaded files for viruses using ClamAV
    """
    def save(self, name, content, save=True):
        # First, save the file normally (to disk)
        file_path = super().save(name, content, save=False)
        full_path = os.path.join(self.storage.location, file_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Save temporarily
        with open(full_path, 'wb+') as destination:
            for chunk in content.chunks():
                destination.write(chunk)

        # Virus scan
        try:
            is_clean, virus_name = scan_file(full_path)
            if not is_clean:
                os.remove(full_path)  # Delete infected file
                logger.warning(f"Blocked infected file: {virus_name}")
                raise ValueError(f"Infected file blocked: {virus_name}")
        except Exception as e:
            if os.path.exists(full_path):
                os.remove(full_path)
            raise ValueError(f"File scan failed: {str(e)}")

        # File is clean → save normally
        return super().save(name, content, save=save)