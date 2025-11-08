import os
import random
from androguard.core.apk import APK

# Define the permissions being monitored (23 critical permissions)
selected_permissions = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.GET_TASKS",
    "android.permission.CHANGE_WIFI_STATE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_PHONE_STATE",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "com.google.android.c2dm.permission.C2D_MESSAGE",
    "android.permission.CAMERA",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.ACCESS_WIFI_STATE",
    "android.permission.GET_ACCOUNTS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.VIBRATE",
    "android.permission.WAKE_LOCK",
    "com.android.vending.BILLING",
    "com.google.android.c2dm.permission.RECEIVE",
    "com.google.android.gms.permission.BIND_GET_INSTALL_REFERRER_SERVICE",
    "android.permission.WRITE_SETTINGS",
    "com.android.launcher.permission.INSTALL_SHORTCUT",
    "android.permission.MOUNT_UNMOUNT_FILESYSTEMS",
]

# Suspicious permission combinations that indicate adware
ADWARE_PATTERNS = [
    ["android.permission.INTERNET", "android.permission.READ_PHONE_STATE", "android.permission.ACCESS_FINE_LOCATION"],
    ["android.permission.SYSTEM_ALERT_WINDOW", "android.permission.INTERNET"],
    ["android.permission.GET_TASKS", "android.permission.INTERNET", "android.permission.WRITE_EXTERNAL_STORAGE"],
    ["com.android.launcher.permission.INSTALL_SHORTCUT", "android.permission.INTERNET"],
]

# Function to extract permissions from an APK
def extract_permissions(apk_path):
    try:
        apk = APK(apk_path)
        permissions = apk.get_permissions()
        return permissions
    except Exception as e:
        print(f"Error processing APK {apk_path}: {e}")
        return []

# Function to analyze permissions and generate demo prediction
def analyze_permissions_demo(permissions):
    """
    Demo function that analyzes permissions and generates realistic predictions.
    Uses pattern matching to detect suspicious permission combinations.
    """
    permissions_set = set(permissions)
    
    # Count how many monitored permissions are present
    monitored_count = sum(1 for perm in selected_permissions if perm in permissions_set)
    
    # Check for adware patterns
    pattern_matches = 0
    for pattern in ADWARE_PATTERNS:
        if all(perm in permissions_set for perm in pattern):
            pattern_matches += 1
    
    # Calculate a risk score (0.0 to 1.0)
    # More patterns matched = higher risk (lower confidence in safety)
    if pattern_matches >= 2:
        # Multiple suspicious patterns = likely adware
        confidence = random.uniform(0.15, 0.35)  # Low confidence (adware)
        prediction = "Adware Detected!"
    elif pattern_matches == 1:
        # One suspicious pattern = might be adware
        confidence = random.uniform(0.35, 0.55)  # Medium risk
        prediction = "Adware Detected!" if confidence < 0.5 else "No Adware Detected."
    elif monitored_count >= 15:
        # Many permissions but no obvious patterns
        confidence = random.uniform(0.45, 0.65)
        prediction = "No Adware Detected." if confidence >= 0.5 else "Adware Detected!"
    elif monitored_count >= 8:
        # Moderate permissions
        confidence = random.uniform(0.60, 0.80)
        prediction = "No Adware Detected."
    else:
        # Few permissions = likely safe
        confidence = random.uniform(0.75, 0.95)
        prediction = "No Adware Detected."
    
    return prediction, confidence

# Main function to scan a single APK (Demo Mode)
def scan_single_apk(apk_path, model_path=None, threshold=0.5):
    """
    Demo version of APK scanner.
    Analyzes permissions and generates demonstration predictions.
    No actual ML model required - this is for educational/demo purposes only.
    """
    print(f"[DEMO MODE] Scanning APK: {apk_path}")
    
    # Extract permissions from APK
    permissions = extract_permissions(apk_path)
    
    if not permissions:
        return {
            "APK": os.path.basename(apk_path),
            "Prediction": "Error: Could not extract permissions",
            "Confidence": 0.0,
            "Permissions": []
        }
    
    # Generate demo prediction based on permission analysis
    prediction, confidence = analyze_permissions_demo(permissions)
    
    print(f"[DEMO] Found {len(permissions)} permissions")
    print(f"[DEMO] Prediction: {prediction} (Confidence: {confidence:.2%})")
    
    return {
        "APK": os.path.basename(apk_path),
        "Prediction": prediction,
        "Confidence": confidence,
        "Permissions": permissions
    }

def main():
    """
    Main function for standalone testing (not used by web app)
    """
    print("=" * 60)
    print("  DEMO MODE - Static APK Scanner")
    print("  Educational/Demonstration Purposes Only")
    print("=" * 60)
    print()
    
    # Example usage
    apk_path = input("Enter APK file path: ").strip()
    
    if not os.path.isfile(apk_path):
        print(f"Error: APK file not found at {apk_path}")
        return

    # Call the scan function
    result = scan_single_apk(apk_path)

    if result:
        print("\n" + "=" * 60)
        print("  SCAN RESULT")
        print("=" * 60)
        print(f"APK: {result['APK']}")
        print(f"Prediction: {result['Prediction']}")
        print(f"Confidence: {result['Confidence']:.2%}")
        print(f"\nDetected Permissions ({len(result['Permissions'])}):")
        for i, perm in enumerate(result['Permissions'][:20], 1):  # Show first 20
            print(f"  {i}. {perm}")
        if len(result['Permissions']) > 20:
            print(f"  ... and {len(result['Permissions']) - 20} more")
    else:
        print("Failed to scan the APK.")

if __name__ == "__main__":
    main()
