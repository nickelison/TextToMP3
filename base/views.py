from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO
from PIL import Image, ImageOps
from uuid import uuid4
import boto3
import json
import os
from .forms import CustomUserCreationForm, ConfirmDeleteAccountForm, UserPasswordChangeForm, ProfilePictureForm, CreateMp3Form, DeleteMp3Form
from .models import User, Mp3File
from .utils import lambda_client, delete_from_s3

def home(request):
    if request.user.is_authenticated:
        return render(request, 'base/home.html')
    else:
        return render(request, 'base/index.html')

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    context = {'page': 'login', 'title': 'Sign In'}

    # If request is POST, handle the login.
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        # Attempt to retrieve user by email.
        user = User.objects.filter(email=email).first()

        if user:
            # Authenticate the user.
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Log the user in and redirect to home.
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'Invalid login credentials')
    
    # Render login page.
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    # Initialize form.
    form = CustomUserCreationForm(request.POST if request.method == 'POST' else None)

    # If request is POST and form is valid, register the user.
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.email = user.email.lower()
        user.save()
        login(request, user)
        return redirect('home')
    elif request.method == 'POST':
        messages.error(request, 'An error occurred during registration.')

    context = {'form': form, 'title': 'Sign Up'}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def account(request):
    # Count the number of MP3 files for the user.
    mp3_count = Mp3File.objects.filter(user=request.user).count()
    
    # Initialize form for profile picture.
    form = ProfilePictureForm()

    context = {'user': request.user, 'form': form, 'mp3_count': mp3_count, 'title': 'Account'}
    return render(request, 'base/account.html', context)


@login_required(login_url='login')
def deleteAccountModal(request):
    form = ConfirmDeleteAccountForm()
    return render(request, 'components/delete_account_modal.html', {'form': form})

@login_required(login_url='login')
def deleteUser(request):
    if request.method == 'POST':
        form = ConfirmDeleteAccountForm(request.POST)
        if form.is_valid():
            request.user.delete()
            return redirect('home')

@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            messages.success(request, 'Your password has been updated!')
            return redirect('account')
        else:
            messages.error(request, 'Error updating password. Please try again.')
    else:
        form = UserPasswordChangeForm(request.user)

    return render(request, 'base/change_password.html', {
        'form': form
    })

@login_required(login_url='login')
def uploadProfilePicture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        
        # Get old profile picture filename before form is submitted and `profile_picture` is updated.
        old_filename = request.user.profile_picture
        
        if form.is_valid():
            # Get image file extension.
            uploaded_file = request.FILES['profile_picture']
            _, ext = os.path.splitext(uploaded_file.name)

            # Determine image file format and mimetype by image's file extension.
            # The image mimetype is needed when uploading to S3 to prevent image
            # from automatically being downloaded when opening in new tab.
            if ext.lower().replace('.', '') in ['jpeg', 'jpg']:
                file_format = 'JPEG'
                mimetype = 'image/jpeg'
            else:
                file_format = 'PNG'
                mimetype = 'image/png'

            # Open the uploaded image.
            img = Image.open(uploaded_file)

            # Correct rotation of image.
            img = ImageOps.exif_transpose(img)

            # Resize the image
            basewidth = 500
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.LANCZOS)

            # Generate a new random filename.
            filename = f"{uuid4()}{ext}"

            # Upload the image to S3 if not in debug mode.
            if settings.PROD:
                s3 = boto3.client('s3',
                                  region_name=settings.AWS_REGION,
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                buffer = BytesIO()
                img.save(buffer, format=file_format)
                buffer.seek(0)

                # Upload image to S3.
                s3.upload_fileobj(buffer,
                                  settings.MEDIA_S3_BUCKET,
                                  'avatars/' + filename,
                                  ExtraArgs={'ContentType': mimetype})
                
                # Remove old profile picture from S3 if it exists.
                if old_filename != 'default.jpg':
                    delete_from_s3('avatars/' + old_filename, settings.MEDIA_S3_BUCKET)

                # Update profile picture filename in database.
                request.user.profile_picture = filename
            else: # Save the file locally if in debug mode.
                local_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')

                # Create image directory if it doesn't yet exist.
                os.makedirs(local_dir, exist_ok=True)
                
                # Create local image path and save image.
                local_path = os.path.join(local_dir, filename)
                img.save(local_path, format=file_format)

                # Update profile picture filename in database.
                request.user.profile_picture = filename

            # Save the updated user model.
            request.user.save()

            messages.success(request, 'Your profile picture has been updated!')
            return redirect('account')
    else:
        form = ProfilePictureForm(instance=request.user)
    return render(request, 'base/account.html', {'form': form})

@login_required(login_url='login')
def createFile(request):
    form = CreateMp3Form()

    if request.method == 'POST':
        form = CreateMp3Form(request.POST)
        if form.is_valid():
            # Get data from form.
            mp3_text = form.cleaned_data['text']
            mp3_title = form.cleaned_data['title'] + '.mp3'
            mp3_use_neural_engine = form.cleaned_data['use_neural_engine']
            mp3_voice = form.cleaned_data['voice'].lower()

            # Call Lambda function to generate MP3 file.
            payload = {
                'text': mp3_text,
                'use_neural_engine': mp3_use_neural_engine,
                'voice': mp3_voice
            }
            client = lambda_client()
            response = client.invoke(FunctionName=settings.LAMBDA_POLLY_FUNCTION_ARN,
                                 InvocationType='RequestResponse',
                                 Payload=json.dumps(payload))
            response_json = json.loads(response['Payload'].read())

            if response_json.get('statusCode') != 200:
                messages.error(request, 'Error creating MP3 file. Please try again.')
                return redirect('createFile')
            
            # Extract mp3_filename and create S3 key.
            mp3_filename = response_json['body']['filename']
            s3_key = f'mp3/{mp3_filename}'

            # Create and save database entry for MP3 file.
            mp3_entry = Mp3File(user=request.user,
                                custom_file_name=mp3_title,
                                file_name=mp3_filename,
                                text=mp3_text,
                                s3_key=s3_key)
            mp3_entry.save()

            messages.success(request, f'Successfully created MP3 file.')
            return redirect('files')  # Redirect to a success page or any desired URL
    context = {'form': form, 'title': 'Create MP3 File'}
    return render(request, 'base/upload.html', context)

@login_required(login_url='login')
def viewFileText(request, pk):
    mp3_file = get_object_or_404(Mp3File, pk=pk)

    # Check if the logged-in user is the owner of the file.
    if request.user != mp3_file.user:
        messages.error(request, "You do not have permission to view this file text.")
        return redirect('files')

    return render(request, 'components/view_file_text.html', {'mp3_file': mp3_file})

@login_required(login_url='login')
def deleteFile(request, pk):
    mp3_file = get_object_or_404(Mp3File, pk=pk)

    # Check if the logged-in user is the owner of the file.
    if request.user != mp3_file.user:
        messages.error(request, "You do not have permission to delete this file.")
        return redirect('files')

    # Remove the file from the S3 bucket.
    mp3_file.delete_from_s3()

    # Delete the MP3 file from the database.
    mp3_file.delete()

    messages.success(request, "File deleted successfully.")
    return redirect('files')

@login_required(login_url='login')
def files(request):
    form = DeleteMp3Form()

    # Get all the Mp3File objects related to the current user.
    mp3_files = Mp3File.objects.filter(user=request.user).order_by('-created')

    context = {'user': request.user, 'mp3_files': mp3_files, 'form': form, 'title': 'Your MP3 Files'}
    return render(request, 'base/files.html', context)