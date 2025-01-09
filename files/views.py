# pylint: disable=no-member
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from files.models import File
from django.core.files.base import ContentFile

import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY = get_random_bytes(16)


def encrypt_file(file_obj):
    """Encrypts a file-like object using AES."""
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_obj.read())

    return cipher.nonce, ciphertext


def decrypt_file(nonce, encrypted_data):
    """Decrypts data using AES and the provided nonce."""
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(encrypted_data)


@login_required
def file_upload(request):
    all_users = User.objects.exclude(id=request.user.id)  # get all users except the current user
    if request.method == 'POST':
        nonce, encrypted_data = encrypt_file(request.FILES['file'])
        file_model = File(owner=request.user)
        file_model.uploaded_file.save(request.FILES['file'].name, ContentFile(encrypted_data))
        file_model.nonce = nonce
        file_model.sha256_hash = compute_sha256(ContentFile(encrypted_data))
        file_model.file_name = request.FILES['file'].name
        file_model.save()

        # Share the file with selected users
        user_ids = request.POST.getlist('users')
        users_to_share_with = User.objects.filter(id__in=user_ids)
        file_model.shared_with.set(users_to_share_with)

        return redirect('file_list')
    return render(request, 'files/file_upload.html', {'all_users': all_users})


def compute_sha256(file_obj):
    """Compute the SHA-256 hash of a file-like object."""
    sha256 = hashlib.sha256()
    for chunk in file_obj.chunks():
        sha256.update(chunk)
    return sha256.hexdigest()


@login_required
def file_download(request, file_id):
    file_model = get_object_or_404(File, id=file_id)
    if request.user != file_model.owner and request.user not in file_model.shared_with.all():
        raise PermissionDenied

    decrypted_data = decrypt_file(file_model.nonce, file_model.uploaded_file.read())
    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_model.file_name}"'
    return response


@login_required
def share_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    if request.method == 'POST':
        usernames = request.POST['usernames'].split(",")  # Assume a comma-separated list of usernames
        users_to_share_with = User.objects.filter(username__in=usernames)
        file.shared_with.set(users_to_share_with)
        return redirect('file_detail', file_id=file.id)  # Redirect to file details or any appropriate view
    return render(request, 'files/share_file.html', {'file': file})


@login_required
def file_list(request):
    user_files = File.objects.filter(owner=request.user)
    shared_files = request.user.shared_files.all()
    return render(request, 'files/file_list.html', {'user_files': user_files, 'shared_files': shared_files})


def general_download(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_files = File.objects.filter(owner=request.user)
    return render(request, 'files/general_download.html', {'files': user_files})


def delete_old_files(request):
    # Ensure the user is an admin or has necessary permissions
    if not request.user.is_superuser:
        return HttpResponse("Unauthorized", status=401)

    count = File.objects.all().count()
    File.objects.all().delete()

    return HttpResponse(f"Deleted {count} files.")

@login_required
def file_interface(request):
    return render(request, 'files/interface.html')
