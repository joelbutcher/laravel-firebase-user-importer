# Firebase Laravel User Importer

A simple Python 3 script that will import users from a Laravel database to your Google Firebase project in batches of 100.

## Getting Started

### Configuring Laravel

In order to import users to Firebase, each user instance must have a uniquely identifiable non-empty string with no more than 128 characters.

You will likely need to update your Laravel projects `users` table to include a `firebase_uid` field.
As, by default, Laravel ensures your users emails are unique you can simply set the values to an `md5` hash of the users email.
See the below migration for an example:

```php
<?php

use App\Models\User;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('firebase_uid', 128)->after('id');
        });

        User::query()
            ->chunkById(100, function (Collection $users) {
                $users->each(function (User $user) {
                   $user->firebase_uid = md5($user->email);
                   $user->save();
                });
            });
    }
};

```

### The Firebase project

Firstly, head over to [firebase.google.com](https://firebase.google.com) and click "getting started" to create a new Firebase project.

> Tip: you don't need Google Analytics.

Once you have created the project, click on the card for setting up Authentication and enable the `Email/Password` sign in provider in.

Next, head over to you [Google Developer Service accounts page](https://console.cloud.google.com/iam-admin/serviceaccounts) and 
create a new set of key credentials for your firebase project and download the generated JSON file, you will need this for later.

### Environment configuration

Copy the `.env.example` file to `.env` and make sure you've configured your database:

```dotenv
# Laravel database configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```

Next, ensure you've configured firebase correctly, but setting the following keys.

```dotenv
# Google Firebase configuration
FIREBASE_APP_ID=
FIREBASE_API_KEY=
FIREBASE_PROJECT_ID=
```

> You can find the values of these keys by heading to the `Project Settings` section of your Firebase project. 

Finally, set the following keys from the JSON file you've just downloaded:

```dotenv
# Google Service Account Credentials
GOOGLE_SERVICE_ACCOUNT_PROJECT_ID=
GOOGLE_SERVICE_ACCOUNT_PRIVATE_ID=
GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY=
GOOGLE_SERVICE_ACCOUNT_CLIENT_EMAIL=
GOOGLE_SERVICE_ACCOUNT_CLIENT_ID=
GOOGLE_SERVICE_ACCOUNT_AUTH_URL=
GOOGLE_SERVICE_ACCOUNT_TOKEN_URL=
GOOGLE_SERVICE_ACCOUNT_AUTH_PROVIDER_CERT_URL=
GOOGLE_SERVICE_ACCOUNT_CLIENT_CERT_URL=
```

## Password Hashing

By default, Laravel hashes users passwords using the `bcrypt` hashing algorithm. If you have changed this,
you may edit the [get_hash_alg](./src/config/hashing.py) method found in `./src/config/hashing.py` to suit your needs.

Currently supported hashing algorithms:

- hmac_sha512
- hmac_sha256
- hmac_sha1
- hmac_md5
- md5
- sha1
- sha256
- sha512
- pbkdf_sha1
- pbkdf2_sha256
- scrypt
- bcrypt
- standard_scrypt