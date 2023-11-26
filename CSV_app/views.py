import csv
from datetime import datetime
from django.shortcuts import render, redirect,HttpResponse
from .models import User, CustomerDetails
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            User.objects.all().delete()
            CustomerDetails.objects.all().delete()
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                email = row['email']
                existing_user = User.objects.filter(email=email).first()
                
                if existing_user:
                    # If the user with the same email exists, update the data in the second table
                    customer_details, created = CustomerDetails.objects.update_or_create(
                        user=existing_user,
                        defaults={
                            'phone_no': row['phone no'],
                            'gender': row['gender'],
                            'dob': datetime.strptime(row['dob'], '%m/%d/%Y').strftime('%Y-%m-%d'),
                            'address1': row['address 1'],
                            'address2': row.get('address 2', ''),  # Handle optional field
                            'pincode': row['pincode'],
                            'state': row['state'],
                            'country': row['country'],
                        }
                    )
                else:
                    # If the user with the same email does not exist, create a new record in both tables
                    user = User.objects.create(
                        first_name=row['first name'],
                        last_name=row['last name'],
                        email=row['email']
                    )
                    CustomerDetails.objects.create(
                        user=user,
                        phone_no=row['phone no'],
                        gender=row['gender'],
                        dob=datetime.strptime(row['dob'], '%m/%d/%Y').strftime('%Y-%m-%d'),
                        address1=row['address 1'],
                        address2=row.get('address 2', ''),  # Handle optional field
                        pincode=row['pincode'],
                        state=row['state'],
                        country=row['country'],
                    )
            
            return redirect('display_users')
    else:
        form = UploadFileForm()
    return render(request, 'upload_csv.html', {'form': form})



def display_users(request):
    users_with_details = User.objects.select_related('customerdetails').all()
    return render(request, 'display_data.html', {'users_with_details': users_with_details})


#This is view function for downloading CSV
def download_csv(request):
    users_with_details = User.objects.select_related('customerdetails').all()

    #HttpResponse object with CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_data.csv"'

    #The CSV writer using the HttpResponse as the "file".
    csv_writer = csv.writer(response)

    #The header row.
    csv_writer.writerow([
        'First Name', 'Last Name', 'Email', 'Phone No', 'Gender', 'DOB',
        'Address 1', 'Address 2', 'Pincode', 'State', 'Country'
    ])

    #The data rows.
    for user in users_with_details:
        csv_writer.writerow([
            user.first_name,
            user.last_name,
            user.email,
            user.customerdetails.phone_no,
            user.customerdetails.gender,
            user.customerdetails.dob,
            user.customerdetails.address1,
            user.customerdetails.address2,
            user.customerdetails.pincode,
            user.customerdetails.state,
            user.customerdetails.country,
        ])

    return response