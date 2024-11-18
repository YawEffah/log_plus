from django.db import models
import random

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    unique_id = models.CharField(max_length=8, unique=True, blank=True)
    picture = models.ImageField(upload_to='employee_pictures', blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    type = models.CharField(
        choices=[
            ('NSS', 'NSS'),
            ('Full-time', 'Full-Time'),
            ('Intern', 'Intern'),
            ('Contractor', 'Contractor'),
        ],
        max_length=100,
    )

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        """Generate a unique ID in the format '0525XXXX', where XXXX is a sequence number."""
        base_prefix = "0525"  # Static prefix
        last_employee = Employee.objects.filter(unique_id__startswith=base_prefix).order_by('-unique_id').first()
        if last_employee and last_employee.unique_id:
            # Extract the numeric suffix and increment it
            last_number = int(last_employee.unique_id[4:])
            new_number = last_number + 1
        else:
            # Start the sequence if no employees exist
            new_number = 1

        # Format the new number as a zero-padded 4-digit number
        return f"{base_prefix}{new_number:04d}"

    def __str__(self):
        return f"{self.name} - {self.unique_id}"




class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
