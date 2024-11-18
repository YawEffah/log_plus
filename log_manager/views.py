from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from collections import defaultdict
from .models import AttendanceRecord, Employee
from .forms import EmployeeIDForm, LoginForm, EmployeeForm
from django.contrib.auth import authenticate, login, logout






def index(request):
    return render(request, 'log_manager/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed in successfully')
                return redirect(reverse('dashboard'))
            else:
                # Invalid credentials
                # messages.error(request, 'Invalid credentials')
                return render(request, 'log_manager/login.html', {
                    'form': form, 'errors': 'Invalid credentials'
                })
    else:
        form = LoginForm()

    return render(request, 'log_manager/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.error(request, 'Logged out')
    return redirect(reverse('login'))



def dashboard_view(request):
    # Redirect to login page if user is not authenticated
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    # Get filters from query parameters
    filter_date = request.GET.get('date')
    employee_id = request.GET.get('employee_id')

    # Determine the filter date
    if filter_date:
        try:
            # Convert filter_date from string to date
            filter_date = timezone.datetime.strptime(filter_date, '%Y-%m-%d').date()
        except ValueError:
            # If parsing fails, use today's date
            filter_date = timezone.now().date()
    else:
        # Default to today's date if no date is provided and no employee filter
        filter_date = timezone.now().date() if not employee_id else None

    # Start with all attendance records, then apply filters
    current_records = AttendanceRecord.objects.all()

    # Apply employee ID filter if provided
    if employee_id:
        current_records = current_records.filter(employee__unique_id=employee_id)
    # Apply date filter if set (default to today if no filters)
    if filter_date:
        current_records = current_records.filter(date=filter_date)
    
    all_records = AttendanceRecord.objects.all()

    context = {
        'current_records': current_records,
        'all_records': all_records,
        'filter_date': filter_date if filter_date else timezone.now().date(),
        'employee_id': employee_id,
    }
    return render(request, 'log_manager/dashboard.html', context)



def employees_view(request):

    employees = Employee.objects.all()

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Added successfully")
            return redirect(reverse('employees'))
        else:
            return render(request, 'log_manager/employees.html', {'form': form})
        
    form = EmployeeForm()

    context = {
        'form': form,
        'employees': employees
    }
    # Render the form in the template
    return render(request, 'log_manager/employees.html', context)



def edit_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee Info updated successfully!')
            return redirect('employees')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'log_manager/edit-employee.html', {'employee':employee, 'form': form})



def delete_employee_view(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete() 
    messages.error(request, "Employee deleted successfully")
    return redirect('employees')



def statistics_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))


    employee_id = request.GET.get('employee_id')
    employee = Employee.objects.get(id=employee_id) if employee_id else None
    
    # Group attendance records by month and count attendance
    monthly_data = defaultdict(int)
    total_working_days = 23 
    total_present = 0
    total_absent = 0

    
    if employee:
        records = AttendanceRecord.objects.filter(employee=employee)
        
        # Counting attendance for each month
        for record in records:
            month = record.date.strftime('%B %Y')  # Format as "Month Year"
            monthly_data[month] += 1  # Count attendance records per month
            # if record.checkin_time and record.checkout_time:
            if record.checkin_time or record.checkout_time:
                total_present += 1
            else:
                total_absent += 1

    # Prepare data for Google Charts with attendance capped at 23
    chart_data = [['Month', 'Attendance']]
    for month, count in monthly_data.items():
        chart_data.append([month, min(count, total_working_days)])

    if chart_data == [['Month', 'Attendance']]:
        no_chart_data = True
    else:
        no_chart_data = False

    workings_days = total_working_days * len(monthly_data)


    try:
        present_percentage = round((total_present / workings_days ) * 100, 2)
        absent_percentage = round(100 - present_percentage, 2)
    except ZeroDivisionError:
         present_percentage = 0
         absent_percentage = 0

    context = {
        'employee': employee,
        'monthly_data': monthly_data,
        'chart_data': chart_data,
        'total_working_days': workings_days,
        'total_present': total_present,
        'total_absent': total_absent,
        'present_percentage': present_percentage,
        'absent_percentage': absent_percentage,
        'employees': Employee.objects.all(),
        'no_chart_data': no_chart_data
    }
    return render(request, 'log_manager/statistics.html', context)



def checkin_view(request):
    if request.method == "POST":
        form = EmployeeIDForm(request.POST)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            try:
                employee = Employee.objects.get(unique_id=unique_id)
                record, created = AttendanceRecord.objects.get_or_create(
                    employee=employee,
                    date=timezone.now().date(),
                    defaults={'checkin_time': timezone.now()}
                )
                if not created:
                    return render(request, 'log_manager/checkin.html', {'form': form, 'error': 'Already checked in!'})
                messages.success(request, 'Checked-in!')
                return redirect(reverse('checkin'))
            except Employee.DoesNotExist:
                return render(request, 'log_manager/checkin.html', {'form': form, 'error': 'Invalid credentials!'})
    else:
        form = EmployeeIDForm()
    return render(request, 'log_manager/checkin.html', {'form': form})



def checkout_view(request):
    if request.method == "POST":
        form = EmployeeIDForm(request.POST)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            try:
                # Get the employee based on the unique ID
                employee = Employee.objects.get(unique_id=unique_id)
                
                # Get the attendance record for the employee and today's date
                record = AttendanceRecord.objects.get(employee=employee, date=timezone.now().date())
                
                # Check if the employee has already checked out
                if record.checkout_time:
                    messages.warning(request, 'Already checked-out!')
                    return redirect(reverse('checkout'))
                
                # Set checkout time and save the record
                record.checkout_time = timezone.now()
                record.save()
                messages.success(request, 'Checked-out!')
                return redirect(reverse('checkout'))
            
            except (Employee.DoesNotExist, AttendanceRecord.DoesNotExist):
                # Handle the case where the employee or record does not exist
                return render(request, 'log_manager/checkout.html', {'form': form, 'error': 'Invalid id or no record found for today!'})
    else:
        form = EmployeeIDForm()

    return render(request, 'log_manager/checkout.html', {'form': form})
