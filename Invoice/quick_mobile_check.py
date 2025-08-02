"""
Simple mobile compatibility validation
"""
import os

def validate_mobile_features():
    print("🔍 Validating Mobile Compatibility...")
    print("=" * 50)
    
    # Check critical files
    critical_files = {
        'mobile_upload.html': 'Mobile interface',
        'static/manifest.json': 'PWA manifest',
        'static/sw.js': 'Service worker',
        'web_invoice_app.py': 'Flask backend'
    }
    
    missing_files = []
    for file, description in critical_files.items():
        if os.path.exists(file):
            print(f"✅ {description}: {file}")
        else:
            print(f"❌ {description}: {file} (MISSING)")
            missing_files.append(file)
    
    # Check mobile features in HTML
    if os.path.exists('mobile_upload.html'):
        with open('mobile_upload.html', 'r', encoding='utf-8') as f:
            html_content = f.read().lower()
        
        mobile_checks = [
            ('user-scalable=no', 'iOS zoom prevention'),
            ('apple-mobile-web-app-capable', 'iOS web app mode'),
            ('capture="environment"', 'Camera capture'),
            ('manifest.json', 'PWA manifest link'),
            ('-webkit-appearance', 'iOS styling fixes'),
            ('navigator.vibrate', 'Haptic feedback'),
            ('service worker', 'Offline support')
        ]
        
        print("\n📱 Mobile Feature Analysis:")
        for feature, description in mobile_checks:
            if feature in html_content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description} (Missing: {feature})")
    
    # Summary
    print("\n📊 Compatibility Summary:")
    if len(missing_files) == 0:
        print("🎉 All critical mobile files are present!")
        print("📱 App is ready for mobile deployment!")
        return True
    else:
        print(f"⚠️  {len(missing_files)} critical files missing")
        print("📝 Please create missing files for full mobile support")
        return False

if __name__ == "__main__":
    validate_mobile_features()
