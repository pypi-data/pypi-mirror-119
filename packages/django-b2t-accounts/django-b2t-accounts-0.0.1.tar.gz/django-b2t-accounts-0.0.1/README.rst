=====
Polls
=====

This "Account" app is an authentication app based on Django's built in
Authentication module and is an email authentication system.

Quick start
-----------
0. Install dependencies::

    pip install -r requirements.txt

1. Add "account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'account',
    ]
2. Include the polls URLconf in your project urls.py like this::

        path('', include('account.urls')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

3. Add to end of settings.py for static media::

    #ADD TO BOTTOM OF SETTINGS FILE

    # Static File Handling Settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn")

    # Media file handling Settings
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media_cdn')


    # Auth Redirects
    LOGIN_REDIRECT_URL = '/YOUR-URL'
    LOGOUT_REDIRECT_URL = '/YOUR-URL'


4. Migrate to create the account models.::

    python manage.py migrate

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a new user (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/ to begin using the authentication app.
