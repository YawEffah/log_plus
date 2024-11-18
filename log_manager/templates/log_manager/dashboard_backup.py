{% extends 'attendance/base.html' %}

{% block nav-items %}
<li class="nav-item">
  <a class="nav-link active" href="{% url 'dashboard' %}">
    <i class="fa fa-list-alt nav-icon"></i>Records
  </a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{% url 'statistics' %}">
    <i class="fa fa-bar-chart nav-icon"></i>Statistics
  </a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{% url 'employees' %}">
    <i class="fa-solid fa-users nav-icon"></i>Employees
  </a>
</li>
{% endblock %}

{% block main-content %}
<div class="main-wrap">
  <h2 class="scroll-animation">Attendance Records</h2>

  <!-- Date Filter Form -->
  <form method="get" action="{% url 'dashboard' %}" class="filter-form">
    <input class="filter-field" type="date" id="date" name="date" value="{{ filter_date }}" required />
    <button type="submit" class="cta-btn filter-cta">Filter</button>
  </form>
  <br />

  <div class="application-table-wrap custom-table-wrap">
    <div class="table-scroll">
      <table class="application-table custom-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Employee</th>
            <th>Time In</th>
            <th>Time Out</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {% for record in current_records %}
          <tr>
            <td data-label="employee_id">{{ record.employee.unique_id }}</td>
            <td data-label="employee">{{ record.employee.name }}</td>
            <td data-label="time-in">{{ record.checkin_time }}</td>
            <td data-label="time-out">{{ record.checkout_time }}</td>
            <td>
              <div class="action-menu">
                <i class="fa fa-ellipsis-v action-menu-icon"></i>
                <div class="action-menu-content">
                  <a href="javascript:void(0);" class="open-modal view-btn" data-record-id="{{ record.id }}">
                    <i class="fa fa-eye action-icon"></i> View
                  </a>
                </div>
              </div>
            </td>
          </tr>
          
          <!-- Records Modal -->
          <div id="recordModal-{{ record.id }}" class="modal record-modal custom-modal" role="dialog" aria-labelledby="modalTitle-{{ record.id }}" aria-hidden="true">
            <div class="modal-content">
              <div class="modal-header">
                <h4 class="modal-title" id="modalTitle-{{ record.id }}">Record Details</h4>
                <button type="button" class="close-modal" data-record-id="{{ record.id }}" aria-label="Close">
                  <i class="fa fa-times close-icon"></i>
                </button>
              </div>
              <div class="modal-body">
                <div class="record-details">
                  <span>
                    <label>Employee ID</label>
                    <input type="text" value="{{ record.employee.unique_id }}" disabled />
                  </span>
                  <span>
                    <label>Employee Name</label>
                    <input type="text" value="{{ record.employee.name }}" disabled />
                  </span>
                  <span>
                    <label>Employee Email</label>
                    <input type="text" value="{{ record.employee.email }}" disabled />
                  </span>
                  <span>
                    <label>Employee Phone</label>
                    <input type="text" value="{{ record.employee.phone }}" disabled />
                  </span>
                  <span>
                    <label>Employee Type</label>
                    <input type="text" value="{{ record.employee.type }}" disabled />
                  </span>
                  <span>
                    <label>Department</label>
                    <input type="text" value="{{ record.employee.department }}" disabled />
                  </span>
                  <span>
                    <label>Time In</label>
                    <input type="text" value="{{ record.checkin_time }}" disabled />
                  </span>
                  <span>
                    <label>Time Out</label>
                    <input type="text" value="{{ record.checkout_time }}" disabled />
                  </span>
                </div>
              </div>
            </div>
          </div>
          {% empty %}
          <tr>
            <td colspan="5">No records available</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>

    <br />
    <button type="button" class="cta-btn register-cta">
      <i class="fa fa-download"></i> Download
    </button>
  </div>
</div>
{% endblock %}




from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import AttendanceRecord

def dashboard_view(request):
    # Redirect to login page if user is not authenticated
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    
    # Get the date from query parameters or default to today's date
    filter_date = request.GET.get('date')
    if filter_date:
        try:
            # Convert filter_date from string to date
            filter_date = timezone.datetime.strptime(filter_date, '%Y-%m-%d').date()
        except ValueError:
            # If parsing fails, default to today's date
            filter_date = timezone.localdate()
    else:
        # Default to today's date if no date is provided
        filter_date = timezone.localdate()
    
    # Filter records based on the selected date
    current_records = AttendanceRecord.objects.filter(date=filter_date)
    all_records = AttendanceRecord.objects.all()

    context = {
        'current_records': current_records,
        'all_records': all_records,
        'filter_date': filter_date,  # Pass the selected date to the template
    }
    return render(request, 'attendance/dashboard.html', context)









# def dashboard_view(request):
#     # Redirect to login page if user is not authenticated
#     if not request.user.is_authenticated:
#         return redirect(reverse('login'))
    
#     # Get filters from query parameters
#     filter_date = request.GET.get('date')
#     employee_id = request.GET.get('employee_id')

#     # Parse date filter, default to today's date if invalid or missing
#     if filter_date:
#         try:
#             filter_date = timezone.datetime.strptime(filter_date, '%Y-%m-%d').date()
#         except ValueError:
#             filter_date = None
#     else:
#         filter_date = None

#     # Start with all attendance records, then apply filters if present
#     current_records = AttendanceRecord.objects.all()

    
#     # Apply employee ID filter if provided
#     if employee_id:
#         current_records = current_records.filter(employee__unique_id=employee_id)
#     # Apply date filter only if an employee ID is not provided, or if both are provided
#     elif filter_date:
#         current_records = current_records.filter(date=filter_date)
    
#     all_records = AttendanceRecord.objects.all()

#     context = {
#         'current_records': current_records,
#         'all_records': all_records,
#         'filter_date': filter_date,  # Pass the date to the template
#         'employee_id': employee_id,  # Pass the employee ID to the template
#     }
#     return render(request, 'attendance/dashboard.html', context)
