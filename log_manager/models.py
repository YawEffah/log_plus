from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    unique_id = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to='employee_pictures', blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    type = models.CharField(
        choices=[
            ('NSS', 'NSS'),
            ('Tull-time', 'Full-Time'),
            ('Intern', 'Intern'),
            ('Contractor', 'Contractor'),
        ],
        max_length=100,
    )

    def __str__(self):
        return f"{self.name} - {self.unique_id}"
    
    

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    checkin_time = models.DateTimeField(null=True, blank=True)
    checkout_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"
