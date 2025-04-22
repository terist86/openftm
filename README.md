# openftm

Open-source implementation of FortiToken's TOTP algorithm.

You can extract the actual TOTP seed and use it with apps like [KeePassXC](https://keepassxc.org/) or [andOTP](https://github.com/andOTP/andOTP). Make sure to set the period to **60 seconds**.

## Prerequisites

For this to work, you need to extract three things: [SSAID](https://developer.android.com/reference/android/provider/Settings.Secure#ANDROID_ID), encrypted UUID, and encrypted seed. This requires **root** access on your Android device.

### SSAID

The **SSAID** is stored in the file located at `/data/system/users/0/settings_ssaid.xml`.

Starting from Android version 12 and newer, the original XML format has been replaced with a newer binary version known as ABX. Despite this change, the filename `settings_ssaid.xml` has remained unchanged, but the file is no longer human-readable.

For more detailed information about this format, please visit the following link: [CCL Solutions Group - Android ABX Binary XML](https://www.cclsolutionsgroup.com/post/android-abx-binary-xml).

### Seed

The **seed** is stored in the app's database located at `/data/data/com.fortinet.android.ftm/databases/FortiToken.db`.

### UUID Key and Token

The **UUID** and the **token** are stored in the app's preferences file located at `/data/data/com.fortinet.android.ftm/shared_prefs/FortiToken_SharedPrefs_NAME.xml`.

## Usage

1. Install the required dependencies with `pip3 install -U -r requirements.txt`.
2. Copy all three required files
3. Run the script with `python3 generate.py`.

## Disclaimer

All product and company names are trademarks™ or registered® trademarks of their respective holders. Use of them does not imply any affiliation with or endorsement by them.
